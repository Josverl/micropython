

### MICROPY_ALLOC

This configuration set controls various aspects of memory allocation related to parsing, garbage collection, and string management in MicroPython. It optimizes memory usage by defining initial sizes and increment values for different data structures, ensuring efficient handling of resources during program execution.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_ALLOC_GC_STACK_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_GC_STACK_SIZE&type=code) | Sets the size of the garbage collector stack to manage memory allocation efficiently. | (1024) // Avoid slowdown when GC stack overflow causes a full sweep of PSRAM-backed heap |
| [`MICROPY_ALLOC_LEXEL_INDENT_INC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_LEXEL_INDENT_INC&type=code) | Defines the increment size for allocating additional lexer indentation levels. | (8) |
| [`MICROPY_ALLOC_LEXER_INDENT_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_LEXER_INDENT_INIT&type=code) | Initial allocation size for lexer indentation levels. | (10) |
| [`MICROPY_ALLOC_PARSE_CHUNK_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_PARSE_CHUNK_INIT&type=code) | Initial byte allocation for parse node chunks to minimize fragmentation. | (16) |
| [`MICROPY_ALLOC_PARSE_INTERN_STRING_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_PARSE_INTERN_STRING_LEN&type=code) | Maximum length of strings to be interned by the parser. | (10) |
| [`MICROPY_ALLOC_PARSE_RESULT_INC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_PARSE_RESULT_INC&type=code) | Defines the increment size for the parse result stack. | (16) |
| [`MICROPY_ALLOC_PARSE_RESULT_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_PARSE_RESULT_INIT&type=code) | Initial allocation size for the parse result stack. | (32) |
| [`MICROPY_ALLOC_PARSE_RULE_INC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_PARSE_RULE_INC&type=code) | Defines the increment size for the parse rule stack allocation. | (16) |
| [`MICROPY_ALLOC_PARSE_RULE_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_PARSE_RULE_INIT&type=code) | Initial allocation size for the parse rule stack. | (64) |
| [`MICROPY_ALLOC_PATH_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_PATH_MAX&type=code) | Defines the maximum length of a path for filesystem operations. | (128) |
| [`MICROPY_ALLOC_QSTR_CHUNK_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_QSTR_CHUNK_INIT&type=code) | Initial byte allocation for chunks storing interned string data, affecting memory usage. | (64) |
| [`MICROPY_ALLOC_QSTR_ENTRIES_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_QSTR_ENTRIES_INIT&type=code) | Initial count of entries for the qstr pool, influencing dynamic allocation size. | (10) |
| [`MICROPY_ALLOC_SCOPE_ID_INC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_SCOPE_ID_INC&type=code) | Increment value for allocating memory for scope IDs. | (6) |
| [`MICROPY_ALLOC_SCOPE_ID_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ALLOC_SCOPE_ID_INIT&type=code) | Initial allocation size for identifiers in a scope. | (4) |

> REVIEW: No user-facing docs mention these allocation limits (e.g. [docs/library/gc.rst](docs/library/gc.rst)), so please confirm whether the GC stack/path defaults (1024/128) should be surfaced there or if values differ per port.


### MICROPY_BOARD

This configuration group manages board-specific functionalities and behaviors during various operational states, including initialization, power management, and reset processes. It provides macros for handling low-power modes, executing startup scripts, and interfacing with peripherals like Bluetooth and SD cards, ensuring tailored performance for different hardware setups.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_BOARD_BEFORE_SOFT_RESET_LOOP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_BEFORE_SOFT_RESET_LOOP&type=code) | Calls the function boardctrl_before_soft_reset_loop before executing a soft reset. | boardctrl_before_soft_reset_loop |
| [`MICROPY_BOARD_BT_HCI_POLL_IN_MS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_BT_HCI_POLL_IN_MS&type=code) | Defines the timeout for polling Bluetooth HCI in milliseconds. | mp_bluetooth_hci_poll_in_ms_default |
| [`MICROPY_BOARD_BT_HCI_POLL_NOW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_BT_HCI_POLL_NOW&type=code) | Calls the default function to poll Bluetooth HCI immediately. | mp_bluetooth_hci_poll_now_default |
| [`MICROPY_BOARD_BUILD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_BUILD&type=code) | Indicates whether the board build is defined as 1 or 0. | (1) |
| [`MICROPY_BOARD_DEINIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_DEINIT&type=code) | Function called to deinitialize the board. | NANO33_board_deinit |
| [`MICROPY_BOARD_EARLY_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_EARLY_INIT&type=code) | Invoked for early initialization of board-specific settings, particularly for SPI flash chip parameters. | board_early_init_sf6 |
| [`MICROPY_BOARD_END_SOFT_RESET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_END_SOFT_RESET&type=code) | Calls the board-specific function to execute at the end of a soft reset. | boardctrl_end_soft_reset |
| [`MICROPY_BOARD_ENTER_BOOTLOADER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_ENTER_BOOTLOADER&type=code) | Calls the board-specific function to enter the bootloader mode. | board_enter_bootloader |
| [`MICROPY_BOARD_ENTER_STANDBY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_ENTER_STANDBY&type=code) | Triggers the board to enter a low-power standby mode. | PORTENTA_board_low_power(2); |
| [`MICROPY_BOARD_ENTER_STOP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_ENTER_STOP&type=code) | Triggers low power mode on the board. | PORTENTA_board_low_power(1); |
| [`MICROPY_BOARD_EXIT_STANDBY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_EXIT_STANDBY&type=code) | Calls the board_exit_standby function to exit a low-power standby state. | board_exit_standby |
| [`MICROPY_BOARD_FATAL_ERROR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_FATAL_ERROR&type=code) | Triggers a fatal error handling function, typically leading to a system halt. | boardctrl_fatal_error |
| [`MICROPY_BOARD_LEAVE_STANDBY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_LEAVE_STANDBY&type=code) | Calls the board_leave_standby function during the boot process. | board_leave_standby() |
| [`MICROPY_BOARD_LEAVE_STOP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_LEAVE_STOP&type=code) | Calls the low power function with mode 0 to leave stop mode. | PORTENTA_board_low_power(0); |
| [`MICROPY_BOARD_NETWORK_INTERFACES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_NETWORK_INTERFACES&type=code) | Enables board-specific network interface configurations. | - |
| [`MICROPY_BOARD_PENDSV_ENTRIES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_PENDSV_ENTRIES&type=code) | Holds additional entries for use with pendsv_schedule_dispatch. | - |
| [`MICROPY_BOARD_POST_STOP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_POST_STOP&type=code) | Enables the board oscillator after exiting STOP mode. | PORTENTA_board_osc_enable(1); |
| [`MICROPY_BOARD_PRE_STOP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_PRE_STOP&type=code) | Calls the board-specific function to disable the oscillator before entering low power mode. | PORTENTA_board_osc_enable(0); |
| [`MICROPY_BOARD_ROOT_POINTERS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_ROOT_POINTERS&type=code) | Defines pointers to board-specific root objects for I2S functionality. | \ |
| [`MICROPY_BOARD_RUN_BOOT_PY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_RUN_BOOT_PY&type=code) | Calls the function to execute boot.py during the initialization process. | boardctrl_run_boot_py |
| [`MICROPY_BOARD_RUN_MAIN_PY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_RUN_MAIN_PY&type=code) | Calls the function to execute main.py during board initialization. | boardctrl_run_main_py |
> REVIEW: Boot order docs (boot.py then main.py) in [docs/pyboard/general.rst](docs/pyboard/general.rst#L31-L37) assume the standard sequence; verify this hook matches that behaviour or add a note about board-specific overrides.
| [`MICROPY_BOARD_SDCARD_POWER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_SDCARD_POWER&type=code) | Activates the SD card power by setting a specific pin high. | mp_hal_pin_high(pyb_pin_EN_3V3); |
| [`MICROPY_BOARD_SPIFLASH_CHIP_PARAMS0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_SPIFLASH_CHIP_PARAMS0&type=code) | Reference to the SPI flash chip parameters for external SPI flash #1. | (spi_bdev.spiflash.chip_params) // SPI flash #1, R/W storage |
| [`MICROPY_BOARD_SPIFLASH_CHIP_PARAMS1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_SPIFLASH_CHIP_PARAMS1&type=code) | References the chip parameters for the second SPI flash device. | (spi_bdev2.spiflash.chip_params) // SPI flash #2, memory mapped |
| [`MICROPY_BOARD_STARTUP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_STARTUP&type=code) | Invokes board-specific initialization code at startup. | board_init |
| [`MICROPY_BOARD_START_SOFT_RESET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_START_SOFT_RESET&type=code) | Triggers the start of a soft reset process. | boardctrl_start_soft_reset |
| [`MICROPY_BOARD_TOP_SOFT_RESET_LOOP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_TOP_SOFT_RESET_LOOP&type=code) | Calls the top-level soft reset loop function for the board. | boardctrl_top_soft_reset_loop |
| [`MICROPY_BOARD_USBD_CDC_RX_EVENT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BOARD_USBD_CDC_RX_EVENT&type=code) | Callback invoked when USBD CDC data is available. | usbd_cdc_rx_event_callback |


### MICROPY_COMP

This configuration set controls various optimization features in the MicroPython compiler, focusing on constant expressions and tuple assignments. It enhances performance by allowing compile-time evaluations and optimizations for different types of constants and expressions, thereby improving the efficiency of the generated bytecode.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_COMP_ALLOW_TOP_LEVEL_AWAIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_COMP_ALLOW_TOP_LEVEL_AWAIT&type=code) | Controls the allowance of top-level await expressions in the compiler. | (0) |
| [`MICROPY_COMP_CONST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_COMP_CONST&type=code) | Enables constant optimization for expressions using the 'const' function. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_COMP_CONST_FLOAT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_COMP_CONST_FLOAT&type=code) | Enables float constant folding and optimization features based on ROM level configuration. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_COMP_CONST_FOLDING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_COMP_CONST_FOLDING&type=code) | Enables constant folding optimizations for expressions like 1+2 to be evaluated at compile time. | (1) |
| [`MICROPY_COMP_CONST_LITERAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_COMP_CONST_LITERAL&type=code) | Enables optimizations for constant literals like OrderedDict. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_COMP_CONST_TUPLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_COMP_CONST_TUPLE&type=code) | Enables immediate compilation of constant tuples to their respective objects. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_COMP_DOUBLE_TUPLE_ASSIGN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_COMP_DOUBLE_TUPLE_ASSIGN&type=code) | Enables optimization for double tuple assignments like 'a, b = c, d'. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_COMP_MODULE_CONST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_COMP_MODULE_CONST&type=code) | Enables lookup of constants in modules, allowing expressions like module.CONST. | (0) |
| [`MICROPY_COMP_RETURN_IF_EXPR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_COMP_RETURN_IF_EXPR&type=code) | Enables optimization for returning expressions in the form of 'return a if b else c'. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_COMP_TRIPLE_TUPLE_ASSIGN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_COMP_TRIPLE_TUPLE_ASSIGN&type=code) | Enables optimization for triple tuple assignments in the compiler. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
> REVIEW: User-facing language docs (e.g. [docs/reference/micropython.rst](docs/reference/micropython.rst)) do not describe which compiler optimisations are enabled per ROM level; confirm defaults or document per-port differences.


### MICROPY_CONFIG

This configuration group manages the feature set of the MicroPython build by defining various ROM levels, allowing developers to tailor the build according to the available memory and specific application requirements. It provides options ranging from minimal configurations to full-featured builds, enabling or disabling features based on the selected ROM level.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_CONFIG_ROM_LEVEL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CONFIG_ROM_LEVEL&type=code) | Controls the feature level of the MicroPython build, with options ranging from minimal to full features. | (MICROPY_CONFIG_ROM_LEVEL_MINIMUM) |
| [`MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_BASIC_FEATURES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_BASIC_FEATURES&type=code) | Checks if the ROM level is at least BASIC_FEATURES for enabling certain features. | (MICROPY_CONFIG_ROM_LEVEL >= MICROPY_CONFIG_ROM_LEVEL_BASIC_FEATURES) |
| [`MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES&type=code) | Checks if the ROM level is at least the core features level. | (MICROPY_CONFIG_ROM_LEVEL >= MICROPY_CONFIG_ROM_LEVEL_CORE_FEATURES) |
| [`MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING&type=code) | Checks if the ROM level is at least 'everything' for enabling certain features. | (MICROPY_CONFIG_ROM_LEVEL >= MICROPY_CONFIG_ROM_LEVEL_EVERYTHING) |
| [`MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES&type=code) | Checks if the ROM level is at least the extra features level. | (MICROPY_CONFIG_ROM_LEVEL >= MICROPY_CONFIG_ROM_LEVEL_EXTRA_FEATURES) |
| [`MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_FULL_FEATURES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_FULL_FEATURES&type=code) | Checks if the ROM level is at least 'full features' for conditional compilation. | (MICROPY_CONFIG_ROM_LEVEL >= MICROPY_CONFIG_ROM_LEVEL_FULL_FEATURES) |
| [`MICROPY_CONFIG_ROM_LEVEL_BASIC_FEATURES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CONFIG_ROM_LEVEL_BASIC_FEATURES&type=code) | Enables most common features suitable for small on-device flash, like STM32F411. | (20) |
| [`MICROPY_CONFIG_ROM_LEVEL_CORE_FEATURES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CONFIG_ROM_LEVEL_CORE_FEATURES&type=code) | Enables only core features for constrained flash environments. | (10) |
| [`MICROPY_CONFIG_ROM_LEVEL_EVERYTHING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CONFIG_ROM_LEVEL_EVERYTHING&type=code) | Enables all features, including coverage for testing. | (50) |
| [`MICROPY_CONFIG_ROM_LEVEL_EXTRA_FEATURES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CONFIG_ROM_LEVEL_EXTRA_FEATURES&type=code) | Enables convenience features for medium on-device flash, suitable for devices like STM32F405. | (30) |
| [`MICROPY_CONFIG_ROM_LEVEL_FULL_FEATURES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CONFIG_ROM_LEVEL_FULL_FEATURES&type=code) | Enables all common features for larger or external flash systems. | (40) |
| [`MICROPY_CONFIG_ROM_LEVEL_MINIMUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CONFIG_ROM_LEVEL_MINIMUM&type=code) | Enables a minimal configuration by disabling all optional features. | (0) |
> REVIEW: Consider adding a short mapping of ROM levels to feature sets in [docs/develop/README.md](docs/develop/README.md) or [docs/reference/manifest.rst](docs/reference/manifest.rst) so values (0–50) are explainable to readers.


### MICROPY_EMIT

This configuration set controls the emission of various types of native and inline assembly code across multiple architectures, including ARM, RISC-V, Xtensa, and x86. It allows for the customization of bytecode handling, debugging options, and the use of specific assembly features, enabling optimized performance and functionality tailored to different hardware platforms.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_EMIT_ARM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_ARM&type=code) | Enables the emission of ARM native code. | (1) |
| [`MICROPY_EMIT_BYTECODE_USES_QSTR_TABLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_BYTECODE_USES_QSTR_TABLE&type=code) | Enables the use of a qstr table for mapping internal qstr indices in bytecode to global qstr values. | (MICROPY_PERSISTENT_CODE) |
| [`MICROPY_EMIT_INLINE_ASM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_INLINE_ASM&type=code) | Indicates if any inline assembler emitter is enabled, based on specific architecture flags. | (MICROPY_EMIT_INLINE_THUMB \|\| MICROPY_EMIT_INLINE_XTENSA \|\| MICROPY_EMIT_INLINE_RV32) |
| [`MICROPY_EMIT_INLINE_RV32`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_INLINE_RV32&type=code) | Enables the RISC-V RV32 inline assembler. | (1) |
| [`MICROPY_EMIT_INLINE_THUMB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_INLINE_THUMB&type=code) | Enables the use of inline assembly for Thumb architecture. | (SAMD21_EXTRA_FEATURES) |
| [`MICROPY_EMIT_INLINE_THUMB_FLOAT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_INLINE_THUMB_FLOAT&type=code) | Enables float support in the Thumb2 inline assembler. | (1) |
| [`MICROPY_EMIT_INLINE_XTENSA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_INLINE_XTENSA&type=code) | Enables the use of inline assembly for the Xtensa architecture. | (1) |
| [`MICROPY_EMIT_INLINE_XTENSA_UNCOMMON_OPCODES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_INLINE_XTENSA_UNCOMMON_OPCODES&type=code) | Enables support for uncommon Xtensa inline assembler opcodes. | (0) |
| [`MICROPY_EMIT_MACHINE_CODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_MACHINE_CODE&type=code) | Indicates if native or inline assembler emitters are enabled. | (MICROPY_EMIT_NATIVE \|\| MICROPY_EMIT_INLINE_ASM) |
| [`MICROPY_EMIT_NATIVE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_NATIVE&type=code) | Indicates if any native emitter is enabled, allowing for native code generation. | (MICROPY_EMIT_X64 \|\| MICROPY_EMIT_X86 \|\| MICROPY_EMIT_THUMB \|\| MICROPY_EMIT_ARM \|\| MICROPY_EMIT_XTENSA \|\| MICROPY_EMIT_XTENSAWIN \|\| MICROPY_EMIT_RV32 \|\| MICROPY_EMIT_NATIVE_DEBUG) |
| [`MICROPY_EMIT_NATIVE_DEBUG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_NATIVE_DEBUG&type=code) | Enables the human-readable native instructions emitter for debugging purposes. | (1) |
| [`MICROPY_EMIT_NATIVE_DEBUG_PRINTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_NATIVE_DEBUG_PRINTER&type=code) | Defines the output function for native debug printing. | (&mp_stdout_print) |
| [`MICROPY_EMIT_NATIVE_PRELUDE_SEPARATE_FROM_MACHINE_CODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_NATIVE_PRELUDE_SEPARATE_FROM_MACHINE_CODE&type=code) | Separates the prelude of a native function from machine code for architectures that cannot read executable memory byte-wise. | (MICROPY_EMIT_XTENSAWIN) |
| [`MICROPY_EMIT_RV32`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_RV32&type=code) | Enables the emission of RISC-V RV32 native code. | (1) |
| [`MICROPY_EMIT_RV32_ZBA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_RV32_ZBA&type=code) | Controls the emission of RISC-V RV32 Zba opcodes in native code. | (0) |
| [`MICROPY_EMIT_THUMB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_THUMB&type=code) | Controls the emission of thumb native code, with a default value of 0. | (0) |
| [`MICROPY_EMIT_THUMB_ARMV7M`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_THUMB_ARMV7M&type=code) | Enables ARMv7-M instruction support in thumb native code. | (1) |
| [`MICROPY_EMIT_X64`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_X64&type=code) | Enables the x64 native code emitter. | (1) |
| [`MICROPY_EMIT_X86`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_X86&type=code) | Disables the x86 native code emitter when nan-boxing is enabled. | (0) |
| [`MICROPY_EMIT_XTENSA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_XTENSA&type=code) | Enables the emission of Xtensa native code. | (1) |
| [`MICROPY_EMIT_XTENSAWIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMIT_XTENSAWIN&type=code) | Enables the emission of Xtensa-Windowed native code. | (1) |
> REVIEW: Native emitter availability is not summarised in user docs (see [docs/reference/micropython.rst](docs/reference/micropython.rst)); please confirm which ports ship each emitter or add a table there.


### MICROPY_ENABLE

The MICROPY_ENABLE macros configure various features and functionalities of the MicroPython environment, allowing developers to customize aspects such as memory management, exception handling, and module imports. By enabling or disabling these options, users can optimize performance and resource usage according to their specific application needs.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_ENABLE_COMPILER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ENABLE_COMPILER&type=code) | Enables the built-in MicroPython compiler for executing scripts and REPL functionality. | (1) |
| [`MICROPY_ENABLE_DOC_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ENABLE_DOC_STRING&type=code) | Controls inclusion of doc strings, affecting RAM usage. | (0) |
| [`MICROPY_ENABLE_EMERGENCY_EXCEPTION_BUF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ENABLE_EMERGENCY_EXCEPTION_BUF&type=code) | Enables a buffer for exception details during low-memory situations. | (1) |
| [`MICROPY_ENABLE_EXTERNAL_IMPORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ENABLE_EXTERNAL_IMPORT&type=code) | Enables the import of external modules from the filesystem. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_ENABLE_FINALISER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ENABLE_FINALISER&type=code) | Enables the finalizer feature for garbage collection, allowing cleanup of objects before they are freed. | (1) |
| [`MICROPY_ENABLE_GC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ENABLE_GC&type=code) | Enables the garbage collector for memory management. | (1) |
| [`MICROPY_ENABLE_PYSTACK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ENABLE_PYSTACK&type=code) | Enables a separate allocator for the Python stack, requiring initialization with mp_pystack_init. | (0) |
| [`MICROPY_ENABLE_RUNTIME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ENABLE_RUNTIME&type=code) | Controls the inclusion of runtime features, set to 0 to disable. | (0) |
| [`MICROPY_ENABLE_SCHEDULER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ENABLE_SCHEDULER&type=code) | Enables the internal scheduler for managing asynchronous tasks and callbacks. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_ENABLE_SOURCE_LINE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ENABLE_SOURCE_LINE&type=code) | Includes source line number information in bytecode, increasing RAM usage. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_ENABLE_VM_ABORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ENABLE_VM_ABORT&type=code) | Enables support for asynchronously aborting the virtual machine execution. | (0) |
> REVIEW: Clarify in [docs/reference/micropython.rst](docs/reference/micropython.rst) which of these runtime toggles are exposed to users versus build-time only; current docs omit VM abort, pystack, and scheduler defaults.


### MICROPY_FATFS

This configuration group manages various aspects of FAT filesystem support, including options for long file names, partitioning, and synchronization. It allows customization of file system behavior, such as enabling exFAT support, setting maximum file name lengths, and defining timeout durations for operations.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_FATFS_ENABLE_LFN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FATFS_ENABLE_LFN&type=code) | Controls the use of long file names in FAT filesystem support. | (2) |
| [`MICROPY_FATFS_EXFAT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FATFS_EXFAT&type=code) | Enables support for the exFAT filesystem. | (1) |
| [`MICROPY_FATFS_LFN_CODE_PAGE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FATFS_LFN_CODE_PAGE&type=code) | Sets the OEM code page for long file names in FATFS, defaulting to 437 for U.S. (OEM). Examples: 437 for U.S., 850 for Western Europe. | 437 /* 1=SFN/ANSI 437=LFN/U.S.(OEM) */ |
| [`MICROPY_FATFS_MAX_LFN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FATFS_MAX_LFN&type=code) | Sets the maximum length for long file names in the FAT filesystem. | (MICROPY_ALLOC_PATH_MAX) |
| [`MICROPY_FATFS_MAX_SS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FATFS_MAX_SS&type=code) | Determines the maximum sector size for FatFS, typically set to the flash sector size. | (MICROPY_HW_FLASH_BLOCK_SIZE_BYTES) |
| [`MICROPY_FATFS_MULTI_PARTITION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FATFS_MULTI_PARTITION&type=code) | Enables support for multiple partitions in the FAT filesystem. | (1) |
| [`MICROPY_FATFS_NORTC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FATFS_NORTC&type=code) | Enables non-real-time clock support for the FatFs filesystem. | (1) |
| [`MICROPY_FATFS_REENTRANT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FATFS_REENTRANT&type=code) | Enables re-entrant file system operations for FATFS. | (1) |
| [`MICROPY_FATFS_RPATH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FATFS_RPATH&type=code) | Sets the relative path depth for FatFS support. | (2) |
| [`MICROPY_FATFS_SYNC_T`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FATFS_SYNC_T&type=code) | Defines the type for synchronization objects used in the FatFs module. | SemaphoreHandle_t |
| [`MICROPY_FATFS_TIMEOUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FATFS_TIMEOUT&type=code) | Sets the timeout duration for FATFS operations in milliseconds. | (2500) |
| [`MICROPY_FATFS_USE_LABEL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FATFS_USE_LABEL&type=code) | Enables the use of volume labels in the FatFS file system. | (1) |
> REVIEW: Filesystem user docs (e.g. [docs/reference/filesystem.rst](docs/reference/filesystem.rst)) don’t describe these FatFS tunables; note defaults per port or mark as build-time only.


### MICROPY_FLOAT

This configuration set controls the implementation and representation of floating-point numbers in MicroPython, allowing developers to choose between various precision levels and formats. It also includes options for enabling or disabling floating-point support, optimizing for code size, and enhancing the quality of hash functions for float and complex numbers.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_FLOAT_FORMAT_IMPL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FLOAT_FORMAT_IMPL&type=code) | Determines the floating-point format implementation level, affecting precision and representation. | (MICROPY_FLOAT_FORMAT_IMPL_APPROX) |
| [`MICROPY_FLOAT_FORMAT_IMPL_APPROX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FLOAT_FORMAT_IMPL_APPROX&type=code) | Defines a floating-point format implementation that is slightly larger and nearly perfect in representation. | (1) // slightly bigger, almost perfect |
| [`MICROPY_FLOAT_FORMAT_IMPL_BASIC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FLOAT_FORMAT_IMPL_BASIC&type=code) | Enables the smallest code size for float to string conversion, resulting in inexact representations. | (0)  // smallest code, but inexact |
| [`MICROPY_FLOAT_FORMAT_IMPL_EXACT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FLOAT_FORMAT_IMPL_EXACT&type=code) | Enables 100% exact representation of floating-point numbers with larger code size. | (2)  // bigger code, and 100% exact repr |
| [`MICROPY_FLOAT_HIGH_QUALITY_HASH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FLOAT_HIGH_QUALITY_HASH&type=code) | Enables a high-quality hash function for float and complex numbers. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_FLOAT_IMPL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FLOAT_IMPL&type=code) | Determines the floating-point implementation type, either single or double precision. | (MICROPY_FLOAT_IMPL_DOUBLE) |
| [`MICROPY_FLOAT_IMPL_DOUBLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FLOAT_IMPL_DOUBLE&type=code) | Enables the use of double precision floating point representation. | (2) |
| [`MICROPY_FLOAT_IMPL_FLOAT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FLOAT_IMPL_FLOAT&type=code) | Enables single-precision floating point implementation using float type. | (1) |
| [`MICROPY_FLOAT_IMPL_NONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FLOAT_IMPL_NONE&type=code) | Disables floating point and complex number support. | (0) |
| [`MICROPY_FLOAT_USE_NATIVE_FLT16`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FLOAT_USE_NATIVE_FLT16&type=code) | Enables the use of native _Float16 for 16-bit float support if available. | (1) |
| [`MICROPY_FLOAT_ZERO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FLOAT_ZERO&type=code) | Represents the float value zero as a constant. | MICROPY_FLOAT_CONST(0.0) |
> REVIEW: Floating-point options (impl single/double/none/float16, format modes) are not surfaced in [docs/reference/constrained.rst](docs/reference/constrained.rst) or [docs/library/math.rst](docs/library/math.rst); add a short capability matrix per port.


### MICROPY_HW

This collection of macros configures various hardware features and settings for embedded systems, including ADC channels, analog switches, block device operations, Bluetooth communication parameters, and board-specific identifiers. It allows developers to customize hardware interactions and optimize performance based on the specific capabilities and requirements of their devices.

#### MICROPY_HW_ADC

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_ADC_EXT_COUNT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ADC_EXT_COUNT&type=code) | Determines the number of external ADC channels available. | (4) |
| [`MICROPY_HW_ADC_VREF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ADC_VREF&type=code) | Defines the ADC reference voltage value for the hardware. | (2) |
#### MICROPY_HW_ANALOG

This configuration set manages the states of various analog switches associated with specific pins on the hardware. It allows for the control of analog signal routing by enabling or disabling connections for designated pins, facilitating the proper functioning of connected peripherals.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_ANALOG_SWITCH_PA0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ANALOG_SWITCH_PA0&type=code) | Configures the analog switch for pin PA0 to be open. | (SYSCFG_SWITCH_PA0_OPEN) |
| [`MICROPY_HW_ANALOG_SWITCH_PA1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ANALOG_SWITCH_PA1&type=code) | Configures the analog switch for pin PA1 as open. | (SYSCFG_SWITCH_PA1_OPEN) |
| [`MICROPY_HW_ANALOG_SWITCH_PC2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ANALOG_SWITCH_PC2&type=code) | Configures the analog switch for pin PC2, connected to ULPI NXT and DIR pins. | (SYSCFG_SWITCH_PC2_CLOSE) |
| [`MICROPY_HW_ANALOG_SWITCH_PC3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ANALOG_SWITCH_PC3&type=code) | Configures the state of the analog switch for pin PC3. | (SYSCFG_SWITCH_PC3_CLOSE) |
#### MICROPY_HW_ANTENNA

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_ANTENNA_DIVERSITY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ANTENNA_DIVERSITY&type=code) | Enables antenna diversity functionality for the hardware. | (0) |
#### MICROPY_HW_BDEV

This configuration set manages the block device operations for internal flash storage and external SPI flash in MicroPython. It defines parameters such as block size, I/O operations, and function pointers for reading and writing blocks, enabling efficient data handling and storage management.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_BDEV_BLOCKSIZE_EXT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BDEV_BLOCKSIZE_EXT&type=code) | Defines the block size for extended block protocol on internal flash storage. | (FLASH_BLOCK_SIZE) |
| [`MICROPY_HW_BDEV_IOCTL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BDEV_IOCTL&type=code) | Enables block device I/O operations for internal flash storage. | flash_bdev_ioctl |
| [`MICROPY_HW_BDEV_READBLOCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BDEV_READBLOCK&type=code) | Function pointer for reading a block from the block device. | flash_bdev_readblock |
| [`MICROPY_HW_BDEV_SPIFLASH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BDEV_SPIFLASH&type=code) | Pointer to the SPI block device configuration. | (&spi_bdev) |
| [`MICROPY_HW_BDEV_SPIFLASH_CONFIG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BDEV_SPIFLASH_CONFIG&type=code) | Pointer to the SPI flash configuration structure. | (&spiflash_config) |
| [`MICROPY_HW_BDEV_SPIFLASH_EXTENDED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BDEV_SPIFLASH_EXTENDED&type=code) | Enables the use of an external SPI flash with an extended block protocol. | (&spi_bdev) // for extended block protocol |
| [`MICROPY_HW_BDEV_SPIFLASH_OFFSET_BLOCKS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BDEV_SPIFLASH_OFFSET_BLOCKS&type=code) | Calculates the number of flash blocks offset based on the byte offset divided by the block size. | (MICROPY_HW_BDEV_SPIFLASH_OFFSET_BYTES / FLASH_BLOCK_SIZE) |
| [`MICROPY_HW_BDEV_SPIFLASH_OFFSET_BYTES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BDEV_SPIFLASH_OFFSET_BYTES&type=code) | Defines the byte offset for the SPI flash block device. | (4 * 1024 * 1024) |
| [`MICROPY_HW_BDEV_SPIFLASH_SIZE_BYTES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BDEV_SPIFLASH_SIZE_BYTES&type=code) | Calculates the size in bytes of the SPI flash based on the logarithmic size in bits. | ((1 << MICROPY_HW_QSPIFLASH_SIZE_BITS_LOG2) / 8) |
| [`MICROPY_HW_BDEV_WRITEBLOCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BDEV_WRITEBLOCK&type=code) | Defines the function for writing a block to the block device. | flash_bdev_writeblock |
> REVIEW: Storage selection and offsets (internal flash vs SPI/QSPI, `*_OFFSET_BYTES`, mount-at-boot) are not summarised in [docs/reference/filesystem.rst](docs/reference/filesystem.rst) or the port quickrefs; add a per-port table of default boot volume and reserved regions.
#### MICROPY_HW_BLE

This configuration group manages the settings and parameters for Bluetooth Low Energy (BLE) communication, specifically focusing on the UART interface. It includes definitions for baud rates, flow control, and pin assignments necessary for establishing and maintaining Bluetooth connectivity.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_BLE_BTSTACK_CHIPSET_INSTANCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BLE_BTSTACK_CHIPSET_INSTANCE&type=code) | Defines the Bluetooth chipset instance for the BTstack HCI. | btstack_chipset_cc256x_instance() |
| [`MICROPY_HW_BLE_UART_BAUDRATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BLE_UART_BAUDRATE&type=code) | Defines the baud rate for the Bluetooth UART communication. | (1000000) |
| [`MICROPY_HW_BLE_UART_BAUDRATE_DOWNLOAD_FIRMWARE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BLE_UART_BAUDRATE_DOWNLOAD_FIRMWARE&type=code) | Sets the baud rate for Bluetooth UART during firmware download. | (3000000) |
| [`MICROPY_HW_BLE_UART_BAUDRATE_SECONDARY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BLE_UART_BAUDRATE_SECONDARY&type=code) | Defines the secondary baud rate for Bluetooth UART communication, set to 3000000. | (3000000) |
| [`MICROPY_HW_BLE_UART_FLOW_CONTROL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BLE_UART_FLOW_CONTROL&type=code) | Configures the flow control setting for BLE UART communication. | (3) |
| [`MICROPY_HW_BLE_UART_ID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BLE_UART_ID&type=code) | Identifies the UART interface used for Bluetooth communication. | (1) |
| [`MICROPY_HW_BLE_UART_RTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BLE_UART_RTS&type=code) | Defines the RTS pin for the Bluetooth UART interface. | (MICROPY_HW_UART8_RTS) |
| [`MICROPY_HW_BLE_UART_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BLE_UART_RX&type=code) | Defines the RX pin number for the BLE UART interface. | (7) |
| [`MICROPY_HW_BLE_UART_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BLE_UART_TX&type=code) | Defines the UART transmit pin number for Bluetooth communication. | (4) |
#### MICROPY_HW_BOARD

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_BOARD_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BOARD_NAME&type=code) | Identifies the hardware board name being used. | "F769DISC" |
#### MICROPY_HW_BOOTSEL

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_BOOTSEL_DELAY_US`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_BOOTSEL_DELAY_US&type=code) | Defines the delay duration in microseconds for the BOOTSEL button functionality. | 8 |
#### MICROPY_HW_CAN

