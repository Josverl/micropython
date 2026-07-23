# CMake fragment for the stm32_dma_timer USER_C_MODULE.
#
# The stm32 port is Makefile-based (use micropython.mk there).  This CMake
# fragment is provided only for completeness / CMake-based ports.

add_library(usermod_stm32_dma_timer INTERFACE)

target_sources(usermod_stm32_dma_timer INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}/stm32_dma_timer.c
)

target_include_directories(usermod_stm32_dma_timer INTERFACE
    ${CMAKE_CURRENT_LIST_DIR}
)

target_link_libraries(usermod INTERFACE usermod_stm32_dma_timer)
