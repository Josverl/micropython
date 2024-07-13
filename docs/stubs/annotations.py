from enum import Enum, StrEnum

class Port(StrEnum):
    ESP8266 = "esp8266"
    ESP32 = "esp32"
    STM32 = "stm32"
    RP2 = "rp2"
    MIMXRT = "mimxrt"
    SAMD = "samd"
    UNIX = "unix"
    WINDOWS = "windows"

class Level(Enum):
    MINIMUM = 0
    CORE_FEATURES = 10
    BASIC_FEATURES = 20
    EXTRA_FEATURES = 30
    FULL_FEATURES = 40
    EVERYTHING = 50

def availability(*args, details=None):
    return lambda fn: fn

def overload_availability(*args, details=None):
    return lambda fn: fn

def module_availability(*args, details=None):
    pass

def cpython_stdlib(modname):
    pass

# TODO: https://peps.python.org/pep-0688/#collections-abc-buffer
Buffer = bytes
WriteableBuffer = bytearray