This configuration group manages the setup of multiple CAN bus interfaces, including their names and the specific GPIO pins used for transmitting and receiving data. It allows for flexible hardware configuration to support various communication needs across different CAN buses.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_CAN1_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CAN1_NAME&type=code) | Defines the name of the first CAN bus, typically used for configuration. | "FDCAN1" |
| [`MICROPY_HW_CAN1_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CAN1_RX&type=code) | Defines the receive pin for CAN1 communication, typically assigned to pin_B8. | (pin_B8)    //              pin 3 on CN10 |
| [`MICROPY_HW_CAN1_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CAN1_TX&type=code) | Defines the transmit pin for CAN1 communication. | (pin_B9)    //              pin 5 on CN10 |
| [`MICROPY_HW_CAN2_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CAN2_NAME&type=code) | Identifies the second CAN bus name for hardware configuration. | "Y" |
| [`MICROPY_HW_CAN2_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CAN2_RX&type=code) | Defines the receive pin for CAN2 communication, typically assigned to a specific GPIO pin. | (pin_B5)    //              pin 29 on CN10 |
| [`MICROPY_HW_CAN2_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CAN2_TX&type=code) | Defines the transmit pin for CAN2 communication. | (pin_B6)    //              pin 17 on CN10 |
| [`MICROPY_HW_CAN3_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CAN3_RX&type=code) | Defines the receive pin for CAN3, shared with UART1 or I2C3. | (pin_B3) // shared with UART1 or use pin_A8 shared with I2C3 |
| [`MICROPY_HW_CAN3_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CAN3_TX&type=code) | Defines the transmit pin for CAN3 communication. | (pin_B4) |
#### MICROPY_HW_CLK

This configuration group manages the clock settings for various buses and PLLs, allowing for precise control over the system's clock frequencies and dividers. It enables the adjustment of clock parameters such as division factors and PLL configurations to optimize performance and power consumption in embedded applications.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_CLK_AHB_DIV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_AHB_DIV&type=code) | Defines the AHB bus clock divider value. | (RCC_HCLK_DIV2) |
| [`MICROPY_HW_CLK_APB1_DIV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_APB1_DIV&type=code) | Defines the clock divider for the APB1 bus. | (RCC_APB1_DIV2) |
| [`MICROPY_HW_CLK_APB2_DIV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_APB2_DIV&type=code) | Defines the clock divider value for the APB2 bus. | (RCC_APB2_DIV2) |
| [`MICROPY_HW_CLK_APB3_DIV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_APB3_DIV&type=code) | Defines the clock divider for the APB3 bus. | (RCC_APB3_DIV2) |
| [`MICROPY_HW_CLK_APB4_DIV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_APB4_DIV&type=code) | Defines the clock divider for the APB4 bus. | (RCC_APB4_DIV2) |
| [`MICROPY_HW_CLK_LAST_FREQ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_LAST_FREQ&type=code) | Enables saving the last clock frequency settings for reconfiguration after a hard reset. | (1) |
| [`MICROPY_HW_CLK_PLL2FRAC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL2FRAC&type=code) | Fractional part of the PLL2 configuration, set to 0. | (0) |
| [`MICROPY_HW_CLK_PLL2M`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL2M&type=code) | Sets the PLL2M value for configuring the PLL2 clock at 200MHz for FMC and QSPI. | (4) |
| [`MICROPY_HW_CLK_PLL2N`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL2N&type=code) | Sets the PLL2 N value for clock configuration. | (100) |
| [`MICROPY_HW_CLK_PLL2P`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL2P&type=code) | Sets the division factor for PLL2 output clock. | (2) |
| [`MICROPY_HW_CLK_PLL2Q`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL2Q&type=code) | Sets the division factor for PLL2 output clock. | (2) |
| [`MICROPY_HW_CLK_PLL2R`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL2R&type=code) | Sets the division factor for PLL2 output clock. | (2) |
| [`MICROPY_HW_CLK_PLL2VCI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL2VCI&type=code) | Defines the range for PLL2 VCI clock configuration. | (RCC_PLL2VCIRANGE_2) |
| [`MICROPY_HW_CLK_PLL2VCO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL2VCO&type=code) | Defines the VCO selection for PLL2 as RCC_PLL2VCOWIDE. | (RCC_PLL2VCOWIDE) |
| [`MICROPY_HW_CLK_PLL3FRAC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL3FRAC&type=code) | Fractional part of the PLL3 configuration, set to 0. | (0) |
| [`MICROPY_HW_CLK_PLL3M`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL3M&type=code) | Sets the division factor M for PLL3, affecting the output frequency. | (8) |
| [`MICROPY_HW_CLK_PLL3N`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL3N&type=code) | Sets the N value for PLL3 configuration, affecting the output frequency. | (160) |
| [`MICROPY_HW_CLK_PLL3P`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL3P&type=code) | Sets the P divider value for PLL3 configuration. | (17) |
| [`MICROPY_HW_CLK_PLL3Q`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL3Q&type=code) | Sets the division factor for the PLL3 output Q. | (2) |
| [`MICROPY_HW_CLK_PLL3R`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL3R&type=code) | Sets the division factor R for PLL3 clock configuration. | (2) |
| [`MICROPY_HW_CLK_PLL3VCI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL3VCI&type=code) | Defines the PLL3 voltage range configuration. | (RCC_PLL3VCIRANGE_2) |
| [`MICROPY_HW_CLK_PLL3VCI_LL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL3VCI_LL&type=code) | Defines the input range for PLL3 VCO as LL_RCC_PLLINPUTRANGE_1_2. | (LL_RCC_PLLINPUTRANGE_1_2) |
| [`MICROPY_HW_CLK_PLL3VCO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL3VCO&type=code) | Defines the VCO selection for PLL3 as RCC_PLL3VCOWIDE. | (RCC_PLL3VCOWIDE) |
| [`MICROPY_HW_CLK_PLL3VCO_LL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLL3VCO_LL&type=code) | Sets the VCO output range for PLL3 to medium. | (LL_RCC_PLLVCORANGE_MEDIUM) |
| [`MICROPY_HW_CLK_PLLDIV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLDIV&type=code) | Sets the PLL division factor for clock configuration. | (RCC_CFGR_PLLDIV3) |
| [`MICROPY_HW_CLK_PLLFRAC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLFRAC&type=code) | Configures the fractional part of the PLL frequency. | (0) |
| [`MICROPY_HW_CLK_PLLM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLM&type=code) | Sets the PLLM value for clock configuration, affecting system clock frequency. | (25) |
| [`MICROPY_HW_CLK_PLLMUL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLMUL&type=code) | Determines the PLL multiplication factor for clock configuration. | (RCC_CFGR_PLLMUL12) |
| [`MICROPY_HW_CLK_PLLN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLN&type=code) | Sets the N value for the PLL configuration to achieve the desired CPU frequency. | (192) |
| [`MICROPY_HW_CLK_PLLP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLP&type=code) | Divides the PLL clock to obtain the core clock frequency. | (RCC_PLLP_DIV2) // divide PLL clock by this to get core clock |
| [`MICROPY_HW_CLK_PLLP1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLP1&type=code) | Sets the division factor for PLL1 output clock. | (1) |
| [`MICROPY_HW_CLK_PLLP2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLP2&type=code) | Sets the division factor for the PLL output clock. | (1) |
| [`MICROPY_HW_CLK_PLLQ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLQ&type=code) | Divides the core clock to achieve a 48MHz output frequency. | (7)             // divide core clock by this to get 48MHz |
| [`MICROPY_HW_CLK_PLLR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLR&type=code) | Sets the division factor for the PLLR clock output. | (RCC_PLLR_DIV2) |
| [`MICROPY_HW_CLK_PLLVCI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLVCI&type=code) | Defines the PLL VCI range for clock configuration. | (RCC_PLL1VCIRANGE_2) |
| [`MICROPY_HW_CLK_PLLVCI_LL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLVCI_LL&type=code) | Defines the input range for the PLL VCO as 4-8 MHz. | (LL_RCC_PLLINPUTRANGE_4_8) |
| [`MICROPY_HW_CLK_PLLVCO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLVCO&type=code) | Determines the VCO (Voltage Controlled Oscillator) range for the PLL configuration. | (RCC_PLL1VCOWIDE) |
| [`MICROPY_HW_CLK_PLLVCO_LL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_PLLVCO_LL&type=code) | Defines the VCO output range for the PLL as wide. | (LL_RCC_PLLVCORANGE_WIDE) |
| [`MICROPY_HW_CLK_USE_BYPASS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_USE_BYPASS&type=code) | Enables bypass mode for the HSE clock, using an external 8MHz signal instead of a crystal. | (1) |
| [`MICROPY_HW_CLK_USE_HSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_USE_HSE&type=code) | Enables the use of an external 32MHz TCXO with PLL as the system clock source. | (1) |
| [`MICROPY_HW_CLK_USE_HSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_USE_HSI&type=code) | Enables the use of the internal high-speed oscillator (HSI) as the clock source. | (1) |
| [`MICROPY_HW_CLK_USE_HSI48`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_USE_HSI48&type=code) | Enables the use of the internal 48MHz oscillator for the system clock. | (1) // internal 48MHz. |
| [`MICROPY_HW_CLK_VALUE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_CLK_VALUE&type=code) | Defines the clock source value using HSE (High-Speed External) oscillator. | (HSE_VALUE) |
#### MICROPY_HW_DAC

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_DAC0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_DAC0&type=code) | Defines the pin used for DAC0 functionality. | (pin_P014) // A4 |
| [`MICROPY_HW_DAC1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_DAC1&type=code) | Defines the DAC1 pin as pin_P015 (A5). Examples: Used in DAC initialization and configuration. | (pin_P015) // A5 |
#### MICROPY_HW_DEFAULT

This configuration group sets the default identifiers for various hardware communication protocols, including I2C, SPI, and UART. By defining these default IDs, it streamlines the setup process for hardware interactions, ensuring that the appropriate communication interfaces are readily available for use.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_DEFAULT_I2C_ID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_DEFAULT_I2C_ID&type=code) | Defines the default I2C bus ID for hardware configurations. | (-1) |
| [`MICROPY_HW_DEFAULT_SPI_ID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_DEFAULT_SPI_ID&type=code) | Identifies the default SPI bus ID, with a default value of -1 indicating no SPI bus. | (-1) |
| [`MICROPY_HW_DEFAULT_UART_ID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_DEFAULT_UART_ID&type=code) | Defines the default UART ID for hardware configurations, defaulting to -1 if not set. | (-1) |
#### MICROPY_HW_DFLL

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_DFLL_USB_SYNC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_DFLL_USB_SYNC&type=code) | Enables synchronization of the DFLL48M oscillator with the USB 1 kHz sync signal. | (1) |
#### MICROPY_HW_DMA

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_DMA_ENABLE_AUTO_TURN_OFF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_DMA_ENABLE_AUTO_TURN_OFF&type=code) | Enables automatic turn-off of the DMA after a period of inactivity. | (1) |
#### MICROPY_HW_ENABLE

This configuration group manages the enabling and availability of various hardware peripherals and GPIO functionalities on supported microcontroller platforms. It allows developers to customize the hardware capabilities, such as ADC, DAC, CAN, and specific GPIO pins, to suit their application needs.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_ENABLE_ADC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_ADC&type=code) | Controls the availability of the ADC peripheral, enabling pyb.ADC and pyb.ADCAll. | (0) // use machine.ADC instead |
| [`MICROPY_HW_ENABLE_ANALOG_ONLY_PINS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_ANALOG_ONLY_PINS&type=code) | Enables support for analog-only pins based on defined analog switches. | (1) |
| [`MICROPY_HW_ENABLE_CAN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_CAN&type=code) | Enables CAN bus support if CAN peripherals are defined. | (1) |
| [`MICROPY_HW_ENABLE_DAC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_DAC&type=code) | Enables the DAC peripheral for audio output and other applications. | (1) // A4, A5 |
| [`MICROPY_HW_ENABLE_DCMI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_DCMI&type=code) | Controls the enabling of the DCMI peripheral. | (0) |
| [`MICROPY_HW_ENABLE_FDCAN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_FDCAN&type=code) | Enables support for FDCAN peripherals on compatible MCUs. | (1) // define for MCUs with FDCAN |
| [`MICROPY_HW_ENABLE_GPIO0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO0&type=code) | Enables GPIO0 for various ESP32 SoC configurations. | (1) |
| [`MICROPY_HW_ENABLE_GPIO1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO1&type=code) | Enables GPIO1 for specific ESP32 configurations. | (1) |
| [`MICROPY_HW_ENABLE_GPIO10`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO10&type=code) | Enables GPIO10 functionality on the ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO11`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO11&type=code) | Enables GPIO pin 11 for hardware functionality. | (1) |
| [`MICROPY_HW_ENABLE_GPIO12`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO12&type=code) | Enables GPIO12 functionality on the ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO13`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO13&type=code) | Enables GPIO13 functionality on the ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO14`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO14&type=code) | Enables GPIO14 functionality on the ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO15`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO15&type=code) | Enables GPIO15 functionality on the ESP32. | (1) |
| [`MICROPY_HW_ENABLE_GPIO16`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO16&type=code) | Enables GPIO16 functionality on the ESP32. | (1) |
| [`MICROPY_HW_ENABLE_GPIO17`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO17&type=code) | Enables GPIO17 functionality on the ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO18`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO18&type=code) | Enables GPIO18 functionality on ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO19`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO19&type=code) | Enables GPIO19 for UART0_RXD functionality. | (1) // UART0_RXD |
| [`MICROPY_HW_ENABLE_GPIO2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO2&type=code) | Enables GPIO2 functionality on supported ESP32 targets. | (1) |
| [`MICROPY_HW_ENABLE_GPIO20`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO20&type=code) | Enables GPIO20 for UART0_TXD functionality. | (1) // UART0_TXD |
| [`MICROPY_HW_ENABLE_GPIO21`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO21&type=code) | Enables GPIO21 functionality on ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO22`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO22&type=code) | Enables GPIO22 functionality on the ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO23`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO23&type=code) | Enables GPIO23 functionality on the ESP32. | (1) |
| [`MICROPY_HW_ENABLE_GPIO25`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO25&type=code) | Enables GPIO25 functionality on the ESP32. | (1) |
| [`MICROPY_HW_ENABLE_GPIO26`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO26&type=code) | Enables GPIO26 functionality on the ESP32. | (1) |
| [`MICROPY_HW_ENABLE_GPIO27`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO27&type=code) | Enables GPIO pin 27 for use. | (1) |
| [`MICROPY_HW_ENABLE_GPIO3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO3&type=code) | Enables GPIO3 functionality on supported ESP32 targets. | (1) |
| [`MICROPY_HW_ENABLE_GPIO32`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO32&type=code) | Enables GPIO32 functionality on the ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO33`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO33&type=code) | Enables GPIO33 functionality on the ESP32. | (1) |
| [`MICROPY_HW_ENABLE_GPIO34`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO34&type=code) | Enables GPIO34 functionality on the ESP32. | (1) |
| [`MICROPY_HW_ENABLE_GPIO35`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO35&type=code) | Enables GPIO pin 35 for hardware functionality. | (1) |
| [`MICROPY_HW_ENABLE_GPIO36`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO36&type=code) | Enables GPIO36 functionality on the ESP32 platform. | (1) |
| [`MICROPY_HW_ENABLE_GPIO37`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO37&type=code) | Enables GPIO37 functionality on the ESP32 platform. | (1) |
| [`MICROPY_HW_ENABLE_GPIO38`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO38&type=code) | Enables GPIO pin 38 for hardware functionality. | (1) |
| [`MICROPY_HW_ENABLE_GPIO39`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO39&type=code) | Enables GPIO39 functionality on the ESP32 platform. | (1) |
| [`MICROPY_HW_ENABLE_GPIO4`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO4&type=code) | Enables GPIO4 functionality on the ESP32. | (1) |
| [`MICROPY_HW_ENABLE_GPIO40`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO40&type=code) | Enables GPIO pin 40 for hardware functionality. | (1) |
| [`MICROPY_HW_ENABLE_GPIO41`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO41&type=code) | Enables GPIO41 functionality. | (1) |
| [`MICROPY_HW_ENABLE_GPIO42`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO42&type=code) | Enables GPIO42 functionality. | (1) |
| [`MICROPY_HW_ENABLE_GPIO43`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO43&type=code) | Enables GPIO43 functionality. | (1) |
| [`MICROPY_HW_ENABLE_GPIO44`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO44&type=code) | Enables GPIO44 functionality on the ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO45`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO45&type=code) | Enables GPIO 45 functionality. | (1) |
| [`MICROPY_HW_ENABLE_GPIO46`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO46&type=code) | Enables GPIO46 functionality on the ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO47`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO47&type=code) | Enables GPIO47 functionality on ESP32S3 with extended I/O support. | (1) |
| [`MICROPY_HW_ENABLE_GPIO48`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO48&type=code) | Enables GPIO pin 48 for use on ESP32S3 with extended I/O. | (1) |
| [`MICROPY_HW_ENABLE_GPIO5`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO5&type=code) | Enables GPIO5 functionality on the ESP32. | (1) |
| [`MICROPY_HW_ENABLE_GPIO6`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO6&type=code) | Enables GPIO6 functionality on the ESP32. | (1) |
| [`MICROPY_HW_ENABLE_GPIO7`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO7&type=code) | Enables GPIO7 functionality on the ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO8`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO8&type=code) | Enables GPIO8 functionality on the ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_GPIO9`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_GPIO9&type=code) | Enables GPIO9 functionality on the ESP32 hardware. | (1) |
| [`MICROPY_HW_ENABLE_HW_DAC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_HW_DAC&type=code) | Enables hardware DAC support if DAC0 or DAC1 is defined. | (1) |
| [`MICROPY_HW_ENABLE_HW_I2C`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_HW_I2C&type=code) | Enables hardware I2C support when peripherals are defined. | (1) |
| [`MICROPY_HW_ENABLE_HW_I2C_TARGET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_HW_I2C_TARGET&type=code) | Enables hardware I2C target functionality for STM32 peripherals. | (1) |
| [`MICROPY_HW_ENABLE_HW_PWM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_HW_PWM&type=code) | Enables hardware PWM functionality. | (1) |
| [`MICROPY_HW_ENABLE_INTERNAL_FLASH_STORAGE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_INTERNAL_FLASH_STORAGE&type=code) | Selects between using internal flash storage (1 MByte) or onboard SPI flash (512 KByte). Examples: 1 for internal flash, 0 for SPI flash. | (0) |
| [`MICROPY_HW_ENABLE_INTERNAL_FLASH_STORAGE_SEGMENT2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_INTERNAL_FLASH_STORAGE_SEGMENT2&type=code) | Controls the use of a second segment of internal flash storage. | (0) |
| [`MICROPY_HW_ENABLE_MDNS_QUERIES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_MDNS_QUERIES&type=code) | Enables mDNS queries functionality for hostname resolution. | (1) |
| [`MICROPY_HW_ENABLE_MDNS_RESPONDER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_MDNS_RESPONDER&type=code) | Enables the mDNS responder functionality for network services. | (1) |
| [`MICROPY_HW_ENABLE_MMCARD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_MMCARD&type=code) | Enables the MMC interface, allowing interaction with MMC cards. | (0) |
| [`MICROPY_HW_ENABLE_OSPI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_OSPI&type=code) | Enables OSPI (OctoSPI) support for flash memory access. | (CORE_M55_HP) |
| [`MICROPY_HW_ENABLE_PSRAM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_PSRAM&type=code) | Enables the use of PSRAM for additional memory allocation. | (0) |
| [`MICROPY_HW_ENABLE_RF_SWITCH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_RF_SWITCH&type=code) | Enables the RF switch functionality for Wi-Fi modules. | (1) |
| [`MICROPY_HW_ENABLE_RNG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_RNG&type=code) | Enables the hardware RNG peripheral for random number generation. | (1) |
| [`MICROPY_HW_ENABLE_RTC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_RTC&type=code) | Enables the Real-Time Clock (RTC) functionality. | (1) |
| [`MICROPY_HW_ENABLE_SDCARD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_SDCARD&type=code) | Enables support for SD card functionality, requiring appropriate driver configuration for SPI interface. | (0) |
| [`MICROPY_HW_ENABLE_SERVO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_SERVO&type=code) | Enables the servo driver functionality for controlling hobby servos. | (0) // SERVO requires TIM5 (not on L452). |
| [`MICROPY_HW_ENABLE_STORAGE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_STORAGE&type=code) | Enables the storage subsystem if a block device is defined. | (1) |
| [`MICROPY_HW_ENABLE_TIMER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_TIMER&type=code) | Enables timer functionality on the hardware. | (1) |
| [`MICROPY_HW_ENABLE_UART_REPL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_UART_REPL&type=code) | Enables UART REPL for modules with external USB-UART, disabling native USB. | (1) |
| [`MICROPY_HW_ENABLE_USB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_USB&type=code) | Enables USB support when a USB cable is connected to specific pins. | (0) // can be enabled if USB cable connected to PA11/PA12 (D-/D+) |
| [`MICROPY_HW_ENABLE_USBDEV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_USBDEV&type=code) | Enables USB device support if the hardware supports USB OTG. | (SOC_USB_OTG_SUPPORTED) |
| [`MICROPY_HW_ENABLE_USB_RUNTIME_DEVICE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENABLE_USB_RUNTIME_DEVICE&type=code) | Enables support for the machine.USBDevice functionality. | (1) // Support machine.USBDevice |
#### MICROPY_HW_ENTER

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_ENTER_BOOTLOADER_VIA_RESET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ENTER_BOOTLOADER_VIA_RESET&type=code) | Determines if the bootloader is entered via a reset or direct jump. | (1) |
#### MICROPY_HW_ESP

This configuration set manages essential hardware functionalities for ESP devices, including GPIO pin assignments for hosted features, reset control for Wi-Fi, and support for advanced communication protocols like I2C and USB Serial/JTAG. It allows developers to customize hardware interactions and optimize performance based on specific ESP hardware capabilities.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_ESP_HOSTED_GPIO0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ESP_HOSTED_GPIO0&type=code) | Defines the GPIO pin used for ESP hosted functionality. | (pin_P803) |
| [`MICROPY_HW_ESP_HOSTED_RESET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ESP_HOSTED_RESET&type=code) | Controls the reset pin for ESP hosted Wi-Fi functionality. | (pin_P804) |
| [`MICROPY_HW_ESP_NEW_I2C_DRIVER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ESP_NEW_I2C_DRIVER&type=code) | Enables the use of a new I2C driver for ESP hardware. | (0) |
| [`MICROPY_HW_ESP_USB_SERIAL_JTAG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ESP_USB_SERIAL_JTAG&type=code) | Enables USB Serial/JTAG support if the hardware supports it and USB CDC is not enabled. | (SOC_USB_SERIAL_JTAG_SUPPORTED && !MICROPY_HW_USB_CDC) |
#### MICROPY_HW_ESP32S

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_ESP32S3_EXTENDED_IO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ESP32S3_EXTENDED_IO&type=code) | Enables extended GPIO functionality for ESP32-S3, allowing access to GPIO47 and GPIO48. | (1) |
#### MICROPY_HW_ETH

This configuration set manages the hardware settings for Ethernet communication, specifically focusing on the RMII interface. It includes definitions for various pins related to data transmission, reception, and control signals, as well as optimizations for DMA performance.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_ETH_DMA_ATTRIBUTE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ETH_DMA_ATTRIBUTE&type=code) | Aligns Ethernet DMA structures to a 16KB boundary for optimal performance. | __attribute__((aligned(16384))); |
| [`MICROPY_HW_ETH_MDC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ETH_MDC&type=code) | Defines the pin used for the Ethernet Management Data Clock (MDC) in RMII configuration. | (pyb_pin_W24) |
| [`MICROPY_HW_ETH_MDIO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ETH_MDIO&type=code) | Defines the pin used for the MDIO interface in Ethernet communication. | (pyb_pin_W15) |
| [`MICROPY_HW_ETH_RMII_CRS_DV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ETH_RMII_CRS_DV&type=code) | Defines the pin used for the Ethernet RMII Carrier Sense/Receive Data Valid signal. | (pyb_pin_W14) |
| [`MICROPY_HW_ETH_RMII_REF_CLK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ETH_RMII_REF_CLK&type=code) | Defines the reference clock pin for RMII Ethernet configuration. | (pyb_pin_W17) |
| [`MICROPY_HW_ETH_RMII_RXD0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ETH_RMII_RXD0&type=code) | Pin configuration for the RMII receive data line 0. | (pyb_pin_W51) |
| [`MICROPY_HW_ETH_RMII_RXD1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ETH_RMII_RXD1&type=code) | Pin configuration for the RMII receive data line 1. | (pyb_pin_W47) |
| [`MICROPY_HW_ETH_RMII_RXER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ETH_RMII_RXER&type=code) | Defines the pin used for the RMII receive error signal. | (pin_G2) |
| [`MICROPY_HW_ETH_RMII_TXD0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ETH_RMII_TXD0&type=code) | Pin configuration for the RMII transmit data line 0. | (pyb_pin_W45) |
| [`MICROPY_HW_ETH_RMII_TXD1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ETH_RMII_TXD1&type=code) | Pin configuration for the RMII transmit data line 1. | (pyb_pin_W49) |
| [`MICROPY_HW_ETH_RMII_TX_EN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ETH_RMII_TX_EN&type=code) | Pin configuration for the RMII transmit enable signal. | (pyb_pin_W8) |
#### MICROPY_HW_FLASH

This configuration group manages various parameters related to flash memory, including block size, clock frequency, and storage allocation. It ensures optimal performance and functionality of the flash filesystem, enabling features such as automatic mounting at boot and defining storage limits for firmware and data.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_FLASH_BLOCK_SIZE_BYTES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FLASH_BLOCK_SIZE_BYTES&type=code) | Defines the size of a flash memory block in bytes, set to 4096. | (4096) |
| [`MICROPY_HW_FLASH_CLK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FLASH_CLK&type=code) | Clock frequency for the flash memory interface, typically set to kFlexSpiSerialClk_100MHz or kFlexSpiSerialClk_133MHz. | kFlexSpiSerialClk_133MHz |
| [`MICROPY_HW_FLASH_DQS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FLASH_DQS&type=code) | Configures the read sample clock source for FlexSPI to use loopback from the DQS pad. | kFlexSPIReadSampleClk_LoopbackFromDqsPad |
| [`MICROPY_HW_FLASH_FS_LABEL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FLASH_FS_LABEL&type=code) | Defines the label for the flash filesystem. | "WEACT_F411_BLACKPILL" |
| [`MICROPY_HW_FLASH_LATENCY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FLASH_LATENCY&type=code) | Determines the number of wait states for flash memory access based on system clock frequency. | FLASH_LATENCY_7 // 210-216 MHz needs 7 wait states |
| [`MICROPY_HW_FLASH_MAX_FREQ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FLASH_MAX_FREQ&type=code) | Calculates the maximum frequency for flash operations based on system clock and SPI clock divider. | (SYS_CLK_HZ / 4) |
| [`MICROPY_HW_FLASH_MOUNT_AT_BOOT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FLASH_MOUNT_AT_BOOT&type=code) | Controls automatic mounting of the flash filesystem at boot based on storage enablement. | (MICROPY_HW_ENABLE_STORAGE) |
| [`MICROPY_HW_FLASH_STORAGE_BASE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FLASH_STORAGE_BASE&type=code) | Calculates the base address for flash storage by subtracting the storage size from total flash size. | (PICO_FLASH_SIZE_BYTES - MICROPY_HW_FLASH_STORAGE_BYTES) |
| [`MICROPY_HW_FLASH_STORAGE_BASE_ADDR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FLASH_STORAGE_BASE_ADDR&type=code) | Defines the base address for flash storage used in alif.Flash() and USB MSC. | (0) |
| [`MICROPY_HW_FLASH_STORAGE_BYTES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FLASH_STORAGE_BYTES&type=code) | Defines the number of bytes allocated for filesystem storage after reserving space for the firmware image. | (PICO_FLASH_SIZE_BYTES - (1 * 1024 * 1024)) |
| [`MICROPY_HW_FLASH_STORAGE_FS_BYTES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FLASH_STORAGE_FS_BYTES&type=code) | Defines the size of the flash storage filesystem in bytes (16 MB). Examples: Used in alif_flash.c and msc_disk.c for flash operations. | (16 * 1024 * 1024) |
| [`MICROPY_HW_FLASH_STORAGE_ROMFS_BYTES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FLASH_STORAGE_ROMFS_BYTES&type=code) | Defines the size of the ROM filesystem storage in bytes. | (16 * 1024 * 1024) |
#### MICROPY_HW_FMC

This configuration set defines the pin assignments for the Flexible Memory Controller (FMC) interface, which is essential for connecting external memory devices to the microcontroller. It specifies the pin mappings for address lines, data lines, and bank address lines, enabling proper communication and functionality with various memory types.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_FMC_A0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A0&type=code) | Defines the pin used for FMC address line A0. | (pyb_pin_FMC_A0) |
| [`MICROPY_HW_FMC_A1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A1&type=code) | Defines the pin used for FMC_A1 functionality. | (pyb_pin_FMC_A1) |
| [`MICROPY_HW_FMC_A10`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A10&type=code) | Represents the pin configuration for FMC_A10, typically used for external memory interfaces. | (pyb_pin_FMC_A10) |
| [`MICROPY_HW_FMC_A11`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A11&type=code) | Represents the pin configuration for FMC_A11, typically assigned to a specific GPIO pin. | (pyb_pin_FMC_A11) |
| [`MICROPY_HW_FMC_A12`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A12&type=code) | Defines the pin configuration for FMC_A12, used for static speed pin configuration. | (pyb_pin_FMC_A12) |
| [`MICROPY_HW_FMC_A2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A2&type=code) | Defines the pin used for FMC address line A2. | (pyb_pin_FMC_A2) |
| [`MICROPY_HW_FMC_A3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A3&type=code) | Defines the pin used for FMC address line A3. | (pyb_pin_FMC_A3) |
| [`MICROPY_HW_FMC_A4`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A4&type=code) | Defines the pin used for FMC_A4 functionality. | (pyb_pin_FMC_A4) |
| [`MICROPY_HW_FMC_A5`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A5&type=code) | Represents the pin configuration for FMC_A5, typically assigned to pyb_pin_FMC_A5. | (pyb_pin_FMC_A5) |
| [`MICROPY_HW_FMC_A6`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A6&type=code) | Defines the pin used for FMC_A6 functionality. | (pyb_pin_FMC_A6) |
| [`MICROPY_HW_FMC_A7`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A7&type=code) | Defines the pin used for FMC_A7 functionality, mapped to pyb_pin_FMC_A7. | (pyb_pin_FMC_A7) |
| [`MICROPY_HW_FMC_A8`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A8&type=code) | Represents the pin configuration for FMC_A8, typically assigned to pyb_pin_FMC_A8. | (pyb_pin_FMC_A8) |
| [`MICROPY_HW_FMC_A9`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_A9&type=code) | Represents the pin configuration for FMC_A9, typically assigned to (pyb_pin_FMC_A9). Examples include STM32F769DISC and ARDUINO_GIGA. | (pyb_pin_FMC_A9) |
| [`MICROPY_HW_FMC_BA0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_BA0&type=code) | Defines the pin used for the FMC Bank Address 0. | (pyb_pin_FMC_BA0) |
| [`MICROPY_HW_FMC_BA1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_BA1&type=code) | Defines the pin used for the FMC Bank Address line 1. | (pyb_pin_FMC_BA1) |
| [`MICROPY_HW_FMC_D0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D0&type=code) | Represents the FMC data pin D0, mapped to pyb_pin_FMC_D0. | (pyb_pin_FMC_D0) |
| [`MICROPY_HW_FMC_D1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D1&type=code) | Defines the pin used for FMC data line D1. | (pyb_pin_FMC_D1) |
| [`MICROPY_HW_FMC_D10`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D10&type=code) | Represents the pin configuration for FMC_D10, typically used for external memory interfaces. | (pyb_pin_FMC_D10) |
| [`MICROPY_HW_FMC_D11`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D11&type=code) | Defines the pin configuration for FMC data line D11. | (pyb_pin_FMC_D11) |
| [`MICROPY_HW_FMC_D12`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D12&type=code) | Defines the pin configuration for FMC data line D12. | (pyb_pin_FMC_D12) |
| [`MICROPY_HW_FMC_D13`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D13&type=code) | Defines the pin used for FMC data line D13. | (pyb_pin_FMC_D13) |
| [`MICROPY_HW_FMC_D14`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D14&type=code) | Defines the pin configuration for FMC_D14, mapped to pyb_pin_FMC_D14. | (pyb_pin_FMC_D14) |
| [`MICROPY_HW_FMC_D15`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D15&type=code) | Defines the pin configuration for FMC data line D15. | (pyb_pin_FMC_D15) |
| [`MICROPY_HW_FMC_D16`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D16&type=code) | Defines the pin configuration for FMC_D16 on the STM32F769DISC board. | (pyb_pin_FMC_D16) |
| [`MICROPY_HW_FMC_D17`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D17&type=code) | Represents the FMC data pin D17 for hardware configuration. | (pyb_pin_FMC_D17) |
| [`MICROPY_HW_FMC_D18`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D18&type=code) | Represents the FMC data pin D18 for hardware configuration. | (pyb_pin_FMC_D18) |
| [`MICROPY_HW_FMC_D19`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D19&type=code) | Represents the FMC data pin D19 for hardware configuration. | (pyb_pin_FMC_D19) |
| [`MICROPY_HW_FMC_D2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D2&type=code) | Defines the pin used for FMC data line D2. | (pyb_pin_FMC_D2) |
| [`MICROPY_HW_FMC_D20`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D20&type=code) | Represents the pin configuration for FMC_D20 on the STM32F769DISC board. | (pyb_pin_FMC_D20) |
| [`MICROPY_HW_FMC_D21`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D21&type=code) | Defines the pin configuration for FMC_D21 on the STM32F769DISC board. | (pyb_pin_FMC_D21) |
| [`MICROPY_HW_FMC_D22`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D22&type=code) | Defines the pin configuration for FMC_D22 as pyb_pin_FMC_D22. | (pyb_pin_FMC_D22) |
| [`MICROPY_HW_FMC_D23`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D23&type=code) | Defines the pin configuration for FMC data line D23. | (pyb_pin_FMC_D23) |
| [`MICROPY_HW_FMC_D24`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D24&type=code) | Represents the FMC data pin D24 for hardware configuration. | (pyb_pin_FMC_D24) |
| [`MICROPY_HW_FMC_D25`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D25&type=code) | Represents the pin configuration for FMC_D25 on the STM32F769DISC board. | (pyb_pin_FMC_D25) |
| [`MICROPY_HW_FMC_D26`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D26&type=code) | Defines the pin configuration for FMC_D26 as pyb_pin_FMC_D26. | (pyb_pin_FMC_D26) |
| [`MICROPY_HW_FMC_D27`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D27&type=code) | Defines the pin configuration for FMC_D27 as pyb_pin_FMC_D27. | (pyb_pin_FMC_D27) |
| [`MICROPY_HW_FMC_D28`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D28&type=code) | Defines the pin configuration for FMC_D28 as pyb_pin_FMC_D28. | (pyb_pin_FMC_D28) |
| [`MICROPY_HW_FMC_D29`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D29&type=code) | Defines the pin configuration for FMC_D29 on the STM32F769DISC board. | (pyb_pin_FMC_D29) |
| [`MICROPY_HW_FMC_D3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D3&type=code) | Represents the pin configuration for FMC data line D3. | (pyb_pin_FMC_D3) |
| [`MICROPY_HW_FMC_D30`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D30&type=code) | Represents the FMC_D30 pin configuration for hardware abstraction. | (pyb_pin_FMC_D30) |
| [`MICROPY_HW_FMC_D31`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D31&type=code) | Defines the pin configuration for FMC_D31 on the STM32F769DISC board. | (pyb_pin_FMC_D31) |
| [`MICROPY_HW_FMC_D4`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D4&type=code) | Defines the pin configuration for FMC data line D4. | (pyb_pin_FMC_D4) |
| [`MICROPY_HW_FMC_D5`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D5&type=code) | Represents the pin configuration for FMC data line D5. | (pyb_pin_FMC_D5) |
| [`MICROPY_HW_FMC_D6`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D6&type=code) | Defines the pin used for FMC data line D6. | (pyb_pin_FMC_D6) |
| [`MICROPY_HW_FMC_D7`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D7&type=code) | Represents the pin configuration for FMC data line D7. | (pyb_pin_FMC_D7) |
| [`MICROPY_HW_FMC_D8`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D8&type=code) | Represents the pin configuration for FMC data line D8. | (pyb_pin_FMC_D8) |
| [`MICROPY_HW_FMC_D9`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_D9&type=code) | Defines the pin configuration for FMC_D9 as pyb_pin_FMC_D9. | (pyb_pin_FMC_D9) |
| [`MICROPY_HW_FMC_NBL0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_NBL0&type=code) | Represents the pin configuration for the FMC NBL0 signal. | (pyb_pin_FMC_NBL0) |
| [`MICROPY_HW_FMC_NBL1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_NBL1&type=code) | Defines the pin used for the FMC NBL1 signal. | (pyb_pin_FMC_NBL1) |
| [`MICROPY_HW_FMC_NBL2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_NBL2&type=code) | Defines the pin configuration for FMC NBL2. | (pyb_pin_FMC_NBL2) |
| [`MICROPY_HW_FMC_NBL3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_NBL3&type=code) | Defines the pin for FMC NBL3 functionality. | (pyb_pin_FMC_NBL3) |
| [`MICROPY_HW_FMC_SDCKE0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_SDCKE0&type=code) | Defines the pin used for the SDRAM clock enable signal. | (pyb_pin_FMC_SDCKE0) |
| [`MICROPY_HW_FMC_SDCKE1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_SDCKE1&type=code) | Defines the pin used for the SDRAM chip enable signal. | (pin_B5) |
| [`MICROPY_HW_FMC_SDCLK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_SDCLK&type=code) | Defines the pin used for the SDRAM clock signal. | (pyb_pin_FMC_SDCLK) |
| [`MICROPY_HW_FMC_SDNBL0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_SDNBL0&type=code) | Defines the pin used for the SDRAM bank 0 low signal. | (pin_E0) |
| [`MICROPY_HW_FMC_SDNBL1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_SDNBL1&type=code) | Pin configuration for the second bank of the SDRAM. | (pin_E1) |
| [`MICROPY_HW_FMC_SDNCAS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_SDNCAS&type=code) | Defines the pin used for the SDNCAS signal in FMC configuration. | (pyb_pin_FMC_SDNCAS) |
| [`MICROPY_HW_FMC_SDNE0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_SDNE0&type=code) | Defines the pin used for the SDRAM chip select (SDNE0) in hardware configurations. | (pyb_pin_FMC_SDNE0) |
| [`MICROPY_HW_FMC_SDNE1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_SDNE1&type=code) | Defines the pin used for the SDRAM chip select (SDNE1). Examples: (pin_B6) | (pin_B6) |
| [`MICROPY_HW_FMC_SDNRAS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_SDNRAS&type=code) | Defines the pin used for the SD RAM Row Address Strobe (RAS). Examples: (pyb_pin_FMC_SDNRAS), (pin_F11). | (pyb_pin_FMC_SDNRAS) |
| [`MICROPY_HW_FMC_SDNWE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_SDNWE&type=code) | Defines the pin used for the SDRAM write enable signal. | (pyb_pin_FMC_SDNWE) |
| [`MICROPY_HW_FMC_SWAP_BANKS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_FMC_SWAP_BANKS&type=code) | Enables swapping of SDRAM banks for memory configuration. | (1) |
#### MICROPY_HW_HARD

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_HARD_FAULT_DEBUG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_HARD_FAULT_DEBUG&type=code) | Prints error information at reboot if the board crashed. | (0) |
#### MICROPY_HW_HAS

