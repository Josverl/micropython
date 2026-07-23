// Example USER_C_MODULE for the stm32 port (STM32H7 series).
//
// It shows the *architecture* for driving a peripheral from a timer-triggered
// DMA burst from an out-of-tree C module, while cooperating with MicroPython's
// DMA/IRQ ownership.  A typical use is generating auto-repeating waveforms such
// as DShot ESC frames: the timer paces the transfer and the DMA feeds a
// peripheral register (e.g. TIMx->CCRn, i.e. PWM duty), so the CPU is free.
//
// Each DmaBurst instance owns one of the H7's 16 independent DMA streams, so
// several instances run in parallel (e.g. four DShot channels at once).
//
// Key points about the integration boundary (see discussion micropython#19420):
//
//   * The Cortex-M vector table is fixed at firmware link time.  Every
//     `DMAx_StreamY_IRQHandler` and `TIMx_IRQHandler` symbol is already defined
//     (strongly) by the stm32 port, so a user module cannot redefine them and a
//     dynamically-loaded native .mpy cannot install one at all.
//
//   * Therefore this must be a *static* USER_C_MODULE, compiled into the
//     firmware, and it must not fight the vector table.  It instead:
//       - claims a DMA stream from MicroPython with dma_external_acquire() so
//         the port keeps the DMA clock enabled and won't reuse the stream, and
//       - polls transfer completion (NDTR) rather than taking the DMA IRQ,
//         because that IRQ vector belongs to the port.
//
//   * To receive a real hardware completion *interrupt* you have two options,
//     both noted below in start()/busy(): poll (done here), or forward through
//     the port's dispatcher (requires a small change to ports/stm32/dma.c).

#include "py/runtime.h"
#include "py/mphal.h"

#if !defined(STM32H7)

// Keep the rest of the tree buildable: this example is STM32H7-only.  Other
// ports/families simply get an empty module registration below is skipped.
#warning "stm32_dma_timer example only builds meaningfully on the STM32H7 series; module not registered."

#else

// dma_external_acquire()/dma_external_release() live in the stm32 port.  The
// stm32 build already has ports/stm32 on the include path.
#include "dma.h"

// Kernel clock feeding the pacing timers, in Hz.  On many H7 boards the APB1
// timer clock is 200 MHz; verify for your board/clock tree and adjust.
#define BURST_TIM_KERNEL_HZ     (200000000UL)

// H7 has DMA1 and DMA2, 8 streams each.  DMAMUX1 channels 0..7 map to DMA1
// streams 0..7, channels 8..15 to DMA2 streams 0..7.
static DMA_Stream_TypeDef *const dma_streams[2][8] = {
    { DMA1_Stream0, DMA1_Stream1, DMA1_Stream2, DMA1_Stream3,
      DMA1_Stream4, DMA1_Stream5, DMA1_Stream6, DMA1_Stream7 },
    { DMA2_Stream0, DMA2_Stream1, DMA2_Stream2, DMA2_Stream3,
      DMA2_Stream4, DMA2_Stream5, DMA2_Stream6, DMA2_Stream7 },
};

static DMAMUX_Channel_TypeDef *const dmamux_channels[16] = {
    DMAMUX1_Channel0, DMAMUX1_Channel1, DMAMUX1_Channel2, DMAMUX1_Channel3,
    DMAMUX1_Channel4, DMAMUX1_Channel5, DMAMUX1_Channel6, DMAMUX1_Channel7,
    DMAMUX1_Channel8, DMAMUX1_Channel9, DMAMUX1_Channel10, DMAMUX1_Channel11,
    DMAMUX1_Channel12, DMAMUX1_Channel13, DMAMUX1_Channel14, DMAMUX1_Channel15,
};

// This example paces the DMA from a timer's UPDATE event.  Map the DMAMUX
// request line to the timer that owns it, enabling its clock on the way.  Only
// the timer-UP requests are supported here; extend the table as needed.
static TIM_TypeDef *resolve_pacing_timer(uint32_t request) {
    switch (request) {
        case DMA_REQUEST_TIM1_UP:
            __HAL_RCC_TIM1_CLK_ENABLE();
            return TIM1;
        case DMA_REQUEST_TIM2_UP:
            __HAL_RCC_TIM2_CLK_ENABLE();
            return TIM2;
        case DMA_REQUEST_TIM3_UP:
            __HAL_RCC_TIM3_CLK_ENABLE();
            return TIM3;
        case DMA_REQUEST_TIM4_UP:
            __HAL_RCC_TIM4_CLK_ENABLE();
            return TIM4;
        case DMA_REQUEST_TIM5_UP:
            __HAL_RCC_TIM5_CLK_ENABLE();
            return TIM5;
        case DMA_REQUEST_TIM8_UP:
            __HAL_RCC_TIM8_CLK_ENABLE();
            return TIM8;
        default:
            return NULL;
    }
}

