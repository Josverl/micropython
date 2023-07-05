"""
This module implements conversions between binary data and various
encodings of it in ASCII form (in both directions).
"""

from annotations import module_availability, cpython_stdlib, Level, Buffer

cpython_stdlib("binascii")
module_availability(Level.EXTRA_FEATURES)

def hexlify(data: Buffer, sep: Buffer = None, /) -> bytes:
    """
    Convert an object implementing the `buffer protocol` to a hexadecimal
    representation.

    Arguments:
        data:
            An object implementing the :term:`buffer protocol` (e.g. `bytes`
            or `bytearray`).
        sep:
            Optional separator between each pair of nibbles. Must be a `bytes`
            of length 1.

    Returns:
        A `bytes` instance containing a string of hexadecimal nibbles.

    Notes:
        Consider using `bytes.hex` instead (also available as `bytearray.hex`
        and `memoryview.hex`).
    """
    ...

def unhexlify(data: Buffer, /) -> bytes:
    """
    Convert hexadecimal data to binary representation. Returns bytes string.
    (i.e. inverse of hexlify)

    ``unhexlify`` does not support separator-delimited inputs. Use
    `str.replace` to remove separators first.

    Arguments:
        data:
            An object implementing the :term:`buffer protocol` (e.g. `bytes`
            or `bytearray`) containing the hexadecimal-encoded nibbles.

    Returns:
        A `bytes` instance containing the decoded data.

    Notes:
        Consider using `bytes.fromhex` instead.
    """
    ...

def b2a_base64(data: Buffer, /, newline=True) -> bytes:
    """
    Encode binary data in base64 format, as in `RFC 3548 <https://tools.ietf.org/html/rfc3548.html>`_.

    Arguments:
        data:
            An object implementing the :term:`buffer protocol` (e.g. `bytes`
            or `bytearray`).
        newline:
            If set to ``True``, appends a newline to the end of the output.

    Returns:
        A `bytes` instance containing the base64-encoded data.
    """
    ...

def a2b_base64(data: Buffer, /) -> bytes:
    """
    Decode base64-encoded data, ignoring invalid characters in the input.
    Conforms to `RFC 2045 s.6.8 <https://tools.ietf.org/html/rfc2045#section-6.8>`_.

    Arguments:
        data:
            An object implementing the :term:`buffer protocol` (e.g. `bytes`
            or `bytearray`) containing the base64-encoded data.

    Returns:
        A `bytes` instance containing the decoded data.
    """
    ...