This configuration group controls the detection and availability of various hardware components on a microcontroller board, such as storage options, sensors, and user interface elements. By indicating the presence or absence of these components, it enables or disables specific functionalities and drivers, allowing for tailored software behavior based on the hardware capabilities.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_HAS_FLASH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_HAS_FLASH&type=code) | Indicates the presence of internal flash storage for use with pyb.Flash. | (0) // QSPI extflash not mounted |
| [`MICROPY_HW_HAS_KXTJ3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_HAS_KXTJ3&type=code) | Indicates the presence of the KXTJ3 accelerometer. | (1) |
| [`MICROPY_HW_HAS_LCD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_HAS_LCD&type=code) | Indicates the presence of an LCD driver, enabling related functionality. | (0) |
| [`MICROPY_HW_HAS_LED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_HAS_LED&type=code) | Indicates the presence of LED hardware on the board. | (1) |
| [`MICROPY_HW_HAS_LIS3DSH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_HAS_LIS3DSH&type=code) | Indicates the absence of the LIS3DSH sensor on the hardware. | (0) |
| [`MICROPY_HW_HAS_MMA7660`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_HAS_MMA7660&type=code) | Enables the MMA7660 accelerometer driver, allowing access to accelerometer functionalities. | (0) |
| [`MICROPY_HW_HAS_QSPI_FLASH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_HAS_QSPI_FLASH&type=code) | Indicates the presence of external QSPI flash storage on the MCU. | (0) |
| [`MICROPY_HW_HAS_SDCARD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_HAS_SDCARD&type=code) | Indicates the presence of an SD card on the hardware. | (0) |
| [`MICROPY_HW_HAS_SDHI_CARD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_HAS_SDHI_CARD&type=code) | Enables access to the SD card through the SDHI controller. | (0) |
| [`MICROPY_HW_HAS_SWITCH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_HAS_SWITCH&type=code) | Indicates the presence of a user switch, enabling related functionality. | (1) |
#### MICROPY_HW_I2C

This configuration set manages the I2C hardware interfaces, defining the specific pins for SCL and SDA lines across multiple I2C buses. It also establishes parameters such as baud rates, the number of interfaces, and the mapping of hardware controllers to logical indices, ensuring proper communication setup for I2C devices.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_I2C0_SCL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C0_SCL&type=code) | Defines the SCL pin for I2C0, requiring explicit pin arguments when no default is set. | (0) |
| [`MICROPY_HW_I2C0_SDA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C0_SDA&type=code) | Defines the SDA pin for I2C0 communication, typically assigned to a specific GPIO pin. | (pin_P407) // Note that conflict with PMOD IO1 |
| [`MICROPY_HW_I2C1_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C1_NAME&type=code) | Identifies the name of the first I2C bus, often linked to specific hardware slots. | "SLOT1234H" |
| [`MICROPY_HW_I2C1_SCL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C1_SCL&type=code) | Defines the SCL pin for I2C1 communication, typically assigned to a specific GPIO pin. | (pin_P205) |
| [`MICROPY_HW_I2C1_SDA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C1_SDA&type=code) | Defines the SDA pin for I2C1 communication, typically assigned to a specific GPIO pin. | (pin_B9)        // Arduino D14, pin 5 on CN10 |
| [`MICROPY_HW_I2C2_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C2_NAME&type=code) | Identifies the name of the I2C2 bus, often associated with specific hardware slots. | "SLOT2" |
| [`MICROPY_HW_I2C2_SCL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C2_SCL&type=code) | Defines the SCL pin for I2C2 communication, set to pin_P512. | (pin_P512) |
| [`MICROPY_HW_I2C2_SDA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C2_SDA&type=code) | Defines the SDA pin for I2C2, assigned to pin_B11. | (pin_B11)       //              pin 18 on CN10 |
| [`MICROPY_HW_I2C3_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C3_NAME&type=code) | Identifies the I2C3 interface associated with mikroBUS slot 1. | "SLOT1" |
| [`MICROPY_HW_I2C3_SCL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C3_SCL&type=code) | Defines the SCL pin for I2C3 as pin_A8. | (pin_A8) |
| [`MICROPY_HW_I2C3_SDA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C3_SDA&type=code) | Defines the SDA pin for I2C3, set to pin_C9. | (pin_C9)        //              pin  1 on CN10 |
| [`MICROPY_HW_I2C4_SCL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C4_SCL&type=code) | Defines the SCL pin for I2C4, mapped to pin C0. | (pin_C0)    //              pin 38 on CN7 |
| [`MICROPY_HW_I2C4_SDA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C4_SDA&type=code) | Defines the data line (SDA) pin for I2C4 communication. | (pin_C1)    //              pin 36 on CN7 |
| [`MICROPY_HW_I2C_BAUDRATE_DEFAULT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C_BAUDRATE_DEFAULT&type=code) | Sets the default I2C baud rate for communication, typically defined as PYB_I2C_SPEED_STANDARD. | (PYB_I2C_SPEED_STANDARD) |
| [`MICROPY_HW_I2C_BAUDRATE_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C_BAUDRATE_MAX&type=code) | Defines the maximum I2C baud rate for hardware configurations. | (PYB_I2C_SPEED_STANDARD) |
| [`MICROPY_HW_I2C_BAUDRATE_TIMING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C_BAUDRATE_TIMING&type=code) | Defines I2C baud rate timing values for various STM32 microcontrollers. | { \ |
| [`MICROPY_HW_I2C_INDEX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C_INDEX&type=code) | Defines the mapping of hardware I2C controllers to logical I2C indices. | { 5, 3, 1, 6, 2 } |
| [`MICROPY_HW_I2C_NO_DEFAULT_PINS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C_NO_DEFAULT_PINS&type=code) | Indicates that no default I2C pins are defined, requiring explicit pin arguments. | (1) |
| [`MICROPY_HW_I2C_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2C_NUM&type=code) | Determines the number of I2C interfaces based on the size of the i2c_index_table array. | ARRAY_SIZE(i2c_index_table) |
#### MICROPY_HW_I2S

This configuration controls the availability and functionality of I2S audio interfaces, allowing for the transmission of audio data through multiple buses. It specifies the number of I2S interfaces and enables specific buses for audio applications.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_I2S1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2S1&type=code) | Enables the first I2S bus for audio data transmission. | (1) |
| [`MICROPY_HW_I2S2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2S2&type=code) | Enables the second I2S bus for audio data transmission. | (1) |
| [`MICROPY_HW_I2S_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_I2S_NUM&type=code) | Determines the number of I2S interfaces available. | (3) |
#### MICROPY_HW_LED

This configuration set manages the hardware settings for multiple LEDs on a board, including their pin assignments, pull-up resistor options, and PWM control parameters. It allows for customization of LED behavior, such as active state and color support, facilitating effective status indication and visual feedback in applications.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_LED1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED1&type=code) | Configures the first LED pin for status indication. | (pin_A15) |
| [`MICROPY_HW_LED1_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED1_PIN&type=code) | Defines the pin used for the first LED on the board. | (pin_GPIO_SD_B1_00) |
| [`MICROPY_HW_LED1_PULLUP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED1_PULLUP&type=code) | Indicates whether pull-up resistor is enabled for LED1 (0 = disabled). Examples: 0 for no pull-up, 1 for pull-up enabled. | (0) |
| [`MICROPY_HW_LED1_PWM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED1_PWM&type=code) | Configures PWM settings for LED1 using timer and channel information. | { TIM12, 12, TIM_CHANNEL_1, GPIO_AF9_TIM12 } |
| [`MICROPY_HW_LED2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED2&type=code) | Defines the pin for the second LED, typically used for indicating status. | (pin_A5) // Green (next to power LED) |
| [`MICROPY_HW_LED2_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED2_PIN&type=code) | Defines the pin for the second LED on the MIMXRT1015 EVK board. | (pin_GPIO_SD_B1_01) |
| [`MICROPY_HW_LED2_PWM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED2_PWM&type=code) | Configures PWM settings for LED2 using TIM4, channel 2. | { TIM4, 4, TIM_CHANNEL_2, GPIO_AF2_TIM4 } |
| [`MICROPY_HW_LED3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED3&type=code) | Defines the pin for the third LED, typically used for indicating status. | (pin_B14) // Red LED on Nucleo |
| [`MICROPY_HW_LED3_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED3_PIN&type=code) | Defines the pin for the third LED on the MIMXRT1015 EVK board. | (pin_GPIO_SD_B1_02) |
| [`MICROPY_HW_LED3_PWM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED3_PWM&type=code) | Configures PWM settings for the third LED using timer and GPIO settings. | { TIM12, 12, TIM_CHANNEL_1, GPIO_AF9_TIM12 } |
| [`MICROPY_HW_LED4`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED4&type=code) | Defines the pin associated with the fourth LED on the hardware. | (pin_C13)   // Same as Led(2) |
| [`MICROPY_HW_LED4_PULLUP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED4_PULLUP&type=code) | Indicates that the yellow LED (LED4) is active high. | (0)     // Yellow is active high |
| [`MICROPY_HW_LED4_PWM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED4_PWM&type=code) | Configures PWM settings for LED4 using TIM3, channel 1, and GPIO alternate function 2. | { TIM3, 3, TIM_CHANNEL_1, GPIO_AF2_TIM3 } |
| [`MICROPY_HW_LED5_PWM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED5_PWM&type=code) | Configures the PWM settings for LED5. | { NULL, 0, 0, 0 } |
| [`MICROPY_HW_LED6_PWM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED6_PWM&type=code) | Configures LED6 for PWM control with default parameters. | { NULL, 0, 0, 0 } |
| [`MICROPY_HW_LED_BLUE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED_BLUE&type=code) | Defines the GPIO pin number for the blue LED. | (18)  // LED3 DS8 Blue |
| [`MICROPY_HW_LED_COUNT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED_COUNT&type=code) | Determines the number of LEDs available on the hardware, such as 4 for 3 RGB and 1 Yellow. | (4)     // 3 RGB + 1 Yellow |
| [`MICROPY_HW_LED_GREEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED_GREEN&type=code) | Defines the pin number for the green LED on the board. | (16)  // LED2 DS8 Green |
| [`MICROPY_HW_LED_INVERTED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED_INVERTED&type=code) | Indicates that LEDs are on when the pin is driven low. | (1) // LEDs are on when pin is driven low |
| [`MICROPY_HW_LED_PULLUP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED_PULLUP&type=code) | Indicates whether the RGB LED is active low (1) or active high (0). Examples: 1 for active low RGB LED, 0 for active high yellow LED. | (1)     // RGB LED is active low |
| [`MICROPY_HW_LED_RED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED_RED&type=code) | Defines the pin number for the red LED. | (8)   // LED1 DS8 Red |
| [`MICROPY_HW_LED_TRICOLOR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LED_TRICOLOR&type=code) | Enables support for a tricolor LED (red, green, blue) on the hardware. | (1) |
#### MICROPY_HW_LIGHTSLEEP

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_LIGHTSLEEP_ALARM_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LIGHTSLEEP_ALARM_NUM&type=code) | Defines the hardware timer alarm index for light sleep functionality. | (1) |
#### MICROPY_HW_LPSPI

This configuration controls the pin assignments for the LPSPI0 interface, specifying the MISO, MOSI, and SCK pins. It ensures that the correct hardware connections are established for SPI communication, facilitating data transfer between devices.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_LPSPI0_MISO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LPSPI0_MISO&type=code) | Defines the MISO pin for the LPSPI0 interface as pin_P7_4. | (pin_P7_4) |
| [`MICROPY_HW_LPSPI0_MOSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LPSPI0_MOSI&type=code) | Defines the MOSI pin for LPSPI0 as pin_P7_5. | (pin_P7_5) |
| [`MICROPY_HW_LPSPI0_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LPSPI0_SCK&type=code) | Defines the SCK pin for LPSPI0 as pin_P7_6. | (pin_P7_6) |
#### MICROPY_HW_LPUART

This configuration set defines the receive and transmit pins for two Low Power Universal Asynchronous Receiver-Transmitter (LPUART) interfaces, enabling serial communication capabilities. By specifying these pins, it allows for flexible hardware setups tailored to specific application needs.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_LPUART1_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LPUART1_RX&type=code) | Defines the receive pin for LPUART1, typically used for serial communication. | (pin_A3)  // A3 (to STLINK), B10, C0 |
| [`MICROPY_HW_LPUART1_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LPUART1_TX&type=code) | Defines the transmit pin for LPUART1, typically used for serial communication. | (pin_A9) |
| [`MICROPY_HW_LPUART2_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LPUART2_RX&type=code) | Defines the receive pin for LPUART2 as pin_C7. | (pin_C7) |
| [`MICROPY_HW_LPUART2_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_LPUART2_TX&type=code) | Defines the transmit pin for LPUART2. | (pin_C6) |
#### MICROPY_HW_MAX

This configuration group defines the maximum available hardware interfaces and peripherals for various communication protocols and timers, including CAN, I2C, I2S, UART, and timers. It allows developers to tailor the MicroPython environment to the specific capabilities of the target hardware, ensuring efficient resource management.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_MAX_CAN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MAX_CAN&type=code) | Determines the maximum number of CAN interfaces available. | (0) |
| [`MICROPY_HW_MAX_I2C`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MAX_I2C&type=code) | Determines the maximum number of I2C interfaces available on the hardware. | (2) |
| [`MICROPY_HW_MAX_I2S`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MAX_I2S&type=code) | Sets the maximum number of I2S peripherals available. | (2) |
| [`MICROPY_HW_MAX_LPUART`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MAX_LPUART&type=code) | Sets the maximum number of Low Power UARTs available. | (0) |
| [`MICROPY_HW_MAX_TIMER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MAX_TIMER&type=code) | Sets the maximum number of hardware timers available. | (11) |
| [`MICROPY_HW_MAX_UART`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MAX_UART&type=code) | Sets the maximum number of UART interfaces available, including LPUART. | (5) // UART1-5 + LPUART1 |
#### MICROPY_HW_MCU

This configuration group manages essential parameters related to the microcontroller hardware, including its name, clock settings, and oscillator options. It allows for the customization of system and peripheral clock frequencies, as well as the choice of clock source, ensuring optimal performance and power management for the specific hardware setup.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_MCU_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MCU_NAME&type=code) | Defines the name of the microcontroller used in the hardware. | MICROPY_PY_SYS_PLATFORM |
| [`MICROPY_HW_MCU_OSC32KULP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MCU_OSC32KULP&type=code) | Enables the use of the 32K Low Power oscillator instead of the 32kHz crystal for clock generation. | (1) |
| [`MICROPY_HW_MCU_PCLK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MCU_PCLK&type=code) | Defines the peripheral clock frequency for the MCU. | 100000000 |
| [`MICROPY_HW_MCU_SYSCLK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MCU_SYSCLK&type=code) | Defines the system clock frequency for the MCU. | 200000000 |
#### MICROPY_HW_MCUFLASH

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_MCUFLASH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MCUFLASH&type=code) | Enables the use of internal flash memory for the file system. | (1) |
#### MICROPY_HW_MMA

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_MMA_AVDD_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MMA_AVDD_PIN&type=code) | Pin configuration for the AVDD power supply of the MMA accelerometer. | (pin_A10) |
#### MICROPY_HW_MMCARD

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_MMCARD_LOG_BLOCK_NBR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MMCARD_LOG_BLOCK_NBR&type=code) | Defines the number of logical blocks for the MMC card to support specific hardware configurations. | (7469056 + 2048) |
#### MICROPY_HW_MUSIC

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_MUSIC_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_MUSIC_PIN&type=code) | Defines the pin used for music output on the micro:bit. | (3) |
#### MICROPY_HW_NIC

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_NIC_ETH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_NIC_ETH&type=code) | Defines the Ethernet network interface using LAN type. | { MP_ROM_QSTR(MP_QSTR_LAN), MP_ROM_PTR(&network_lan_type) }, |
#### MICROPY_HW_NINA

This configuration set manages the pin assignments and functionalities for the NINA module, including acknowledgment, chip select, and various GPIO operations. It ensures proper communication and control of the ublox Nina-W10 module by defining essential signal pins such as RTS and CTS.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_NINA_ACK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_NINA_ACK&type=code) | Pin configuration for the NINA module's acknowledgment signal. | pin_find(MP_OBJ_NEW_QSTR(MP_QSTR_ESP_BUSY)) |
| [`MICROPY_HW_NINA_CS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_NINA_CS&type=code) | Identifies the chip select pin for the NINA module. | pin_find(MP_OBJ_NEW_QSTR(MP_QSTR_ESP_CS)) |
| [`MICROPY_HW_NINA_CTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_NINA_CTS&type=code) | Represents the Clear To Send (CTS) pin for the NINA module, linked to the ACK pin. | MICROPY_HW_NINA_ACK |
| [`MICROPY_HW_NINA_GPIO0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_NINA_GPIO0&type=code) | Defines the GPIO pin number used for the NINA module's GPIO0 functionality. | (2) |
| [`MICROPY_HW_NINA_GPIO1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_NINA_GPIO1&type=code) | Defines the GPIO pin number for the NINA module's GPIO1. | (15) |
| [`MICROPY_HW_NINA_RESET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_NINA_RESET&type=code) | Pin configuration for resetting the ublox Nina-W10 module. | (3) |
| [`MICROPY_HW_NINA_RTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_NINA_RTS&type=code) | Defines the RTS pin for the NINA module using the MOSI pin. | pin_find(MP_OBJ_NEW_QSTR(MP_QSTR_MOSI)) |
#### MICROPY_HW_NUM

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_NUM_PIN_IRQS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_NUM_PIN_IRQS&type=code) | Determines the number of pin interrupt requests available. | (4 * 32 + 3) |
#### MICROPY_HW_OSPI

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_OSPI_CS_HIGH_CYCLES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPI_CS_HIGH_CYCLES&type=code) | Determines the number of cycles nCS remains high, set to 2 cycles. | (2) // nCS stays high for 2 cycles |
| [`MICROPY_HW_OSPI_PRESCALER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPI_PRESCALER&type=code) | Sets the prescaler for the OSPI clock, determining F_CLK as F_AHB/3. | (3) // F_CLK = F_AHB/3 |
#### MICROPY_HW_OSPIFLASH

This configuration set defines the pin assignments and parameters for interfacing with external OSPI flash memory. It specifies the chip select, data lines, clock, and size of the flash, enabling proper communication and functionality between the hardware and the flash storage.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_OSPIFLASH_CS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPIFLASH_CS&type=code) | Defines the chip select pin for the external OSPI flash. | (pin_G6) |
| [`MICROPY_HW_OSPIFLASH_DQS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPIFLASH_DQS&type=code) | Defines the data strobe pin for external OSPI flash. | (pin_C5) |
| [`MICROPY_HW_OSPIFLASH_IO0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPIFLASH_IO0&type=code) | Defines the pin used for the first data line of the external OSPI flash. | (pin_D11) |
| [`MICROPY_HW_OSPIFLASH_IO1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPIFLASH_IO1&type=code) | Defines the pin used for the OSPIFLASH IO1 connection. | (pin_D12) |
| [`MICROPY_HW_OSPIFLASH_IO2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPIFLASH_IO2&type=code) | Defines the pin used for the OSPIFLASH IO2 interface. | (pin_C2) |
| [`MICROPY_HW_OSPIFLASH_IO3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPIFLASH_IO3&type=code) | Defines the pin used for OSPIFLASH IO3, set to pin_D13. | (pin_D13) |
| [`MICROPY_HW_OSPIFLASH_IO4`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPIFLASH_IO4&type=code) | Defines the pin used for the OSPIFLASH IO4 interface. | (pin_H2) |
| [`MICROPY_HW_OSPIFLASH_IO5`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPIFLASH_IO5&type=code) | Defines the pin used for OSPIFLASH IO5, assigned to pin_H3. | (pin_H3) |
| [`MICROPY_HW_OSPIFLASH_IO6`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPIFLASH_IO6&type=code) | Defines the pin used for OSPIFLASH IO6 as pin_G9. | (pin_G9) |
| [`MICROPY_HW_OSPIFLASH_IO7`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPIFLASH_IO7&type=code) | Defines the pin used for OSPIFLASH IO7 as pin_C0. | (pin_C0) |
| [`MICROPY_HW_OSPIFLASH_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPIFLASH_SCK&type=code) | Defines the SCK pin for the external OSPI flash interface. | (pin_F10) |
| [`MICROPY_HW_OSPIFLASH_SIZE_BITS_LOG2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_OSPIFLASH_SIZE_BITS_LOG2&type=code) | Defines the size of the external OSPI flash in bits, set to 512MBit. | (29) |
#### MICROPY_HW_PIN

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_PIN_EXT_COUNT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PIN_EXT_COUNT&type=code) | Enables support for externally controlled pins. | (7) |
#### MICROPY_HW_PSRAM

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_PSRAM_CS_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PSRAM_CS_PIN&type=code) | Defines the chip select pin for PSRAM. | (0) |
#### MICROPY_HW_PWM

This configuration set defines the names and output pins for multiple PWM channels, enabling precise control over PWM signal generation for various applications. It facilitates the management of hardware interfaces for tasks such as motor control and LED brightness adjustment.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_PWM0_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM0_NAME&type=code) | Defines the name for the first PWM channel. | "PWM0" |
| [`MICROPY_HW_PWM1_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM1_NAME&type=code) | Defines the name for the second PWM channel. | "PWM1" |
| [`MICROPY_HW_PWM2_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM2_NAME&type=code) | Defines the name for the second PWM channel. | "PWM2" |
| [`MICROPY_HW_PWM3_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM3_NAME&type=code) | Defines the name for the PWM3 hardware interface. | "PWM3" |
| [`MICROPY_HW_PWM_1A`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_1A&type=code) | Defines the PWM output on pin P105. | (pin_P105) |
| [`MICROPY_HW_PWM_2A`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_2A&type=code) | Defines the PWM output on pin P113 (D5). Examples: Used for controlling motors or LED brightness. | (pin_P113) // D5 |
| [`MICROPY_HW_PWM_2B`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_2B&type=code) | Defines the PWM output for pin P114 (D6) on the VK_RA6M5 board. | (pin_P114) // D6 |
| [`MICROPY_HW_PWM_3A`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_3A&type=code) | Defines the PWM output for channel 3A on pin P111 (D3). Examples: Used in PWM configuration for VK_RA6M5 board. | (pin_P111) // D3 |
| [`MICROPY_HW_PWM_3B`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_3B&type=code) | Defines the PWM pin for channel 3B as pin_P112 (D4). Examples: Used in PWM configurations for devices. | (pin_P112) // D4 |
| [`MICROPY_HW_PWM_4A`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_4A&type=code) | Defines the PWM output for channel 4A on pin P115 (D9). Examples: Used in PWM configurations for devices requiring PWM signal generation. | (pin_P115) // D9 |
| [`MICROPY_HW_PWM_4B`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_4B&type=code) | Defines the PWM pin for channel 4B as pin_P608 (D7). Examples: Used in PWM configuration for devices. | (pin_P608) // D7 |
| [`MICROPY_HW_PWM_6A`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_6A&type=code) | Defines the PWM output for channel 6A on pin P601. | (pin_P601) |
| [`MICROPY_HW_PWM_6B`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_6B&type=code) | Defines the PWM pin for channel 6B, associated with pin P408. | (pin_P408) // PN3_8 |
| [`MICROPY_HW_PWM_7A`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_7A&type=code) | Defines the PWM pin for channel 7A as pin_P304. | (pin_P304) // H6_5 |
| [`MICROPY_HW_PWM_7B`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_7B&type=code) | Defines the PWM pin for channel 7B as pin_P303. | (pin_P303) // H6_3 |
| [`MICROPY_HW_PWM_8A`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_8A&type=code) | Defines the PWM output for channel 8A on pin P605. | (pin_P605) // PN4_4 |
| [`MICROPY_HW_PWM_8B`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWM_8B&type=code) | Defines the PWM output pin for channel 8B, mapped to pin P604. | (pin_P604) // PN4_3 |
#### MICROPY_HW_PWR

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_PWR_SMPS_CONFIG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_PWR_SMPS_CONFIG&type=code) | Configures the power supply mode for SMPS on supported STM32 boards. | (PWR_SMPS_1V8_SUPPLIES_LDO) |
#### MICROPY_HW_QSPI

This configuration set manages various parameters related to Quad Serial Peripheral Interface (QSPI) operations, including timing, memory region sizing, and clock frequency settings. It allows for fine-tuning of QSPI behavior to optimize performance and reliability in embedded applications.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_QSPI_CS_HIGH_CYCLES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPI_CS_HIGH_CYCLES&type=code) | Sets the number of cycles nCS remains high, configured to 2 cycles. | 2  // nCS stays high for 2 cycles |
| [`MICROPY_HW_QSPI_MPU_REGION_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPI_MPU_REGION_SIZE&type=code) | Calculates the MPU region size for QSPI in units of 1024*1024 bytes. | ((1 << (MICROPY_HW_QSPIFLASH_SIZE_BITS_LOG2 - 3)) >> 20) |
| [`MICROPY_HW_QSPI_PRESCALER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPI_PRESCALER&type=code) | Determines the prescaler value for the QSPI clock frequency. | (MICROPY_BOARD_SPIFLASH_CHIP_PARAMS1->qspi_prescaler) |
| [`MICROPY_HW_QSPI_SAMPLE_SHIFT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPI_SAMPLE_SHIFT&type=code) | Enables sample shift for QSPI configuration. | 1  // sample shift enabled |
| [`MICROPY_HW_QSPI_TIMEOUT_COUNTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPI_TIMEOUT_COUNTER&type=code) | Controls the timeout counter for QSPI operations, with 0 disabling it. | 0  // timeout counter disabled (see F7 errata) |
#### MICROPY_HW_QSPIFLASH

This configuration set defines the parameters for interfacing with QSPI flash memory, including the specific chip used, the pin assignments for data lines, chip select, and clock signals. It also specifies the size of the external flash memory, enabling proper communication and functionality within the hardware setup.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_QSPIFLASH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPIFLASH&type=code) | Defines the specific QSPI flash memory chip used in the hardware configuration. | W25Q16JV_IQ |
| [`MICROPY_HW_QSPIFLASH_CS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPIFLASH_CS&type=code) | Defines the chip select pin for QSPI flash. | (pyb_pin_QSPI2_CS) |
| [`MICROPY_HW_QSPIFLASH_IO0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPIFLASH_IO0&type=code) | Defines the pin used for QSPI flash data line 0. | (pyb_pin_QSPI2_D0) |
| [`MICROPY_HW_QSPIFLASH_IO1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPIFLASH_IO1&type=code) | Defines the pin used for QSPI flash data line 1. | (pyb_pin_QSPI2_D1) |
| [`MICROPY_HW_QSPIFLASH_IO2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPIFLASH_IO2&type=code) | Defines the pin used for QSPI Flash IO2. | (pyb_pin_QSPI2_D2) |
| [`MICROPY_HW_QSPIFLASH_IO3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPIFLASH_IO3&type=code) | Defines the pin used for QSPI Flash IO3, mapped to pyb_pin_QSPI2_D3. | (pyb_pin_QSPI2_D3) |
| [`MICROPY_HW_QSPIFLASH_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPIFLASH_SCK&type=code) | Defines the clock pin for the QSPI flash interface. | (pyb_pin_QSPI2_CLK) |
| [`MICROPY_HW_QSPIFLASH_SIZE_BITS_LOG2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_QSPIFLASH_SIZE_BITS_LOG2&type=code) | Log2 of the size of external QSPI flash in bits, indicating 512MBit capacity. | (29) |
#### MICROPY_HW_RCC

This configuration set manages the clock sources and states for various peripherals within the hardware, ensuring proper operation of components such as ADC, I2C, SPI, and USB. It allows for customization of oscillator states and PLL sources, facilitating optimized performance and functionality across the system.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_RCC_ADC_CLKSOURCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_ADC_CLKSOURCE&type=code) | Sets the clock source for the ADC peripheral to PLL3. | (RCC_ADCCLKSOURCE_PLL3) |
| [`MICROPY_HW_RCC_FDCAN_CLKSOURCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_FDCAN_CLKSOURCE&type=code) | Clock source configuration for the FDCAN peripheral, set to use the PLL. | (RCC_FDCANCLKSOURCE_PLL) |
| [`MICROPY_HW_RCC_FMC_CLKSOURCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_FMC_CLKSOURCE&type=code) | Defines the clock source for the FMC peripheral as PLL2. | (RCC_FMCCLKSOURCE_PLL2) |
| [`MICROPY_HW_RCC_HSE_STATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_HSE_STATE&type=code) | Determines the state of the High-Speed External (HSE) oscillator, set to bypass power mode. | (RCC_HSE_BYPASS_PWR) |
| [`MICROPY_HW_RCC_HSI48_STATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_HSI48_STATE&type=code) | Defines the state of the HSI48 oscillator as enabled. | (RCC_HSI48_ON) |
| [`MICROPY_HW_RCC_HSI_STATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_HSI_STATE&type=code) | Determines the state of the HSI oscillator, either ON or OFF. | (RCC_HSI_OFF) |
| [`MICROPY_HW_RCC_I2C123_CLKSOURCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_I2C123_CLKSOURCE&type=code) | Clock source for I2C123 peripheral set to D2PCLK1. | (RCC_I2C123CLKSOURCE_D2PCLK1) |
| [`MICROPY_HW_RCC_OSCILLATOR_TYPE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_OSCILLATOR_TYPE&type=code) | Combines HSE and HSI48 oscillator types for clock configuration, enabling RNG functionality. | (RCC_OSCILLATORTYPE_HSE \| RCC_OSCILLATORTYPE_HSI48) |
| [`MICROPY_HW_RCC_PLL_SRC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_PLL_SRC&type=code) | Determines the source for the PLL clock, set to HSI or HSE. | (RCC_PLLSOURCE_HSI) |
| [`MICROPY_HW_RCC_QSPI_CLKSOURCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_QSPI_CLKSOURCE&type=code) | Defines the clock source for the QSPI peripheral as PLL2. | (RCC_QSPICLKSOURCE_PLL2) |
| [`MICROPY_HW_RCC_RNG_CLKSOURCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_RNG_CLKSOURCE&type=code) | Defines the clock source for the RNG peripheral as HSI48. | (RCC_RNGCLKSOURCE_HSI48) |
| [`MICROPY_HW_RCC_RTC_CLKSOURCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_RTC_CLKSOURCE&type=code) | Defines the clock source for the RTC peripheral, set to LSI. | (RCC_RTCCLKSOURCE_LSI) |
| [`MICROPY_HW_RCC_SDMMC_CLKSOURCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_SDMMC_CLKSOURCE&type=code) | Defines the clock source for the SDMMC peripheral as PLL. | (RCC_SDMMCCLKSOURCE_PLL) |
| [`MICROPY_HW_RCC_SPI123_CLKSOURCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_SPI123_CLKSOURCE&type=code) | Defines the clock source for SPI123 peripheral as PLL3. | (RCC_SPI123CLKSOURCE_PLL3) |
| [`MICROPY_HW_RCC_USB_CLKSOURCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RCC_USB_CLKSOURCE&type=code) | Defines the clock source for USB peripheral as HSI48. | (RCC_USBCLKSOURCE_HSI48) |
#### MICROPY_HW_REPL

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_REPL_UART_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_REPL_UART_RX&type=code) | Defines the RX pin for the REPL UART interface. | (pin_P12_1) |
| [`MICROPY_HW_REPL_UART_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_REPL_UART_TX&type=code) | Defines the UART transmit pin for the REPL interface. | (pin_P12_2) |
#### MICROPY_HW_RFCORE