// ---------------------------------------------------------------------------
// Instance object.  Each instance owns exactly one DMA stream + one DMAMUX
// channel + one pacing timer, so several instances can run concurrently on the
// 16 independent H7 streams (e.g. four DShot channels in parallel).
// ---------------------------------------------------------------------------

typedef struct _dma_burst_obj_t {
    mp_obj_base_t base;
    uint8_t controller;             // 0 == DMA1, 1 == DMA2
    uint8_t stream;                 // 0..7
    DMA_Stream_TypeDef *dma;        // resolved stream instance
    DMAMUX_Channel_TypeDef *dmamux; // resolved DMAMUX channel
    uint32_t request;               // DMAMUX request line (timer UP)
    volatile uint32_t *dst;         // destination register (e.g. &TIMx->CCR1)
    TIM_TypeDef *tim;               // pacing timer resolved from request
    bool acquired;
} dma_burst_obj_t;

// Forward declaration of the type.
extern const mp_obj_type_t stm32_dma_timer_type_DmaBurst;

// DmaBurst(controller, stream, dmamux_request, dst_addr, freq_hz)
//   controller     : 1 for DMA1, 2 for DMA2
//   stream         : 0..7
//   dmamux_request : DMAMUX request line, e.g. stm32_dma_timer.REQ_TIM3_UP
//   dst_addr       : peripheral register address, e.g. stm.TIM3 + stm.TIM_CCR1
//   freq_hz        : pacing rate (configures the request's timer)
static mp_obj_t dma_burst_make_new(const mp_obj_type_t *type, size_t n_args, size_t n_kw, const mp_obj_t *args) {
    mp_arg_check_num(n_args, n_kw, 5, 5, false);

    mp_int_t controller = mp_obj_get_int(args[0]);
    mp_int_t stream = mp_obj_get_int(args[1]);
    mp_uint_t request = mp_obj_get_int(args[2]);
    mp_uint_t dst_addr = mp_obj_get_int(args[3]);
    mp_uint_t freq_hz = mp_obj_get_int(args[4]);

    if (controller != 1 && controller != 2) {
        mp_raise_ValueError(MP_ERROR_TEXT("controller must be 1 (DMA1) or 2 (DMA2)"));
    }
    if (stream < 0 || stream > 7) {
        mp_raise_ValueError(MP_ERROR_TEXT("stream must be 0..7"));
    }
    if (freq_hz == 0) {
        mp_raise_ValueError(MP_ERROR_TEXT("freq_hz must be > 0"));
    }
    // Guard: only allow writing into the peripheral address space, so a bad
    // dst_addr can't scribble over RAM/flash via DMA.
    if (dst_addr < 0x40000000 || dst_addr >= 0x60000000) {
        mp_raise_ValueError(MP_ERROR_TEXT("dst_addr must be a peripheral register"));
    }
    TIM_TypeDef *tim = resolve_pacing_timer(request);
    if (tim == NULL) {
        mp_raise_ValueError(MP_ERROR_TEXT("dmamux_request must be a supported TIMx_UP request"));
    }

    dma_burst_obj_t *self = mp_obj_malloc(dma_burst_obj_t, type);
    self->controller = controller - 1;  // convert to 0-based for the port API
    self->stream = stream;
    self->dma = dma_streams[self->controller][stream];
    self->dmamux = dmamux_channels[self->controller * 8 + stream];
    self->request = request;
    self->dst = (volatile uint32_t *)dst_addr;
    self->tim = tim;

    // Ask the port for exclusive use of this DMA stream.  This enables and
    // "holds" the DMA controller clock so the port won't power it down, and
    // marks the stream as in-use so MicroPython drivers avoid it.
    dma_external_acquire(self->controller, self->stream);
    self->acquired = true;

    // Program the timer update rate: update_hz = kernel / ((PSC+1)*(ARR+1)).
    // Note: several instances may share one timer (e.g. TIM3_UP driving CCR1..4
    // for four motors); they will program it to the same freq, which is fine.
    uint32_t ticks = BURST_TIM_KERNEL_HZ / freq_hz;
    uint32_t psc = 0;
    while (ticks > 0x10000) {
        psc++;
        ticks = BURST_TIM_KERNEL_HZ / (freq_hz * (psc + 1));
    }
    tim->PSC = psc;
    tim->ARR = (ticks ? ticks : 1) - 1;
    tim->EGR = TIM_EGR_UG; // latch PSC/ARR
    // The timer output channels (CCMRx/CCERx) that drive pins for a real DShot
    // waveform are left to the caller to configure; here we only set up the
    // time base that generates the UPDATE requests pacing the DMA.

    return MP_OBJ_FROM_PTR(self);
}

