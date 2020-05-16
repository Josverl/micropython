#compile for newer chips only, and avoid warning
CONFIG_IDF_FIRMWARE_CHIP_ID=0x0001

SDKCONFIG += boards/sdkconfig.base
SDKCONFIG += boards/sdkconfig.spiram