This configuration set manages various parameters and settings related to Bluetooth Low Energy (BLE) functionality within the RF core. It allows developers to customize aspects such as attribute sizes, connection parameters, and clock sources to optimize BLE performance and resource allocation.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_RFCORE_BLE_ATT_VALUE_ARRAY_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_ATT_VALUE_ARRAY_SIZE&type=code) | Defines the size of the attribute value array for BLE. | (0) |
| [`MICROPY_HW_RFCORE_BLE_DATA_LENGTH_EXTENSION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_DATA_LENGTH_EXTENSION&type=code) | Enables data length extension for BLE communication. | (1) |
| [`MICROPY_HW_RFCORE_BLE_HSE_STARTUP_TIME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_HSE_STARTUP_TIME&type=code) | Defines the startup time for the High-Speed External (HSE) clock in BLE applications. | (0x148) |
| [`MICROPY_HW_RFCORE_BLE_LL_ONLY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_LL_ONLY&type=code) | Enables the use of the Link Layer (LL) only for the BLE stack. | (1) // use LL only, we provide the rest of the BLE stack |
| [`MICROPY_HW_RFCORE_BLE_LSE_SOURCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_LSE_SOURCE&type=code) | Selects LSE as the clock source for the rfcore. | (0) // use LSE to clock the rfcore (see errata 2.2.1) |
| [`MICROPY_HW_RFCORE_BLE_MASTER_SCA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_MASTER_SCA&type=code) | Configures the Slave Clock Accuracy for BLE master mode. | (0) |
| [`MICROPY_HW_RFCORE_BLE_MAX_ATT_MTU`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_MAX_ATT_MTU&type=code) | Defines the maximum ATT MTU size for BLE connections. | (0) |
| [`MICROPY_HW_RFCORE_BLE_MAX_CONN_EVENT_LENGTH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_MAX_CONN_EVENT_LENGTH&type=code) | Maximum connection event length for BLE, set to the maximum value. | (0xffffffff) |
| [`MICROPY_HW_RFCORE_BLE_MBLOCK_COUNT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_MBLOCK_COUNT&type=code) | Defines the count of memory blocks for BLE operations. | (0x79) |
| [`MICROPY_HW_RFCORE_BLE_NUM_GATT_ATTRIBUTES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_NUM_GATT_ATTRIBUTES&type=code) | Sets the number of GATT attributes for BLE configuration, defaulting to 0. | (0) |
| [`MICROPY_HW_RFCORE_BLE_NUM_GATT_SERVICES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_NUM_GATT_SERVICES&type=code) | Sets the number of GATT services for BLE configuration. | (0) |
| [`MICROPY_HW_RFCORE_BLE_NUM_LINK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_NUM_LINK&type=code) | Sets the number of BLE links supported. | (1) |
| [`MICROPY_HW_RFCORE_BLE_PREPARE_WRITE_LIST_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_PREPARE_WRITE_LIST_SIZE&type=code) | Determines the size of the prepare write list for BLE operations. | (0) |
| [`MICROPY_HW_RFCORE_BLE_SLAVE_SCA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_SLAVE_SCA&type=code) | Defines the Slave Clock Accuracy for BLE in the RF core. | (0) |
| [`MICROPY_HW_RFCORE_BLE_VITERBI_MODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RFCORE_BLE_VITERBI_MODE&type=code) | Enables Viterbi decoding mode for BLE communication. | (1) |
> REVIEW: BLE ATT/MTU/conn-event limits set here are not called out in [docs/library/bluetooth.rst](docs/library/bluetooth.rst) or the STM32/NUCLEO port notes; include a short limits table (MTU, links, prepare-write slots) per port.
#### MICROPY_HW_ROMFS

This configuration set manages the setup and parameters for the ROM filesystem, including its storage locations, sizes, and the ability to utilize both internal and external flash memory options. It allows for the definition of multiple partitions within the filesystem, enabling flexible storage solutions tailored to the hardware capabilities.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_ROMFS_BASE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_BASE&type=code) | Calculates the base address for the ROM filesystem in flash memory. | (MICROPY_HW_FLASH_STORAGE_BASE - MICROPY_HW_ROMFS_BYTES) |
| [`MICROPY_HW_ROMFS_BYTES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_BYTES&type=code) | Defines the size of the ROM filesystem in bytes. | (uintptr_t)(&_micropy_hw_romfs_part0_size) |
| [`MICROPY_HW_ROMFS_ENABLE_EXTERNAL_QSPI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_ENABLE_EXTERNAL_QSPI&type=code) | Enables the use of ROMFS on external QSPI flash. | (1) |
| [`MICROPY_HW_ROMFS_ENABLE_EXTERNAL_XSPI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_ENABLE_EXTERNAL_XSPI&type=code) | Enables the use of ROMFS on external XSPI flash. | (1) |
| [`MICROPY_HW_ROMFS_ENABLE_INTERNAL_FLASH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_ENABLE_INTERNAL_FLASH&type=code) | Controls the enabling of ROMFS on internal flash storage. | (0) |
| [`MICROPY_HW_ROMFS_ENABLE_PART0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_ENABLE_PART0&type=code) | Enables the first ROMFS partition. | (1) |
| [`MICROPY_HW_ROMFS_ENABLE_PART1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_ENABLE_PART1&type=code) | Enables the second ROMFS partition if defined, allowing for additional file system storage. | (CORE_M55_HP) |
| [`MICROPY_HW_ROMFS_PART0_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_PART0_SIZE&type=code) | Determines the size of the first ROM filesystem partition based on the memory size of the SPI flash. | (1 << MICROPY_BOARD_SPIFLASH_CHIP_PARAMS1->memory_size_bytes_log2) |
| [`MICROPY_HW_ROMFS_PART0_START`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_PART0_START&type=code) | Address of the start of ROMFS partition 0 in SPI flash. | (uintptr_t)(&_micropy_hw_romfs_part0_start) |
| [`MICROPY_HW_ROMFS_PART1_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_PART1_SIZE&type=code) | Holds the size of the second part of the ROM filesystem. | (uintptr_t)(&_micropy_hw_romfs_part1_size) |
| [`MICROPY_HW_ROMFS_PART1_START`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_PART1_START&type=code) | Address of the start of the second ROM filesystem partition. | (uintptr_t)(&_micropy_hw_romfs_part1_start) |
| [`MICROPY_HW_ROMFS_QSPI_SPIFLASH_OBJ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_QSPI_SPIFLASH_OBJ&type=code) | Reference to the SPI flash object used for ROM filesystem operations. | (&spi_bdev2.spiflash) |
| [`MICROPY_HW_ROMFS_XSPI_SPIBDEV_OBJ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_ROMFS_XSPI_SPIBDEV_OBJ&type=code) | Reference to the SPI block device used for external ROM filesystem operations. | (&spi_bdev) |
#### MICROPY_HW_RTC

This configuration set manages various aspects of the Real-Time Clock (RTC) functionality, including timeout settings for different clock sources, memory allocation for user data, and options for utilizing external oscillators. It allows for fine-tuning of the RTC's operational parameters, ensuring reliable timekeeping and flexibility in clock source selection.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_RTC_BYP_TIMEOUT_MS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RTC_BYP_TIMEOUT_MS&type=code) | Defines the timeout duration for the RTC bypass mode in milliseconds. | 150 |
| [`MICROPY_HW_RTC_LSE_TIMEOUT_MS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RTC_LSE_TIMEOUT_MS&type=code) | Defines the timeout duration for LSE startup in milliseconds, set to 1000 ms. | 1000  // ST docs spec 2000 ms LSE startup, seems to be too pessimistic |
| [`MICROPY_HW_RTC_LSI_TIMEOUT_MS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RTC_LSI_TIMEOUT_MS&type=code) | Timeout duration for LSI clock readiness check, set to 500 ms. | 500   // this is way too pessimistic, typ. < 1ms |
| [`MICROPY_HW_RTC_SOURCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RTC_SOURCE&type=code) | Selects the RTC clock source: 0 for subclock, 1 for LOCO (32.768kHz). Examples: 0 for EK_RA4M1, 1 for EK_RA4W1. | (1)     // 0: subclock, 1: LOCO (32.768khz) |
| [`MICROPY_HW_RTC_USER_MEM_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RTC_USER_MEM_MAX&type=code) | Maximum size of user memory for RTC, defaulting to 2048 bytes to prevent overflow issues. | 2048 |
| [`MICROPY_HW_RTC_USE_BYPASS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RTC_USE_BYPASS&type=code) | Controls the use of bypass mode for the RTC's LSE oscillator. | (0) |
| [`MICROPY_HW_RTC_USE_CALOUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RTC_USE_CALOUT&type=code) | Controls the activation of the PC13 512Hz output. | (0)  // turn on/off PC13 512Hz output |
| [`MICROPY_HW_RTC_USE_LSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RTC_USE_LSE&type=code) | Enables the use of an external 32.768 kHz crystal for the RTC. | (1) |
| [`MICROPY_HW_RTC_USE_US`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_RTC_USE_US&type=code) | Enables the use of microsecond resolution for the RTC if set to 1. | (0) |
#### MICROPY_HW_SDCARD

This configuration set manages the hardware interface for SD and MMC cards, including pin assignments for data, command, and clock lines, as well as detection mechanisms for card presence. It also allows for customization of bus width and automatic mounting options at boot, ensuring proper integration and functionality of SD card support in embedded systems.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_SDCARD_BUS_WIDTH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDCARD_BUS_WIDTH&type=code) | Determines the bus width for the SD/MMC card interface, defaulting to 4 bits. | (4) |
| [`MICROPY_HW_SDCARD_CK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDCARD_CK&type=code) | Defines the clock pin for the SD card interface. | (pyb_pin_SD_SDIO_CK) |
| [`MICROPY_HW_SDCARD_CMD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDCARD_CMD&type=code) | Defines the command pin for the SD card interface. | (pyb_pin_SD_SDIO_CMD) |
| [`MICROPY_HW_SDCARD_D0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDCARD_D0&type=code) | Defines the data line 0 pin for the SD card using custom SDIO pins. | (pin_B7) |
| [`MICROPY_HW_SDCARD_D1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDCARD_D1&type=code) | Defines the data line 1 pin for the SD card interface. | (pyb_pin_SD_SDIO_D1) |
| [`MICROPY_HW_SDCARD_D2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDCARD_D2&type=code) | Defines the pin used for SD card data line D2. | (pyb_pin_SD_SDIO_D2) |
| [`MICROPY_HW_SDCARD_D3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDCARD_D3&type=code) | Defines the pin used for SD card data line 3. | (pyb_pin_SD_SDIO_D3) |
| [`MICROPY_HW_SDCARD_DETECT_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDCARD_DETECT_PIN&type=code) | Pin used for detecting the presence of an SD card. | (pin_G2) |
| [`MICROPY_HW_SDCARD_DETECT_PRESENT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDCARD_DETECT_PRESENT&type=code) | Indicates the presence of an SD card by defining its GPIO state, typically GPIO_PIN_RESET. | (GPIO_PIN_RESET) |
| [`MICROPY_HW_SDCARD_DETECT_PULL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDCARD_DETECT_PULL&type=code) | Configures the pull-up or pull-down resistor for the SD card detect pin. | (GPIO_PULLDOWN) |
| [`MICROPY_HW_SDCARD_MOUNT_AT_BOOT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDCARD_MOUNT_AT_BOOT&type=code) | Controls automatic mounting of the SD card at boot if enabled. | (MICROPY_HW_ENABLE_SDCARD) |
| [`MICROPY_HW_SDCARD_SDMMC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDCARD_SDMMC&type=code) | Selects the SDMMC peripheral for SD card driver, with values indicating which peripheral to use. | (1) |
#### MICROPY_HW_SDIO

This configuration set defines the pin assignments and alternate functions for the SDIO interface, including clock, command, and data lines. It allows for the customization of hardware connections necessary for SDIO communication, ensuring proper integration with the SDMMC peripheral.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_SDIO_CK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_CK&type=code) | Defines the clock pin for the SDIO interface. | (pyb_pin_WL_SDIO_CLK) |
| [`MICROPY_HW_SDIO_CLK_ALT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_CLK_ALT&type=code) | Defines the alternate function for the SDIO clock pin. | (0) |
| [`MICROPY_HW_SDIO_CMD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_CMD&type=code) | Defines the command pin for the SDIO interface. | (pyb_pin_WL_SDIO_CMD) |
| [`MICROPY_HW_SDIO_CMD_ALT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_CMD_ALT&type=code) | Defines the alternate function for the SDIO command pin. | (0) |
| [`MICROPY_HW_SDIO_D0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_D0&type=code) | Pin configuration for SDIO data line 0. | (pyb_pin_WL_SDIO_D0) |
| [`MICROPY_HW_SDIO_D0_ALT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_D0_ALT&type=code) | Defines the alternate function for the SDIO data line 0 pin. | (0) |
| [`MICROPY_HW_SDIO_D1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_D1&type=code) | Defines the pin used for SDIO data line 1. | (pyb_pin_WL_SDIO_D1) |
| [`MICROPY_HW_SDIO_D1_ALT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_D1_ALT&type=code) | Configures the alternate function for the SDIO data line 1. | (0) |
| [`MICROPY_HW_SDIO_D2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_D2&type=code) | Pin configuration for SDIO data line 2. | (pyb_pin_WL_SDIO_D2) |
| [`MICROPY_HW_SDIO_D2_ALT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_D2_ALT&type=code) | Configures the alternate function for the SDIO data line 2. | (0) |
| [`MICROPY_HW_SDIO_D3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_D3&type=code) | Defines the pin used for SDIO data line 3. | (pyb_pin_WL_SDIO_D3) |
| [`MICROPY_HW_SDIO_D3_ALT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_D3_ALT&type=code) | Configures the alternate function for SDIO data line 3. | (0) |
| [`MICROPY_HW_SDIO_SDMMC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDIO_SDMMC&type=code) | Selects the SDMMC peripheral for the SDIO driver, either 1 or 2. | (1) |
#### MICROPY_HW_SDMMC

This configuration set controls the hardware settings for SDMMC interfaces, including clock and data line pin assignments. It allows for the customization of multiple SDMMC interfaces, enabling efficient communication with SD cards or SDIO peripherals.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_SDMMC1_CK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDMMC1_CK&type=code) | Indicates the use of the SDMMC1 clock for SD card or SDIO peripherals. | (1) |
| [`MICROPY_HW_SDMMC2_CK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDMMC2_CK&type=code) | Enables the clock for the second SDMMC interface. | (1) |
| [`MICROPY_HW_SDMMC_CK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDMMC_CK&type=code) | Defines the clock pin for the SDMMC interface. | (pin_C12) |
| [`MICROPY_HW_SDMMC_CMD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDMMC_CMD&type=code) | Defines the command pin for the SDMMC interface. | (pin_D2) |
| [`MICROPY_HW_SDMMC_D0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDMMC_D0&type=code) | Defines the data line 0 pin for the SDMMC interface. | (pin_C8) |
| [`MICROPY_HW_SDMMC_D1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDMMC_D1&type=code) | Defines the data line 1 pin for SDMMC interface. | (pin_C9) |
| [`MICROPY_HW_SDMMC_D2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDMMC_D2&type=code) | Defines the pin used for SDMMC data line D2. | (pin_C10) |
| [`MICROPY_HW_SDMMC_D3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDMMC_D3&type=code) | Defines the data line 3 pin for SDMMC interface as pin_C11. | (pin_C11) |
#### MICROPY_HW_SDRAM

This configuration set manages various parameters and timing settings for SDRAM, including refresh cycles, burst lengths, and latency. It ensures optimal performance and reliability of SDRAM operations by defining critical aspects such as memory size, clock frequency, and timing delays.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_SDRAM_AUTOREFRESH_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_AUTOREFRESH_NUM&type=code) | Sets the number of auto-refresh cycles for SDRAM. | (8) |
| [`MICROPY_HW_SDRAM_BURST_LENGTH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_BURST_LENGTH&type=code) | Defines the burst length for SDRAM operations, affecting data transfer efficiency. | (kSEMC_Sdram_BurstLen8) |
| [`MICROPY_HW_SDRAM_CAS_LATENCY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_CAS_LATENCY&type=code) | Defines the CAS latency for SDRAM configuration. | (kSEMC_LatencyThree) |
| [`MICROPY_HW_SDRAM_CLOCK_PERIOD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_CLOCK_PERIOD&type=code) | Timing configuration for SDRAM clock period, set to 2 for 100MHz operation. | 2 |
| [`MICROPY_HW_SDRAM_COLUMN_BITS_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_COLUMN_BITS_NUM&type=code) | Defines the number of column address bits for SDRAM configuration. | (kSEMC_SdramColunm_9bit) |
| [`MICROPY_HW_SDRAM_DELAY_CHAIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_DELAY_CHAIN&type=code) | Configures the delay chain for SDRAM timing. | (2) |
| [`MICROPY_HW_SDRAM_FREQUENCY_KHZ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_FREQUENCY_KHZ&type=code) | Defines the SDRAM frequency in kilohertz, set to 100 MHz. | (100000) // 100 MHz |
| [`MICROPY_HW_SDRAM_INTERN_BANKS_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_INTERN_BANKS_NUM&type=code) | Defines the number of internal banks in the SDRAM, set to 4. | 4 |
| [`MICROPY_HW_SDRAM_MEM_BUS_WIDTH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_MEM_BUS_WIDTH&type=code) | Defines the memory bus width for SDRAM, affecting data transfer size and performance. | (kSEMC_PortSize32Bit) |
| [`MICROPY_HW_SDRAM_RBURST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_RBURST&type=code) | Enables or disables read burst mode for SDRAM. | (1) |
| [`MICROPY_HW_SDRAM_RBURST_LENGTH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_RBURST_LENGTH&type=code) | Defines the refresh burst length for SDRAM. | (1) |
| [`MICROPY_HW_SDRAM_REFRESH_CYCLES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_REFRESH_CYCLES&type=code) | Determines the number of refresh cycles for SDRAM operation. | 4096 |
| [`MICROPY_HW_SDRAM_REFRESH_RATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_REFRESH_RATE&type=code) | Determines the SDRAM refresh rate in milliseconds. | (64) // ms |
| [`MICROPY_HW_SDRAM_ROW_BITS_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_ROW_BITS_NUM&type=code) | Defines the number of bits used for the row address in SDRAM. | 12 |
| [`MICROPY_HW_SDRAM_RPIPE_DELAY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_RPIPE_DELAY&type=code) | Configures the read pipe delay for SDRAM initialization. | 0 |
| [`MICROPY_HW_SDRAM_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_SIZE&type=code) | Defines the size of the SDRAM in bytes, calculated from 64 Mbit. | (64 / 8 * 1024 * 1024)  // 64 Mbit |
| [`MICROPY_HW_SDRAM_STARTUP_TEST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_STARTUP_TEST&type=code) | Enables a test for SDRAM validity during startup. | (1) |
| [`MICROPY_HW_SDRAM_TEST_FAIL_ON_ERROR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_TEST_FAIL_ON_ERROR&type=code) | Enables error handling during SDRAM tests, triggering fatal errors on test failures. | (true) |
| [`MICROPY_HW_SDRAM_TIMING_TMRD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_TIMING_TMRD&type=code) | Defines the number of clock cycles for the Load-to-Active delay in SDRAM timing. | (2) |
| [`MICROPY_HW_SDRAM_TIMING_TRAS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_TIMING_TRAS&type=code) | Defines the minimum time for a row to be active before it can be precharged, measured in nanoseconds. | (42) |
| [`MICROPY_HW_SDRAM_TIMING_TRC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_TIMING_TRC&type=code) | Defines the Row Cycle Time for SDRAM in nanoseconds. | (60) |
| [`MICROPY_HW_SDRAM_TIMING_TRCD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_TIMING_TRCD&type=code) | Defines the time delay between a row activation and a read/write command in nanoseconds. | (15) |
| [`MICROPY_HW_SDRAM_TIMING_TREF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_TIMING_TREF&type=code) | Calculates the refresh timing for SDRAM based on a 64ms interval divided by 8192. | (64 * 1000000 / 8192) // 64ms/8192 |
| [`MICROPY_HW_SDRAM_TIMING_TRP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_TIMING_TRP&type=code) | Defines the time delay for precharging a row in SDRAM, measured in nanoseconds. | (15) |
| [`MICROPY_HW_SDRAM_TIMING_TRRD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_TIMING_TRRD&type=code) | Defines the time required for a row to be activated after another row has been activated, measured in nanoseconds. | (60) |
| [`MICROPY_HW_SDRAM_TIMING_TWR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_TIMING_TWR&type=code) | Defines the write recovery time for SDRAM in nanoseconds. | (12) |
| [`MICROPY_HW_SDRAM_TIMING_TXSR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_TIMING_TXSR&type=code) | Defines the exit self-refresh delay timing for SDRAM, measured in nanoseconds. | (70) |
| [`MICROPY_HW_SDRAM_WRITE_PROTECTION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SDRAM_WRITE_PROTECTION&type=code) | Controls write protection for SDRAM, with 0 indicating disabled. | (0) |
#### MICROPY_HW_SOFT

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_SOFT_TIMER_ALARM_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SOFT_TIMER_ALARM_NUM&type=code) | Index for the hardware timer alarm, with a range of 0-3, where 3 is reserved for the pico-sdk. | (2) |
#### MICROPY_HW_SOFTSPI

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_SOFTSPI_MAX_BAUDRATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SOFTSPI_MAX_BAUDRATE&type=code) | Calculates the maximum baud rate for software SPI based on CPU ticks per microsecond. | (esp_rom_get_cpu_ticks_per_us() * 1000000 / 200) // roughly |
| [`MICROPY_HW_SOFTSPI_MIN_DELAY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SOFTSPI_MIN_DELAY&type=code) | Sets the minimum delay for software SPI operations, influencing the maximum baud rate. | (0) |
#### MICROPY_HW_SPI

