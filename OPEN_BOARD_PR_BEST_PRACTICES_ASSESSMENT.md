# Open Board PR Assessment Against Best Practices

Generated from currently open PRs labeled `board-definition` in `micropython/micropython`.

Scoring model:
- MUST score: 5 checks (M1-M5), each 2 points, total 10
- Best-practice bonus: 5 checks, each 1 point, total 5
- Total: /15

**MUST criteria (M1–M5):**

| | Criterion | Description |
|---|---|---|
| M1 | `board.json` | Board metadata file present with name, id, vendor, and machine fields |
| M2 | Config files | Both `mpconfigboard.h` and `mpconfigboard.cmake` (or `.mk`) present |
| M3 | `pins.csv` | Pin mapping file present (where applicable to the port) |
| M4 | Testing evidence | PR description includes hardware test results or flash/run evidence |
| M5 | Correct directory | Board files placed under the correct `ports/<port>/boards/<BOARD_NAME>/` path |

## Summary Table

| PR | Port | Board/Title | M1 | M2 | M3 | M4 | M5 | MUST Pass | Score (/15) |
|---|---|---|---|---|---|---|---|---|---|
| [#19026](https://github.com/micropython/micropython/pull/19026) | esp32 | esp32/boards: Add Pycom LoPy and LoPy4 board definitions with SX127x LoRa driver | Y | Y | Y | Y | Y | Yes | 14 |
| [#19012](https://github.com/micropython/micropython/pull/19012) | stm32 | stm32/boards/: Add  LCKFB_SKYSTAR_STM32F407VET6 boards. | Y | Y | Y | Y | Y | Yes | 11 |
| [#18977](https://github.com/micropython/micropython/pull/18977) | esp32 | Mch2022 | Y | Y | N | Y | Y | No | 9 |
| [#18940](https://github.com/micropython/micropython/pull/18940) | zephyr | `ports/zephyr: Add board config for Arduino UNO Q.` | N | N | N | Y | N | No | 3 |
| [#18871](https://github.com/micropython/micropython/pull/18871) | stm32 | Add GARATRONIC_PYMATE_CORE && GARATRONIC_PYMATE_16ADI16DO support | Y | Y | Y | N | Y | No | 9 |
| [#18829](https://github.com/micropython/micropython/pull/18829) | esp32 | esp32/boards: Add LILYGO T3-S3 board definition | Y | Y | Y | Y | Y | Yes | 12 |
| [#18303](https://github.com/micropython/micropython/pull/18303) | stm32 | stm32: Add STM32H747I-DISCO board | Y | Y | Y | Y | Y | Yes | 13 |
| [#18090](https://github.com/micropython/micropython/pull/18090) | rp2 | rp2: boards: Add Soldered NULA RP2350 Board Definition | Y | Y | Y | Y | Y | Yes | 12 |
| [#18064](https://github.com/micropython/micropython/pull/18064) | rp2 | rp2: boards: Add W5100S-EVB-Pico2 board definition. | Y | Y | Y | Y | Y | Yes | 12 |
| [#18035](https://github.com/micropython/micropython/pull/18035) | ports | ports/rp2/boards: Add WIZnet-EVB-boards and wiznet6k submodule | Y | Y | Y | Y | Y | Yes | 12 |
| [#17857](https://github.com/micropython/micropython/pull/17857) | rp2 | adding support for the W55RP20_EVB_PICO. | Y | Y | Y | Y | Y | Yes | 12 |
| [#17590](https://github.com/micropython/micropython/pull/17590) | stm32 | stm32/boards: Add WeAct_H723VG board support. | Y | Y | Y | Y | Y | Yes | 12 |
| [#17001](https://github.com/micropython/micropython/pull/17001) | rp2 | rp2/boards/SOLDERPARTY_RP2350_STAMP_XL: Add new Solder Party board. | Y | Y | Y | Y | Y | Yes | 12 |
| [#16409](https://github.com/micropython/micropython/pull/16409) | renesas-ra | renesas-ra/boards/WEACT_RA4M1_CORE: Add board profile. | Y | Y | Y | Y | Y | Yes | 12 |
| [#16407](https://github.com/micropython/micropython/pull/16407) | ports | ports/stm32/board/MPY_v11: Add new board MPY_v11 and acceleration IC. | Y | Y | Y | Y | Y | Yes | 13 |
| [#16325](https://github.com/micropython/micropython/pull/16325) | esp32 | add new board: ESP32_GENERIC_S3_N16R8_CAMERA | Y | Y | N | Y | Y | No | 10 |
| [#16124](https://github.com/micropython/micropython/pull/16124) | ports | ports/esp32/boards: Add WAVESHARE_ESP32_S3_PICO board configuration. | Y | Y | N | N | Y | No | 8 |
| [#15889](https://github.com/micropython/micropython/pull/15889) | samd | ports: adafruit grand central board support | Y | Y | Y | Y | Y | Yes | 11 |
| [#15516](https://github.com/micropython/micropython/pull/15516) | stm32 | I have added new stm32 boards(NUCLEO_H753xx) | Y | Y | Y | Y | Y | Yes | 12 |
| [#15482](https://github.com/micropython/micropython/pull/15482) | ports | ports/nrf/boards/SUPERMINI_NRF52840 board definition + machine_bitstream. | Y | Y | Y | Y | Y | Yes | 12 |
| [#15443](https://github.com/micropython/micropython/pull/15443) | ports | ports/rp2/boards: Add ARCHI board by Newsan. | Y | Y | Y | N | Y | No | 8 |
| [#13361](https://github.com/micropython/micropython/pull/13361) | esp32 | esp32/boards: Add board definition for WalnutPi PicoW. | Y | Y | N | N | Y | No | 7 |
| [#13204](https://github.com/micropython/micropython/pull/13204) | ports | ports/esp32/boards: Add uPesy EDU ESP32 board. | Y | Y | Y | N | Y | No | 10 |
| [#12749](https://github.com/micropython/micropython/pull/12749) | ports | ports/rp2/boards/W5100S_EVB_PICO/mpconfigboard.cmake: Set default mode to HardWired | N | N | N | N | Y | No | 2 |
| [#12676](https://github.com/micropython/micropython/pull/12676) | stm32 | stm32/boards/ARDUINO_PORTENTA_H7: Update pin definitions. | N | N | Y | N | Y | No | 4 |
| [#12642](https://github.com/micropython/micropython/pull/12642) | unknown | samd: Add board definition for Sparkfun SAMD51 MicroMod | Y | Y | Y | N | Y | No | 8 |
| [#12319](https://github.com/micropython/micropython/pull/12319) | rp2 | Board Definition Added for Pi-Plates MICROpi | Y | Y | Y | N | Y | No | 8 |
| [#12042](https://github.com/micropython/micropython/pull/12042) | esp32 | esp32/boards: Add support for XIAO ESP32S3/C3 boards. | Y | Y | N | N | Y | No | 7 |
| [#11398](https://github.com/micropython/micropython/pull/11398) | stm32 | NUCLEO-H7A3ZI-Q | N | Y | Y | N | Y | No | 6 |
| [#10752](https://github.com/micropython/micropython/pull/10752) | ports | ports/renesas-ra/boards/VK-RA6M3: Another New Board. | Y | Y | Y | N | Y | No | 10 |
| [#10665](https://github.com/micropython/micropython/pull/10665) | rp2 | rp2/boards/VCC_GND_RP2040: add VCC_GND_RP2040 with multiple variants. | Y | Y | Y | N | Y | No | 10 |
| [#10595](https://github.com/micropython/micropython/pull/10595) | ports | ports/renesas-ra/boards/VK-RA4W1: New board. | Y | Y | Y | N | Y | No | 9 |
| [#9859](https://github.com/micropython/micropython/pull/9859) | ports | ports/rp2/boards/ADAFRUIT_KB2040: Add Adafruit KB2040 board. | Y | Y | N | N | Y | No | 6 |
| [#9367](https://github.com/micropython/micropython/pull/9367) | stm32 | SMT32G4: Add USB, QPSI and AEMICS Board PYglet | Y | Y | Y | N | Y | No | 8 |
| [#9177](https://github.com/micropython/micropython/pull/9177) | esp32 | esp32/boards: Add LOLIN S3 ESP32-S3 based board. | Y | Y | N | N | Y | No | 7 |
| [#8822](https://github.com/micropython/micropython/pull/8822) | ports | ports/esp32/boards: Add supoprt to Franzininho WiFi WROVER(SPIRAM). | Y | Y | N | N | Y | No | 7 |
| [#8801](https://github.com/micropython/micropython/pull/8801) | esp32 | esp32: Add supoprt to Franzininho WiFi an ESP32-S2 based board | Y | Y | N | N | Y | No | 7 |
| [#7604](https://github.com/micropython/micropython/pull/7604) | rp2 | rp2/boards/PICO: Add USB VID/PID. | N | N | N | N | Y | No | 2 |
| [#7580](https://github.com/micropython/micropython/pull/7580) | rp2 | rp2/boards: Add Adafruit Trinkey QT2040. | N | Y | N | N | Y | No | 4 |
| [#7579](https://github.com/micropython/micropython/pull/7579) | rp2 | rp2/boards: Add Seeed XIAO RP2040. | N | Y | N | N | Y | No | 4 |
| [#7300](https://github.com/micropython/micropython/pull/7300) | esp32 | esp32/boards: Add board definition for ESP32-S2-Saola-1 | Y | Y | N | N | Y | No | 6 |
| [#7123](https://github.com/micropython/micropython/pull/7123) | stm32 | STM32L4: Support all STM32L4 MCUs with all features. Add NUCLEO boards. | N | Y | Y | N | Y | No | 6 |
| [#6677](https://github.com/micropython/micropython/pull/6677) | nrf | nrf/boards/waveshare_ble400: added board definition | N | Y | Y | N | Y | No | 6 |
| [#6488](https://github.com/micropython/micropython/pull/6488) | nrf | Add ports/nrf for BLYST840 nRF52840 Boards : | N | Y | Y | N | Y | No | 6 |

## Per-PR Notes

### [#19026](https://github.com/micropython/micropython/pull/19026) - esp32/boards: Add Pycom LoPy and LoPy4 board definitions with SX127x LoRa driver

Scope: ports/esp32/boards/PYCOM_LOPY, ports/esp32/boards/PYCOM_LOPY4, ports/esp32/boards/pycom_common. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py, variant configs, port tests. PR summary: Add board definitions, LoRa driver, LoRaWAN MAC, OTA support, and hardware validation for Pycom LoPy and LoPy4 — bringing these archived boards back to life on modern MicroPython. PYCOM_LOPY: ESP32 + 4MB flash + SX1272 LoRa (868 MHz). This PR currently meets the minimum MUST criteria. Notable strengths: manifest.py included, variant configs included, tests added under tests/ports, detailed PR description.

### [#19012](https://github.com/micropython/micropython/pull/19012) - stm32/boards/: Add  LCKFB_SKYSTAR_STM32F407VET6 boards.

Scope: ports/stm32/boards/LCKFB_SKYSTAR_STM32F407VET6. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv. PR summary: Add LCKFB_SKYSTAR_STM32F407VET6 boards.. This PR currently meets the minimum MUST criteria. Notable strengths: detailed PR description.

### [#18977](https://github.com/micropython/micropython/pull/18977) - Mch2022

Scope: ports/esp32/boards/mch2022. Key files detected: board.json, mpconfigboard.h, board build config, board docs. PR summary: Add support for the MCH2022 badge. This PR does not yet meet the minimum MUST criteria. Key gaps: pins.csv. Notable strengths: detailed PR description.

### [#18940](https://github.com/micropython/micropython/pull/18940) - `ports/zephyr: Add board config for Arduino UNO Q.`

Scope: no board directory detected from patch. PR summary: Add board configuration files for the Arduino UNO Q, enabling arduino_uno_q.overlay: Redirects zephyr,console from &usart1 Adds a 256 KB storage_partition at 0xF0000 for littlefs /flash arduino_uno_q.conf:. This PR does not yet meet the minimum MUST criteria. Key gaps: board.json, mpconfigboard.h/mpconfigboard.cmake|mk, pins.csv, board-path file changes. Notable strengths: detailed PR description.

### [#18871](https://github.com/micropython/micropython/pull/18871) - Add GARATRONIC_PYMATE_CORE && GARATRONIC_PYMATE_16ADI16DO support

Scope: ports/stm32/boards/GARATRONIC_PYMATE_16ADI16DO, ports/stm32/boards/GARATRONIC_PYMATE_CORE. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py. PR summary: Add two new PYMATEIO PLC boards, STM32 powered. See www.pymate.io. This PR does not yet meet the minimum MUST criteria. Key gaps: testing evidence in PR body. Notable strengths: manifest.py included.

### [#18829](https://github.com/micropython/micropython/pull/18829) - esp32/boards: Add LILYGO T3-S3 board definition

Scope: ports/esp32/boards/LILYGO_T3_S3. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py, board docs. PR summary: ESP32-S3FH4R2 with SX1262 LoRa (HPD17A), SSD1306 OLED, SD card. Freezes lora-sx126x and ssd1306 from micropython-lib.. This PR currently meets the minimum MUST criteria. Notable strengths: manifest.py included, board docs included.

### [#18303](https://github.com/micropython/micropython/pull/18303) - stm32: Add STM32H747I-DISCO board

Scope: ports/stm32/boards/STM32H747I_DISCO. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py, board docs. PR summary: Adds board definition for the STM32H747I-DISCO evaluation board. Hardware features: 32MB SDRAM (IS42S32800G, 32-bit bus @ 120MHz) Dual QSPI flash (2x512Mbit MT25QL512ABB = 128MB total) USB High-Speed via ULPI PHY (USB3320C-EZK @ 480Mbps). This PR currently meets the minimum MUST criteria. Notable strengths: manifest.py included, board docs included, detailed PR description.

### [#18090](https://github.com/micropython/micropython/pull/18090) - rp2: boards: Add Soldered NULA RP2350 Board Definition

Scope: ports/rp2/boards/SOLDERED_NULA_RP2350. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py, variant configs. PR summary: Add Support for the upcoming Soldered NULA RP2350 board by Soldered Electronics. This PR currently meets the minimum MUST criteria. Notable strengths: manifest.py included, variant configs included.

### [#18064](https://github.com/micropython/micropython/pull/18064) - rp2: boards: Add W5100S-EVB-Pico2 board definition.

Scope: ports/rp2/boards/W5100S_EVB_PICO2. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, variant configs. PR summary: This adds a board definition for the WIZnet W5100S evaluation board with the RP2350 ("Pico2") chip, named "W5100S-EVB-Pico2".. This PR currently meets the minimum MUST criteria. Notable strengths: variant configs included, detailed PR description.

### [#18035](https://github.com/micropython/micropython/pull/18035) - ports/rp2/boards: Add WIZnet-EVB-boards and wiznet6k submodule

Scope: ports/rp2/boards/W5100S_EVB_PICO, ports/rp2/boards/W5100S_EVB_PICO2, ports/rp2/boards/W5500_EVB_PICO, and 6 more. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py. PR summary: This PR adds full support for WIZnet Ethernet controller EVB (Evaluation Board) series W5100S_EVB_PICO W5500_EVB_PICO W5100S_EVB_PICO2 – Pico2 with W5100S (#16280). This PR currently meets the minimum MUST criteria. Notable strengths: manifest.py included, detailed PR description.

### [#17857](https://github.com/micropython/micropython/pull/17857) - adding support for the W55RP20_EVB_PICO.

Scope: ports/rp2/boards/W55RP20_EVB_PICO. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py. PR summary: adding support for the W55RP20_EVB_PICO, data copied from the manufacturer. This PR currently meets the minimum MUST criteria. Notable strengths: manifest.py included, detailed PR description.

### [#17590](https://github.com/micropython/micropython/pull/17590) - stm32/boards: Add WeAct_H723VG board support.

Scope: ports/stm32/boards/WEACTSTUDIO_MINI_STM32H723, ports/stm32/boards/WEACT_STM32H723, ports/stm32/boards/WeAct_H723VG. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py. PR summary: This change adds WeAct STM32H723 Core Board support to the STM32 port. REPL via USB VCP works. SPI flash is available (8MB) as an internal storage. QSPI flash is available (8MB) as ROMFS. USB Storage is available. Some peripherals (GPIO, SP. This PR currently meets the minimum MUST criteria. Notable strengths: manifest.py included, detailed PR description.

### [#17001](https://github.com/micropython/micropython/pull/17001) - rp2/boards/SOLDERPARTY_RP2350_STAMP_XL: Add new Solder Party board.

Scope: ports/rp2/boards/SOLDERPARTY_RP2350_STAMP_XL. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py, variant configs. PR summary: Add Solder Party RP2350 Stamp XL board. This PR currently meets the minimum MUST criteria. Notable strengths: manifest.py included, variant configs included.

### [#16409](https://github.com/micropython/micropython/pull/16409) - renesas-ra/boards/WEACT_RA4M1_CORE: Add board profile.

Scope: ports/renesas-ra/boards/WEACT_RA4M1_CORE. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py. PR summary: Adds renesas port board profile for WeAct RA4M1 CORE board.. This PR currently meets the minimum MUST criteria. Notable strengths: manifest.py included, detailed PR description.

### [#16407](https://github.com/micropython/micropython/pull/16407) - ports/stm32/board/MPY_v11: Add new board MPY_v11 and acceleration IC.

Scope: ports/stm32/boards/MPY_v11. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, board docs, variant configs. PR summary: This Pull Request aims to add support for the MPY_v11 board, which integrates a new acceleration sensor. To fully support the. This PR currently meets the minimum MUST criteria. Notable strengths: board docs included, variant configs included, detailed PR description.

### [#16325](https://github.com/micropython/micropython/pull/16325) - add new board: ESP32_GENERIC_S3_N16R8_CAMERA

Scope: ports/esp32/boards/ESP32_GENERIC_S3_N16R8_CAMERA. Key files detected: board.json, mpconfigboard.h, board build config, board docs. PR summary: This Pull Request aims to add support for the ESP32_GENERIC_S3_N16R8_CAMERA board, which integrates a camera module. To fully support the camera functionality of this board, this PR depends on an external camera driver module: micropython-c. This PR does not yet meet the minimum MUST criteria. Key gaps: pins.csv. Notable strengths: board docs included, detailed PR description.

### [#16124](https://github.com/micropython/micropython/pull/16124) - ports/esp32/boards: Add WAVESHARE_ESP32_S3_PICO board configuration.

Scope: ports/esp32/boards/WAVESHARE_ESP32_S3_PICO. Key files detected: board.json, mpconfigboard.h, board build config, manifest.py, board docs. PR summary: Add WAVESHARE_ESP32_S3_PICO definition. This PR does not yet meet the minimum MUST criteria. Key gaps: pins.csv, testing evidence in PR body. Notable strengths: manifest.py included, board docs included.

### [#15889](https://github.com/micropython/micropython/pull/15889) - ports: adafruit grand central board support

Scope: ports/samd/boards/ADAFRUIT_GRAND_CENTRAL_M4_EXPRESS. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py. PR summary: Adds board support for Adafruit Grand Central M4 (this is an updated version of #11104 which I am about to close, and includes contributions from @robert-hh). This PR currently meets the minimum MUST criteria. Notable strengths: manifest.py included.

### [#15516](https://github.com/micropython/micropython/pull/15516) - I have added new stm32 boards(NUCLEO_H753xx)

Scope: ports/stm32/boards/NUCLEO_H753ZI. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py. This PR currently meets the minimum MUST criteria. Notable strengths: manifest.py included, detailed PR description.

### [#15482](https://github.com/micropython/micropython/pull/15482) - ports/nrf/boards/SUPERMINI_NRF52840 board definition + machine_bitstream.

Scope: ports/nrf/boards/SUPERMINI_NRF52840. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py. PR summary: The Supermini NRF52840 is a clone of the NiceNano board based on the Pro Micro layout. The board definition includes a machine_bitstream driver to drive NeoPixel leds.. This PR currently meets the minimum MUST criteria. Notable strengths: manifest.py included, detailed PR description.

### [#15443](https://github.com/micropython/micropython/pull/15443) - ports/rp2/boards: Add ARCHI board by Newsan.

Scope: ports/rp2/boards/ARCHI. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv. PR summary: Add new Newsan's Archi educational board.. This PR does not yet meet the minimum MUST criteria. Key gaps: testing evidence in PR body.

### [#13361](https://github.com/micropython/micropython/pull/13361) - esp32/boards: Add board definition for WalnutPi PicoW.

Scope: ports/esp32/boards/WPI_PICO_W. Key files detected: board.json, mpconfigboard.h, board build config, board docs. PR summary: !walnutpi_pico_w. This PR does not yet meet the minimum MUST criteria. Key gaps: pins.csv, testing evidence in PR body. Notable strengths: board docs included.

### [#13204](https://github.com/micropython/micropython/pull/13204) - ports/esp32/boards: Add uPesy EDU ESP32 board.

Scope: ports/esp32/boards/UPESY_EDU_ESP32. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py, board docs. PR summary: Create a new ESP32 board variant for the uPesy EDU ESP32 board.. This PR does not yet meet the minimum MUST criteria. Key gaps: testing evidence in PR body. Notable strengths: manifest.py included, board docs included.

### [#12749](https://github.com/micropython/micropython/pull/12749) - ports/rp2/boards/W5100S_EVB_PICO/mpconfigboard.cmake: Set default mode to HardWired

Scope: ports/rp2/boards/W5100S_EVB_PICO, ports/rp2/boards/W5500_EVB_PICO. Key files detected: board build config. PR summary: The W5100S and W5500 modules are optimized for hard-wired settings.. This PR does not yet meet the minimum MUST criteria. Key gaps: board.json, mpconfigboard.h/mpconfigboard.cmake|mk, pins.csv, testing evidence in PR body.

### [#12676](https://github.com/micropython/micropython/pull/12676) - stm32/boards/ARDUINO_PORTENTA_H7: Update pin definitions.

Scope: ports/stm32/boards/ARDUINO_PORTENTA_H7. Key files detected: pins.csv. PR summary: Changes made to pins.csv: Removed processor pin designations from board pin names. Added board designations for the high-density connectors.. This PR does not yet meet the minimum MUST criteria. Key gaps: board.json, mpconfigboard.h/mpconfigboard.cmake|mk, testing evidence in PR body.

### [#12642](https://github.com/micropython/micropython/pull/12642) - samd: Add board definition for Sparkfun SAMD51 MicroMod

Scope: ports/samd/boards/SPARKFUN_SAMD51_MICROMOD. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv. This PR does not yet meet the minimum MUST criteria. Key gaps: testing evidence in PR body.

### [#12319](https://github.com/micropython/micropython/pull/12319) - Board Definition Added for Pi-Plates MICROpi

Scope: ports/rp2/boards/PI-PLATES_MICROPI, ports/rp2/boards/PICOPLATE. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv. This PR does not yet meet the minimum MUST criteria. Key gaps: testing evidence in PR body.

### [#12042](https://github.com/micropython/micropython/pull/12042) - esp32/boards: Add support for XIAO ESP32S3/C3 boards.

Scope: ports/esp32/boards/SEEED_XIAO_ESP32C3, ports/esp32/boards/SEEED_XIAO_ESP32S3, ports/esp32/boards/XIAO_ESP32C3, and 1 more. Key files detected: board.json, mpconfigboard.h, board build config, manifest.py. This PR does not yet meet the minimum MUST criteria. Key gaps: pins.csv, testing evidence in PR body. Notable strengths: manifest.py included.

### [#11398](https://github.com/micropython/micropython/pull/11398) - NUCLEO-H7A3ZI-Q

Scope: ports/stm32/boards/NUCLEO_H7A3ZI. Key files detected: mpconfigboard.h, board build config, pins.csv. PR summary: This works on my NUCLEO-H7A3ZI-Q boards. It was mainly adapted from the STM32H7B3I_DK board files.. This PR does not yet meet the minimum MUST criteria. Key gaps: board.json, testing evidence in PR body.

### [#10752](https://github.com/micropython/micropython/pull/10752) - ports/renesas-ra/boards/VK-RA6M3: Another New Board.

Scope: ports/renesas-ra/boards/VK_RA6M3, ports/renesas-ra/boards/VK_RA6M5. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py, board docs. PR summary: Thanks to the kind help of @TakeoTakahashi2020 & the mentioned intention for a new ports earlier (#10595), this confirms 2-nd board is also uPy ready.. This PR does not yet meet the minimum MUST criteria. Key gaps: testing evidence in PR body. Notable strengths: manifest.py included, board docs included.

### [#10665](https://github.com/micropython/micropython/pull/10665) - rp2/boards/VCC_GND_RP2040: add VCC_GND_RP2040 with multiple variants.

Scope: ports/rp2/boards/VCC_GND_RP2040. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv, manifest.py, board docs. PR summary: This supports 4, 8 and 16MB flash variants.. This PR does not yet meet the minimum MUST criteria. Key gaps: testing evidence in PR body. Notable strengths: manifest.py included, board docs included.

### [#10595](https://github.com/micropython/micropython/pull/10595) - ports/renesas-ra/boards/VK-RA4W1: New board.

Scope: ports/renesas-ra/boards/RA4M1_CLICKER, ports/renesas-ra/boards/RA4M1_EK, ports/renesas-ra/boards/RA4W1_EK, and 1 more. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv. PR summary: ports/renesas-ra/boards/VK-RA4W1: Adding new dev board. This PR does not yet meet the minimum MUST criteria. Key gaps: testing evidence in PR body. Notable strengths: detailed PR description.

### [#9859](https://github.com/micropython/micropython/pull/9859) - ports/rp2/boards/ADAFRUIT_KB2040: Add Adafruit KB2040 board.

Scope: ports/rp2/boards/ADAFRUIT_KB2040. Key files detected: board.json, mpconfigboard.h, board build config. PR summary: Add Adafruit KB2040 board to rp2 port.. This PR does not yet meet the minimum MUST criteria. Key gaps: pins.csv, testing evidence in PR body.

### [#9367](https://github.com/micropython/micropython/pull/9367) - SMT32G4: Add USB, QPSI and AEMICS Board PYglet

Scope: ports/stm32/boards/AEMICS_PYglet. Key files detected: board.json, mpconfigboard.h, board build config, pins.csv. PR summary: We build our own basic MicroPython board with a ST G473 processor. We are using it internally for some time now, and we thought to finally do a Pull Request on the board.. This PR does not yet meet the minimum MUST criteria. Key gaps: testing evidence in PR body.

### [#9177](https://github.com/micropython/micropython/pull/9177) - esp32/boards: Add LOLIN S3 ESP32-S3 based board.

Scope: ports/esp32/boards/GENERIC_S3_SPIRAM, ports/esp32/boards/LOLIN_S3. Key files detected: board.json, mpconfigboard.h, board build config, manifest.py. PR summary: based ESP32-S3-WROOM-1 2x Type-C USB (OTG, UART) 16MB Flash (Quad SPI) 8MB PSRAM (Octal SPI) 31x IO 1x LOLIN I2C Port. This PR does not yet meet the minimum MUST criteria. Key gaps: pins.csv, testing evidence in PR body. Notable strengths: manifest.py included.

### [#8822](https://github.com/micropython/micropython/pull/8822) - ports/esp32/boards: Add supoprt to Franzininho WiFi WROVER(SPIRAM).

Scope: ports/esp32/boards/FRANZININHO_WIFI_WROVER. Key files detected: board.json, mpconfigboard.h, board build config, manifest.py. PR summary: Adding files to Franzininho WiFi Wrover board. A variation of the https://github.com/Franzininho/Franzininho-WiFi https://docs.franzininho.com.br/docs/franzininho-wifi/franzininho-wifi/ (PT_BR). This PR does not yet meet the minimum MUST criteria. Key gaps: pins.csv, testing evidence in PR body. Notable strengths: manifest.py included.

### [#8801](https://github.com/micropython/micropython/pull/8801) - esp32: Add supoprt to Franzininho WiFi an ESP32-S2 based board

Scope: ports/esp32/boards/FRANZININHO_WIFI. Key files detected: board.json, mpconfigboard.h, board build config, manifest.py. PR summary: Adding support to Franzininho WiFi. A dev board based on ESP32-S2. https://github.com/Franzininho/Franzininho-WiFi https://docs.franzininho.com.br/docs/franzininho-wifi/franzininho-wifi/ (PT_BR). This PR does not yet meet the minimum MUST criteria. Key gaps: pins.csv, testing evidence in PR body. Notable strengths: manifest.py included.

### [#7604](https://github.com/micropython/micropython/pull/7604) - rp2/boards/PICO: Add USB VID/PID.

Scope: ports/rp2/boards/PICO. Key files detected: mpconfigboard.h. PR summary: Added VID/PID as per CircuitPython board def. This PR does not yet meet the minimum MUST criteria. Key gaps: board.json, mpconfigboard.h/mpconfigboard.cmake|mk, pins.csv, testing evidence in PR body.

### [#7580](https://github.com/micropython/micropython/pull/7580) - rp2/boards: Add Adafruit Trinkey QT2040.

Scope: ports/rp2/boards/ADAFRUIT_TRINKEY_QT2040. Key files detected: mpconfigboard.h, board build config. PR summary: Depends on: https://github.com/raspberrypi/pico-sdk/pull/525. This PR does not yet meet the minimum MUST criteria. Key gaps: board.json, pins.csv, testing evidence in PR body.

### [#7579](https://github.com/micropython/micropython/pull/7579) - rp2/boards: Add Seeed XIAO RP2040.

Scope: ports/rp2/boards/SEEED_XIAO_RP2040. Key files detected: mpconfigboard.h, board build config. PR summary: Depends on: https://github.com/raspberrypi/pico-sdk/pull/524. This PR does not yet meet the minimum MUST criteria. Key gaps: board.json, pins.csv, testing evidence in PR body.

### [#7300](https://github.com/micropython/micropython/pull/7300) - esp32/boards: Add board definition for ESP32-S2-Saola-1

Scope: ports/esp32/boards/GENERIC_S2_SAOLA. Key files detected: board.json, mpconfigboard.h, board build config. PR summary: This PR adds a new esp32 port board definition GENERIC_S2_SAOLA. v4.3-beta2 v4.3-beta3. This PR does not yet meet the minimum MUST criteria. Key gaps: pins.csv, testing evidence in PR body.

### [#7123](https://github.com/micropython/micropython/pull/7123) - STM32L4: Support all STM32L4 MCUs with all features. Add NUCLEO boards.

Scope: ports/stm32/boards/NUCLEO_L432KC, ports/stm32/boards/NUCLEO_L432KC_LFS1, ports/stm32/boards/NUCLEO_L433RC-P, and 3 more. Key files detected: mpconfigboard.h, board build config, pins.csv. PR summary: This corrects errors and omissions in the STM32L4 ports. USB for STM32L45x family. STM32L433/443 support. An easier way to fine tune memory allocation per board which is Adds all series members instead of just one, eg L451, L452, L462. This PR does not yet meet the minimum MUST criteria. Key gaps: board.json, testing evidence in PR body.

### [#6677](https://github.com/micropython/micropython/pull/6677) - nrf/boards/waveshare_ble400: added board definition

Scope: ports/nrf/boards/waveshare_ble400. Key files detected: mpconfigboard.h, board build config, pins.csv. PR summary: Added Waveshare BLE400.. This PR does not yet meet the minimum MUST criteria. Key gaps: board.json, testing evidence in PR body.

### [#6488](https://github.com/micropython/micropython/pull/6488) - Add ports/nrf for BLYST840 nRF52840 Boards :

Scope: ports/nrf/boards/ibk-nrf52840, ports/nrf/boards/udg-nrf52840, ports/nrf/boards/udg-nrf52840C. Key files detected: mpconfigboard.h, board build config, pins.csv. PR summary: Breakout board USB dongle type-A USB dongle type-C. This PR does not yet meet the minimum MUST criteria. Key gaps: board.json, testing evidence in PR body.
