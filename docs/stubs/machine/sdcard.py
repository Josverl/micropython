class SD:
    """
    Create a SD card object. See ``init()`` for parameters if initialization.
    """

    def __init__(self, id, *args, **kwargs) -> None: ...
    def init(self, id=0, pins=("GP10", "GP11", "GP15")) -> None:
        """
        Enable the SD card. In order to initialize the card, give it a 3-tuple:
        ``(clk_pin, cmd_pin, dat0_pin)``.
        """
        ...
    def deinit(self) -> None:
        """
        Disable the SD card.
        """
        ...

class SDCard:
    """
    This class provides access to SD or MMC storage cards using either
    a dedicated SD/MMC interface hardware or through an SPI channel.
    The class implements the block protocol defined by :class:`os.AbstractBlockDev`.
    This allows the mounting of an SD card to be as simple as::

      os.mount(machine.SDCard(), "/sd")

    The constructor takes the following parameters:

     - *slot* selects which of the available interfaces to use. Leaving this
       unset will select the default interface.

     - *width* selects the bus width for the SD/MMC interface.

     - *cd* can be used to specify a card-detect pin.

     - *wp* can be used to specify a write-protect pin.

     - *sck* can be used to specify an SPI clock pin.

     - *miso* can be used to specify an SPI miso pin.

     - *mosi* can be used to specify an SPI mosi pin.

     - *cs* can be used to specify an SPI chip select pin.

     - *freq* selects the SD/MMC interface frequency in Hz (only supported on the ESP32).
    """

    def __init__(self, slot=1, width=1, cd=None, wp=None, sck=None, miso=None, mosi=None, cs=None, freq=20000000) -> None: ...