This configuration set defines the hardware parameters for multiple SPI (Serial Peripheral Interface) buses, including the assignment of pins for MISO, MOSI, SCK, and chip select (NSS) for each SPI interface. It allows for customization of the SPI communication setup, enabling developers to specify the exact hardware connections for their applications.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_SPI0_MISO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI0_MISO&type=code) | Defines the MISO pin for SPI0 communication. | (pin_P1_0) |
| [`MICROPY_HW_SPI0_MOSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI0_MOSI&type=code) | Defines the pin used for the MOSI (Master Out Slave In) line of SPI0. | (PICO_DEFAULT_SPI_TX_PIN) |
| [`MICROPY_HW_SPI0_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI0_NAME&type=code) | Defines the name for the SPI0 interface. | "SPI0" |
| [`MICROPY_HW_SPI0_RSPCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI0_RSPCK&type=code) | Defines the pin used for the SPI0 clock signal. | (pin_P102) // PMOD A |
| [`MICROPY_HW_SPI0_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI0_SCK&type=code) | Defines the SCK pin for SPI0, requiring pin arguments when no default SPI is set. | (0) |
| [`MICROPY_HW_SPI0_SSL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI0_SSL&type=code) | Defines the SSL pin for SPI0, assigned to pin P103. | (pin_P103) // PMOD A |
| [`MICROPY_HW_SPI1_MISO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI1_MISO&type=code) | Defines the MISO pin for SPI1, typically used for data input. | (pin_G9) // Arduino Connector CN7-Pin12 (D12) |
| [`MICROPY_HW_SPI1_MOSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI1_MOSI&type=code) | Defines the MOSI pin for SPI1, set to pin_B5. | (pin_B5) // Arduino Connector CN7-Pin14 (D11) |
| [`MICROPY_HW_SPI1_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI1_NAME&type=code) | Defines the name of the first SPI bus, used for identification in the code. | "SLOT12H" |
| [`MICROPY_HW_SPI1_NSS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI1_NSS&type=code) | Defines the chip select (NSS) pin for SPI1, typically used for selecting the slave device. | (pin_D14) // Arduino Connector CN7-Pin16 (D10) |
| [`MICROPY_HW_SPI1_RSPCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI1_RSPCK&type=code) | Defines the pin used for the SPI1 clock signal. | (pin_P102) |
| [`MICROPY_HW_SPI1_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI1_SCK&type=code) | Defines the default clock pin for SPI1, using IO_MUX pins unless overridden. | SPI2_IOMUX_PIN_NUM_CLK |
| [`MICROPY_HW_SPI1_SSL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI1_SSL&type=code) | Defines the SSL pin for SPI1 communication, set to pin_P104. | (pin_P104) |
| [`MICROPY_HW_SPI2_MISO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI2_MISO&type=code) | Defines the MISO pin for SPI2 communication, typically used for data input. | (pin_I2) // Arduino Connector CN13-Pin5 (D12) |
| [`MICROPY_HW_SPI2_MOSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI2_MOSI&type=code) | Defines the MOSI pin for SPI2, typically set to pin_B15. | (pin_B15) // Arduino Connector CN13-Pin4 (D11) |
| [`MICROPY_HW_SPI2_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI2_NAME&type=code) | Identifies the name of the second SPI bus, typically associated with a specific hardware slot. | "SLOT2" |
| [`MICROPY_HW_SPI2_NSS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI2_NSS&type=code) | Defines the chip select pin for SPI2. | (pin_A3) // Arduino Connector CN13-Pin3 (D10) |
| [`MICROPY_HW_SPI2_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI2_SCK&type=code) | Defines the SCK pin for SPI2, set to GPIO 36 for ESP32S2 and S3. | (36) |
| [`MICROPY_HW_SPI3_MISO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI3_MISO&type=code) | Defines the MISO pin for SPI3, set to pin_B4. | (pin_B4)    // Arduino D5,  pin 27 on CN10 |
| [`MICROPY_HW_SPI3_MOSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI3_MOSI&type=code) | Defines the MOSI pin for SPI3 communication, set to pin_B5. | (pin_B5)    // Arduino D4,  pin 29 on CN10 |
| [`MICROPY_HW_SPI3_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI3_NAME&type=code) | Identifies the name of SPI3 interface for mikroBUS slot 3, 4, and FLASH. | "SLOT34F" |
| [`MICROPY_HW_SPI3_NSS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI3_NSS&type=code) | Defines the chip select (NSS) pin for SPI3, which is pin_A15. | (pin_A15) |
| [`MICROPY_HW_SPI3_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI3_SCK&type=code) | Defines the SCK pin for SPI3, set to pin_B3. | (pin_B3)    // Arduino D3,  pin 31 on CN10 |
| [`MICROPY_HW_SPI4_MISO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI4_MISO&type=code) | Defines the MISO pin for SPI4 as pin_A1. | (pin_A1)    //              pin 30 on CN7 |
| [`MICROPY_HW_SPI4_MOSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI4_MOSI&type=code) | Defines the MOSI pin for SPI4 as pin_A11. | (pin_A11)   //              pin 14 on CN10 |
| [`MICROPY_HW_SPI4_NSS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI4_NSS&type=code) | Defines the chip select pin for SPI4. | (pin_E11) |
| [`MICROPY_HW_SPI4_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI4_SCK&type=code) | Defines the SCK pin for SPI4, set to pin_B13. | (pin_B13)   //              pin 30 on CN10 |
| [`MICROPY_HW_SPI5_MISO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI5_MISO&type=code) | Defines the MISO pin for SPI5, typically used for data input. | (pin_A12)   //              pin 12 on CN10 |
| [`MICROPY_HW_SPI5_MOSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI5_MOSI&type=code) | Defines the MOSI pin for SPI5, set to pin_B0. | (pin_B0)    //              pin 34 on CN7 |
| [`MICROPY_HW_SPI5_NSS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI5_NSS&type=code) | Defines the chip select pin for SPI5, set to pin_F6. | (pin_F6) |
| [`MICROPY_HW_SPI5_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI5_SCK&type=code) | Defines the SCK pin for SPI5, set to pin_A10. | (pin_A10)   //              pin 33 on CN10 |
| [`MICROPY_HW_SPI_INDEX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI_INDEX&type=code) | Defines the SPI index values for hardware SPI configurations. | { 1, 6, 5 } |
| [`MICROPY_HW_SPI_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI_MAX&type=code) | Determines the maximum number of hardware SPI peripherals available. | (2) |
| [`MICROPY_HW_SPI_NO_DEFAULT_PINS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI_NO_DEFAULT_PINS&type=code) | Indicates that no default SPI pins are defined, requiring explicit pin assignments. | (1) |
| [`MICROPY_HW_SPI_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI_NUM&type=code) | Determines the number of SPI interfaces based on the size of the spi_index_table array. | MP_ARRAY_SIZE(spi_index_table) |
| [`MICROPY_HW_SPI_PIN_UNUSED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPI_PIN_UNUSED&type=code) | Represents an unused SPI pin, set to UINT8_MAX to indicate no valid pin assigned. | UINT8_MAX |
#### MICROPY_HW_SPIFLASH

This configuration set manages the integration and operation of external SPI flash memory within a hardware environment. It allows for customization of communication parameters, pin assignments, and device detection, ensuring efficient interaction with the flash storage for file system operations.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_SPIFLASH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH&type=code) | Enables the use of external SPI flash for the file system. | (1) |
| [`MICROPY_HW_SPIFLASH_BAUDRATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_BAUDRATE&type=code) | Sets the baud rate for SPI communication with the flash memory. | (24000000) |
| [`MICROPY_HW_SPIFLASH_CHIP_PARAMS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_CHIP_PARAMS&type=code) | Enables dynamic detection and configuration of SPI flash chip parameters. | (1) |
| [`MICROPY_HW_SPIFLASH_CS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_CS&type=code) | Defines the chip select pin for SPI flash memory. | (pyb_pin_FLASH_CS) |
| [`MICROPY_HW_SPIFLASH_DETECT_DEVICE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_DETECT_DEVICE&type=code) | Enables detection of the SPI flash device during initialization. | (1) |
| [`MICROPY_HW_SPIFLASH_ENABLE_CACHE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_ENABLE_CACHE&type=code) | Enables caching for external SPI flash to support block writes smaller than the page-erase size. | (1) |
| [`MICROPY_HW_SPIFLASH_ID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_ID&type=code) | Identifies the SPI flash memory device used in the hardware configuration. | (2) |
| [`MICROPY_HW_SPIFLASH_IO0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_IO0&type=code) | Defines the pin used for the first I/O line of the external SPI flash. | (pyb_pin_QSPI1_D0) |
| [`MICROPY_HW_SPIFLASH_IO1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_IO1&type=code) | Defines the pin used for the second data line (D1) in the QSPI interface. | (pyb_pin_QSPI1_D1) |
| [`MICROPY_HW_SPIFLASH_IO2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_IO2&type=code) | Defines the pin used for the second data line (D2) in QSPI flash communication. | (pyb_pin_QSPI1_D2) |
| [`MICROPY_HW_SPIFLASH_IO3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_IO3&type=code) | Defines the pin used for the third data line in QSPI flash communication. | (pyb_pin_QSPI1_D3) |
| [`MICROPY_HW_SPIFLASH_MISO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_MISO&type=code) | Defines the MISO pin for SPI flash communication, varying by board version. | (pyb_pin_FLASH_MISO_V13) |
| [`MICROPY_HW_SPIFLASH_MOSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_MOSI&type=code) | Defines the MOSI pin for the SPI flash interface. | (MICROPY_HW_SPI1_MOSI) |
| [`MICROPY_HW_SPIFLASH_OFFSET_BYTES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_OFFSET_BYTES&type=code) | Offset in bytes for SPI flash storage, skipping the first 1MiB used by the bootloader. | (1024 * 1024) |
| [`MICROPY_HW_SPIFLASH_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_SCK&type=code) | Defines the clock pin for the SPI flash interface. | (MICROPY_HW_SPI1_SCK) |
| [`MICROPY_HW_SPIFLASH_SIZE_BITS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_SIZE_BITS&type=code) | Defines the size of the SPI flash memory in bits, allowing for configuration of external storage. | (120 * 1024 * 1024) |
| [`MICROPY_HW_SPIFLASH_SOFT_RESET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SPIFLASH_SOFT_RESET&type=code) | Enables software reset functionality for SPI flash. | (1) |
#### MICROPY_HW_STDIN

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_STDIN_BUFFER_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_STDIN_BUFFER_LEN&type=code) | Defines the length of the standard input buffer, defaulting to 512 bytes. | 512 |
#### MICROPY_HW_STM

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_STM_USB_STACK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_STM_USB_STACK&type=code) | Enables the STM USB stack when USB is enabled and TinyUSB stack is not used. | (MICROPY_HW_ENABLE_USB && !MICROPY_HW_TINYUSB_STACK) |
#### MICROPY_HW_STM32WB

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_STM32WB_FLASH_SYNCRONISATION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_STM32WB_FLASH_SYNCRONISATION&type=code) | Enables synchronization mechanisms for flash operations on STM32WB. | (1) |
#### MICROPY_HW_SUBGHZSPI

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_SUBGHZSPI_ID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SUBGHZSPI_ID&type=code) | Identifies the SUBGHZSPI interface for configuration and usage. | 3 |
| [`MICROPY_HW_SUBGHZSPI_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SUBGHZSPI_NAME&type=code) | Identifies the SPI bus used for the SUBGHZ internal radio. | "SUBGHZ" |
#### MICROPY_HW_SYSTEM

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_SYSTEM_TICK_USE_SYSTICK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SYSTEM_TICK_USE_SYSTICK&type=code) | Enables the use of the SysTick timer for system tick management. | (1) |
| [`MICROPY_HW_SYSTEM_TICK_USE_UTIMER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_SYSTEM_TICK_USE_UTIMER&type=code) | Enables the use of the UTIMER for system tick implementation. | (1) |
#### MICROPY_HW_TINYUSB

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_TINYUSB_STACK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_TINYUSB_STACK&type=code) | Enables the use of the TinyUSB stack for USB functionality. | (0) |
#### MICROPY_HW_UART

This configuration group manages the settings for multiple UART interfaces, allowing for the definition of specific GPIO pins for transmit (TX), receive (RX), and flow control signals (CTS/RTS). It enables customization of hardware flow control and naming for each UART, facilitating flexible serial communication setups across various hardware platforms.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_UART0_CTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART0_CTS&type=code) | Defines the pin used for the Clear To Send (CTS) signal of UART0. | (pin_P0_2) |
| [`MICROPY_HW_UART0_RTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART0_RTS&type=code) | Defines the pin used for the RTS (Request to Send) signal of UART0. | (pin_P0_3) |
| [`MICROPY_HW_UART0_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART0_RX&type=code) | Defines the receive pin for UART0, typically assigned to a specific GPIO pin. | (pin_P410) // MBRX0 |
| [`MICROPY_HW_UART0_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART0_TX&type=code) | Defines the transmit pin for UART0, allowing customization of UART pin assignments. | (16) |
| [`MICROPY_HW_UART10_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART10_RX&type=code) | Defines the receive pin for UART10 as pyb_pin_PORTE_RX. | (pyb_pin_PORTE_RX) |
| [`MICROPY_HW_UART10_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART10_TX&type=code) | Defines the transmit pin for UART10 on Port E. | (pyb_pin_PORTE_TX) |
| [`MICROPY_HW_UART1_CTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART1_CTS&type=code) | Defines the pin used for the Clear To Send (CTS) signal for UART1. | (pin_P403) // PMOD B |
| [`MICROPY_HW_UART1_HWFC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART1_HWFC&type=code) | Enables hardware flow control for UART1. | (1) |
| [`MICROPY_HW_UART1_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART1_NAME&type=code) | Defines the name for UART1, used for identifying the UART interface. | "SLOT4" |
| [`MICROPY_HW_UART1_PINS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART1_PINS&type=code) | Defines the GPIO pins used for UART1 communication. | (GPIO_PIN_6 \| GPIO_PIN_7) |
| [`MICROPY_HW_UART1_PORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART1_PORT&type=code) | Defines the GPIO port used for UART1 communication. | (GPIOB) |
| [`MICROPY_HW_UART1_RTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART1_RTS&type=code) | Defines the RTS (Request to Send) pin for UART1 communication. | (pyb_pin_BT_RTS) |
| [`MICROPY_HW_UART1_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART1_RX&type=code) | Defines the receive pin for UART1, typically used for serial communication. | (28) |
| [`MICROPY_HW_UART1_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART1_TX&type=code) | Defines the transmit pin for UART1, typically assigned to a specific GPIO pin. | (pin_P213) |
| [`MICROPY_HW_UART2_CTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART2_CTS&type=code) | Defines the pin used for Clear To Send (CTS) flow control in UART2. | (pin_D3) |
| [`MICROPY_HW_UART2_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART2_NAME&type=code) | Defines the name for UART2, used for UART communication. | "UART1" |
| [`MICROPY_HW_UART2_PINS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART2_PINS&type=code) | Defines the GPIO pins used for UART2 communication. | (GPIO_PIN_2 \| GPIO_PIN_3) |
| [`MICROPY_HW_UART2_PORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART2_PORT&type=code) | Defines the GPIO port for UART2 as GPIOA. | (GPIOA) |
| [`MICROPY_HW_UART2_RTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART2_RTS&type=code) | Defines the RTS (Request to Send) pin for UART2 communication. | (pin_A1)    // Arduino A1,  pin 30 on CN7 |
| [`MICROPY_HW_UART2_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART2_RX&type=code) | Defines the receive pin for UART2, typically set to pin_A3. | (pin_A3)    // Arduino D0,  pin 37 on CN10 |
| [`MICROPY_HW_UART2_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART2_TX&type=code) | Defines the transmit pin for UART2, typically assigned to a specific GPIO pin. | (pin_P302) |
| [`MICROPY_HW_UART3_CTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART3_CTS&type=code) | Defines the pin used for the Clear To Send (CTS) signal for UART3. | (pin_B13)   //              pin 30 on CN10 |
| [`MICROPY_HW_UART3_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART3_NAME&type=code) | Defines the name for UART3 configuration, typically associated with specific pins. | "SLOT1" |
| [`MICROPY_HW_UART3_PINS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART3_PINS&type=code) | Defines the GPIO pins used for UART3 communication. | (GPIO_PIN_10 \| GPIO_PIN_11) |
| [`MICROPY_HW_UART3_PORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART3_PORT&type=code) | Defines the GPIO port for UART3 as GPIOB. | (GPIOB) |
| [`MICROPY_HW_UART3_RTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART3_RTS&type=code) | Defines the RTS (Request to Send) pin for UART3, set to pin_B14. | (pin_B14)   //              pin 28 on CN10 |
| [`MICROPY_HW_UART3_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART3_RX&type=code) | Defines the RX pin for UART3, typically set to pin_B11. | (pin_B11) // Arduino Connector CN15-Pin1 (D0) |
| [`MICROPY_HW_UART3_RX_PULL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART3_RX_PULL&type=code) | Configures the pull-up/pull-down resistor setting for UART3 RX pin. | (GPIO_NOPULL) |
| [`MICROPY_HW_UART3_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART3_TX&type=code) | Defines the transmit pin for UART3, typically set to pin_B10. | (pin_B10) // B9, B10, C10, D8 |
| [`MICROPY_HW_UART4_CTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART4_CTS&type=code) | Defines the pin used for the Clear To Send (CTS) signal in UART4 communication. | (pyb_pin_BT_CTS) |
| [`MICROPY_HW_UART4_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART4_NAME&type=code) | Defines the name for UART4, used for identifying the UART interface. | "HDR2" |
| [`MICROPY_HW_UART4_PINS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART4_PINS&type=code) | Defines the GPIO pins used for UART4 communication. | (GPIO_PIN_0 \| GPIO_PIN_1) |
| [`MICROPY_HW_UART4_PORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART4_PORT&type=code) | Defines the GPIO port for UART4 as GPIOA. | (GPIOA) |
| [`MICROPY_HW_UART4_RTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART4_RTS&type=code) | Defines the RTS pin for UART4 communication. | (pyb_pin_BT_RTS) |
| [`MICROPY_HW_UART4_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART4_RX&type=code) | Defines the receive pin for UART4, typically set to a specific GPIO pin. | (pin_A1)    // Arduino A1,  pin 30 on CN7 |
| [`MICROPY_HW_UART4_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART4_TX&type=code) | Defines the transmit pin for UART4, typically set to a specific GPIO pin. | (pin_A0) |
| [`MICROPY_HW_UART5_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART5_RX&type=code) | Defines the receive pin for UART5, set to pyb_pin_PORTD_RX. | (pyb_pin_PORTD_RX) |
| [`MICROPY_HW_UART5_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART5_TX&type=code) | Defines the transmit pin for UART5, set to pin_B0. | (pin_B0) |
| [`MICROPY_HW_UART6_CTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART6_CTS&type=code) | Defines the pin used for the Clear To Send (CTS) signal for UART6. | (pin_G13) // PG13,PG15 |
| [`MICROPY_HW_UART6_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART6_NAME&type=code) | Defines the name for UART6, used for identifying the UART interface. | "YA" |
| [`MICROPY_HW_UART6_PINS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART6_PINS&type=code) | Defines the GPIO pins used for UART6 communication. | (GPIO_PIN_6 \| GPIO_PIN_7) |
| [`MICROPY_HW_UART6_PORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART6_PORT&type=code) | Defines the GPIO port for UART6 as GPIOC. | (GPIOC) |
| [`MICROPY_HW_UART6_RTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART6_RTS&type=code) | Defines the RTS pin for UART6, set to pin_G8. | (pin_G8)  // PG8,PG12 |
| [`MICROPY_HW_UART6_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART6_RX&type=code) | Defines the receive pin for UART6, set to pin_C7. | (pin_C7)    // Arduino D9,  pin 19 on CN10 |
| [`MICROPY_HW_UART6_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART6_TX&type=code) | Defines the transmit pin for UART6, typically set to pin_C6. | (pin_C6) |
| [`MICROPY_HW_UART7_CTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART7_CTS&type=code) | Defines the pin used for UART7 Clear To Send (CTS) functionality. | (pin_P403) // PMOD B |
| [`MICROPY_HW_UART7_RTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART7_RTS&type=code) | Defines the RTS pin for UART7 communication. | (pyb_pin_BT_RTS) |
| [`MICROPY_HW_UART7_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART7_RX&type=code) | Defines the receive pin for UART7, set to pin_P402. | (pin_P402) // PMOD B |
| [`MICROPY_HW_UART7_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART7_TX&type=code) | Defines the transmit pin for UART7, set to pin_P401. | (pin_P401) // PMOD B |
| [`MICROPY_HW_UART8_CTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART8_CTS&type=code) | Defines the pin used for UART8 Clear To Send (CTS) functionality. | (pin_P107) // PMOD B |
| [`MICROPY_HW_UART8_RTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART8_RTS&type=code) | Defines the RTS pin for UART8 communication, set to pin_P606. | (pin_P606) |
| [`MICROPY_HW_UART8_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART8_RX&type=code) | Defines the receive pin for UART8, set to pin_P104. | (pin_P104) // PMOD B |
| [`MICROPY_HW_UART8_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART8_TX&type=code) | Defines the transmit pin for UART8, set to pin_P105. | (pin_P105) // PMOD B |
| [`MICROPY_HW_UART9_CTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART9_CTS&type=code) | Defines the pin used for the Clear To Send (CTS) signal of UART9. | (pin_P604) |
| [`MICROPY_HW_UART9_RTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART9_RTS&type=code) | Defines the RTS pin for UART9 as pin_P603. | (pin_P603) |
| [`MICROPY_HW_UART9_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART9_RX&type=code) | Defines the receive pin for UART9, typically used for serial communication. | (pyb_pin_PORTF_RX) |
| [`MICROPY_HW_UART9_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART9_TX&type=code) | Defines the transmit pin for UART9, set to pin_P602. | (pin_P602) |
| [`MICROPY_HW_UART_INDEX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART_INDEX&type=code) | Defines the mapping of logical UART indices to hardware UART numbers. | { 0, 6, 4, 2, 3, 8, 1, 7, 5 } |
| [`MICROPY_HW_UART_NO_DEFAULT_PINS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART_NO_DEFAULT_PINS&type=code) | Indicates that UART pins must be explicitly defined instead of using default pins. | (1) |
| [`MICROPY_HW_UART_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART_NUM&type=code) | Calculates the number of UARTs based on the size of the uart_index_table array. | (sizeof(uart_index_table) / sizeof(uart_index_table)[0]) |
| [`MICROPY_HW_UART_REPL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART_REPL&type=code) | Identifies the UART interface used for the REPL (Read-Eval-Print Loop). Examples: HW_UART_0, HW_UART_1. | HW_UART_0 |
| [`MICROPY_HW_UART_REPL_BAUD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART_REPL_BAUD&type=code) | Defines the baud rate for the REPL UART interface, defaulting to 115200. | (115200) |
| [`MICROPY_HW_UART_REPL_RXBUF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART_REPL_RXBUF&type=code) | Defines the size of the receive buffer for the UART REPL, set to 260 bytes. | (260) |
| [`MICROPY_HW_UART_RTSCTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART_RTSCTS&type=code) | Enables RTS/CTS hardware flow control for UART. | (SAMD21_EXTRA_FEATURES) |
| [`MICROPY_HW_UART_TXBUF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_UART_TXBUF&type=code) | Enables the use of a transmit buffer for UART communication. | (1) |
#### MICROPY_HW_USB

This configuration group manages various aspects of USB functionality, including support for USB CDC, HID, and Mass Storage Class, as well as defining interface strings and buffer sizes. It allows for customization of USB communication parameters, such as speed modes and timeout settings, ensuring compatibility with different hardware setups and use cases.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_USB_CDC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_CDC&type=code) | Enables USB CDC functionality if USB device support is enabled. | (MICROPY_HW_ENABLE_USBDEV) |
| [`MICROPY_HW_USB_CDC_1200BPS_TOUCH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_CDC_1200BPS_TOUCH&type=code) | Enables USB CDC support for 1200 bps touch communication. | (1) |
| [`MICROPY_HW_USB_CDC_DTR_RTS_BOOTLOADER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_CDC_DTR_RTS_BOOTLOADER&type=code) | Enables bootloader functionality via DTR/RTS signals for USB CDC. | (0) |
| [`MICROPY_HW_USB_CDC_INTERFACE_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_CDC_INTERFACE_STRING&type=code) | Defines the USB CDC interface string for the board. | "Board CDC" |
| [`MICROPY_HW_USB_CDC_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_CDC_NUM&type=code) | Sets the maximum number of CDC VCP interfaces available. | (1) |
| [`MICROPY_HW_USB_CDC_RX_DATA_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_CDC_RX_DATA_SIZE&type=code) | Defines the size of the incoming buffer for each CDC instance, must be a power of 2. | (1024) |
| [`MICROPY_HW_USB_CDC_TX_DATA_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_CDC_TX_DATA_SIZE&type=code) | Defines the size of the outgoing buffer for each CDC instance, set to 1024 bytes. | (1024) |
| [`MICROPY_HW_USB_CDC_TX_TIMEOUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_CDC_TX_TIMEOUT&type=code) | Defines the timeout duration for USB CDC transmission in milliseconds. | (500) |
| [`MICROPY_HW_USB_CDC_TX_TIMEOUT_MS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_CDC_TX_TIMEOUT_MS&type=code) | Sets the timeout duration for USB CDC transmission in milliseconds. | (500) |
| [`MICROPY_HW_USB_CONFIGURATION_FS_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_CONFIGURATION_FS_STRING&type=code) | Defines the USB configuration string for full-speed mode. | "Nicla Vision Config" |
| [`MICROPY_HW_USB_CONFIGURATION_HS_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_CONFIGURATION_HS_STRING&type=code) | Defines the USB configuration string for high-speed mode. | "Nicla Vision Config" |
| [`MICROPY_HW_USB_DESC_STR_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_DESC_STR_MAX&type=code) | Maximum length for USB descriptor strings, including the terminating byte. | (40) |
| [`MICROPY_HW_USB_FS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_FS&type=code) | Enables USB Full Speed support for hardware configurations. | (1) |
| [`MICROPY_HW_USB_HID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_HID&type=code) | Enables USB HID functionality when the STM USB stack is used. | (MICROPY_HW_STM_USB_STACK) |
| [`MICROPY_HW_USB_HS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_HS&type=code) | Enables USB OTG HS support with external PHY for STM32 boards. | (1) |
| [`MICROPY_HW_USB_HS_IN_FS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_HS_IN_FS&type=code) | Enables USB high-speed functionality in full-speed mode. | (1) |
| [`MICROPY_HW_USB_HS_ULPI3320`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_HS_ULPI3320&type=code) | Enables support for the ULPI3320 USB high-speed PHY. | (1) |
| [`MICROPY_HW_USB_HS_ULPI_DIR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_HS_ULPI_DIR&type=code) | Defines the pin used for the ULPI direction signal in USB high-speed configuration. | (pin_I11) |
| [`MICROPY_HW_USB_HS_ULPI_NXT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_HS_ULPI_NXT&type=code) | Defines the pin used for the ULPI NXT signal in USB high-speed configuration. | (pin_C3) |
| [`MICROPY_HW_USB_HS_ULPI_STP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_HS_ULPI_STP&type=code) | Defines the STP pin for USB HS ULPI interface. | (pin_C0) |
| [`MICROPY_HW_USB_INTERFACE_FS_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_INTERFACE_FS_STRING&type=code) | Defines the USB interface string for full-speed communication, e.g., 'Nicla Vision Interface'. | "Nicla Vision Interface" |
| [`MICROPY_HW_USB_INTERFACE_HS_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_INTERFACE_HS_STRING&type=code) | Defines the high-speed USB interface string for the device. | "Nicla Vision Interface" |
| [`MICROPY_HW_USB_IS_MULTI_OTG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_IS_MULTI_OTG&type=code) | Indicates whether the USB peripheral supports multiple OTG modes (0 for single mode, 1 for multi-OTG). Examples: STM32G0 and STM32H5 set to 0; others set to 1. | (0) |
| [`MICROPY_HW_USB_LANGID_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_LANGID_STRING&type=code) | Language ID for USB communication, set to 0x409 (English). Examples: 0x409 for English, 0x0409 for US English. | 0x409 |
| [`MICROPY_HW_USB_MAIN_DEV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_MAIN_DEV&type=code) | Determines the main USB device used for the REPL or DFU interface, based on USB PHY configuration. | (USB_PHY_FS_ID) |
| [`MICROPY_HW_USB_MANUFACTURER_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_MANUFACTURER_STRING&type=code) | Defines the USB manufacturer string for the device. | CONFIG_TINYUSB_DESC_MANUFACTURER_STRING |
| [`MICROPY_HW_USB_MSC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_MSC&type=code) | Enables USB Mass Storage functionality with FatFS filesystem support. | (1) |
| [`MICROPY_HW_USB_MSC_INQUIRY_PRODUCT_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_MSC_INQUIRY_PRODUCT_STRING&type=code) | Defines the product string for USB MSC inquiries, typically identifying the device. | "pyboard Flash   " |
| [`MICROPY_HW_USB_MSC_INQUIRY_REVISION_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_MSC_INQUIRY_REVISION_STRING&type=code) | Defines the revision string for USB Mass Storage Class inquiries, typically set to '1.00'. | "1.00" |
| [`MICROPY_HW_USB_MSC_INQUIRY_VENDOR_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_MSC_INQUIRY_VENDOR_STRING&type=code) | Defines the vendor string for USB Mass Storage Class inquiries, limited to 8 characters. | "MicroPy " |
| [`MICROPY_HW_USB_MSC_INTERFACE_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_MSC_INTERFACE_STRING&type=code) | Defines the USB MSC interface string for the board. | "Board MSC" |
| [`MICROPY_HW_USB_OTG_ID_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_OTG_ID_PIN&type=code) | Defines the pin used for USB OTG ID detection, typically set to pin_A10. | (pin_A10) |
| [`MICROPY_HW_USB_PID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PID&type=code) | USB Product ID for TinyUSB Stack, used to identify the device. | (0x9802) |
| [`MICROPY_HW_USB_PID_CDC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PID_CDC&type=code) | Defines the USB Product ID for CDC (Communication Device Class) functionality. | (MICROPY_HW_USB_PID) |
| [`MICROPY_HW_USB_PID_CDC2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PID_CDC2&type=code) | Defines the USB Product ID for the second CDC interface. | (MICROPY_HW_USB_PID) |
| [`MICROPY_HW_USB_PID_CDC2_MSC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PID_CDC2_MSC&type=code) | Defines the USB Product ID for CDC and MSC functionality with two CDC interfaces. | (MICROPY_HW_USB_PID) |
| [`MICROPY_HW_USB_PID_CDC2_MSC_HID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PID_CDC2_MSC_HID&type=code) | Defines the USB Product ID for CDC2, MSC, and HID functionality. | (MICROPY_HW_USB_PID) |
| [`MICROPY_HW_USB_PID_CDC3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PID_CDC3&type=code) | Defines the USB Product ID for CDC3 functionality. | (MICROPY_HW_USB_PID) |
| [`MICROPY_HW_USB_PID_CDC3_MSC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PID_CDC3_MSC&type=code) | Defines the USB Product ID for CDC3 and MSC functionality. | (MICROPY_HW_USB_PID) |
| [`MICROPY_HW_USB_PID_CDC3_MSC_HID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PID_CDC3_MSC_HID&type=code) | Defines the USB Product ID for CDC3 with MSC and HID support. | (MICROPY_HW_USB_PID) |
| [`MICROPY_HW_USB_PID_CDC_HID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PID_CDC_HID&type=code) | Defines the USB Product ID for CDC and HID functionality. | (MICROPY_HW_USB_PID) |
| [`MICROPY_HW_USB_PID_CDC_MSC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PID_CDC_MSC&type=code) | USB Product ID for CDC+MSC mode in STM USB stack. | (0x9800) |
| [`MICROPY_HW_USB_PID_CDC_MSC_HID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PID_CDC_MSC_HID&type=code) | Defines the USB Product ID for CDC, MSC, and HID functionality. | (MICROPY_HW_USB_PID) |
| [`MICROPY_HW_USB_PID_MSC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PID_MSC&type=code) | Defines the USB Product ID for the Mass Storage Class. | (MICROPY_HW_USB_PID) |
| [`MICROPY_HW_USB_PRODUCT_FS_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PRODUCT_FS_STRING&type=code) | Defines the USB product string for full-speed mode. | "Nicla Vision Virtual Comm Port in FS Mode" |
| [`MICROPY_HW_USB_PRODUCT_HS_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_PRODUCT_HS_STRING&type=code) | Defines the USB product string for high-speed mode. | "Nicla Vision Virtual Comm Port in HS Mode" |
| [`MICROPY_HW_USB_VBUS_DETECT_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_VBUS_DETECT_PIN&type=code) | Defines the pin used for USB VBUS detection. | (pyb_pin_USB_VBUS) |
| [`MICROPY_HW_USB_VID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USB_VID&type=code) | Defines the Vendor ID for USB devices. | (0x2886) |
#### MICROPY_HW_USES

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_USES_BOOTLOADER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USES_BOOTLOADER&type=code) | Indicates whether the hardware uses a bootloader based on the vector table offset. | (MICROPY_HW_VTOR != 0x08000000) |
#### MICROPY_HW_USRSW

This configuration group manages the settings for a user switch, including its pin assignment, interrupt mode, state indication when pressed, and pull resistor configuration. It allows for flexible integration and behavior of the user switch in various applications.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_USRSW_EXTI_MODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USRSW_EXTI_MODE&type=code) | Configures the external interrupt mode for the user switch. | (MP_HAL_PIN_TRIGGER_FALLING) |
| [`MICROPY_HW_USRSW_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USRSW_PIN&type=code) | Defines the pin used for the user switch, which can be configured for different behaviors. | (pin_C13) |
| [`MICROPY_HW_USRSW_PRESSED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USRSW_PRESSED&type=code) | Indicates the state of the user switch when pressed, typically defined as 1 for active high configurations. | (1) |
| [`MICROPY_HW_USRSW_PULL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_USRSW_PULL&type=code) | Configures the pull-up or pull-down resistor for the user switch. | (MP_HAL_PIN_PULL_NONE) |
#### MICROPY_HW_WIFI

This configuration group manages the hardware settings and pin assignments necessary for WiFi communication, including data signaling, SPI interface parameters, and interrupt handling. It ensures proper connectivity and functionality of WiFi modules by defining critical pins and communication speeds.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_WIFI_DATAREADY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIFI_DATAREADY&type=code) | Indicates the data ready pin for WiFi operations. | (pin_P803) |
| [`MICROPY_HW_WIFI_HANDSHAKE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIFI_HANDSHAKE&type=code) | Pin used for WiFi handshake signaling. | (pin_P806) |
| [`MICROPY_HW_WIFI_IRQ_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIFI_IRQ_PIN&type=code) | Defines the interrupt pin for Wi-Fi data ready events. | (MICROPY_HW_WIFI_DATAREADY) |
| [`MICROPY_HW_WIFI_SPI_BAUDRATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIFI_SPI_BAUDRATE&type=code) | Sets the baud rate for the WiFi SPI communication. | (25 * 1000 * 1000) |
| [`MICROPY_HW_WIFI_SPI_CS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIFI_SPI_CS&type=code) | Defines the chip select pin for the WiFi SPI interface. | (pin_P104) |
| [`MICROPY_HW_WIFI_SPI_ID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIFI_SPI_ID&type=code) | Identifies the SPI interface used for WiFi communication. | (1) |
| [`MICROPY_HW_WIFI_SPI_MISO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIFI_SPI_MISO&type=code) | Defines the GPIO pin number for the MISO line in the Wi-Fi SPI interface. | (14) |
| [`MICROPY_HW_WIFI_SPI_MOSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIFI_SPI_MOSI&type=code) | Defines the GPIO pin number for the MOSI line in the Wi-Fi SPI interface. | (12) |
| [`MICROPY_HW_WIFI_SPI_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIFI_SPI_SCK&type=code) | Defines the GPIO pin number for the SPI clock line used in Wi-Fi communication. | (13) |
#### MICROPY_HW_WIZNET

This configuration set manages the hardware interface for the WIZnet network module, including pin assignments for chip select, reset, and interrupt handling. It also specifies the SPI communication parameters such as baud rate and pin mappings for MISO, MOSI, and SCK, ensuring proper connectivity and data transfer between the microcontroller and the WIZnet module.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_WIZNET_PIN_CS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIZNET_PIN_CS&type=code) | Defines the chip select pin for the WIZnet network module. | (21) |
| [`MICROPY_HW_WIZNET_PIN_INTN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIZNET_PIN_INTN&type=code) | Enables RECV interrupt handling for incoming data on the INTN pin. | (21) |
| [`MICROPY_HW_WIZNET_PIN_RST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIZNET_PIN_RST&type=code) | Maps the reset pin for the WIZnet module to an unused GPIO pin. | (9) |
| [`MICROPY_HW_WIZNET_SPI_BAUDRATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIZNET_SPI_BAUDRATE&type=code) | Sets the baud rate for the Wiznet SPI interface to 20 MHz. | (20 * 1000 * 1000) |
| [`MICROPY_HW_WIZNET_SPI_ID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIZNET_SPI_ID&type=code) | Identifies the SPI interface for Wiznet hardware configuration. | (0) |
| [`MICROPY_HW_WIZNET_SPI_MISO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIZNET_SPI_MISO&type=code) | Defines the GPIO pin number for the MISO line of the Wiznet SPI interface. | (12) |
| [`MICROPY_HW_WIZNET_SPI_MOSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIZNET_SPI_MOSI&type=code) | Defines the GPIO pin number for the MOSI (Master Out Slave In) line in the Wiznet SPI configuration. | (11) |
| [`MICROPY_HW_WIZNET_SPI_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_WIZNET_SPI_SCK&type=code) | Defines the SPI clock pin number for Wiznet hardware configurations. | (10) |
#### MICROPY_HW_XOSC32K

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_XOSC32K`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_XOSC32K&type=code) | Enables the use of a 32kHz crystal oscillator for clock generation. | (1) |
#### MICROPY_HW_XSPI

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_XSPI_CS_HIGH_CYCLES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_XSPI_CS_HIGH_CYCLES&type=code) | Determines the number of cycles nCS remains high, set to 4 cycles. | (2) // nCS stays high for 4 cycles |
| [`MICROPY_HW_XSPI_PRESCALER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_XSPI_PRESCALER&type=code) | Sets the prescaler for the XSPI clock frequency, calculated as F_CLK = F_AHB/4. | (4) // F_CLK = F_AHB/4 |
#### MICROPY_HW_XSPIFLASH

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_HW_XSPIFLASH_SIZE_BITS_LOG2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HW_XSPIFLASH_SIZE_BITS_LOG2&type=code) | Log2 of the size in bits of the external SPI flash memory. | (29) |


### MICROPY_MODULE

This configuration set manages various aspects of module behavior and attributes in MicroPython, including initialization, delegation, and import handling. It allows for customization of module loading, supports frozen modules, and controls how attributes like __all__ and __file__ are processed, enhancing the flexibility and functionality of module management.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_MODULE_ATTR_DELEGATION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE_ATTR_DELEGATION&type=code) | Enables delegation of attribute lookups to a custom handler in modules. | (MICROPY_PY_SYS_ATTR_DELEGATION \|\| MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_MODULE_BUILTIN_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE_BUILTIN_INIT&type=code) | Controls whether to call __init__ when importing built-in modules for the first time. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_MODULE_BUILTIN_SUBPACKAGES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE_BUILTIN_SUBPACKAGES&type=code) | Enables support for built-in subpackages in modules. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_MODULE_DELEGATIONS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE_DELEGATIONS&type=code) | Defines delegation entries for module attribute handling. | \ |
| [`MICROPY_MODULE_DICT_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE_DICT_SIZE&type=code) | Initial size of the module dictionary. | (1) |
| [`MICROPY_MODULE_FROZEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE_FROZEN&type=code) | Enables support for frozen modules, allowing the use of precompiled bytecode or string modules. | (MICROPY_MODULE_FROZEN_STR \|\| MICROPY_MODULE_FROZEN_MPY) |
| [`MICROPY_MODULE_FROZEN_LEXER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE_FROZEN_LEXER&type=code) | Defines the function used for creating a lexer from frozen module strings. | mp_lexer_new_from_str_len |
| [`MICROPY_MODULE_FROZEN_MPY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE_FROZEN_MPY&type=code) | Enables support for frozen modules in the form of .mpy files. | (0) |
| [`MICROPY_MODULE_FROZEN_STR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE_FROZEN_STR&type=code) | Enables support for frozen modules in the form of strings. | (0) |
| [`MICROPY_MODULE_GETATTR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE_GETATTR&type=code) | Enables support for module-level __getattr__ functionality. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_MODULE_OVERRIDE_MAIN_IMPORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE_OVERRIDE_MAIN_IMPORT&type=code) | Enables modules to be imported with __name__ set to '__main__' when using the -m flag. | (1) |
| [`MICROPY_MODULE___ALL__`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE___ALL__&type=code) | Controls processing of __all__ when importing public symbols from a module. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_BASIC_FEATURES) |
| [`MICROPY_MODULE___FILE__`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MODULE___FILE__&type=code) | Controls whether the __file__ attribute is set on imported modules. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |


### MICROPY_NLR

This configuration set manages the support for non-local returns (NLR) across various CPU architectures, allowing for efficient exception handling and control flow. It specifies the number of registers to be saved during non-local jumps and enables architecture-specific optimizations, ensuring compatibility and performance across different platforms.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_NLR_AARCH64`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_AARCH64&type=code) | Enables non-local returns (NLR) support for AArch64 architecture. | (1) |
| [`MICROPY_NLR_MIPS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_MIPS&type=code) | Enables non-local returns for MIPS architecture. | (1) |
| [`MICROPY_NLR_NUM_REGS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_NUM_REGS&type=code) | Determines the number of registers to save for non-local returns based on the architecture. | (MICROPY_NLR_NUM_REGS_ARM_THUMB_FP) |
| [`MICROPY_NLR_NUM_REGS_AARCH64`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_NUM_REGS_AARCH64&type=code) | Defines the number of registers to save for non-local jumps on AArch64 architecture. | (13) |
| [`MICROPY_NLR_NUM_REGS_ARM_THUMB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_NUM_REGS_ARM_THUMB&type=code) | Defines the number of registers used for non-local returns in ARM Thumb architecture. | (10) |
| [`MICROPY_NLR_NUM_REGS_ARM_THUMB_FP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_NUM_REGS_ARM_THUMB_FP&type=code) | Defines the number of registers for ARM Thumb architecture with floating-point support. | (10 + 6) |
| [`MICROPY_NLR_NUM_REGS_MIPS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_NUM_REGS_MIPS&type=code) | Defines the number of non-local return (NLR) registers for MIPS architecture. | (13) |
| [`MICROPY_NLR_NUM_REGS_RV32I`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_NUM_REGS_RV32I&type=code) | Defines the number of registers for non-local returns in RV32I architecture. | (14) |
| [`MICROPY_NLR_NUM_REGS_RV64I`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_NUM_REGS_RV64I&type=code) | Defines the number of registers for non-local returns in RV64I architecture. | (14) |
| [`MICROPY_NLR_NUM_REGS_X64`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_NUM_REGS_X64&type=code) | Defines the number of registers used for non-local returns on x64 architecture. | (8) |
| [`MICROPY_NLR_NUM_REGS_X64_WIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_NUM_REGS_X64_WIN&type=code) | Defines the number of NLR (Non-Local Return) registers for x64 architecture on Windows systems. | (10) |
| [`MICROPY_NLR_NUM_REGS_X86`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_NUM_REGS_X86&type=code) | Defines the number of registers used for non-local returns on x86 architecture. | (6) |
| [`MICROPY_NLR_NUM_REGS_XTENSA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_NUM_REGS_XTENSA&type=code) | Defines the number of registers for non-local returns on Xtensa architecture. | (10) |
| [`MICROPY_NLR_NUM_REGS_XTENSAWIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_NUM_REGS_XTENSAWIN&type=code) | Defines the number of NLR (Non-Local Return) registers for the Xtensa Windows architecture. | (17) |
| [`MICROPY_NLR_OS_WINDOWS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_OS_WINDOWS&type=code) | Indicates the use of Windows-specific handling for non-local returns. | 1 |
| [`MICROPY_NLR_POWERPC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_POWERPC&type=code) | Enables non-local return (NLR) support for PowerPC architecture. | (1) |
| [`MICROPY_NLR_RV32I`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_RV32I&type=code) | Enables non-local return support for RISC-V 32-bit architecture. | (1) |
| [`MICROPY_NLR_RV64I`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_RV64I&type=code) | Enables non-local return support for RISC-V 64-bit architecture. | (1) |
| [`MICROPY_NLR_SETJMP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_SETJMP&type=code) | Enables the use of setjmp/longjmp for non-local jumps in exception handling. | (1) |
| [`MICROPY_NLR_THUMB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_THUMB&type=code) | Enables non-local returns for Thumb architecture. | (1) |
| [`MICROPY_NLR_THUMB_USE_LONG_JUMP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_THUMB_USE_LONG_JUMP&type=code) | Enables the use of long jump for non-local returns in Thumb architecture due to uncertain object layout. | (1) |
| [`MICROPY_NLR_X64`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_X64&type=code) | Enables non-local returns for x86-64 architecture. | (1) |
| [`MICROPY_NLR_X86`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_X86&type=code) | Enables non-local returns for x86 architecture. | (1) |
| [`MICROPY_NLR_XTENSA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NLR_XTENSA&type=code) | Enables non-local returns for Xtensa architecture. | (1) |


### MICROPY_PORT

This configuration group manages various port-specific settings and functionalities, including memory section definitions, built-in functions, and network interface parameters. It allows customization of initialization and deinitialization processes, as well as the setup of WLAN access points and server functionalities like FTP and Telnet.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PORT_BSSSECTION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_BSSSECTION&type=code) | Defines the name of the BSS section for uninitialized variables. | "upybss" |
| [`MICROPY_PORT_BUILTINS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_BUILTINS&type=code) | Defines additional built-in names for the global namespace. | \ |
| [`MICROPY_PORT_CONSTANTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_CONSTANTS&type=code) | Defines extra constants for a specific port. | \ |
| [`MICROPY_PORT_DATASECTION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_DATASECTION&type=code) | Assigns a name for sections containing static/global variables to facilitate easier map file inspection. | "upydata" |
| [`MICROPY_PORT_DEINIT_FUNC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_DEINIT_FUNC&type=code) | Calls a port-specific deinitialization function during the deinitialization process. | deinit() |
| [`MICROPY_PORT_EXTRA_BUILTINS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_EXTRA_BUILTINS&type=code) | Enables additional built-in functions specific to a port. | - |
| [`MICROPY_PORT_HAS_FTP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_HAS_FTP&type=code) | Enables FTP server functionality in the CC3200 port. | (1) |
| [`MICROPY_PORT_HAS_TELNET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_HAS_TELNET&type=code) | Enables Telnet server functionality in the port. | (1) |
| [`MICROPY_PORT_INIT_FUNC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_INIT_FUNC&type=code) | Calls a port-specific initialization function during startup. | init() |
| [`MICROPY_PORT_NETWORK_INTERFACES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_NETWORK_INTERFACES&type=code) | Combines board-specific network interface definitions for use in network modules. | \ |
| [`MICROPY_PORT_SFLASH_BLOCK_COUNT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_SFLASH_BLOCK_COUNT&type=code) | Determines the number of blocks in the serial flash memory. | 32 |
| [`MICROPY_PORT_WLAN_AP_CHANNEL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_WLAN_AP_CHANNEL&type=code) | Sets the channel for the WLAN access point. | 5 |
| [`MICROPY_PORT_WLAN_AP_KEY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_WLAN_AP_KEY&type=code) | Defines the access point key for WLAN connections. | "www.wipy.io" |
| [`MICROPY_PORT_WLAN_AP_SECURITY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_WLAN_AP_SECURITY&type=code) | Sets the security type for the WLAN access point to WPA/WPA2. | SL_SEC_TYPE_WPA_WPA2 |
| [`MICROPY_PORT_WLAN_AP_SSID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PORT_WLAN_AP_SSID&type=code) | Defines the SSID for the WLAN access point. | "wipy-wlan" |


### MICROPY_PY

This configuration group manages various features and functionalities related to Python's special methods, asynchronous programming, and Bluetooth support. It enables efficient data handling, advanced programming constructs, and Bluetooth capabilities, allowing developers to customize their MicroPython builds according to specific application needs.