// Configure and launch a one-shot DMA burst: each timer UPDATE moves one word
// from `buf` into the destination register.  Returns immediately; the transfer
// runs on DMA with no CPU involvement.
static mp_obj_t dma_burst_start(mp_obj_t self_in, mp_obj_t buf_in) {
    dma_burst_obj_t *self = MP_OBJ_TO_PTR(self_in);
    if (!self->acquired) {
        mp_raise_ValueError(MP_ERROR_TEXT("stream released"));
    }

    // Read the source buffer as an array of 32-bit words.
    mp_buffer_info_t bufinfo;
    mp_get_buffer_raise(buf_in, &bufinfo, MP_BUFFER_READ);
    if (bufinfo.len == 0 || (bufinfo.len % sizeof(uint32_t)) != 0) {
        mp_raise_ValueError(MP_ERROR_TEXT("buf must be a non-empty multiple of 4 bytes"));
    }
    uint32_t nwords = bufinfo.len / sizeof(uint32_t);

    DMA_Stream_TypeDef *dma = self->dma;

    // Disable the stream before reconfiguring, then wait for it to stop.
    dma->CR &= ~DMA_SxCR_EN;
    while (dma->CR & DMA_SxCR_EN) {
    }

    // Route the timer request to this DMA stream via its DMAMUX channel.
    self->dmamux->CCR = self->request;

    // Program the transfer: memory (buf) -> peripheral (dst), 32-bit,
    // memory-increment on, one-shot (no circular), memory-to-peripheral.
    dma->PAR = (uint32_t)self->dst;
    dma->M0AR = (uint32_t)bufinfo.buf;
    dma->NDTR = nwords;
    dma->CR =
        (0x1 << DMA_SxCR_DIR_Pos)     // memory-to-peripheral
        | DMA_SxCR_MINC               // increment memory address
        | (0x2 << DMA_SxCR_PSIZE_Pos) // peripheral data size = word (32-bit)
        | (0x2 << DMA_SxCR_MSIZE_Pos) // memory data size = word (32-bit)
        | (0x2 << DMA_SxCR_PL_Pos);   // priority high

    // NOTE on interrupts: we deliberately do NOT set DMA_SxCR_TCIE here.  The
    // DMAx_StreamY_IRQHandler vector is owned by the stm32 port and only
    // forwards to handles it registered itself, so enabling TCIE would fire an
    // IRQ the port ignores (and won't clear).  Completion is polled in busy().
    // To take the real IRQ instead, add a forwarding hook in ports/stm32/dma.c.

    // On H7 the DMA reads from memory; make sure the buffer is flushed from
    // D-cache first so the DMA sees current data.
    #if __DCACHE_PRESENT
    SCB_CleanDCache_by_Addr((uint32_t *)((uint32_t)bufinfo.buf & ~0x1f),
        bufinfo.len + ((uint32_t)bufinfo.buf & 0x1f));
    #endif

    // Enable the stream, then let timer UPDATE events drive it.
    dma->CR |= DMA_SxCR_EN;
    self->tim->DIER |= TIM_DIER_UDE;  // update DMA request enable
    self->tim->CR1 |= TIM_CR1_CEN;    // start timer -> transfer begins

    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_2(dma_burst_start_obj, dma_burst_start);

// True while the DMA still has words left to transfer.  Poll this instead of
// taking the (port-owned) completion interrupt.
static mp_obj_t dma_burst_busy(mp_obj_t self_in) {
    dma_burst_obj_t *self = MP_OBJ_TO_PTR(self_in);
    DMA_Stream_TypeDef *dma = self->dma;
    bool busy = (dma->CR & DMA_SxCR_EN) && (dma->NDTR != 0);
    return mp_obj_new_bool(busy);
}
static MP_DEFINE_CONST_FUN_OBJ_1(dma_burst_busy_obj, dma_burst_busy);

// Stop the DMA and hand the stream back to MicroPython.  Note: if several
// instances share one timer, stopping the timer here stops pacing for all of
// them, so stop() disables this stream but only halts the timer's DMA request.
static mp_obj_t dma_burst_stop(mp_obj_t self_in) {
    dma_burst_obj_t *self = MP_OBJ_TO_PTR(self_in);

    DMA_Stream_TypeDef *dma = self->dma;
    dma->CR &= ~DMA_SxCR_EN;
    while (dma->CR & DMA_SxCR_EN) {
    }
    self->tim->CR1 &= ~TIM_CR1_CEN;
    self->tim->DIER &= ~TIM_DIER_UDE;

    if (self->acquired) {
        dma_external_release(self->controller, self->stream);
        self->acquired = false;
    }
    return mp_const_none;
}
static MP_DEFINE_CONST_FUN_OBJ_1(dma_burst_stop_obj, dma_burst_stop);

// Method table for the DmaBurst type.
static const mp_rom_map_elem_t dma_burst_locals_dict_table[] = {
    { MP_ROM_QSTR(MP_QSTR_start), MP_ROM_PTR(&dma_burst_start_obj) },
    { MP_ROM_QSTR(MP_QSTR_busy),  MP_ROM_PTR(&dma_burst_busy_obj) },
    { MP_ROM_QSTR(MP_QSTR_stop),  MP_ROM_PTR(&dma_burst_stop_obj) },
};
static MP_DEFINE_CONST_DICT(dma_burst_locals_dict, dma_burst_locals_dict_table);

MP_DEFINE_CONST_OBJ_TYPE(
    stm32_dma_timer_type_DmaBurst,
    MP_QSTR_DmaBurst,
    MP_TYPE_FLAG_NONE,
    make_new, dma_burst_make_new,
    locals_dict, &dma_burst_locals_dict
    );

// Module globals.  The REQ_* constants expose the DMAMUX timer-UP request
// lines so the pacing timer can be selected from Python.
static const mp_rom_map_elem_t stm32_dma_timer_globals_table[] = {
    { MP_ROM_QSTR(MP_QSTR___name__), MP_ROM_QSTR(MP_QSTR_stm32_dma_timer) },
    { MP_ROM_QSTR(MP_QSTR_DmaBurst), MP_ROM_PTR(&stm32_dma_timer_type_DmaBurst) },
    { MP_ROM_QSTR(MP_QSTR_REQ_TIM1_UP), MP_ROM_INT(DMA_REQUEST_TIM1_UP) },
    { MP_ROM_QSTR(MP_QSTR_REQ_TIM2_UP), MP_ROM_INT(DMA_REQUEST_TIM2_UP) },
    { MP_ROM_QSTR(MP_QSTR_REQ_TIM3_UP), MP_ROM_INT(DMA_REQUEST_TIM3_UP) },
    { MP_ROM_QSTR(MP_QSTR_REQ_TIM4_UP), MP_ROM_INT(DMA_REQUEST_TIM4_UP) },
    { MP_ROM_QSTR(MP_QSTR_REQ_TIM5_UP), MP_ROM_INT(DMA_REQUEST_TIM5_UP) },
    { MP_ROM_QSTR(MP_QSTR_REQ_TIM8_UP), MP_ROM_INT(DMA_REQUEST_TIM8_UP) },
};
static MP_DEFINE_CONST_DICT(stm32_dma_timer_globals, stm32_dma_timer_globals_table);


const mp_obj_module_t stm32_dma_timer_user_cmodule = {
    .base = { &mp_type_module },
    .globals = (mp_obj_dict_t *)&stm32_dma_timer_globals,
};

MP_REGISTER_MODULE(MP_QSTR_stm32_dma_timer, stm32_dma_timer_user_cmodule);

#endif // STM32H7
