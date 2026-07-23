# stm32_dma_timer — timer-triggered DMA burst (STM32H7)

A minimal, self-contained `USER_C_MODULE` skeleton showing how out-of-tree C
code can drive a **timer-paced DMA burst** on the stm32 port while cooperating
with MicroPython's ownership of the DMA/interrupt vectors.

This is the concrete starting point referenced in
[micropython#19420](https://github.com/orgs/micropython/discussions/19420)
(e.g. auto-repeating DShot-style output where the CPU must stay free).

## Why a static C module (and not a native `.mpy`)

The Cortex-M vector table is fixed at firmware link time. Every
`DMAx_StreamY_IRQHandler` / `TIMx_IRQHandler` is already defined by the stm32
port, so:

* a **native `.mpy`** cannot install an interrupt handler or reach the HAL — it
  only links against `mp_fun_table`; and
* a user module **cannot redefine** those handlers (duplicate symbol).

So this is a **static `USER_C_MODULE`**, compiled into the firmware, that:

1. claims a DMA stream with `dma_external_acquire()` so the port keeps the DMA
   clock on and won't reuse the stream;
2. programs a timer's UPDATE event to pace the DMA, feeding a buffer into
   `TIMx->CCR1`;
3. **polls** completion (`NDTR`) instead of taking the DMA IRQ, because that IRQ
   vector belongs to the port.

To take a real completion *interrupt* instead of polling, add a small
forwarding hook to `ports/stm32/dma.c` (upstream change / PR) — see the note in
`stm32_dma_timer.c` `start()`.

## Build

The stm32 port is Makefile-based, so `micropython.mk` is used. The port
discovers modules by globbing `$(USER_C_MODULES)/*/micropython.mk`, so point
`USER_C_MODULES` at the **parent** `usercmodule` directory (this also builds the
sibling `cexample`/`cppexample` modules):

```bash
cd ports/stm32
make BOARD=NUCLEO_H743ZI \
     USER_C_MODULES=../../examples/usercmodule
```

Set `BURST_TIM_KERNEL_HZ` at the top of `stm32_dma_timer.c` to your timer clock
(200 MHz on many H7 boards). All other resources are chosen per instance from
Python. Pick DMA streams the port isn't using (avoid SPI/I2C/SDMMC/DAC streams).

## Usage

Constructor: `DmaBurst(controller, stream, dmamux_request, dst_addr, freq_hz)`

* `controller` — `1` for DMA1, `2` for DMA2
* `stream` — `0..7`
* `dmamux_request` — a timer-UP request, e.g. `stm32_dma_timer.REQ_TIM3_UP`
* `dst_addr` — peripheral register address, e.g. `stm.TIM3 + stm.TIM_CCR1`
* `freq_hz` — pacing rate (configures the request's timer)

```python
import stm32_dma_timer, stm, array

# One 32-bit word is pushed into TIM3->CCR1 on every TIM3 update at 1 kHz.
b = stm32_dma_timer.DmaBurst(1, 4, stm32_dma_timer.REQ_TIM3_UP,
                             stm.TIM3 + stm.TIM_CCR1, 1000)

data = array.array("I", [10, 20, 30, 40, 50])  # e.g. per-bit PWM duties
b.start(data)          # returns immediately; DMA runs autonomously
while b.busy():
    pass               # or do other work; CPU is free during the transfer
b.stop()               # stops DMA/pacing and releases the stream
```

### Four parallel channels (e.g. 4-motor DShot)

The H7 has 16 independent DMA streams, so four instances run concurrently. Here
all four share TIM3's update event to stay synchronised, each feeding a
different capture/compare register:

```python
import stm32_dma_timer, stm, array

REQ = stm32_dma_timer.REQ_TIM3_UP
channels = [
    stm32_dma_timer.DmaBurst(1, 0, REQ, stm.TIM3 + stm.TIM_CCR1, 1000),
    stm32_dma_timer.DmaBurst(1, 1, REQ, stm.TIM3 + stm.TIM_CCR2, 1000),
    stm32_dma_timer.DmaBurst(1, 2, REQ, stm.TIM3 + stm.TIM_CCR3, 1000),
    stm32_dma_timer.DmaBurst(1, 3, REQ, stm.TIM3 + stm.TIM_CCR4, 1000),
]

frames = [array.array("I", [i * 10 + 1, i * 10 + 2, i * 10 + 3]) for i in range(4)]
for ch, frame in zip(channels, frames):
    ch.start(frame)                 # four streams armed on the same timer
while any(ch.busy() for ch in channels):
    pass
for ch in channels:
    ch.stop()
```

Alternatively give each channel its own timer (`REQ_TIM3_UP`, `REQ_TIM4_UP`,
`REQ_TIM5_UP`, `REQ_TIM8_UP`) for fully independent rates.

The module only sets up each timer's *time base*; configuring the output
compare channels (CCMRx/CCERx) that drive pins for a real DShot waveform is left
to the caller.

## Files

* `stm32_dma_timer.c` — the module (STM32H7-guarded).
* `micropython.mk` — Makefile fragment (stm32 port).
* `micropython.cmake` — CMake fragment (for CMake-based ports; not stm32).

> This example is intentionally **not** added to
> `examples/usercmodule/micropython.cmake`, because it is STM32H7-specific and
> would break builds on other ports. Include it explicitly via
> `USER_C_MODULES` as shown above.