#### MICROPY_PY_ALL

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_ALL_INPLACE_SPECIAL_METHODS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ALL_INPLACE_SPECIAL_METHODS&type=code) | Enables support for all inplace arithmetic operation methods like __imul__ and __iadd__. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_PY_ALL_SPECIAL_METHODS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ALL_SPECIAL_METHODS&type=code) | Enables support for all special methods in user-defined classes. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_ARRAY

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_ARRAY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ARRAY&type=code) | Enables the 'array' module, allowing for efficient array handling. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_ARRAY_SLICE_ASSIGN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ARRAY_SLICE_ASSIGN&type=code) | Enables support for slice assignments in array and bytearray types. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_ASSIGN

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_ASSIGN_EXPR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ASSIGN_EXPR&type=code) | Enables support for assignment expressions using := syntax. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
#### MICROPY_PY_ASYNC

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_ASYNC_AWAIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ASYNC_AWAIT&type=code) | Enables support for async/await syntax and related features. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
#### MICROPY_PY_ASYNCIO

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_ASYNCIO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ASYNCIO&type=code) | Enables support for the asyncio module based on ROM level configuration. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_ASYNCIO_TASK_QUEUE_PUSH_CALLBACK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ASYNCIO_TASK_QUEUE_PUSH_CALLBACK&type=code) | Enables a callback function when a task is pushed to the asyncio task queue. | (0) |
#### MICROPY_PY_ATTRTUPLE

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_ATTRTUPLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ATTRTUPLE&type=code) | Enables support for attrtuple type, providing space-efficient tuples with attribute access. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
#### MICROPY_PY_BINASCII

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_BINASCII`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BINASCII&type=code) | Enables the binascii module for binary-to-ASCII conversions. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BINASCII_CRC32`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BINASCII_CRC32&type=code) | Enables CRC32 functionality in the binascii module based on ROM level configuration. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_BLE

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_BLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLE&type=code) | Enables Bluetooth Low Energy (BLE) support in the build. | (1) |
| [`MICROPY_PY_BLE_NUS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLE_NUS&type=code) | Enables the Nordic UART Service for BLE, allowing REPL access over Bluetooth. | (0) |
#### MICROPY_PY_BLUETOOTH

This configuration set controls various aspects of Bluetooth functionality, enabling features such as central mode, GATT client support, and pairing capabilities. It also manages diagnostic logging, event handling, and memory allocation for Bluetooth operations, ensuring robust and efficient Bluetooth communication in applications.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_BLUETOOTH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH&type=code) | Enables Bluetooth support in the build. | (1) |
| [`MICROPY_PY_BLUETOOTH_DEFAULT_GAP_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_DEFAULT_GAP_NAME&type=code) | Sets the default GAP device name for Bluetooth, defaulting to 'MPY BTSTACK'. | "MPY BTSTACK" |
| [`MICROPY_PY_BLUETOOTH_DIAGNOSTIC_LOGGING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_DIAGNOSTIC_LOGGING&type=code) | Enables Bluetooth diagnostic logging for debugging purposes. | (1) |
| [`MICROPY_PY_BLUETOOTH_ENABLE_CENTRAL_MODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_ENABLE_CENTRAL_MODE&type=code) | Enables central mode functionality for Bluetooth operations. | (0) |
| [`MICROPY_PY_BLUETOOTH_ENABLE_GATT_CLIENT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_ENABLE_GATT_CLIENT&type=code) | Enables the GATT client functionality, defaulting to enabled if central mode is active. | (MICROPY_PY_BLUETOOTH_ENABLE_CENTRAL_MODE) |
| [`MICROPY_PY_BLUETOOTH_ENABLE_HCI_CMD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_ENABLE_HCI_CMD&type=code) | Enables support for low-level HCI commands in Bluetooth functionality. | (0) |
| [`MICROPY_PY_BLUETOOTH_ENABLE_L2CAP_CHANNELS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_ENABLE_L2CAP_CHANNELS&type=code) | Enables support for L2CAP Connection Oriented Channels in Bluetooth. | (MICROPY_BLUETOOTH_NIMBLE) |
| [`MICROPY_PY_BLUETOOTH_ENABLE_PAIRING_BONDING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_ENABLE_PAIRING_BONDING&type=code) | Enables support for Bluetooth pairing and bonding features. | (0) |
| [`MICROPY_PY_BLUETOOTH_ENTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_ENTER&type=code) | Prevents PendSV execution from racing with scheduler execution during asynchronous Bluetooth events. | MICROPY_PY_PENDSV_ENTER |
| [`MICROPY_PY_BLUETOOTH_EXIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_EXIT&type=code) | Ends an atomic section for Bluetooth operations, ensuring thread safety. | MICROPY_END_ATOMIC_SECTION(atomic_state); |
| [`MICROPY_PY_BLUETOOTH_HCI_READ_MODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_HCI_READ_MODE&type=code) | Determines the HCI read mode for Bluetooth, either packet or byte. | MICROPY_PY_BLUETOOTH_HCI_READ_MODE_PACKET |
| [`MICROPY_PY_BLUETOOTH_HCI_READ_MODE_BYTE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_HCI_READ_MODE_BYTE&type=code) | Defines the read mode for Bluetooth HCI as byte. | (0) |
| [`MICROPY_PY_BLUETOOTH_HCI_READ_MODE_PACKET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_HCI_READ_MODE_PACKET&type=code) | Enables reading Bluetooth HCI packets mode. | (1) |
| [`MICROPY_PY_BLUETOOTH_MAX_EVENT_DATA_TUPLE_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_MAX_EVENT_DATA_TUPLE_LEN&type=code) | Limits the maximum length of event data tuples for Bluetooth events. | 5 |
| [`MICROPY_PY_BLUETOOTH_NINAW10`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_NINAW10&type=code) | Enables Bluetooth Low Energy (BLE) support for NINA W10 modules. | (1) |
| [`MICROPY_PY_BLUETOOTH_RANDOM_ADDR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_RANDOM_ADDR&type=code) | Enables support for Bluetooth random address functionality. | (1) |
| [`MICROPY_PY_BLUETOOTH_RINGBUF_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_RINGBUF_SIZE&type=code) | Sets the size of the Bluetooth ring buffer, defaulting to 128 bytes. | (128) |
| [`MICROPY_PY_BLUETOOTH_SYNC_EVENT_STACK_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_SYNC_EVENT_STACK_SIZE&type=code) | Calculates the event stack size for Bluetooth synchronization by subtracting a fixed allowance from the RTOS stack size. | (CONFIG_BT_NIMBLE_TASK_STACK_SIZE - 1024) |
| [`MICROPY_PY_BLUETOOTH_USE_GATTC_EVENT_DATA_REASSEMBLY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_USE_GATTC_EVENT_DATA_REASSEMBLY&type=code) | Enables reassembly of fragmented GATTC event data in NimBLE. | MICROPY_BLUETOOTH_NIMBLE |
| [`MICROPY_PY_BLUETOOTH_USE_SYNC_EVENTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_USE_SYNC_EVENTS&type=code) | Enables synchronous Bluetooth events for direct VM callback execution in the BLE stack. | (0) |
| [`MICROPY_PY_BLUETOOTH_USE_SYNC_EVENTS_WITH_INTERLOCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BLUETOOTH_USE_SYNC_EVENTS_WITH_INTERLOCK&type=code) | Enables synchronization of Bluetooth event callbacks with the MicroPython runtime using interlock mechanisms. | (1) |
REVIEW: [docs/library/bluetooth.rst](docs/library/bluetooth.rst) and the port quick reference pages do not spell out which builds enable central/GATT client/HCI command support or pairing, nor the default ring buffer/event stack sizes (NimBLE vs CYW43). Users cannot tell feature availability per board.
#### MICROPY_PY_BOUND

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_BOUND_METHOD_FULL_EQUALITY_CHECK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BOUND_METHOD_FULL_EQUALITY_CHECK&type=code) | Controls whether bound methods use a direct comparison or require a function call for equality checks. | (0) |
#### MICROPY_PY_BTREE

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_BTREE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BTREE&type=code) | Enables the Berkeley DB btree module for MicroPython. | (0) |
#### MICROPY_PY_BUILTINS

This configuration group manages the availability and functionality of various built-in objects and functions in the MicroPython runtime, such as data types, collection methods, and utility functions. It allows developers to enable or disable specific features, tailoring the environment to meet the needs of their applications while optimizing resource usage.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_BUILTINS_BYTEARRAY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_BYTEARRAY&type=code) | Enables support for the bytearray object in the MicroPython runtime. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_BUILTINS_BYTES_HEX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_BYTES_HEX&type=code) | Enables the bytes.hex() and bytes.fromhex() methods for byte objects. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_CODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_CODE&type=code) | Determines the level of support for code objects based on various configuration options. | (MICROPY_PY_SYS_SETTRACE ? MICROPY_PY_BUILTINS_CODE_FULL : (MICROPY_PY_FUNCTION_ATTRS_CODE ? MICROPY_PY_BUILTINS_CODE_BASIC : (MICROPY_PY_BUILTINS_COMPILE ? MICROPY_PY_BUILTINS_CODE_MINIMUM : MICROPY_PY_BUILTINS_CODE_NONE))) |
| [`MICROPY_PY_BUILTINS_CODE_BASIC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_CODE_BASIC&type=code) | Enables basic support for code objects with limited features. | (2) |
| [`MICROPY_PY_BUILTINS_CODE_FULL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_CODE_FULL&type=code) | Enables full support for code objects with all features. | (3) |
| [`MICROPY_PY_BUILTINS_CODE_MINIMUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_CODE_MINIMUM&type=code) | Enables minimal support for code objects with basic features. | (1) |
| [`MICROPY_PY_BUILTINS_CODE_NONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_CODE_NONE&type=code) | Disables support for code objects. | (0) |
| [`MICROPY_PY_BUILTINS_COMPILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_COMPILE&type=code) | Enables the built-in compile function if the compiler is enabled and extra features are available. | (MICROPY_ENABLE_COMPILER && MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_COMPLEX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_COMPLEX&type=code) | Enables support for complex number types, contingent on the presence of float support. | (MICROPY_PY_BUILTINS_FLOAT) |
| [`MICROPY_PY_BUILTINS_DICT_FROMKEYS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_DICT_FROMKEYS&type=code) | Enables support for the dict.fromkeys() class method. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_BUILTINS_ENUMERATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_ENUMERATE&type=code) | Enables support for the enumerate built-in function. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_BUILTINS_EVAL_EXEC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_EVAL_EXEC&type=code) | Enables support for the eval() and exec() built-in functions when the compiler is enabled. | (MICROPY_ENABLE_COMPILER) |
| [`MICROPY_PY_BUILTINS_EXECFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_EXECFILE&type=code) | Enables support for the Python 2 execfile function when the compiler and specific ROM level features are enabled. | (MICROPY_ENABLE_COMPILER && MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_FILTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_FILTER&type=code) | Enables support for the filter built-in function. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_BUILTINS_FLOAT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_FLOAT&type=code) | Enables support for float data types and operations. | (1) |
| [`MICROPY_PY_BUILTINS_FROZENSET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_FROZENSET&type=code) | Enables support for the frozenset object when extra features are included. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_HELP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_HELP&type=code) | Enables the built-in help function for providing documentation and usage information. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_HELP_MODULES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_HELP_MODULES&type=code) | Enables the listing of available modules when executing help('modules'). Examples: help('modules') output includes available modules. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_HELP_TEXT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_HELP_TEXT&type=code) | Configures the help text displayed by the help() function. | rp2_help_text |
| [`MICROPY_PY_BUILTINS_INPUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_INPUT&type=code) | Enables the built-in input() function, requiring readline support. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_MEMORYVIEW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_MEMORYVIEW&type=code) | Enables support for the memoryview object in MicroPython. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_MEMORYVIEW_ITEMSIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_MEMORYVIEW_ITEMSIZE&type=code) | Controls support for the memoryview.itemsize attribute based on ROM level. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_PY_BUILTINS_MIN_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_MIN_MAX&type=code) | Enables support for the min() and max() built-in functions. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_BUILTINS_NEXT2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_NEXT2&type=code) | Enables support for calling the next() function with a second argument. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_BASIC_FEATURES) |
| [`MICROPY_PY_BUILTINS_NOTIMPLEMENTED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_NOTIMPLEMENTED&type=code) | Enables the definition of the 'NotImplemented' special constant. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_POW3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_POW3&type=code) | Enables support for the pow() function with three integer arguments. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_PROPERTY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_PROPERTY&type=code) | Enables support for the property object in the built-in features. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_BUILTINS_RANGE_ATTRS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_RANGE_ATTRS&type=code) | Enables implementation of start/stop/step attributes for the range type. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_BUILTINS_RANGE_BINOP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_RANGE_BINOP&type=code) | Enables binary operations (equality) for range objects, aligning behavior with CPython. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_PY_BUILTINS_REVERSED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_REVERSED&type=code) | Enables support for the reversed() built-in function. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_BUILTINS_ROUND_INT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_ROUND_INT&type=code) | Enables support for rounding integers, including bignum, allowing operations like round(123, -1) to yield 120. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_SET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_SET&type=code) | Enables support for the set object in MicroPython. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_BUILTINS_SLICE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_SLICE&type=code) | Enables support for slice subscript operators and the slice object. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_BUILTINS_SLICE_ATTRS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_SLICE_ATTRS&type=code) | Enables read access to slice attributes like start, stop, and step. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_SLICE_INDICES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_SLICE_INDICES&type=code) | Enables support for the .indices(len) method on slice objects. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_STR_CENTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_STR_CENTER&type=code) | Enables the str.center() method for string objects. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_STR_COUNT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_STR_COUNT&type=code) | Enables the str.count() method for string objects. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_BUILTINS_STR_OP_MODULO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_STR_OP_MODULO&type=code) | Enables the string formatting operator '%' for strings. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_BUILTINS_STR_PARTITION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_STR_PARTITION&type=code) | Enables the str.partition() and str.rpartition() methods based on ROM level configuration. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_STR_SPLITLINES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_STR_SPLITLINES&type=code) | Enables the str.splitlines() method for string objects. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_STR_UNICODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_STR_UNICODE&type=code) | Enables support for Unicode strings in the built-in str type. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_BUILTINS_STR_UNICODE_CHECK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_BUILTINS_STR_UNICODE_CHECK&type=code) | Enables UTF-8 validity checks when converting bytes to string. | (MICROPY_PY_BUILTINS_STR_UNICODE) |
#### MICROPY_PY_CMATH

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_CMATH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_CMATH&type=code) | Enables the 'cmath' module if the ROM level supports extra features. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_COLLECTIONS

This configuration set controls the inclusion and functionality of the collections module in MicroPython, allowing for advanced data structures such as deque, namedtuple, and OrderedDict. It enables essential features like iteration, subscription, and key order maintenance, enhancing the language's capability for managing collections of data.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_COLLECTIONS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_COLLECTIONS&type=code) | Enables the collections module if core features are included. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_COLLECTIONS_DEQUE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_COLLECTIONS_DEQUE&type=code) | Enables the 'collections.deque' type in MicroPython. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_COLLECTIONS_DEQUE_ITER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_COLLECTIONS_DEQUE_ITER&type=code) | Enables iteration support for 'collections.deque'. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_COLLECTIONS_DEQUE_SUBSCR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_COLLECTIONS_DEQUE_SUBSCR&type=code) | Enables subscription support for 'collections.deque'. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_COLLECTIONS_NAMEDTUPLE__ASDICT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_COLLECTIONS_NAMEDTUPLE__ASDICT&type=code) | Enables the _asdict function for namedtuple objects. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_PY_COLLECTIONS_ORDEREDDICT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_COLLECTIONS_ORDEREDDICT&type=code) | Enables the 'collections.OrderedDict' type for maintaining order of keys. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_CRYPTOLIB

This configuration controls the inclusion and functionality of the cryptographic library, allowing for SSL support and the definition of constants within the module. It also enables specific cryptographic modes, such as Counter (CTR) mode, enhancing the library's capabilities for secure data processing.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_CRYPTOLIB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_CRYPTOLIB&type=code) | Enables the cryptographic library, dependent on SSL support. | (MICROPY_PY_SSL) |
| [`MICROPY_PY_CRYPTOLIB_CONSTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_CRYPTOLIB_CONSTS&type=code) | Enables the definition of constants for the cryptolib module when set to a non-zero value. | (0) |
| [`MICROPY_PY_CRYPTOLIB_CTR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_CRYPTOLIB_CTR&type=code) | Enables Counter (CTR) mode support in the cryptolib module. | (0) |
#### MICROPY_PY_DEFLATE

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_DEFLATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_DEFLATE&type=code) | Enables the deflate module for decompression functionality. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_DEFLATE_COMPRESS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_DEFLATE_COMPRESS&type=code) | Enables compression support in the deflate module. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_FULL_FEATURES) |
#### MICROPY_PY_DELATTR

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_DELATTR_SETATTR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_DELATTR_SETATTR&type=code) | Enables support for class __delattr__ and __setattr__ methods, affecting code size and attribute access speed. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_DESCRIPTORS

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_DESCRIPTORS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_DESCRIPTORS&type=code) | Enables support for descriptor methods like __get__, __set__, __delete__, and __set_name__. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_ERRNO

This configuration controls the inclusion and functionality of the errno module, which provides error handling capabilities in networking contexts. It allows for the use of an error code dictionary for lookups and supports a customizable list of error constants.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_ERRNO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ERRNO&type=code) | Enables the errno module for error handling in networking contexts. | (1) |
| [`MICROPY_PY_ERRNO_ERRORCODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ERRNO_ERRORCODE&type=code) | Enables the errno.errorcode dictionary for error code lookups. | (1) |
| [`MICROPY_PY_ERRNO_LIST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ERRNO_LIST&type=code) | Custom list of errno constants for the errno module. | \ |
#### MICROPY_PY_ESP

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_ESP32_PCNT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ESP32_PCNT&type=code) | Enables the Pulse Counter (PCNT) module if supported by the SoC. | (SOC_PCNT_SUPPORTED) |
#### MICROPY_PY_ESPNOW

This configuration set enables and enhances support for the ESP-NOW communication protocol, allowing for efficient peer-to-peer communication. It includes features for managing peers, such as modifying and retrieving peer information, as well as tracking the Received Signal Strength Indicator (RSSI) values for better communication quality assessment.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_ESPNOW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ESPNOW&type=code) | Enables support for ESP-NOW communication protocol. | (1) |
| [`MICROPY_PY_ESPNOW_EXTRA_PEER_METHODS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ESPNOW_EXTRA_PEER_METHODS&type=code) | Enables additional peer management methods: mod_peer(), get_peer(), and peer_count(). Examples: mod_peer(peer_mac), get_peer(peer_mac), peer_count(). | 1 |
| [`MICROPY_PY_ESPNOW_RSSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ESPNOW_RSSI&type=code) | Enables tracking of RSSI values for peers in ESP-NOW communication. | 1 |
#### MICROPY_PY_FRAMEBUF

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_FRAMEBUF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_FRAMEBUF&type=code) | Enables the frame buffer module for graphics operations. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_FSTRINGS

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_FSTRINGS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_FSTRINGS&type=code) | Enables support for f-strings, allowing string interpolation in literals. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_FUNCTION

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_FUNCTION_ATTRS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_FUNCTION_ATTRS&type=code) | Enables implementation of attributes on functions. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_FUNCTION_ATTRS_CODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_FUNCTION_ATTRS_CODE&type=code) | Controls the implementation of the __code__ attribute for functions based on ROM level features. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_FULL_FEATURES) |
#### MICROPY_PY_GC

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_GC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_GC&type=code) | Enables the garbage collection module based on ROM level configuration. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_GC_COLLECT_RETVAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_GC_COLLECT_RETVAL&type=code) | Enables returning the number of collected objects from gc.collect(). Examples: gc.collect() returns 5 if 5 objects are collected. | (1) |
#### MICROPY_PY_GENERATOR

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_GENERATOR_PEND_THROW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_GENERATOR_PEND_THROW&type=code) | Enables a non-standard .pend_throw() method for generators to handle exceptions in a future-like manner. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
#### MICROPY_PY_HASHLIB

This configuration controls the availability of various cryptographic hashing functions within the hashlib module, allowing for secure data handling. It enables support for MD5, SHA-1, and SHA-256 hashing algorithms, particularly in contexts where SSL is utilized.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_HASHLIB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_HASHLIB&type=code) | Enables the hashlib module for cryptographic hashing functions. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_HASHLIB_MD5`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_HASHLIB_MD5&type=code) | Enables MD5 hashing support when SSL is enabled. | (MICROPY_PY_SSL) |
| [`MICROPY_PY_HASHLIB_SHA1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_HASHLIB_SHA1&type=code) | Enables SHA-1 hashing support when SSL and AXTLS are enabled. | (MICROPY_PY_SSL && MICROPY_SSL_AXTLS) |
| [`MICROPY_PY_HASHLIB_SHA256`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_HASHLIB_SHA256&type=code) | Enables SHA-256 hashing functionality in the hashlib module. | (1) |
#### MICROPY_PY_HEAPQ

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_HEAPQ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_HEAPQ&type=code) | Enables the heapq module for priority queue operations. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_IO

This configuration controls the inclusion of the 'io' module and its associated classes, which provide essential input/output functionalities in MicroPython. It enables features such as buffered writing, in-memory byte streams, and user-defined stream support, enhancing the flexibility and efficiency of data handling.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_IO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_IO&type=code) | Enables the 'io' module and related I/O functionalities. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_IO_BUFFEREDWRITER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_IO_BUFFEREDWRITER&type=code) | Enables the 'io.BufferedWriter' class for buffered writing operations. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_PY_IO_BYTESIO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_IO_BYTESIO&type=code) | Enables the 'io.BytesIO' class for in-memory byte stream operations. | (1) |
| [`MICROPY_PY_IO_IOBASE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_IO_IOBASE&type=code) | Enables the io.IOBase class for user stream support. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
#### MICROPY_PY_JS

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_JS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_JS&type=code) | Enables the JavaScript module if the ROM level supports extra features. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_JSFFI

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_JSFFI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_JSFFI&type=code) | Enables the jsffi module when extra features are included in the ROM configuration. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_JSON

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_JSON`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_JSON&type=code) | Enables JSON module support based on ROM level configuration. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_JSON_SEPARATORS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_JSON_SEPARATORS&type=code) | Enables support for custom separators in JSON serialization. | (1) |
#### MICROPY_PY_LWIP

This configuration set manages the lwIP network stack functionalities within MicroPython, enabling various networking capabilities such as TCP, PPP, and raw socket support. It also includes mechanisms for concurrency control and resource management during lwIP operations, ensuring safe execution and cleanup.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_LWIP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_LWIP&type=code) | Enables the lwIP network stack for MicroPython, allowing for network functionalities. | (1) |
| [`MICROPY_PY_LWIP_ENTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_LWIP_ENTER&type=code) | Acquires a lock to prevent the lwIP task from executing during critical sections. | lwip_lock_acquire(); |
| [`MICROPY_PY_LWIP_EXIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_LWIP_EXIT&type=code) | Indicates the exit point for LWIP operations, ensuring proper cleanup. | MICROPY_PY_PENDSV_EXIT |
| [`MICROPY_PY_LWIP_PPP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_LWIP_PPP&type=code) | Enables PPP (Point-to-Point Protocol) support when network PPP is enabled. | (MICROPY_PY_NETWORK_PPP_LWIP) |
| [`MICROPY_PY_LWIP_REENTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_LWIP_REENTER&type=code) | Handles re-entering lwIP tasks with concurrency protection. | MICROPY_PY_PENDSV_REENTER |
| [`MICROPY_PY_LWIP_SOCK_RAW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_LWIP_SOCK_RAW&type=code) | Enables support for raw sockets in the LWIP networking stack. | (MICROPY_PY_LWIP) |
| [`MICROPY_PY_LWIP_TCP_CLOSE_TIMEOUT_MS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_LWIP_TCP_CLOSE_TIMEOUT_MS&type=code) | Timeout duration in milliseconds before forcibly aborting a TCP socket closure. | (10000) |
REVIEW: The default forced close timeout for sockets (10s) is not documented in [docs/library/socket.rst](docs/library/socket.rst) or the lwIP notes; unclear whether ports vary this or how users can adjust it.
#### MICROPY_PY_MACHINE

This configuration group manages the functionalities related to hardware control and interfacing in MicroPython, enabling various features such as ADC, DAC, I2C, PWM, and sensor interactions. It allows developers to customize the machine module to suit specific hardware capabilities and application needs, facilitating direct access to low-level hardware operations.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_MACHINE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE&type=code) | Enables the 'machine' module, primarily for memory and hardware control functions. | (1) |
| [`MICROPY_PY_MACHINE_ADC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC&type=code) | Enables ADC (Analog-to-Digital Converter) functionality in the firmware. | (1) |
| [`MICROPY_PY_MACHINE_ADC_ATTEN_WIDTH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_ATTEN_WIDTH&type=code) | Enables legacy ADC.atten() and ADC.width() methods. | (0) |
| [`MICROPY_PY_MACHINE_ADC_BLOCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_BLOCK&type=code) | Enables the ADC.block() method, requiring implementation of mp_machine_adc_block(). Examples: Setting to 1 allows usage of ADC.block() in code. | (0) |
| [`MICROPY_PY_MACHINE_ADC_BLOCK_INCLUDEFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_BLOCK_INCLUDEFILE&type=code) | Path to the ADC block implementation file for the ESP32 port. | "ports/esp32/machine_adc_block.c" |
| [`MICROPY_PY_MACHINE_ADC_CLASS_CONSTANTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_CLASS_CONSTANTS&type=code) | Defines ADC class constants for various ports, allowing for specific ADC functionalities. | \ |
| [`MICROPY_PY_MACHINE_ADC_CLASS_CONSTANTS_CORE_VBAT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_CLASS_CONSTANTS_CORE_VBAT&type=code) | Defines the constant for the core battery voltage ADC channel if ADC_CHANNEL_VBAT is available. | \ |
| [`MICROPY_PY_MACHINE_ADC_CLASS_CONSTANTS_CORE_VDD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_CLASS_CONSTANTS_CORE_VDD&type=code) | Defines the constant for the core voltage ADC channel if available. | \ |
| [`MICROPY_PY_MACHINE_ADC_CLASS_CONSTANTS_WIDTH_12`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_CLASS_CONSTANTS_WIDTH_12&type=code) | Defines a constant for 12-bit ADC width with its corresponding value. | \ |
| [`MICROPY_PY_MACHINE_ADC_CLASS_CONSTANTS_WIDTH_13`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_CLASS_CONSTANTS_WIDTH_13&type=code) | Defines a constant for 13-bit ADC width if supported by the hardware. | \ |
| [`MICROPY_PY_MACHINE_ADC_CLASS_CONSTANTS_WIDTH_9_10_11`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_CLASS_CONSTANTS_WIDTH_9_10_11&type=code) | Defines ADC width constants for 9, 10, and 11 bits if supported by the hardware. | \ |
| [`MICROPY_PY_MACHINE_ADC_DEINIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_DEINIT&type=code) | Enables the ADC.deinit() method, requiring implementation of mp_machine_adc_deinit(). Examples: ADC.deinit() in user code. | (0) |
| [`MICROPY_PY_MACHINE_ADC_INCLUDEFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_INCLUDEFILE&type=code) | Path to the ADC implementation file for the specific port. | "ports/nrf/modules/machine/adc.c" |
| [`MICROPY_PY_MACHINE_ADC_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_INIT&type=code) | Enables the ADC.init() method, requiring implementation of mp_machine_adc_init_helper(). Examples: Set to (1) to enable ADC initialization. | (0) |
| [`MICROPY_PY_MACHINE_ADC_READ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_READ&type=code) | Enables the ADC.read() method, which is considered legacy. | (0) |
| [`MICROPY_PY_MACHINE_ADC_READ_UV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_ADC_READ_UV&type=code) | Enables the ADC.read_uv() method for reading UV values from the ADC. | (0) |
| [`MICROPY_PY_MACHINE_BARE_METAL_FUNCS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_BARE_METAL_FUNCS&type=code) | Enables bare metal functions for machine operations such as unique ID and sleep modes. | (1) |
| [`MICROPY_PY_MACHINE_BITSTREAM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_BITSTREAM&type=code) | Enables support for bitstream protocols, such as driving WS2812 LEDs. | (0) |
| [`MICROPY_PY_MACHINE_BOOTLOADER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_BOOTLOADER&type=code) | Enables bootloader functionality in the machine module. | (1) |
| [`MICROPY_PY_MACHINE_DAC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_DAC&type=code) | Enables support for Digital-to-Analog Converter (DAC) functionality based on hardware capabilities. | (SOC_DAC_SUPPORTED) |
| [`MICROPY_PY_MACHINE_DHT_READINTO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_DHT_READINTO&type=code) | Enables the DHT sensor readinto functionality for reading temperature and humidity data. | (1) |
| [`MICROPY_PY_MACHINE_DISABLE_IRQ_ENABLE_IRQ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_DISABLE_IRQ_ENABLE_IRQ&type=code) | Enables the implementation of functions to disable and enable interrupts. | (1) |
| [`MICROPY_PY_MACHINE_EXTRA_GLOBALS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_EXTRA_GLOBALS&type=code) | Enables the addition of extra global entries to the machine module. | \ |
| [`MICROPY_PY_MACHINE_FREQ_NUM_ARGS_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_FREQ_NUM_ARGS_MAX&type=code) | Maximum number of arguments for the machine.freq() function. | (1) |
| [`MICROPY_PY_MACHINE_HW_PWM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_HW_PWM&type=code) | Enables hardware PWM support in the build. | (0) |
| [`MICROPY_PY_MACHINE_I2C`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2C&type=code) | Enables I2C support based on hardware configuration. | (MICROPY_HW_ENABLE_HW_I2C) |
| [`MICROPY_PY_MACHINE_I2C_TARGET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2C_TARGET&type=code) | Enables I2C target functionality on supported SoCs, excluding ESP32. | (SOC_I2C_SUPPORT_SLAVE && !CONFIG_IDF_TARGET_ESP32) |
| [`MICROPY_PY_MACHINE_I2C_TARGET_FINALISER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2C_TARGET_FINALISER&type=code) | Enables finalization support for I2C target objects. | (1) |
| [`MICROPY_PY_MACHINE_I2C_TARGET_HARD_IRQ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2C_TARGET_HARD_IRQ&type=code) | Enables support for hard IRQs in I2C target functionality. | (1) |
| [`MICROPY_PY_MACHINE_I2C_TARGET_INCLUDEFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2C_TARGET_INCLUDEFILE&type=code) | Path to the I2C target implementation file for various ports. | "ports/mimxrt/machine_i2c_target.c" |
| [`MICROPY_PY_MACHINE_I2C_TARGET_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2C_TARGET_MAX&type=code) | Determines the maximum number of I2C target instances based on hardware capabilities. | (FSL_FEATURE_SOC_LPI2C_COUNT) |
| [`MICROPY_PY_MACHINE_I2C_TRANSFER_WRITE1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2C_TRANSFER_WRITE1&type=code) | Enables support for a separate write as the first transfer in I2C operations. | (0) |
| [`MICROPY_PY_MACHINE_I2S`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2S&type=code) | Enables I2S support based on hardware capabilities. | (SOC_I2S_SUPPORTED) |
| [`MICROPY_PY_MACHINE_I2S_CONSTANT_RX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2S_CONSTANT_RX&type=code) | Defines the I2S mode for receiving data in master mode. | (I2S_MODE_MASTER_RX) |
| [`MICROPY_PY_MACHINE_I2S_CONSTANT_TX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2S_CONSTANT_TX&type=code) | Indicates the I2S mode for master transmit operations. | (I2S_MODE_MASTER_TX) |
| [`MICROPY_PY_MACHINE_I2S_FINALISER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2S_FINALISER&type=code) | Enables the finalizer method for the I2S machine module. | (1) |
| [`MICROPY_PY_MACHINE_I2S_INCLUDEFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2S_INCLUDEFILE&type=code) | Path to the I2S implementation file for the specific port. | "ports/mimxrt/machine_i2s.c" |
| [`MICROPY_PY_MACHINE_I2S_MCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2S_MCK&type=code) | Enables the use of the MCK (master clock) pin in I2S configurations. | (1) |
| [`MICROPY_PY_MACHINE_I2S_RING_BUF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_I2S_RING_BUF&type=code) | Enables the use of a ring buffer for I2S operations. | (1) |
| [`MICROPY_PY_MACHINE_INCLUDEFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_INCLUDEFILE&type=code) | Path to the implementation file for the machine module. | "ports/unix/modmachine.c" |
| [`MICROPY_PY_MACHINE_INFO_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_INFO_ENTRY&type=code) | Defines an entry for the machine info object in the global namespace when DEBUG is enabled. | { MP_ROM_QSTR(MP_QSTR_info), MP_ROM_PTR(&machine_info_obj) }, |
| [`MICROPY_PY_MACHINE_LED_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_LED_ENTRY&type=code) | Defines the entry for the LED machine module with its associated type. | { MP_ROM_QSTR(MP_QSTR_LED), MP_ROM_PTR(&machine_led_type) }, |
| [`MICROPY_PY_MACHINE_MEMX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_MEMX&type=code) | Enables the provision of memory access objects like machine.mem8, machine.mem16, and machine.mem32. | (MICROPY_PY_MACHINE) |
| [`MICROPY_PY_MACHINE_NFC_RESET_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_NFC_RESET_ENTRY&type=code) | Defines the NFC reset entry for the NRF52 series with a corresponding reset constant. | { MP_ROM_QSTR(MP_QSTR_NFC_RESET), MP_ROM_INT(PYB_RESET_NFC) }, |
| [`MICROPY_PY_MACHINE_PIN_ALT_SUPPORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_PIN_ALT_SUPPORT&type=code) | Enables support for alternate function selection in machine.Pin. | (1) |
| [`MICROPY_PY_MACHINE_PIN_BASE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_PIN_BASE&type=code) | Enables the PinBase class for managing GPIO pins. | (1) |
| [`MICROPY_PY_MACHINE_PIN_BOARD_CPU`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_PIN_BOARD_CPU&type=code) | Enables support for board-specific CPU pin configurations. | (1) |
| [`MICROPY_PY_MACHINE_PIN_LEGACY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_PIN_LEGACY&type=code) | Enables inclusion of legacy methods and constants in machine.Pin when not in preview version 2. | (!MICROPY_PREVIEW_VERSION_2) |
| [`MICROPY_PY_MACHINE_PIN_MAKE_NEW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_PIN_MAKE_NEW&type=code) | Maps to the function mp_pin_make_new for creating new pin objects. | mp_pin_make_new |
| [`MICROPY_PY_MACHINE_PULSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_PULSE&type=code) | Enables the time_pulse_us function for measuring pulse durations on pins. | (0) |
| [`MICROPY_PY_MACHINE_PWM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_PWM&type=code) | Enables PWM functionality using either hardware or software implementations. | (MICROPY_PY_MACHINE_HW_PWM \|\| MICROPY_PY_MACHINE_SOFT_PWM) |
| [`MICROPY_PY_MACHINE_PWM_DUTY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_PWM_DUTY&type=code) | Enables PWM duty cycle functionality in the machine module. | (1) |
| [`MICROPY_PY_MACHINE_PWM_INCLUDEFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_PWM_INCLUDEFILE&type=code) | Path to the PWM implementation file for the specific port. | "ports/nrf/modules/machine/soft_pwm.c" |
| [`MICROPY_PY_MACHINE_RESET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_RESET&type=code) | Enables the inclusion of machine reset functionality. | (0) |
| [`MICROPY_PY_MACHINE_RESET_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_RESET_ENTRY&type=code) | Enables the machine reset functionality by defining the reset entry point when CONFIG_REBOOT is enabled. | { MP_ROM_QSTR(MP_QSTR_reset), MP_ROM_PTR(&machine_reset_obj) }, |
| [`MICROPY_PY_MACHINE_RNG_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_RNG_ENTRY&type=code) | Defines the entry for the random number generator in the machine module when RNG is enabled. | { MP_ROM_QSTR(MP_QSTR_rng), MP_ROM_PTR(&pyb_rng_get_obj) }, |
| [`MICROPY_PY_MACHINE_RTCOUNTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_RTCOUNTER&type=code) | Enables the real-time counter functionality. | (0) |
| [`MICROPY_PY_MACHINE_RTCOUNTER_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_RTCOUNTER_ENTRY&type=code) | Entry for the RTCounter module in the machine namespace. | { MP_ROM_QSTR(MP_QSTR_RTCounter), MP_ROM_PTR(&machine_rtcounter_type) }, |
| [`MICROPY_PY_MACHINE_SDCARD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_SDCARD&type=code) | Enables support for SD card functionality. | (1) |
| [`MICROPY_PY_MACHINE_SDCARD_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_SDCARD_ENTRY&type=code) | Defines the entry for the SDCard type in the machine module. | { MP_ROM_QSTR(MP_QSTR_SDCard), MP_ROM_PTR(&machine_sdcard_type) }, |
| [`MICROPY_PY_MACHINE_SIGNAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_SIGNAL&type=code) | Enables the machine.Signal class for handling signal operations. | (MICROPY_PY_MACHINE) |
| [`MICROPY_PY_MACHINE_SOFTI2C`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_SOFTI2C&type=code) | Enables the SoftI2C class for software-based I2C communication. | (0) |
| [`MICROPY_PY_MACHINE_SOFTSPI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_SOFTSPI&type=code) | Enables the SoftSPI class for software-based SPI communication. | (0) |
| [`MICROPY_PY_MACHINE_SOFT_PWM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_SOFT_PWM&type=code) | Enables software PWM functionality for controlling PWM signals. | (0) |
| [`MICROPY_PY_MACHINE_SPI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_SPI&type=code) | Enables support for the SPI protocol in MicroPython. | (0) |
REVIEW: Port docs (machine quickrefs and [docs/library/machine.rst](docs/library/machine.rst)) assume SoftI2C/SoftSPI/PWM fallbacks exist, but these flags can disable them; need per-port availability notes and guidance for boards without software implementations.
| [`MICROPY_PY_MACHINE_SPI_LSB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_SPI_LSB&type=code) | Indicates that the least significant bit is transmitted first in SPI communication. | (SPI_FIRSTBIT_LSB) |
| [`MICROPY_PY_MACHINE_SPI_MIN_DELAY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_SPI_MIN_DELAY&type=code) | Sets the minimum delay for SPI operations to zero. | (0) |
| [`MICROPY_PY_MACHINE_SPI_MSB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_SPI_MSB&type=code) | Indicates that SPI data is transmitted with the most significant bit first. | (SPI_FIRSTBIT_MSB) |
| [`MICROPY_PY_MACHINE_TEMP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_TEMP&type=code) | Enables temperature sensor support in the machine module. | (0) |
| [`MICROPY_PY_MACHINE_TEMP_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_TEMP_ENTRY&type=code) | Entry for the temperature module in the machine API, linking to the temperature type. | { MP_ROM_QSTR(MP_QSTR_Temp), MP_ROM_PTR(&machine_temp_type) }, |
| [`MICROPY_PY_MACHINE_TIMER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_TIMER&type=code) | Enables the 'machine.Timer' class for timing operations. | (0) |
| [`MICROPY_PY_MACHINE_TIMER_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_TIMER_ENTRY&type=code) | Entry for the Timer module in the machine interface, linking to the timer type. | { MP_ROM_QSTR(MP_QSTR_Timer), MP_ROM_PTR(&machine_timer_type) }, |
| [`MICROPY_PY_MACHINE_TIMER_NRF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_TIMER_NRF&type=code) | Enables the NRF timer module for MicroPython. | (1) |
| [`MICROPY_PY_MACHINE_TOUCH_PAD_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_TOUCH_PAD_ENTRY&type=code) | Enables the TouchPad functionality in the machine module for ESP32. | { MP_ROM_QSTR(MP_QSTR_TouchPad), MP_ROM_PTR(&machine_touchpad_type) }, |
| [`MICROPY_PY_MACHINE_UART`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_UART&type=code) | Enables UART peripheral support for serial communication. | (1) |
| [`MICROPY_PY_MACHINE_UART_CLASS_CONSTANTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_UART_CLASS_CONSTANTS&type=code) | Defines UART class constants for various UART features and configurations. | - |
| [`MICROPY_PY_MACHINE_UART_INCLUDEFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_UART_INCLUDEFILE&type=code) | Path to the UART implementation file for the specific port. | "ports/nrf/modules/machine/uart.c" |
| [`MICROPY_PY_MACHINE_UART_INV_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_UART_INV_ENTRY&type=code) | Defines UART inversion features for STM32H7, including TX and RX inversion. | \ |
| [`MICROPY_PY_MACHINE_UART_IRQ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_UART_IRQ&type=code) | Enables the UART.irq() method, requiring implementation of mp_machine_uart_irq(). Examples: Defined as (1) for enabling, (0) for disabling. | (SAMD21_EXTRA_FEATURES) |
| [`MICROPY_PY_MACHINE_UART_READCHAR_WRITECHAR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_UART_READCHAR_WRITECHAR&type=code) | Enables UART.readchar() and UART.writechar() methods, requiring implementation of corresponding functions. | (0) |
| [`MICROPY_PY_MACHINE_UART_SENDBREAK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_UART_SENDBREAK&type=code) | Enables the UART.sendbreak() method, requiring implementation of mp_machine_uart_sendbreak(). Examples: Set to (1) to enable sendbreak functionality. | (0) |
| [`MICROPY_PY_MACHINE_WDT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_WDT&type=code) | Enables the watchdog timer functionality. | (1) |
| [`MICROPY_PY_MACHINE_WDT_INCLUDEFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_WDT_INCLUDEFILE&type=code) | Path to the machine watchdog implementation file for the CC3200 port. | "ports/cc3200/mods/machine_wdt.c" |
| [`MICROPY_PY_MACHINE_WDT_TIMEOUT_MS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MACHINE_WDT_TIMEOUT_MS&type=code) | Enables the watchdog timer timeout functionality with a default timeout value. | (1) |
#### MICROPY_PY_MARSHAL

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_MARSHAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MARSHAL&type=code) | Enables the 'marshal' module for serialization of Python objects. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
#### MICROPY_PY_MATH

This configuration set focuses on enhancing the mathematical capabilities within the environment by enabling various mathematical functions and constants, as well as implementing fixes for specific edge cases involving special values like NaN and infinity. It ensures that users have access to a robust set of mathematical tools while addressing potential issues that may arise during calculations.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_MATH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MATH&type=code) | Enables the math module if core features are included. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_MATH_ATAN2_FIX_INFNAN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MATH_ATAN2_FIX_INFNAN&type=code) | Enables a fix for handling infinity and NaN in the atan2 function. | (0) |
| [`MICROPY_PY_MATH_CONSTANTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MATH_CONSTANTS&type=code) | Enables additional mathematical constants like tau, infinity, and NaN in the math module. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_MATH_COPYSIGN_FIX_NAN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MATH_COPYSIGN_FIX_NAN&type=code) | Enables a fix for NaN values in the copysign function by replacing NaN with 0. | (1) |
| [`MICROPY_PY_MATH_FACTORIAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MATH_FACTORIAL&type=code) | Enables the math.factorial function if the ROM level supports extra features. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_MATH_FMOD_FIX_INFNAN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MATH_FMOD_FIX_INFNAN&type=code) | Controls handling of infinity in the fmod function. | (0) |
| [`MICROPY_PY_MATH_GAMMA_FIX_NEGINF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MATH_GAMMA_FIX_NEGINF&type=code) | Enables a workaround to raise ValueError for gamma function with negative infinity input. | (1) |
| [`MICROPY_PY_MATH_ISCLOSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MATH_ISCLOSE&type=code) | Enables the math.isclose function for comparing floating-point numbers. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_MATH_MODF_FIX_NEGZERO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MATH_MODF_FIX_NEGZERO&type=code) | Enables handling of negative zero in the modf function. | (0) |
| [`MICROPY_PY_MATH_POW_FIX_NAN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MATH_POW_FIX_NAN&type=code) | Enables fixes for pow(1, NaN) and pow(NaN, 0) to return 1 instead of NaN. | (0) |
| [`MICROPY_PY_MATH_SPECIAL_FUNCTIONS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MATH_SPECIAL_FUNCTIONS&type=code) | Enables special mathematical functions like erf, erfc, gamma, and lgamma. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_MICROPYTHON

This configuration set controls various features of the micropython module, enhancing memory management and providing additional functionalities such as heap locking and memory information retrieval. It also enables support for specific features like RingIO and stack usage monitoring, allowing for more efficient resource management in MicroPython applications.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_MICROPYTHON`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MICROPYTHON&type=code) | Enables the micropython module based on the core features configuration level. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_MICROPYTHON_HEAP_LOCKED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MICROPYTHON_HEAP_LOCKED&type=code) | Enables the 'micropython.heap_locked' function for managing heap locking. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_PY_MICROPYTHON_MEM_INFO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MICROPYTHON_MEM_INFO&type=code) | Enables memory information functions in the micropython module. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_MICROPYTHON_RINGIO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MICROPYTHON_RINGIO&type=code) | Enables support for the micropython.RingIO() functionality. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_MICROPYTHON_STACK_USE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MICROPYTHON_STACK_USE&type=code) | Enables the 'micropython.stack_use' function based on memory information availability. | (MICROPY_PY_MICROPYTHON_MEM_INFO) |
#### MICROPY_PY_MUSIC

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_MUSIC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_MUSIC&type=code) | Enables the music module for sound playback functionality. | (0) |
#### MICROPY_PY_NETWORK

