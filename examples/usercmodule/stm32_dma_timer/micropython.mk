# Makefile fragment for the stm32_dma_timer USER_C_MODULE.
#
# The stm32 port uses a Makefile-based build, so this is the relevant fragment.
# Build a board with this module included, for example:
#
#   cd ports/stm32
#   make BOARD=WEACTSTUDIO_MINI_STM32H743 \
#        USER_C_MODULES=../../examples/usercmodule/stm32_dma_timer

STM32_DMA_TIMER_MOD_DIR := $(USERMOD_DIR)

# Add our C file to the build.
SRC_USERMOD += $(STM32_DMA_TIMER_MOD_DIR)/stm32_dma_timer.c

# Make the module's own directory available for #include if needed.
CFLAGS_USERMOD += -I$(STM32_DMA_TIMER_MOD_DIR)
