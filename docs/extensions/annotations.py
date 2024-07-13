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


def _infer_indentation(doc: str):
    """
    Infer the indentation used in the given document.

    Args:
        doc (str): The document to analyze.

    Returns:
        str: The inferred indentation, represented as a string of spaces.
    """
    for line in doc.split("\n"):
        if not line.strip():
            continue
        return " " * (len(line) - len(line.lstrip(" ")))

    return ""


def _append_to_doc(doc: str, extra: str):
    ind = _infer_indentation(doc)
    return (
        doc.lstrip("\r\n").rstrip() + "\n\n" + "\n".join(ind + line for line in extra.split("\n"))
    )


def availability(*args, details=None):
    def _wrap(fn):
        fn.__doc__ = _append_to_doc(
            fn.__doc__,
            "Availability: {}{}".format(
                ",".join(str(x) for x in args), " -- {}".format(details) if details else ""
            ),
        )
        return fn

    return _wrap


def overload_availability(*args, details=None):
    def _wrap(fn):
        fn.__doc__ = _append_to_doc(
            fn.__doc__,
            "Overload availability: {}{}".format(
                ",".join(str(x) for x in args), " -- {}".format(details) if details else ""
            ),
        )
        return fn

    return _wrap


def module_availability(*args, details=None):
    import inspect

    g = inspect.stack()[1].frame.f_globals
    g["__doc__"] = _append_to_doc(
        g["__doc__"],
        "Availability: {}{}".format(
            ",".join(str(x) for x in args), " -- {}".format(details) if details else ""
        ),
    )


def cpython_stdlib(modname: str):
    import inspect

    g = inspect.stack()[1].frame.f_globals
    g["__doc__"] = _append_to_doc(
        g["__doc__"], "|see_cpython_module| :mod:`python:{}`".format(modname)
    )


# TODO: https://peps.python.org/pep-0688/#collections-abc-buffer
Buffer = bytes
WriteableBuffer = bytearray