This configuration group manages networking capabilities, enabling various functionalities such as LAN and WLAN support, as well as socket operations. It also allows customization of network parameters like hostname settings and SPI clock speed for communication, ensuring flexibility in network module integration.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_NETWORK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_NETWORK&type=code) | Enables networking functionality including modules for network and socket operations. | (1) |
| [`MICROPY_PY_NETWORK_HOSTNAME_DEFAULT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_NETWORK_HOSTNAME_DEFAULT&type=code) | Sets the default hostname for network configurations. | "mpy-metro-m7" |
| [`MICROPY_PY_NETWORK_HOSTNAME_MAX_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_NETWORK_HOSTNAME_MAX_LEN&type=code) | Maximum length for network hostname, excluding null terminator. | (32) |
| [`MICROPY_PY_NETWORK_INCLUDEFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_NETWORK_INCLUDEFILE&type=code) | Path to the network module header file for inclusion. | "ports/esp8266/modnetwork.h" |
| [`MICROPY_PY_NETWORK_LAN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_NETWORK_LAN&type=code) | Enables LAN network support for ESP32 builds. | (1) |
| [`MICROPY_PY_NETWORK_LAN_SPI_CLOCK_SPEED_MZ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_NETWORK_LAN_SPI_CLOCK_SPEED_MZ&type=code) | Defines the SPI clock speed for LAN communication in MHz. | (20) |
| [`MICROPY_PY_NETWORK_MODULE_GLOBALS_INCLUDEFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_NETWORK_MODULE_GLOBALS_INCLUDEFILE&type=code) | Path to the header file containing global definitions for the network module. | "ports/esp8266/modnetwork_globals.h" |
| [`MICROPY_PY_NETWORK_PPP_LWIP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_NETWORK_PPP_LWIP&type=code) | Enables PPP support using LWIP for network functionality. | (MICROPY_PY_LWIP) |
| [`MICROPY_PY_NETWORK_WLAN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_NETWORK_WLAN&type=code) | Enables WLAN support for network functionalities. | (1) |
#### MICROPY_PY_NRF

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_NRF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_NRF&type=code) | Enables support for NRF modules and features. | (CORE_FEAT) |
#### MICROPY_PY_ONEWIRE

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_ONEWIRE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ONEWIRE&type=code) | Enables the low-level 1-Wire module for communication with 1-Wire devices. | (SAMD21_EXTRA_FEATURES) |
#### MICROPY_PY_OPENAMP

This configuration set controls various aspects of OpenAMP functionality, enabling features such as ELF file loading, virtual file system support, and resource table usage for communication between host and remote processors. Additionally, it manages trace logging capabilities, allowing for efficient debugging and monitoring of remote processor activities.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_OPENAMP_REMOTEPROC_ELFLD_ENABLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OPENAMP_REMOTEPROC_ELFLD_ENABLE&type=code) | Enables support for loading ELF files, saving around 7KB when disabled. | (1) |
| [`MICROPY_PY_OPENAMP_REMOTEPROC_STORE_ENABLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OPENAMP_REMOTEPROC_STORE_ENABLE&type=code) | Enables support for a VFS-based image store to load ELF files from storage. | (1) |
| [`MICROPY_PY_OPENAMP_RSC_TABLE_ENABLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OPENAMP_RSC_TABLE_ENABLE&type=code) | Enables the use of a resource table for sharing configuration between host and remote cores. | (1) |
| [`MICROPY_PY_OPENAMP_TRACE_BUF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OPENAMP_TRACE_BUF&type=code) | Address of the OpenAMP trace buffer as a uint32_t. | ((uint32_t)openamp_trace_buf) |
| [`MICROPY_PY_OPENAMP_TRACE_BUF_ENABLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OPENAMP_TRACE_BUF_ENABLE&type=code) | Enables a trace buffer for remote processors to write trace logs. | (1) |
| [`MICROPY_PY_OPENAMP_TRACE_BUF_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OPENAMP_TRACE_BUF_LEN&type=code) | Length of the OpenAMP trace buffer. | sizeof(MICROPY_PY_OPENAMP_TRACE_BUF) |
#### MICROPY_PY_OS

This configuration set controls the features and functionalities of the OS module, enabling various system-level operations such as environment variable management, file system synchronization, and terminal stream duplication. It also includes support for executing shell commands and retrieving system information, enhancing the interaction between MicroPython and the underlying operating system.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_OS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS&type=code) | Enables the os built-in module. | (1) |
| [`MICROPY_PY_OS_DUPTERM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_DUPTERM&type=code) | Enables support for duplicate terminal streams in the OS module. | (1) |
| [`MICROPY_PY_OS_DUPTERM_BUILTIN_STREAM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_DUPTERM_BUILTIN_STREAM&type=code) | Enables support for built-in stream duplication in the OS module. | (1) |
| [`MICROPY_PY_OS_DUPTERM_NOTIFY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_DUPTERM_NOTIFY&type=code) | Enables notification functionality for the os.dupterm feature. | (1) |
| [`MICROPY_PY_OS_DUPTERM_STREAM_DETACHED_ATTACHED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_DUPTERM_STREAM_DETACHED_ATTACHED&type=code) | Enables support for detached and attached duplicate terminal streams. | (1) |
| [`MICROPY_PY_OS_ERRNO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_ERRNO&type=code) | Enables the errno functionality in the OS module. | (1) |
| [`MICROPY_PY_OS_GETENV_PUTENV_UNSETENV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_GETENV_PUTENV_UNSETENV&type=code) | Enables the getenv, putenv, and unsetenv functions in the os module. | (1) |
| [`MICROPY_PY_OS_INCLUDEFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_INCLUDEFILE&type=code) | Path to the OS module implementation file for additional Unix features. | "ports/unix/modos.c" |
| [`MICROPY_PY_OS_SEP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_SEP&type=code) | Enables support for the OS path separator feature. | (1) |
| [`MICROPY_PY_OS_STATVFS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_STATVFS&type=code) | Enables the statvfs function in the OS module if OS support is included. | (MICROPY_PY_OS) |
| [`MICROPY_PY_OS_SYNC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_SYNC&type=code) | Enables the sync() function to synchronize all filesystems. | (MICROPY_VFS) |
| [`MICROPY_PY_OS_SYSTEM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_SYSTEM&type=code) | Enables the 'system' function in the OS module for executing shell commands. | (1) |
| [`MICROPY_PY_OS_UNAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_UNAME&type=code) | Enables the os.uname function for testing purposes. | (1) |
| [`MICROPY_PY_OS_UNAME_RELEASE_DYNAMIC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_UNAME_RELEASE_DYNAMIC&type=code) | Enables dynamic retrieval of the OS release version. | (1) |
| [`MICROPY_PY_OS_URANDOM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_OS_URANDOM&type=code) | Enables the urandom function for generating random bytes. | (1) |
#### MICROPY_PY_PENDSV

This configuration manages the PendSV interrupt priority to control the execution of background tasks during context switching. It ensures that critical sections of code can run without interruption by adjusting the interrupt priority levels appropriately.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_PENDSV_ENTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_PENDSV_ENTER&type=code) | Prevents background tasks from executing by raising the PendSV interrupt priority. | uint32_t atomic_state = raise_irq_pri(IRQ_PRI_PENDSV); |
| [`MICROPY_PY_PENDSV_EXIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_PENDSV_EXIT&type=code) | Restores the previous interrupt priority level after PendSV context execution. | restore_irq_pri(atomic_state); |
| [`MICROPY_PY_PENDSV_REENTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_PENDSV_REENTER&type=code) | Raises the interrupt priority to prevent background tasks during re-entry. | atomic_state = raise_irq_pri(IRQ_PRI_PENDSV); |
#### MICROPY_PY_PLATFORM

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_PLATFORM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_PLATFORM&type=code) | Enables the platform module for accessing platform-specific information. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_PYB

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_PYB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_PYB&type=code) | Enables inclusion of the pyb module in the build. | (1) |
| [`MICROPY_PY_PYB_LEGACY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_PYB_LEGACY&type=code) | Enables inclusion of legacy functions and classes in the pyb module. | (1) |
#### MICROPY_PY_RA

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_RA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_RA&type=code) | Enables inclusion of the ra module with peripheral register constants. | (1) |
#### MICROPY_PY_RANDOM

This configuration set controls the availability and functionality of the random number generation features in MicroPython. It allows for the inclusion of basic random functions, additional utilities, hardware support for randomness, and initialization of the random seed, enhancing the randomness capabilities for applications.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_RANDOM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_RANDOM&type=code) | Enables the random module and its functions based on ROM level configuration. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_RANDOM_EXTRA_FUNCS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_RANDOM_EXTRA_FUNCS&type=code) | Enables additional random functions like randrange, randint, and choice. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_RANDOM_HW_RNG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_RANDOM_HW_RNG&type=code) | Enables hardware random number generation support. | (0) |
| [`MICROPY_PY_RANDOM_SEED_INIT_FUNC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_RANDOM_SEED_INIT_FUNC&type=code) | Initializes the random seed function on import. | (mp_random_seed_init()) |
#### MICROPY_PY_RE

This configuration set controls the implementation and features of regular expression support, allowing for pattern matching and manipulation in code. It includes options for debugging, group matching, and substitution functionalities, enhancing the versatility and usability of regular expressions.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_RE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_RE&type=code) | Enables support for regular expressions based on the re1.5 library. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_RE_DEBUG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_RE_DEBUG&type=code) | Enables debugging features for regular expressions. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_PY_RE_MATCH_GROUPS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_RE_MATCH_GROUPS&type=code) | Enables support for matching groups in regular expressions. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_PY_RE_MATCH_SPAN_START_END`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_RE_MATCH_SPAN_START_END&type=code) | Enables support for span, start, and end methods in regular expression matching. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_PY_RE_SUB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_RE_SUB&type=code) | Enables the 're.sub' function for regular expression substitutions. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_REVERSE

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_REVERSE_SPECIAL_METHODS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_REVERSE_SPECIAL_METHODS&type=code) | Enables support for reverse arithmetic operation methods like __radd__ and __rsub__. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
#### MICROPY_PY_SELECT

This configuration group manages the functionality and optimizations of the 'select' module, which is used for I/O multiplexing in MicroPython. It allows for the enabling of the select() function, sets polling intervals for non-file-descriptor objects, and provides options for POSIX-specific enhancements.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_SELECT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SELECT&type=code) | Enables the 'select' module for handling I/O multiplexing. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_SELECT_IOCTL_CALL_PERIOD_MS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SELECT_IOCTL_CALL_PERIOD_MS&type=code) | Sets the polling interval in milliseconds for non-file-descriptor objects during select operations. | (1) |
| [`MICROPY_PY_SELECT_POSIX_OPTIMISATIONS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SELECT_POSIX_OPTIMISATIONS&type=code) | Enables POSIX optimizations in the 'select' module while disabling select.select(). | (1) |
| [`MICROPY_PY_SELECT_SELECT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SELECT_SELECT&type=code) | Enables the select() function in the select module for compatibility. | (1) |
#### MICROPY_PY_SOCKET

This configuration set controls the functionality and behavior of the socket module, enabling network communication and supporting asynchronous event handling. It also allows for extended state management and sets default parameters for socket operations, enhancing the overall networking capabilities.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_SOCKET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SOCKET&type=code) | Enables the socket module for network communication. | (1) |
| [`MICROPY_PY_SOCKET_EVENTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SOCKET_EVENTS&type=code) | Enables support for asynchronous socket event callbacks. | (MICROPY_PY_WEBREPL) |
| [`MICROPY_PY_SOCKET_EVENTS_HANDLER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SOCKET_EVENTS_HANDLER&type=code) | Calls the socket events handler function if socket events are enabled. | extern void socket_events_handler(void); socket_events_handler(); |
| [`MICROPY_PY_SOCKET_EXTENDED_STATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SOCKET_EXTENDED_STATE&type=code) | Enables extended socket state for network interfaces requiring additional state management. | (1) |
| [`MICROPY_PY_SOCKET_LISTEN_BACKLOG_DEFAULT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SOCKET_LISTEN_BACKLOG_DEFAULT&type=code) | Determines the default backlog value for socket.listen(), capped at 128. | (SOMAXCONN < 128 ? SOMAXCONN : 128) |
#### MICROPY_PY_SSL

This configuration set controls the inclusion and management of SSL support within the build, allowing for secure communication through protocols like SSL and DTLS. It also facilitates memory management for SSL objects and ensures proper context handling during SSL operations.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_SSL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SSL&type=code) | Enables SSL support in the build. | (0) |
| [`MICROPY_PY_SSL_DTLS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SSL_DTLS&type=code) | Enables support for the DTLS protocol when using mbedTLS and sufficient ROM level. | (MICROPY_SSL_MBEDTLS && MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_SSL_FINALISER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SSL_FINALISER&type=code) | Enables finaliser code for SSL objects to manage memory cleanup. | (MICROPY_ENABLE_FINALISER) |
| [`MICROPY_PY_SSL_MBEDTLS_NEED_ACTIVE_CONTEXT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SSL_MBEDTLS_NEED_ACTIVE_CONTEXT&type=code) | Enables storage of the current SSLContext for mbedtls callbacks. | (MICROPY_PY_SSL_ECDSA_SIGN_ALT) |
#### MICROPY_PY_STM

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_STM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_STM&type=code) | Enables the STM module for sub-GHz radio functions. | (1) // for subghz radio functions |
| [`MICROPY_PY_STM_CONST`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_STM_CONST&type=code) | Controls inclusion of named register constants in the STM module to save memory. | (0) // saves size, no named registers |
#### MICROPY_PY_STR

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_STR_BYTES_CMP_WARN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_STR_BYTES_CMP_WARN&type=code) | Issues a warning when comparing string and bytes objects. | (1) |
#### MICROPY_PY_STRING

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_STRING_TX_GIL_THRESHOLD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_STRING_TX_GIL_THRESHOLD&type=code) | Minimum string length for GIL-aware stdout printing operations. | (20) |
#### MICROPY_PY_STRUCT

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_STRUCT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_STRUCT&type=code) | Enables the 'struct' module for packing and unpacking binary data. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_PY_STRUCT_UNSAFE_TYPECODES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_STRUCT_UNSAFE_TYPECODES&type=code) | Enables unsafe and non-standard typecodes O, P, S in the struct module, allowing access to arbitrary memory. | (1) |
#### MICROPY_PY_SYS

This configuration set controls various features and functionalities of the 'sys' module, which is essential for system-level operations in MicroPython. It enables access to command-line arguments, exception handling, module import paths, and standard input/output streams, among other capabilities, thereby enhancing the interaction between the MicroPython environment and the underlying system.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_SYS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS&type=code) | Controls the inclusion of the 'sys' module and its features. | (0) |
| [`MICROPY_PY_SYS_ARGV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_ARGV&type=code) | Enables the 'sys.argv' attribute for accessing command-line arguments. | (1) |
| [`MICROPY_PY_SYS_ATEXIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_ATEXIT&type=code) | Enables the sys.atexit function for registering callbacks on program exit. | (1) |
| [`MICROPY_PY_SYS_ATTR_DELEGATION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_ATTR_DELEGATION&type=code) | Enables attribute delegation for the sys module based on the presence of sys.path, sys.ps1/ps2, or sys.tracebacklimit. | (MICROPY_PY_SYS_PATH \|\| MICROPY_PY_SYS_PS1_PS2 \|\| MICROPY_PY_SYS_TRACEBACKLIMIT) |
| [`MICROPY_PY_SYS_EXC_INFO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_EXC_INFO&type=code) | Enables the 'sys.exc_info' function to retrieve information about the current exception. | (0) |
| [`MICROPY_PY_SYS_EXECUTABLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_EXECUTABLE&type=code) | Enables the sys.executable attribute, providing the path to the MicroPython binary. | (1) |
| [`MICROPY_PY_SYS_EXIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_EXIT&type=code) | Enables the 'sys.exit' function in the system module. | (1) |
| [`MICROPY_PY_SYS_GETSIZEOF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_GETSIZEOF&type=code) | Enables the 'sys.getsizeof' function to return the size of an object in bytes. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_PY_SYS_INTERN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_INTERN&type=code) | Enables the 'sys.intern' function for string interning. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_PY_SYS_MAXSIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_MAXSIZE&type=code) | Enables the 'sys.maxsize' constant in the system module. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_SYS_MODULES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_MODULES&type=code) | Disables all optional features of the sys module, including sys.modules. | (0) |
| [`MICROPY_PY_SYS_PATH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_PATH&type=code) | Enables the 'sys.path' attribute for module import functionality. | (1) |
| [`MICROPY_PY_SYS_PATH_ARGV_DEFAULTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_PATH_ARGV_DEFAULTS&type=code) | Controls whether to initialize sys.argv and sys.path to default values during startup. | (0) |
| [`MICROPY_PY_SYS_PATH_DEFAULT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_PATH_DEFAULT&type=code) | Default paths for module search, including frozen modules and user libraries. | ".frozen:~/.micropython/lib:/usr/lib/micropython" |
| [`MICROPY_PY_SYS_PLATFORM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_PLATFORM&type=code) | Defines the platform name for the MicroPython environment. | "alif" |
| [`MICROPY_PY_SYS_PS1_PS2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_PS1_PS2&type=code) | Enables mutable attributes sys.ps1 and sys.ps2 for controlling REPL prompts. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_SYS_SETTRACE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_SETTRACE&type=code) | Enables the 'sys.settrace' function for setting a trace function to monitor execution. | (0) |
| [`MICROPY_PY_SYS_STDFILES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_STDFILES&type=code) | Enables the provision of sys.stdin, sys.stdout, and sys.stderr objects. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_SYS_STDIO_BUFFER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_STDIO_BUFFER&type=code) | Enables the sys.{stdin, stdout, stderr}.buffer object for buffered I/O operations. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_SYS_TRACEBACKLIMIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_SYS_TRACEBACKLIMIT&type=code) | Enables the mutable 'tracebacklimit' attribute in the sys module. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
#### MICROPY_PY_THREAD

This configuration controls the multithreading capabilities within the MicroPython environment, allowing for the use of the _thread module and ensuring thread safety through the implementation of a Global Interpreter Lock (GIL). It also provides options for managing GIL behavior and supports recursive mutexes to enhance thread management.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_THREAD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_THREAD&type=code) | Enables support for the _thread module and multithreading features. | (0) // disable ARM_THUMB_FP using vldr due to RA has single float only |
| [`MICROPY_PY_THREAD_GIL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_THREAD_GIL&type=code) | Enables the use of a Global Interpreter Lock (GIL) for thread safety in the runtime. | (MICROPY_PY_THREAD) |
| [`MICROPY_PY_THREAD_GIL_VM_DIVISOR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_THREAD_GIL_VM_DIVISOR&type=code) | Determines the number of VM jump-loops before releasing the GIL, defaulting to 32. | (32) |
| [`MICROPY_PY_THREAD_RECURSIVE_MUTEX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_THREAD_RECURSIVE_MUTEX&type=code) | Enables the use of recursive mutexes when threading is enabled. | (MICROPY_PY_THREAD) |
#### MICROPY_PY_TIME

