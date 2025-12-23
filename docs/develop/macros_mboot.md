

### MBOOT_CLK

This configuration group manages the clock settings for various buses and the CPU frequency in a system. It allows for the adjustment of clock dividers and PLL parameters to optimize performance and speed up operations, such as updates from SPI flash.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MBOOT_CLK_AHB_DIV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_CLK_AHB_DIV&type=code) | Sets the AHB clock divider for the microcontroller. | (RCC_SYSCLK_DIV1) |
| [`MBOOT_CLK_APB1_DIV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_CLK_APB1_DIV&type=code) | Defines the clock divider for the APB1 bus. | (RCC_HCLK_DIV4) |
| [`MBOOT_CLK_APB2_DIV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_CLK_APB2_DIV&type=code) | Defines the clock divider for the APB2 bus. | (RCC_HCLK_DIV2) |
| [`MBOOT_CLK_APB3_DIV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_CLK_APB3_DIV&type=code) | Defines the clock divider for APB3 peripheral bus. | (RCC_APB3_DIV2) |
| [`MBOOT_CLK_APB4_DIV`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_CLK_APB4_DIV&type=code) | Defines the clock divider for the APB4 bus. | (RCC_APB4_DIV2) |
| [`MBOOT_CLK_PLLM`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_CLK_PLLM&type=code) | Calculates the PLLM value for configuring the CPU frequency to 96MHz. | (MICROPY_HW_CLK_VALUE / 1000000) |
| [`MBOOT_CLK_PLLN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_CLK_PLLN&type=code) | Sets the value for the PLLN parameter in the clock configuration, influencing the CPU frequency. | (192) |
| [`MBOOT_CLK_PLLP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_CLK_PLLP&type=code) | Calculates the PLLP value based on PLLN and core clock frequency. | (MBOOT_CLK_PLLN / (CORE_PLL_FREQ / 1000000)) |
| [`MBOOT_CLK_PLLQ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_CLK_PLLQ&type=code) | Sets the division factor for the PLL output clock Q. | (4) |
| [`MBOOT_CLK_PLLR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_CLK_PLLR&type=code) | Sets the divisor for the PLLR clock output. | (2) |


### MBOOT_SPIFLASH

This configuration group manages the settings and parameters for accessing and utilizing external QSPI flash memory in the Mboot bootloader. It includes specifications for memory layout, communication pins, and operational characteristics, enabling efficient interaction with the flash storage.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MBOOT_SPIFLASH_ADDR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH_ADDR&type=code) | Address for Mboot to access external QSPI flash. | (0x90000000) |
| [`MBOOT_SPIFLASH_BYTE_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH_BYTE_SIZE&type=code) | Calculates the size of the SPI flash memory based on the logarithmic memory size parameter. | (1 << MICROPY_BOARD_SPIFLASH_CHIP_PARAMS0->memory_size_bytes_log2) |
| [`MBOOT_SPIFLASH_CONFIG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH_CONFIG&type=code) | Pointer to the SPI flash configuration structure for external flash initialization. | (&board_mboot_spiflash_config) |
| [`MBOOT_SPIFLASH_CS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH_CS&type=code) | Defines the chip select pin for the SPI flash memory. | (pyb_pin_XSPIM_P2_CS) |
| [`MBOOT_SPIFLASH_ERASE_BLOCKS_PER_PAGE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH_ERASE_BLOCKS_PER_PAGE&type=code) | Determines the number of erase blocks per page for SPI flash memory. | (128 / 4) // 128k page, 4k erase block |
| [`MBOOT_SPIFLASH_LAYOUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH_LAYOUT&type=code) | Determines the layout of the SPI flash based on the memory size log2 value. | (MICROPY_BOARD_SPIFLASH_CHIP_PARAMS0->memory_size_bytes_log2 == 21 ? "/0x80000000/512*4Kg" : "/0x80000000/2048*4Kg") |
| [`MBOOT_SPIFLASH_LAYOUT_DYNAMIC_MAX_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH_LAYOUT_DYNAMIC_MAX_LEN&type=code) | Defines the maximum length for the dynamic layout of Mboot SPI flash #1. | (20) |
| [`MBOOT_SPIFLASH_MISO`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH_MISO&type=code) | Defines the MISO pin for SPI flash communication. | (pyb_pin_XSPIM_P2_IO1) |
| [`MBOOT_SPIFLASH_MOSI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH_MOSI&type=code) | Defines the MOSI pin for SPI flash communication. | (pyb_pin_XSPIM_P2_IO0) |
| [`MBOOT_SPIFLASH_SCK`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH_SCK&type=code) | Defines the SCK pin for the SPI flash interface. | (pyb_pin_XSPIM_P2_SCK) |
| [`MBOOT_SPIFLASH_SPIFLASH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH_SPIFLASH&type=code) | Pointer to the SPI flash device structure for bootloader operations. | (&board_mboot_spiflash) |


### MBOOT_MISC

This collection of macros configures various aspects of the bootloader functionality, including hardware initialization, error handling, and system state management. It allows for customization of boot processes, error messaging, and peripheral settings, ensuring a flexible and robust bootloader environment.

| Macro | Description | Sample value(s) |
|------|-------------|-----------------|
| [`MBOOT_ADDRESS_SPACE_64BIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_ADDRESS_SPACE_64BIT&type=code) | Enables 64-bit address space for mboot, affecting address type and firmware loading. | (0) |
| [`MBOOT_BOARD_CLEANUP`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_BOARD_CLEANUP&type=code) | Calls the board-specific cleanup function during the bootloader process. | board_mboot_cleanup |
| [`MBOOT_BOARD_GET_RESET_MODE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_BOARD_GET_RESET_MODE&type=code) | Retrieves the reset mode for the board during the bootloader process. | board_mboot_get_reset_mode |
| [`MBOOT_BOARD_LED_INIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_BOARD_LED_INIT&type=code) | Calls a custom LED initialization function for the board. | board_mboot_led_init |
| [`MBOOT_BOARD_LED_STATE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_BOARD_LED_STATE&type=code) | Custom function for controlling the LED state on the board. | board_mboot_led_state |
| [`MBOOT_BOARD_STATE_CHANGE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_BOARD_STATE_CHANGE&type=code) | Handles state changes for the bootloader, utilizing a default UI if enabled. | board_mboot_state_change |
| [`MBOOT_BOOTPIN_ACTIVE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_BOOTPIN_ACTIVE&type=code) | Indicates the active state of the boot pin for entering the bootloader. | (0) |
| [`MBOOT_BOOTPIN_PIN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_BOOTPIN_PIN&type=code) | Configures the pin used to trigger entry into the bootloader. | (pin_A10) |
| [`MBOOT_BOOTPIN_PULL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_BOOTPIN_PULL&type=code) | Configures the pull-up/pull-down resistor setting for the boot pin. | (MP_HAL_PIN_PULL_NONE) |
| [`MBOOT_ENABLE_DEFAULT_UI`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_ENABLE_DEFAULT_UI&type=code) | Enables the default user interface code if at least one LED is configured. | (1) |
| [`MBOOT_ERRNO_VFS_LFS_MOUNT_FAILED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_ERRNO_VFS_LFS_MOUNT_FAILED&type=code) | Error code for failed mounting of LFS1 or LFS2 in the virtual file system. | MBOOT_ERRNO_VFS_LFS1_MOUNT_FAILED |
| [`MBOOT_ERRNO_VFS_LFS_OPEN_FAILED`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_ERRNO_VFS_LFS_OPEN_FAILED&type=code) | Error code indicating failure to open a file in the LFS (LittleFS) virtual filesystem. | MBOOT_ERRNO_VFS_LFS1_OPEN_FAILED |
| [`MBOOT_ERROR_STR_INVALID_ADDRESS`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_ERROR_STR_INVALID_ADDRESS&type=code) | Error message indicating an address is out of range. | "Address out of range" |
| [`MBOOT_ERROR_STR_INVALID_ADDRESS_IDX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_ERROR_STR_INVALID_ADDRESS_IDX&type=code) | Index for the error message indicating an invalid address in DFU operations. | 0x11 |
| [`MBOOT_ERROR_STR_INVALID_READ`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_ERROR_STR_INVALID_READ&type=code) | Indicates that read operations are not supported on an encrypted bootloader. | "Read support disabled on encrypted bootloader" |
| [`MBOOT_ERROR_STR_INVALID_READ_IDX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_ERROR_STR_INVALID_READ_IDX&type=code) | Error code indicating read support is disabled on an encrypted bootloader. | 0x13 |
| [`MBOOT_ERROR_STR_INVALID_SIG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_ERROR_STR_INVALID_SIG&type=code) | Error message indicating an invalid signature in a file. | "Invalid signature in file" |
| [`MBOOT_ERROR_STR_INVALID_SIG_IDX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_ERROR_STR_INVALID_SIG_IDX&type=code) | Error index for an invalid signature in the firmware file. | 0x12 |
| [`MBOOT_ERROR_STR_OVERWRITE_BOOTLOADER`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_ERROR_STR_OVERWRITE_BOOTLOADER&type=code) | Error message indicating that the bootloader cannot be overwritten. | "Can't overwrite mboot" |
| [`MBOOT_ERROR_STR_OVERWRITE_BOOTLOADER_IDX`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_ERROR_STR_OVERWRITE_BOOTLOADER_IDX&type=code) | Index for the error message indicating that overwriting the bootloader is not allowed. | 0x10 |
| [`MBOOT_FLASH_LATENCY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_FLASH_LATENCY&type=code) | Configures the flash memory access latency for the bootloader. | FLASH_LATENCY_3 |
| [`MBOOT_FSLOAD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_FSLOAD&type=code) | Enables loading firmware from a filesystem. | (0) |
| [`MBOOT_FSLOAD_DEFAULT_BLOCK_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_FSLOAD_DEFAULT_BLOCK_SIZE&type=code) | Default block size for mount operations, set to 4096 bytes. | (4096) |
| [`MBOOT_I2C_ALTFUNC`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_I2C_ALTFUNC&type=code) | Defines the alternate function number for I2C pins. | (4) |
| [`MBOOT_I2C_PERIPH_ID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_I2C_PERIPH_ID&type=code) | Identifies the I2C peripheral used for bootloader communication. | 1 |
| [`MBOOT_I2C_SCL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_I2C_SCL&type=code) | Defines the I2C SCL pin for the bootloader configuration. | (pin_B10) |
| [`MBOOT_I2C_SDA`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_I2C_SDA&type=code) | Defines the I2C data line pin for the bootloader. | (pin_B11) |
| [`MBOOT_INITIAL_R0_KEY`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_INITIAL_R0_KEY&type=code) | Value used in initial_r0 for programmatic entry into the mboot. | (0x70ad0000) |
| [`MBOOT_INITIAL_R0_KEY_FSLOAD`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_INITIAL_R0_KEY_FSLOAD&type=code) | Value used to indicate the bootloader should enter filesystem load mode. | (MBOOT_INITIAL_R0_KEY \| 0x80) |
| [`MBOOT_LEAVE_BOOTLOADER_VIA_RESET`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_LEAVE_BOOTLOADER_VIA_RESET&type=code) | Determines whether the bootloader exits via a reset or a direct jump to the application. | (1) |
| [`MBOOT_LED1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_LED1&type=code) | Defines the identifier for the first LED, used in bootloader UI. | 0 |
| [`MBOOT_LED2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_LED2&type=code) | Represents the identifier for the second LED in the bootloader. | 1 |
| [`MBOOT_LED3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_LED3&type=code) | Represents the identifier for the third LED in the bootloader. | 2 |
| [`MBOOT_LED_STATE_LED0`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_LED_STATE_LED0&type=code) | Represents the state of LED0 for use in the led_state_all() function, allowing multiple LED states to be combined. | (0x01) |
| [`MBOOT_LED_STATE_LED1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_LED_STATE_LED1&type=code) | Represents the state of LED1 in the bootloader's LED control. | (0x02) |
| [`MBOOT_LED_STATE_LED2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_LED_STATE_LED2&type=code) | Represents the state of LED2 with a value of 0x04. | (0x04) |
| [`MBOOT_LED_STATE_LED3`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_LED_STATE_LED3&type=code) | Represents the state of LED3 with a value of 0x08 for LED control. | (0x08) |
| [`MBOOT_PACK_DFU_CHUNK_BUF_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_PACK_DFU_CHUNK_BUF_SIZE&type=code) | Maximum size for the firmware payload buffer, combining chunk size and header bytes. | (MBOOT_PACK_CHUNKSIZE + hydro_secretbox_HEADERBYTES) |
| [`MBOOT_PACK_GZIP_BUFFER_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_PACK_GZIP_BUFFER_SIZE&type=code) | Sets the buffer size for decompressing gzip files during firmware updates. | (2048) |
| [`MBOOT_PACK_HEADER_VERSION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_PACK_HEADER_VERSION&type=code) | Indicates the current version of a packed DFU file. | (1) |
| [`MBOOT_PACK_HYDRO_CONTEXT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_PACK_HYDRO_CONTEXT&type=code) | Context string for signing and secretbox operations using libhydrogen. | "mbootenc" |
| [`MBOOT_SDCARD_ADDR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SDCARD_ADDR&type=code) | Defines the starting address for SD card memory mapping. | (0x100000000ULL) |
| [`MBOOT_SDCARD_BYTE_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SDCARD_BYTE_SIZE&type=code) | Defines the byte size of the SD card memory space. | (0x400000000ULL) |
| [`MBOOT_SPIFLASH2_ADDR`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH2_ADDR&type=code) | Address for the second external SPI flash device. | (0x90000000) |
| [`MBOOT_SPIFLASH2_BYTE_SIZE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH2_BYTE_SIZE&type=code) | Calculates the byte size of the second SPI flash based on its memory size logarithm. | (1 << MICROPY_BOARD_SPIFLASH_CHIP_PARAMS1->memory_size_bytes_log2) |
| [`MBOOT_SPIFLASH2_CONFIG`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH2_CONFIG&type=code) | Pointer to the configuration structure for the second SPI flash. | (&spiflash2_config) |
| [`MBOOT_SPIFLASH2_ERASE_BLOCKS_PER_PAGE`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH2_ERASE_BLOCKS_PER_PAGE&type=code) | Determines the number of erase blocks per page for the second SPI flash. | (32 / 4) |
| [`MBOOT_SPIFLASH2_LAYOUT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH2_LAYOUT&type=code) | Determines the layout of the second SPI flash based on its memory size. | (MICROPY_BOARD_SPIFLASH_CHIP_PARAMS1->memory_size_bytes_log2 == 21 ? "/0x90000000/512*4Kg" : "/0x90000000/2048*4Kg") |
| [`MBOOT_SPIFLASH2_LAYOUT_DYNAMIC_MAX_LEN`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH2_LAYOUT_DYNAMIC_MAX_LEN&type=code) | Defines the maximum length for the dynamic layout of Mboot SPI flash #2. | (20) |
| [`MBOOT_SPIFLASH2_SPIFLASH`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_SPIFLASH2_SPIFLASH&type=code) | Pointer to the second SPI flash device structure. | (&spi_bdev2.spiflash) |
| [`MBOOT_USBD_LANGID_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_USBD_LANGID_STRING&type=code) | Language ID for USB descriptors, set to 0x409 (English - United States). Examples: 0x409, 0x0409. | (0x409) |
| [`MBOOT_USBD_MANUFACTURER_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_USBD_MANUFACTURER_STRING&type=code) | Manufacturer string for USB device identification, set to 'MicroPython'. | "MicroPython" |
| [`MBOOT_USBD_PRODUCT_STRING`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_USBD_PRODUCT_STRING&type=code) | Defines the USB product string for the bootloader. | "Pyboard DFU" |
| [`MBOOT_USB_AUTODETECT_PORT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_USB_AUTODETECT_PORT&type=code) | Enables automatic detection of USB ports during bootloader operation. | (1) |
| [`MBOOT_USB_PID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_USB_PID&type=code) | Defines the USB Product ID for the bootloader. | BOOTLOADER_DFU_USB_PID |
| [`MBOOT_USB_VID`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_USB_VID&type=code) | Defines the USB Vendor ID for the bootloader. | BOOTLOADER_DFU_USB_VID |
| [`MBOOT_VERSION`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VERSION&type=code) | Defines the version string for the mboot, incorporating the MICROPY_GIT_TAG. | "mboot-" MICROPY_GIT_TAG |
| [`MBOOT_VERSION_64BIT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VERSION_64BIT&type=code) | Defines the bootloader version for 64-bit address space with I2C support. | MBOOT_VERSION_I2C ".64" |
| [`MBOOT_VERSION_FAT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VERSION_FAT&type=code) | Defines the version string for FAT file system support, appending '.fat' to the 64-bit version. | MBOOT_VERSION_64BIT ".fat" |
| [`MBOOT_VERSION_FINAL`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VERSION_FINAL&type=code) | Final version string for the bootloader, derived from MBOOT_VERSION_RAW. | MBOOT_VERSION_RAW |
| [`MBOOT_VERSION_I2C`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VERSION_I2C&type=code) | Combines USB version with '.i2c' if I2C support is enabled. | MBOOT_VERSION_USB ".i2c" |
| [`MBOOT_VERSION_LFS1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VERSION_LFS1&type=code) | Combines MBOOT_VERSION_FAT with the suffix '.lfs1' if LFS1 is enabled. | MBOOT_VERSION_FAT ".lfs1" |
| [`MBOOT_VERSION_LFS2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VERSION_LFS2&type=code) | Combines MBOOT_VERSION_LFS1 with the suffix '.lfs2' if MBOOT_VFS_LFS2 is enabled. | MBOOT_VERSION_LFS1 ".lfs2" |
| [`MBOOT_VERSION_RAW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VERSION_RAW&type=code) | Combines MBOOT_VERSION_LFS2 with the suffix '.raw' if MBOOT_VFS_RAW is enabled. | MBOOT_VERSION_LFS2 ".raw" |
| [`MBOOT_VERSION_USB`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VERSION_USB&type=code) | Appends '+usb' to the MBOOT version string, indicating USB support. | MBOOT_VERSION "+usb"  // USB is always included |
| [`MBOOT_VFS_FAT`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VFS_FAT&type=code) | Enables support for FAT filesystems in the bootloader. | (0) |
| [`MBOOT_VFS_LFS1`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VFS_LFS1&type=code) | Enables support for Littlefs v1 filesystems. | (0) |
| [`MBOOT_VFS_LFS2`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VFS_LFS2&type=code) | Enables support for Littlefs v2 filesystems. | (0) |
| [`MBOOT_VFS_RAW`](https://github.com/search?q=repo%3Amicropython%2Fmicropython%20MBOOT_VFS_RAW&type=code) | Enables support for raw filesystems in the bootloader. | (MBOOT_FSLOAD) |