This configuration set controls the functionalities and features of the time module, enabling various time-related operations such as retrieving the current time, custom sleep functionality, and additional global time functions. It also allows for precise timekeeping through tick functionality and supports both standard and high-resolution time retrieval.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_TIME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_TIME&type=code) | Enables the unix-specific 'time' module for time-related functionalities. | (1) |
| [`MICROPY_PY_TIME_CUSTOM_SLEEP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_TIME_CUSTOM_SLEEP&type=code) | Enables a custom sleep function for time.sleep(). | (1) |
| [`MICROPY_PY_TIME_EXTRA_GLOBALS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_TIME_EXTRA_GLOBALS&type=code) | Adds extra global time-related functions to the time module. | \ |
| [`MICROPY_PY_TIME_GMTIME_LOCALTIME_MKTIME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_TIME_GMTIME_LOCALTIME_MKTIME&type=code) | Enables the time.gmtime, time.localtime, and time.mktime functions. | (1) |
| [`MICROPY_PY_TIME_INCLUDEFILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_TIME_INCLUDEFILE&type=code) | Path to the implementation file for the time module. | "ports/cc3200/mods/modtime.c" |
| [`MICROPY_PY_TIME_TICKS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_TIME_TICKS&type=code) | Enables time tick functionality using RTC1 for millisecond and microsecond resolution. | (1) |
| [`MICROPY_PY_TIME_TICKS_PERIOD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_TIME_TICKS_PERIOD&type=code) | Defines the period for time ticks, calculated as one more than the maximum positive small integer. | (MP_SMALL_INT_POSITIVE_MASK + 1) |
| [`MICROPY_PY_TIME_TIME_TIME_NS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_TIME_TIME_TIME_NS&type=code) | Enables the time.time() and time.time_ns() functions for retrieving the current time in seconds and nanoseconds. | (0) |
#### MICROPY_PY_UBLUEPY

This configuration controls the support for the ubluepy Bluetooth module, allowing for both central and peripheral functionalities. It enables developers to implement Bluetooth communication features in their applications, facilitating device interactions and connectivity.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_UBLUEPY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_UBLUEPY&type=code) | Enables support for the ubluepy Bluetooth module. | (1) |
| [`MICROPY_PY_UBLUEPY_CENTRAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_UBLUEPY_CENTRAL&type=code) | Enables central Bluetooth functionality in ubluepy. | (1) |
| [`MICROPY_PY_UBLUEPY_PERIPHERAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_UBLUEPY_PERIPHERAL&type=code) | Enables support for the ubluepy peripheral functionality. | (1) |
#### MICROPY_PY_UCTYPES

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_UCTYPES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_UCTYPES&type=code) | Enables the uctypes module for defining and accessing raw data structures in memory. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PY_UCTYPES_NATIVE_C_TYPES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_UCTYPES_NATIVE_C_TYPES&type=code) | Enables support for C native type aliases in uctypes. | (1) |
#### MICROPY_PY_UHEAPQ

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_UHEAPQ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_UHEAPQ&type=code) | Enables the uheapq module for priority queue functionality. | (1) |
#### MICROPY_PY_USOCKET

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_USOCKET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_USOCKET&type=code) | Enables support for the uSocket module. | (1) |
#### MICROPY_PY_USSL

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_USSL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_USSL&type=code) | Enables support for SSL in the uPy networking stack. | (1) |
#### MICROPY_PY_UTIMEQ

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_UTIMEQ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_UTIMEQ&type=code) | Enables the utimeq module for managing time queues. | (1) |
#### MICROPY_PY_UWEBSOCKET

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_UWEBSOCKET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_UWEBSOCKET&type=code) | Enables support for the uWebSocket module. | (1) |
#### MICROPY_PY_VFS

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_VFS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_VFS&type=code) | Enables the virtual file system (VFS) module based on ROM level and VFS configuration. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES && MICROPY_VFS) |
#### MICROPY_PY_WAIT

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_WAIT_FOR_INTERRUPT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_WAIT_FOR_INTERRUPT&type=code) | Inserts assembly code to wait for an interrupt on ESP32 architecture. | asm volatile ("waiti 0\n") |
#### MICROPY_PY_WEBREPL

This configuration controls the WebREPL module, which facilitates remote access to the MicroPython environment through a web interface. It includes settings for managing file transfer delays and optimizing memory usage by allowing static allocation of file buffers, making it suitable for various operational contexts.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_WEBREPL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_WEBREPL&type=code) | Enables the WebREPL module for remote access via a web interface. | (MICROPY_PY_LWIP) |
| [`MICROPY_PY_WEBREPL_DELAY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_WEBREPL_DELAY&type=code) | Sets a delay in milliseconds for WebREPL file transfers to manage traffic overload. | (20) |
| [`MICROPY_PY_WEBREPL_STATIC_FILEBUF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_WEBREPL_STATIC_FILEBUF&type=code) | Enables static allocation of the file buffer in WebREPL for memory-constrained environments. | (1) |
#### MICROPY_PY_WEBSOCKET

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_WEBSOCKET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_WEBSOCKET&type=code) | Enables the websocket module for handling WebSocket connections. | (1) |
#### MICROPY_PY_ZEPHYR

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_ZEPHYR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ZEPHYR&type=code) | Enables Zephyr OS support in the MicroPython build. | (1) |
#### MICROPY_PY_ZSENSOR

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_PY_ZSENSOR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PY_ZSENSOR&type=code) | Enables support for the ZSensor module. | (1) |


### MICROPY_MISC

This collection of macros configures various aspects of MicroPython's functionality, including debugging options, error reporting, and system-specific features. It allows developers to customize the behavior of the interpreter, manage memory allocation, and enable or disable specific capabilities such as Bluetooth support and atomic operations.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MICROPY_ASYNC_KBD_INTR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ASYNC_KBD_INTR&type=code) | Enables raising KeyboardInterrupt directly from the signal handler when not using the Global Interpreter Lock (GIL). Examples: Set to 1 for async interrupts; Set to 0 for scheduled interrupts. | (!MICROPY_PY_THREAD_GIL) |
| [`MICROPY_BANNER_MACHINE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BANNER_MACHINE&type=code) | Defines the machine-specific banner message format for display. | MICROPY_PY_SYS_PLATFORM " [" MICROPY_PLATFORM_COMPILER "] version" |
| [`MICROPY_BANNER_NAME_AND_VERSION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BANNER_NAME_AND_VERSION&type=code) | Defines the banner string including MicroPython version, git tag, and build date. | "MicroPython (with v2.0 preview) " MICROPY_GIT_TAG " on " MICROPY_BUILD_DATE |
| [`MICROPY_BEGIN_ATOMIC_SECTION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BEGIN_ATOMIC_SECTION&type=code) | Locks interrupts to ensure atomic operations. | irq_lock |
| [`MICROPY_BLUETOOTH_NIMBLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BLUETOOTH_NIMBLE&type=code) | Enables support for the NimBLE Bluetooth stack. | (1) |
| [`MICROPY_BLUETOOTH_NIMBLE_BINDINGS_ONLY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BLUETOOTH_NIMBLE_BINDINGS_ONLY&type=code) | Enables only the Bluetooth NimBLE bindings without full implementation. | (1) |
| [`MICROPY_BUILD_DATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BUILD_DATE&type=code) | Holds the date when the MicroPython build was created. | "2025-08-16" |
| [`MICROPY_BUILD_TYPE_PAREN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BUILD_TYPE_PAREN&type=code) | Formats the build type in parentheses for display purposes. | " (" MICROPY_BUILD_TYPE ")" |
| [`MICROPY_BUILTIN_METHOD_CHECK_SELF_ARG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BUILTIN_METHOD_CHECK_SELF_ARG&type=code) | Enables checking the type of the 'self' argument in built-in methods to prevent undefined behavior. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_BYTES_PER_GC_BLOCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_BYTES_PER_GC_BLOCK&type=code) | Defines the number of bytes in a memory allocation/GC block, rounded up for allocations. | (4 * MP_BYTES_PER_OBJ_WORD) |
| [`MICROPY_CAN_OVERRIDE_BUILTINS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CAN_OVERRIDE_BUILTINS&type=code) | Enables the ability to override built-in functions in the builtins module. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_CPYTHON_COMPAT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_CPYTHON_COMPAT&type=code) | Enables features that enhance compatibility with CPython, potentially increasing code size and memory usage. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_DEBUG_MP_OBJ_SENTINELS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_DEBUG_MP_OBJ_SENTINELS&type=code) | Enables debugging versions of MP_OBJ_NULL, MP_OBJ_STOP_ITERATION, and MP_OBJ_SENTINEL. | (0) |
| [`MICROPY_DEBUG_PARSE_RULE_NAME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_DEBUG_PARSE_RULE_NAME&type=code) | Enables printing of parse rule names instead of integers in parse node output. | (1) |
| [`MICROPY_DEBUG_PRINTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_DEBUG_PRINTER&type=code) | Defines the printer used for debugging output, typically set to stderr. | (&mp_stderr_print) |
| [`MICROPY_DEBUG_PRINTERS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_DEBUG_PRINTERS&type=code) | Enables functions that print debugging information for bytecode and parsing. | (0) |
| [`MICROPY_DEBUG_VALGRIND`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_DEBUG_VALGRIND&type=code) | Enables additional memory checking instrumentation for Valgrind. | (0) |
| [`MICROPY_DEBUG_VERBOSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_DEBUG_VERBOSE&type=code) | Enables verbose debugging output across various modules. | (0) |
| [`MICROPY_DEBUG_VM_STACK_OVERFLOW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_DEBUG_VM_STACK_OVERFLOW&type=code) | Enables a check for VM stack overflow by adding an extra slot in the stack. | (0) |
| [`MICROPY_DYNAMIC_COMPILER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_DYNAMIC_COMPILER&type=code) | Enables support for dynamic compilation features. | (1) |
| [`MICROPY_EMERGENCY_EXCEPTION_BUF_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EMERGENCY_EXCEPTION_BUF_SIZE&type=code) | Determines the size of the emergency exception buffer, with 0 indicating dynamic allocation. | (0)      // 0 - implies dynamic allocation |
| [`MICROPY_END_ATOMIC_SECTION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_END_ATOMIC_SECTION&type=code) | Ends an atomic section by restoring the previous interrupt state. | irq_unlock |
| [`MICROPY_EPOCH_IS_1970`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EPOCH_IS_1970&type=code) | Indicates that VFS stat functions return time values relative to January 1, 1970. | (1) |
| [`MICROPY_EPOCH_IS_2000`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EPOCH_IS_2000&type=code) | Determines if the epoch date is set to January 1, 2000, affecting timestamp calculations. | (1 - (MICROPY_EPOCH_IS_1970)) |
| [`MICROPY_ERROR_PRINTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ERROR_PRINTER&type=code) | Output stream for printing errors and warnings. | (&mp_stderr_print) |
| [`MICROPY_ERROR_REPORTING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ERROR_REPORTING&type=code) | Controls the level of detail in error messages and warnings. | (MICROPY_ERROR_REPORTING_DETAILED) |
| [`MICROPY_ERROR_REPORTING_DETAILED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ERROR_REPORTING_DETAILED&type=code) | Enables detailed exception messages that include full information such as object names. | (3) |
| [`MICROPY_ERROR_REPORTING_NONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ERROR_REPORTING_NONE&type=code) | Removes exception messages, requiring MICROPY_ROM_TEXT_COMPRESSION to be disabled. | (0) |
| [`MICROPY_ERROR_REPORTING_NORMAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ERROR_REPORTING_NORMAL&type=code) | Enables basic error details in exception messages. | (2) |
| [`MICROPY_ERROR_REPORTING_TERSE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ERROR_REPORTING_TERSE&type=code) | Enables short static strings for exception messages. | (1) |
| [`MICROPY_ESP32_USE_BOOTLOADER_RTC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ESP32_USE_BOOTLOADER_RTC&type=code) | Enables the use of RTC for bootloader functionality on specific ESP32 targets. | (1) |
| [`MICROPY_ESP8266_APA102`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ESP8266_APA102&type=code) | Enables support for APA102 LED strip control on ESP8266. | (1) |
| [`MICROPY_ESP_IDF_ENTRY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_ESP_IDF_ENTRY&type=code) | Defines the entry point for the ESP-IDF application, defaulting to app_main. | app_main |
| [`MICROPY_EVENT_POLL_HOOK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EVENT_POLL_HOOK&type=code) | Triggers a wait-for-interrupt operation, allowing the system to handle events. | __WFI(); |
| [`MICROPY_EVENT_POLL_HOOK_WITH_USB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EVENT_POLL_HOOK_WITH_USB&type=code) | Executes the USB stack when the scheduler is locked and USB data is pending. | \ |
| [`MICROPY_EXPOSE_MP_COMPILE_TO_RAW_CODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_EXPOSE_MP_COMPILE_TO_RAW_CODE&type=code) | Controls the exposure of mp_compile_to_raw_code as a public function based on built-in code settings. | (MICROPY_PY_BUILTINS_CODE >= MICROPY_PY_BUILTINS_CODE_BASIC \|\| MICROPY_PERSISTENT_CODE_SAVE) |
| [`MICROPY_FULL_CHECKS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_FULL_CHECKS&type=code) | Enables full checks for data validity, enhancing error detection during execution. | (1) |
| [`MICROPY_GCREGS_SETJMP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_GCREGS_SETJMP&type=code) | Fallback to setjmp() for discovering GC pointers in registers. | (1) |
| [`MICROPY_GC_ALLOC_THRESHOLD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_GC_ALLOC_THRESHOLD&type=code) | Controls automatic garbage collection based on memory allocation thresholds. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_GC_CONSERVATIVE_CLEAR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_GC_CONSERVATIVE_CLEAR&type=code) | Enables zeroing of newly allocated memory blocks to prevent stray pointers. | (MICROPY_ENABLE_GC) |
| [`MICROPY_GC_INITIAL_HEAP_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_GC_INITIAL_HEAP_SIZE&type=code) | Initial heap size for garbage collection, set to 56 KB for ESP32. | (56 * 1024) |
| [`MICROPY_GC_SPLIT_HEAP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_GC_SPLIT_HEAP&type=code) | Enables testing of a split garbage collection heap. | (1) |
| [`MICROPY_GC_SPLIT_HEAP_AUTO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_GC_SPLIT_HEAP_AUTO&type=code) | Enables automatic management of heap areas based on allocation needs. | (0) |
| [`MICROPY_GC_SPLIT_HEAP_N_HEAPS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_GC_SPLIT_HEAP_N_HEAPS&type=code) | Determines the number of heaps for garbage collection when split heap is enabled. | (1) |
| [`MICROPY_GC_STACK_ENTRY_TYPE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_GC_STACK_ENTRY_TYPE&type=code) | Defines the C-type for entries in the garbage collection stack, affecting memory allocation policies. | uint16_t |
| [`MICROPY_GIT_HASH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_GIT_HASH&type=code) | Contains the current Git commit hash for the build. | "0a119b8164" |
| [`MICROPY_GIT_TAG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_GIT_TAG&type=code) | Contains the current Git tag of the MicroPython build. | "v1.27.0-preview.16.g0a119b8164.dirty" |
| [`MICROPY_HAL_HAS_STDIO_MODE_SWITCH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HAL_HAS_STDIO_MODE_SWITCH&type=code) | Indicates the availability of functions for switching standard I/O modes. | (1) |
| [`MICROPY_HAL_HAS_VT100`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HAL_HAS_VT100&type=code) | Indicates support for VT100 terminal commands. | (1) |
| [`MICROPY_HAL_VERSION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HAL_VERSION&type=code) | Indicates the version of the Hardware Abstraction Layer (HAL). | "2.8.0" |
| [`MICROPY_HAS_FILE_READER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HAS_FILE_READER&type=code) | Enables file reading functionality based on the presence of POSIX or VFS readers. | (MICROPY_READER_POSIX \|\| MICROPY_READER_VFS) |
| [`MICROPY_HEAP_END`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HEAP_END&type=code) | Determines the end address of the heap based on SDRAM validity. | ((sdram_valid) ? sdram_end() : &_heap_end) |
| [`MICROPY_HEAP_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HEAP_SIZE&type=code) | Defines the size of the heap memory in bytes for garbage collection. | (25600) // heap size 25 kilobytes |
| [`MICROPY_HEAP_START`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HEAP_START&type=code) | Determines the starting address of the heap based on SDRAM validity. | ((sdram_valid) ? sdram_start() : &_heap_start) |
| [`MICROPY_HELPER_LEXER_UNIX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HELPER_LEXER_UNIX&type=code) | Enables the inclusion of Unix-specific lexer helper functions. | (1) |
| [`MICROPY_HELPER_REPL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_HELPER_REPL&type=code) | Enables inclusion of REPL helper functions based on ROM level configuration. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_I2C_PINS_ARG_OPTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_I2C_PINS_ARG_OPTS&type=code) | Indicates that I2C pin arguments are not required for most boards. | 0 |
| [`MICROPY_INTERNAL_EVENT_HOOK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_INTERNAL_EVENT_HOOK&type=code) | Fallback for ports lacking non-blocking event processing; evaluates to (void)0. | (void)0 |
| [`MICROPY_INTERNAL_PRINTF_PRINTER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_INTERNAL_PRINTF_PRINTER&type=code) | Pointer to the mp_print_t printer for printf output when internal printf is enabled. | (&mp_plat_print) |
| [`MICROPY_KBD_EXCEPTION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_KBD_EXCEPTION&type=code) | Enables the KeyboardInterrupt exception and related functionality. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_LOADED_MODULES_DICT_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_LOADED_MODULES_DICT_SIZE&type=code) | Initial size of the sys.modules dictionary. | (3) |
| [`MICROPY_LONGINT_IMPL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_LONGINT_IMPL&type=code) | Determines the implementation of long integers, allowing options like long long or MPZ. | (MICROPY_LONGINT_IMPL_LONGLONG) |
| [`MICROPY_LONGINT_IMPL_LONGLONG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_LONGINT_IMPL_LONGLONG&type=code) | Enables long integer implementation using 64-bit long long type. | (1) |
| [`MICROPY_LONGINT_IMPL_MPZ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_LONGINT_IMPL_MPZ&type=code) | Enables the use of MPZ (multiple precision integers) for long integer implementation. | (2) |
| [`MICROPY_LONGINT_IMPL_NONE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_LONGINT_IMPL_NONE&type=code) | Indicates that long integer support is disabled. | (0) |
| [`MICROPY_MACHINE_BITSTREAM_TYPE_HIGH_LOW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MACHINE_BITSTREAM_TYPE_HIGH_LOW&type=code) | Defines a timing format for driving WS2812 LEDs as a 4-tuple of high and low times. | (0) |
| [`MICROPY_MACHINE_MEM_GET_READ_ADDR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MACHINE_MEM_GET_READ_ADDR&type=code) | Function to retrieve the read address for machine memory operations. | mod_machine_mem_get_addr |
| [`MICROPY_MACHINE_MEM_GET_WRITE_ADDR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MACHINE_MEM_GET_WRITE_ADDR&type=code) | Defines the function to retrieve the write address for machine memory operations. | mod_machine_mem_get_addr |
| [`MICROPY_MALLOC_USES_ALLOCATED_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MALLOC_USES_ALLOCATED_SIZE&type=code) | Enables passing the allocated memory size to realloc/free for enhanced memory debugging. | (1) |
| [`MICROPY_MBEDTLS_CONFIG_BARE_METAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MBEDTLS_CONFIG_BARE_METAL&type=code) | Enables bare metal memory management for mbedTLS in coverage builds. | (1) |
| [`MICROPY_MBFS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MBFS&type=code) | Enables the micro:bit filesystem when VFS is disabled. | (!MICROPY_VFS) |
| [`MICROPY_MEM_STATS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MEM_STATS&type=code) | Enables collection of memory allocation statistics. | (0) |
| [`MICROPY_MIN_USE_CORTEX_CPU`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MIN_USE_CORTEX_CPU&type=code) | Enables support for minimal IRQ and reset framework on Cortex-M CPUs. | (1) |
| [`MICROPY_MIN_USE_STDOUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MIN_USE_STDOUT&type=code) | Enables the use of standard output for printing. | (1) |
| [`MICROPY_MIN_USE_STM32_MCU`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MIN_USE_STM32_MCU&type=code) | Enables minimal support for STM32 microcontroller features. | (1) |
| [`MICROPY_MPHALPORT_H`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MPHALPORT_H&type=code) | Defines the header file for the microcontroller hardware abstraction layer. | "pic16bit_mphal.h" |
| [`MICROPY_MULTIPLE_INHERITANCE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_MULTIPLE_INHERITANCE&type=code) | Enables support for multiple inheritance in Python classes, affecting class resolution and method lookup. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_CORE_FEATURES) |
| [`MICROPY_NO_ALLOCA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_NO_ALLOCA&type=code) | Disables the use of alloca() and replaces it with heap allocation via m_malloc. | (1) |
| [`MICROPY_OBJ_BASE_ALIGNMENT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OBJ_BASE_ALIGNMENT&type=code) | Ensures MicroPython objects are aligned on a specified byte boundary for proper memory access. | - |
| [`MICROPY_OBJ_IMMEDIATE_OBJS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OBJ_IMMEDIATE_OBJS&type=code) | Determines if None, False, and True are encoded as immediate objects instead of pointers, reducing code size. | (MICROPY_OBJ_REPR != MICROPY_OBJ_REPR_D) |
| [`MICROPY_OBJ_REPR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OBJ_REPR&type=code) | Controls the object representation format used in MicroPython. | (MICROPY_OBJ_REPR_B) |
| [`MICROPY_OBJ_REPR_A`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OBJ_REPR_A&type=code) | Defines the object representation format for small integers, qstrs, immediate objects, and pointers. | (0) |
| [`MICROPY_OBJ_REPR_B`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OBJ_REPR_B&type=code) | Defines the representation format for MicroPython objects, allowing encoding of small integers, qstrs, immediate objects, and pointers. | (1) |
| [`MICROPY_OBJ_REPR_C`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OBJ_REPR_C&type=code) | Defines the representation of objects using a 32-bit word format for efficient encoding and decoding. | (2) |
| [`MICROPY_OBJ_REPR_D`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OBJ_REPR_D&type=code) | Defines a 64-bit object representation format for nan-boxing, allowing for efficient storage of various object types. | (3) |
| [`MICROPY_OPT_COMPUTED_GOTO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OPT_COMPUTED_GOTO&type=code) | Enables computed gotos for a performance boost in the VM, improving execution speed by approximately 10%. | (1) |
| [`MICROPY_OPT_LOAD_ATTR_FAST_PATH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OPT_LOAD_ATTR_FAST_PATH&type=code) | Optimizes attribute loading from instance types, increasing code size by approximately 48 bytes. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_OPT_MAP_LOOKUP_CACHE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OPT_MAP_LOOKUP_CACHE&type=code) | Enables caching of map lookups to improve performance by reducing search times. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_OPT_MAP_LOOKUP_CACHE_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OPT_MAP_LOOKUP_CACHE_SIZE&type=code) | Determines the size of the RAM allocated for the map lookup cache. | (128) |
| [`MICROPY_OPT_MATH_FACTORIAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OPT_MATH_FACTORIAL&type=code) | Controls the implementation efficiency of the math.factorial function. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_OPT_MPZ_BITWISE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_OPT_MPZ_BITWISE&type=code) | Enables fast bitwise operations for positive arguments, increasing code size. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_PAGE_MASK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PAGE_MASK&type=code) | Mask for aligning addresses to page boundaries. | (MICROPY_PAGE_SIZE - 1) |
| [`MICROPY_PAGE_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PAGE_SIZE&type=code) | Defines the memory page size as 4096 bytes. | 4096 |
| [`MICROPY_PERSISTENT_CODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PERSISTENT_CODE&type=code) | Enables the persistence of generated code independent of the VM/runtime instance. | (MICROPY_PERSISTENT_CODE_LOAD \|\| MICROPY_PERSISTENT_CODE_SAVE \|\| MICROPY_MODULE_FROZEN_MPY) |
| [`MICROPY_PERSISTENT_CODE_LOAD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PERSISTENT_CODE_LOAD&type=code) | Enables loading of .mpy files for persistent code execution. | (1) |
| [`MICROPY_PERSISTENT_CODE_SAVE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PERSISTENT_CODE_SAVE&type=code) | Enables saving of persistent bytecode and native code. | (MICROPY_PY_SYS_SETTRACE) |
| [`MICROPY_PERSISTENT_CODE_SAVE_FILE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PERSISTENT_CODE_SAVE_FILE&type=code) | Enables saving persistent code to a file on supported platforms. | (1) |
| [`MICROPY_PERSISTENT_CODE_SAVE_FUN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PERSISTENT_CODE_SAVE_FUN&type=code) | Enables support for converting functions to persistent code using the marshal module. | (MICROPY_PY_MARSHAL) |
| [`MICROPY_PERSISTENT_CODE_TRACK_BSS_RODATA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PERSISTENT_CODE_TRACK_BSS_RODATA&type=code) | Enables tracking of BSS/rodata memory to prevent garbage collection from reclaiming it. | (1) |
| [`MICROPY_PERSISTENT_CODE_TRACK_FUN_DATA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PERSISTENT_CODE_TRACK_FUN_DATA&type=code) | Enables tracking of native function data to prevent garbage collection from reclaiming it. | (1) |
| [`MICROPY_PIN_DEFS_PORT_H`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PIN_DEFS_PORT_H&type=code) | Includes the port-specific pin definition header file. | "pin_defs_stm32.h" |
| [`MICROPY_PLATFORM_ARCH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PLATFORM_ARCH&type=code) | Identifies the architecture of the platform, such as 'aarch64', 'arm', 'x86_64', or 'riscv64'. | "aarch64" |
| [`MICROPY_PLATFORM_COMPILER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PLATFORM_COMPILER&type=code) | Identifies the compiler used for building MicroPython, formatted as a string. | "" |
| [`MICROPY_PLATFORM_COMPILER_BITS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PLATFORM_COMPILER_BITS&type=code) | Indicates the bitness of the compiler platform, either '64 bit' or '32 bit'. | "64 bit" |
| [`MICROPY_PLATFORM_LIBC_LIB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PLATFORM_LIBC_LIB&type=code) | Identifies the C standard library in use, such as 'glibc', 'newlib', or 'picolibc'. | "picolibc" |
| [`MICROPY_PLATFORM_LIBC_VER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PLATFORM_LIBC_VER&type=code) | Holds the version of the libc library as a string, specifically for Android API. | MP_STRINGIFY(__ANDROID_API__) |
| [`MICROPY_PLATFORM_SYSTEM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PLATFORM_SYSTEM&type=code) | Identifies the underlying platform, such as 'Android', 'Linux', 'Windows', etc. | "MicroPython" |
| [`MICROPY_PLATFORM_VERSION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PLATFORM_VERSION&type=code) | Defines the version of the platform being used, concatenated with the platform identifier. | "IDF" IDF_VER |
| [`MICROPY_PLAT_DEV_MEM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PLAT_DEV_MEM&type=code) | Enables access to physical memory via /dev/mem on Linux systems. | (1) |
| [`MICROPY_PREVIEW_VERSION_2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PREVIEW_VERSION_2&type=code) | Enables in-progress or breaking changes slated for the 2.x release. | (0) |
| [`MICROPY_PROF_INSTR_DEBUG_PRINT_ENABLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PROF_INSTR_DEBUG_PRINT_ENABLE&type=code) | Enables debugging output for the settrace feature, not for production builds. | 0 |
| [`MICROPY_PYEXEC_COMPILE_ONLY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PYEXEC_COMPILE_ONLY&type=code) | Enables compile-only mode for executing scripts without running them. | (1) |
| [`MICROPY_PYEXEC_ENABLE_EXIT_CODE_HANDLING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PYEXEC_ENABLE_EXIT_CODE_HANDLING&type=code) | Enables handling of exit codes from sys.exit() calls. | (1) |
| [`MICROPY_PYEXEC_ENABLE_VM_ABORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PYEXEC_ENABLE_VM_ABORT&type=code) | Controls handling of abort behavior in the pyexec code. | (0) |
| [`MICROPY_PYSTACK_ALIGN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_PYSTACK_ALIGN&type=code) | Determines the byte alignment for memory allocated by the Python stack. | (8) |
| [`MICROPY_QSTR_BYTES_IN_HASH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_QSTR_BYTES_IN_HASH&type=code) | Determines the number of bytes allocated for storing qstr hashes, affecting memory usage and hash computation. | (2) |
| [`MICROPY_QSTR_BYTES_IN_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_QSTR_BYTES_IN_LEN&type=code) | Determines the number of bytes allocated for storing the length of qstrs, affecting maximum identifier length. | (1) |
| [`MICROPY_QSTR_EXTRA_POOL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_QSTR_EXTRA_POOL&type=code) | Defines an additional ROM pool for extra qstrs required by frozen code. | mp_qstr_frozen_const_pool |
| [`MICROPY_READER_POSIX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_READER_POSIX&type=code) | Enables the use of the POSIX file reader for importing files. | (1) |
| [`MICROPY_READER_VFS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_READER_VFS&type=code) | Enables the use of a virtual file system (VFS) reader for importing files. | (1) |
| [`MICROPY_READER_VFS_DEFAULT_BUFFER_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_READER_VFS_DEFAULT_BUFFER_SIZE&type=code) | Calculates the default buffer size for VFS readers based on garbage collection block size. | (2 * MICROPY_BYTES_PER_GC_BLOCK - offsetof(mp_reader_vfs_t, buf)) |
| [`MICROPY_READER_VFS_MAX_BUFFER_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_READER_VFS_MAX_BUFFER_SIZE&type=code) | Limits the maximum buffer size for VFS readers to 255 bytes. | (255) |
| [`MICROPY_READER_VFS_MIN_BUFFER_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_READER_VFS_MIN_BUFFER_SIZE&type=code) | Minimum buffer size for VFS reader based on GC block size and buffer offset. | (MICROPY_BYTES_PER_GC_BLOCK - offsetof(mp_reader_vfs_t, buf)) |
| [`MICROPY_READLINE_HISTORY_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_READLINE_HISTORY_SIZE&type=code) | Determines the maximum number of entries in the readline history. | (50) |
| [`MICROPY_REGISTERED_EXTENSIBLE_MODULES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_REGISTERED_EXTENSIBLE_MODULES&type=code) | Lists the extensible modules registered for the build. | \ |
| [`MICROPY_REGISTERED_MODULES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_REGISTERED_MODULES&type=code) | Lists all registered modules for the MicroPython build. | \ |
| [`MICROPY_REPL_AUTO_INDENT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_REPL_AUTO_INDENT&type=code) | Enables automatic indentation in the REPL when set to a specific ROM level. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_REPL_EMACS_EXTRA_WORDS_MOVE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_REPL_EMACS_EXTRA_WORDS_MOVE&type=code) | Enables extra key bindings for word movement and deletion in the REPL. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EVERYTHING) |
| [`MICROPY_REPL_EMACS_KEYS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_REPL_EMACS_KEYS&type=code) | Enables emacs-style keybindings for readline behavior in the REPL. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_REPL_EMACS_WORDS_MOVE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_REPL_EMACS_WORDS_MOVE&type=code) | Enables emacs-style word movement and kill commands in the REPL. | (1) |
| [`MICROPY_REPL_EVENT_DRIVEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_REPL_EVENT_DRIVEN&type=code) | Enables event-driven REPL functions when set to a non-zero value. | (0) |
| [`MICROPY_REPL_INFO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_REPL_INFO&type=code) | Enables debugging information display in the REPL when set to 1. | (0) |
| [`MICROPY_REPL_STDIN_BUFFER_MAX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_REPL_STDIN_BUFFER_MAX&type=code) | Sets the maximum number of bytes for the stdin buffer, limited to 64 for certain boards. | (64) |
| [`MICROPY_RV32_EXTENSIONS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_RV32_EXTENSIONS&type=code) | Determines the enabled RISC-V 32 extensions based on configuration. | \ |
| [`MICROPY_SAFE_BOOT_PIN_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SAFE_BOOT_PIN_NUM&type=code) | Defines the GPIO pin number used for safe boot functionality. | PIN_15      // GP22 |
| [`MICROPY_SAFE_BOOT_PORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SAFE_BOOT_PORT&type=code) | Defines the GPIO port used for safe boot functionality. | GPIOA2_BASE |
| [`MICROPY_SAFE_BOOT_PORT_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SAFE_BOOT_PORT_PIN&type=code) | Indicates the GPIO pin used for safe boot mode functionality. | GPIO_PIN_6 |
| [`MICROPY_SAFE_BOOT_PRCM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SAFE_BOOT_PRCM&type=code) | Identifies the peripheral clock for the safe boot pin. | PRCM_GPIOA2 |
| [`MICROPY_SCHEDULER_DEPTH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SCHEDULER_DEPTH&type=code) | Maximum number of entries allowed in the scheduler, typically a power of 2. | (4) |
| [`MICROPY_SCHEDULER_STATIC_NODES`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SCHEDULER_STATIC_NODES&type=code) | Enables support for scheduling static nodes with C callbacks in the scheduler. | (0) |
| [`MICROPY_SCHED_HOOK_SCHEDULED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SCHED_HOOK_SCHEDULED&type=code) | Triggers the mp_hal_signal_event function when a function is scheduled on the scheduler queue. | mp_hal_signal_event() |
| [`MICROPY_SELECT_REMAINING_TIME`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SELECT_REMAINING_TIME&type=code) | Enables behavior where select() updates the remaining timeout value when interrupted by a signal. | (1) |
| [`MICROPY_SOFT_TIMER_TICKS_MS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SOFT_TIMER_TICKS_MS&type=code) | Defines the millisecond tick counter for soft timers, typically set to a hardware timer variable. | uwTick |
| [`MICROPY_SPI_PINS_ARG_OPTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SPI_PINS_ARG_OPTS&type=code) | Configures the requirement for SPI pin arguments, defaulting to none for most boards. | 0 |
| [`MICROPY_SSL_MBEDTLS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SSL_MBEDTLS&type=code) | Enables the use of mbedTLS for SSL/TLS support. | (1) |
| [`MICROPY_STACKLESS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_STACKLESS&type=code) | Controls the use of the C stack for Python function calls, enabling stackless mode when set to 1. | (0) |
| [`MICROPY_STACKLESS_STRICT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_STACKLESS_STRICT&type=code) | Controls strict stackless behavior, affecting exception handling during deep recursion. | (0) |
| [`MICROPY_STACK_CHECK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_STACK_CHECK&type=code) | Enables checking of C stack usage to prevent overflow during function calls. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_STACK_CHECK_MARGIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_STACK_CHECK_MARGIN&type=code) | Defines the byte margin subtracted from the stack size for stack checks. | (1024) |
| [`MICROPY_STACK_SIZE_HARD_IRQ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_STACK_SIZE_HARD_IRQ&type=code) | Defines the size of the stack for hard IRQ handlers, checked instead of the main stack during hard callbacks. | (CONFIG_ISR_STACK_SIZE) |
| [`MICROPY_STDIO_UART`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_STDIO_UART&type=code) | Enables the use of UART for standard input/output. | 1 |
| [`MICROPY_STDIO_UART_BAUD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_STDIO_UART_BAUD&type=code) | Sets the baud rate for UART standard input/output. | 115200 |
| [`MICROPY_STREAMS_NON_BLOCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_STREAMS_NON_BLOCK&type=code) | Enables support for POSIX-semantics non-blocking streams. | (MICROPY_CONFIG_ROM_LEVEL_AT_LEAST_EXTRA_FEATURES) |
| [`MICROPY_STREAMS_POSIX_API`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_STREAMS_POSIX_API&type=code) | Enables POSIX-like stream functions for compatibility with C libraries requiring read/write/lseek/fsync. | (1) |
| [`MICROPY_SYS_LED_GPIO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SYS_LED_GPIO&type=code) | Defines the GPIO pin used for the system LED. | pin_GP25 |
| [`MICROPY_SYS_LED_PIN_NUM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SYS_LED_PIN_NUM&type=code) | Defines the pin number for the system LED, set to PIN_21 (GP25) on the WIPY board. | PIN_21      // GP25   (SOP2) |
| [`MICROPY_SYS_LED_PORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SYS_LED_PORT&type=code) | Defines the GPIO port for the system LED. | GPIOA1_BASE |
| [`MICROPY_SYS_LED_PORT_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SYS_LED_PORT_PIN&type=code) | Defines the GPIO pin used for the system LED. | GPIO_PIN_1 |
| [`MICROPY_SYS_LED_PRCM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_SYS_LED_PRCM&type=code) | Defines the peripheral clock for the system LED. | PRCM_GPIOA1 |
| [`MICROPY_TASK_PRIORITY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_TASK_PRIORITY&type=code) | Sets the priority level for the MicroPython task. | (2) |
| [`MICROPY_TASK_STACK_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_TASK_STACK_LEN&type=code) | Calculates the number of stack elements for the MicroPython task based on stack size and element size. | (MICROPY_TASK_STACK_SIZE / sizeof(StackType_t)) |
| [`MICROPY_TASK_STACK_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_TASK_STACK_SIZE&type=code) | Defines the stack size for tasks in bytes, calculated as 6KB plus 512 bytes. | ((6 * 1024) + 512) // in bytes |
| [`MICROPY_TIMESTAMP_IMPL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_TIMESTAMP_IMPL&type=code) | Determines the type used for timestamps, allowing for compatibility with various epoch representations. | (MICROPY_TIMESTAMP_IMPL_TIME_T) |
| [`MICROPY_TIMESTAMP_IMPL_LONG_LONG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_TIMESTAMP_IMPL_LONG_LONG&type=code) | Represents timestamps using a long long type. | (0) |
| [`MICROPY_TIMESTAMP_IMPL_TIME_T`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_TIMESTAMP_IMPL_TIME_T&type=code) | Uses time_t type for representing timestamps. | (2) |
| [`MICROPY_TIMESTAMP_IMPL_UINT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_TIMESTAMP_IMPL_UINT&type=code) | Defines the use of unsigned integer type for representing timestamps. | (1) |
| [`MICROPY_TIME_SUPPORT_Y1969_AND_BEFORE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_TIME_SUPPORT_Y1969_AND_BEFORE&type=code) | Enables support for date and time functions before the year 1970. | (1) |
| [`MICROPY_TIME_SUPPORT_Y2100_AND_BEYOND`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_TIME_SUPPORT_Y2100_AND_BEYOND&type=code) | Enables support for date and time functions beyond the year 2099. | (MICROPY_TIME_SUPPORT_Y1969_AND_BEFORE) |
| [`MICROPY_TRACKED_ALLOC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_TRACKED_ALLOC&type=code) | Enables tracking of memory allocations for garbage collection when using SSL or Bluetooth features. | (MICROPY_SSL_MBEDTLS \|\| MICROPY_BLUETOOTH_BTSTACK) |
| [`MICROPY_TRACKED_ALLOC_STORE_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_TRACKED_ALLOC_STORE_SIZE&type=code) | Determines if the size of tracked allocations is stored based on garbage collection settings. | (!MICROPY_ENABLE_GC) |
| [`MICROPY_UART_PINS_ARG_OPTS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_UART_PINS_ARG_OPTS&type=code) | Indicates that UART pin arguments are required when no default pins are defined. | MP_ARG_REQUIRED |
| [`MICROPY_UNIX_MACHINE_IDLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_UNIX_MACHINE_IDLE&type=code) | Invokes sched_yield() to allow other threads to run during idle state. | sched_yield(); |
| [`MICROPY_USDHC1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_USDHC1&type=code) | Defines pin configurations for USDHC1 interface. | \ |
| [`MICROPY_USE_GCC_MUL_OVERFLOW_INTRINSIC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_USE_GCC_MUL_OVERFLOW_INTRINSIC&type=code) | Enables the use of GCC built-in multiplication overflow detection for ARM architectures with Thumb ISA version 2 or higher. | (__ARM_ARCH_ISA_THUMB >= 2) |
| [`MICROPY_USE_INTERNAL_ERRNO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_USE_INTERNAL_ERRNO&type=code) | Controls the use of internal error numbers instead of system-provided ones. | (0) |
| [`MICROPY_USE_INTERNAL_PRINTF`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_USE_INTERNAL_PRINTF&type=code) | Controls the use of internal printf functions; set to 0 for ESP32 SDK compatibility. | (0) // ESP32 SDK requires its own printf |
| [`MICROPY_USE_READLINE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_USE_READLINE&type=code) | Enables the use of MicroPython's readline functionality for input handling. | (1) |
| [`MICROPY_USE_READLINE_HISTORY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_USE_READLINE_HISTORY&type=code) | Enables the use of readline history functionality for command line input. | (1) |
| [`MICROPY_VARIANT_ENABLE_JS_HOOK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VARIANT_ENABLE_JS_HOOK&type=code) | Enables periodic calls to mp_js_hook() for checking interrupt characters on stdin. | (0) |
| [`MICROPY_VERSION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VERSION&type=code) | Combined version number as a 32-bit integer for version comparison. | MICROPY_MAKE_VERSION(MICROPY_VERSION_MAJOR, MICROPY_VERSION_MINOR, MICROPY_VERSION_MICRO) |
| [`MICROPY_VERSION_MAJOR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VERSION_MAJOR&type=code) | Major version number of MicroPython, used in versioning and fallback mechanisms. | 1 |
| [`MICROPY_VERSION_MICRO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VERSION_MICRO&type=code) | Defines the micro version number of MicroPython, used in versioning. | 0 |
| [`MICROPY_VERSION_MINOR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VERSION_MINOR&type=code) | Indicates the minor version number of MicroPython, currently set to 27. | 27 |
| [`MICROPY_VERSION_PRERELEASE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VERSION_PRERELEASE&type=code) | Indicates if the build is a prerelease version, with 1 for prerelease and 0 for stable release. | 1 |
| [`MICROPY_VERSION_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VERSION_STRING&type=code) | Combines version components into a string, appending '-preview' if in prerelease. | MICROPY_VERSION_STRING_BASE "-preview" |
| [`MICROPY_VERSION_STRING_BASE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VERSION_STRING_BASE&type=code) | Generates a string representation of the version based on major, minor, and micro version numbers. | \ |
| [`MICROPY_VFS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VFS&type=code) | Enables the Virtual File System (VFS) support. | (CORE_FEAT) |
| [`MICROPY_VFS_FAT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VFS_FAT&type=code) | Enables support for mounting FAT filesystems within the virtual filesystem. | (0) |
| [`MICROPY_VFS_LFS1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VFS_LFS1&type=code) | Enables support for the LittleFS v1 filesystem in the virtual file system. | (0) |
| [`MICROPY_VFS_LFS2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VFS_LFS2&type=code) | Enables support for the LittleFS v2 filesystem within the Virtual File System (VFS). Examples: make BOARD=PCA10040 MICROPY_VFS_LFS2=1, make BOARD=PCA10056 MICROPY_VFS_LFS2=1. | (0) |
| [`MICROPY_VFS_POSIX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VFS_POSIX&type=code) | Enables the POSIX virtual filesystem support. | (MICROPY_VFS) |
| [`MICROPY_VFS_POSIX_WRITABLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VFS_POSIX_WRITABLE&type=code) | Enables writable support for POSIX filesystems. | (1) |
| [`MICROPY_VFS_ROM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VFS_ROM&type=code) | Enables support for a ROM filesystem, allowing access to files stored in ROM. | (MICROPY_HW_ROMFS_ENABLE_INTERNAL_FLASH \|\| MICROPY_HW_ROMFS_ENABLE_EXTERNAL_QSPI \|\| MICROPY_HW_ROMFS_ENABLE_EXTERNAL_XSPI) |
| [`MICROPY_VFS_ROM_IOCTL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VFS_ROM_IOCTL&type=code) | Enables the mp_vfs_rom_ioctl function for querying and modifying read-only memory areas. | (MICROPY_VFS_ROM) |
| [`MICROPY_VFS_WRITABLE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VFS_WRITABLE&type=code) | Enables support for writable filesystems, allowing operations like mkdir, remove, and rename. | (1) |
| [`MICROPY_VM_HOOK_COUNT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VM_HOOK_COUNT&type=code) | Sets the count for virtual machine hooks to trigger events. | (10) |
| [`MICROPY_VM_HOOK_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VM_HOOK_INIT&type=code) | Initializes a variable for VM hook divisor with a predefined count. | static uint vm_hook_divisor = MICROPY_VM_HOOK_COUNT; |
| [`MICROPY_VM_HOOK_LOOP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VM_HOOK_LOOP&type=code) | Executes a polling hook during the VM opcode loop. | MICROPY_VM_HOOK_POLL |
| [`MICROPY_VM_HOOK_POLL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VM_HOOK_POLL&type=code) | Triggers an internal event hook when a counter reaches zero. | if (--vm_hook_divisor == 0) { \ |
| [`MICROPY_VM_HOOK_RETURN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_VM_HOOK_RETURN&type=code) | Executes a polling hook for the VM just before the return opcode is completed. | MICROPY_VM_HOOK_POLL |
| [`MICROPY_WARNINGS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_WARNINGS&type=code) | Enables warning messages during compilation and execution. | (1) |
| [`MICROPY_WARNINGS_CATEGORY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MICROPY_WARNINGS_CATEGORY&type=code) | Controls the support for warning categories during runtime. | (0) |