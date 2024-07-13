"""
This module provides a general frame buffer which can be used to create
bitmap images, which can then be sent to a display.

The FrameBuffer class provides a pixel buffer which can be drawn upon with
pixels, lines, rectangles, ellipses, polygons, text and even other
FrameBuffers. It is useful when generating output for displays.

Example::

    import framebuf

    # FrameBuffer needs 2 bytes for every RGB565 pixel
    w = 100
    h = 10
    bytearray(w * h * 2)

    # Create a FrameBuffer backed by buf.
    fbuf = framebuf.FrameBuffer(buf, w, h, framebuf.RGB565)

    fbuf.fill(0)
    fbuf.text('MicroPython!', 0, 0, 0xffff)
    fbuf.hline(0, 9, 96, 0xffff)
"""

from array import array
from annotations import availability, cpython_stdlib, Level, WriteableBuffer

@availability(Level.EXTRA_FEATURES)
class FrameBuffer:
    """
    Construct a FrameBuffer object.

    Arguments:
        buffer:
            An object supporting the buffer protocol(e.g. `bytearray`) which
            must be large enough to contain every pixel defined by the width,
            height and format of the FrameBuffer.
        width:
            The width of the FrameBuffer in pixels.
        height:
            The height of the FrameBuffer in pixels.
        format:
            Specifies the type of pixel used in the FrameBuffer. See the list
            of supported values defined below. These set the number of bits
            used to encode a color value and the layout of these bits in
            *buffer*. Where a color value *color* is passed to a method,
            *color* is a small integer with an encoding that is dependent on
            the format of the FrameBuffer.
        stride:
            The number of pixels between each horizontal line of pixels in the
            FrameBuffer. This defaults to *width* but may need adjustments
            when implementing a FrameBuffer within another larger FrameBuffer
            or screen. The *buffer* size must accommodate an increased step
            size.

    Invalid *buffer* size or dimensions may lead to unexpected errors.
    """

    def __init__(self, buffer: WriteableBuffer, width: int, height: int, format: int, stride: int=-1, /) -> None:
        ...

    def fill(self, color: int, /) -> None:
        """
        Set the entire FrameBuffer to a single color.

        Arguments:
            color:
                An integer in the FrameBuffer's pixel format.
        """
        ...

    def pixel(self, x: int, y: int, color: int = None, /) -> int | None:
        """
        Set or get the pixel value at the specified coordinate.

        Arguments:
            color:
                An integer in the FrameBuffer's pixel format to set the pixel
                value, or ``None`` to get the pixel value.

        Returns:
            If the color parameter is unset, returns the pixel value as an
            integer in the FrameBuffer's pixel format. Otherwise returns
            ``None``.
        """
        ...

    def hline(self, x: int, y: int, w: int, color: int, /) -> None:
        """
        Draw a one-pixel thick horizontal line from ``(x,y)`` to ``(x+w,y)``.

        Arguments:
            x:
                Starting x-coordinate.
            y:
                Starting y-coordinate.
            w:
                Width of the line.
            color:
                An integer in the FrameBuffer's pixel format.
        """
        ...

    def vline(self, x: int, y: int, h: int, color: int, /) -> None:
        """
        Draw a one-pixel thick vertical line from ``(x,y)`` to ``(x,y+h)``.

        Arguments:
            x:
                Starting x-coordinate.
            y:
                Starting y-coordinate.
            h:
                Height of the line.
            color:
                An integer in the FrameBuffer's pixel format.
        """
        ...

    def line(self, x1: int, y1: int, x2: int, y2: int, color: int, /) -> None:
        """
        Draw a one-pixel thick line from ``(x1,y1)`` to ``(x2,y2)``.

        Arguments:
            x1:
                Starting x-coordinate.
            y1:
                Starting y-coordinate.
            x2:
                Ending x-coordinate.
            y2:
                Ending y-coordinate.
            color:
                An integer in the FrameBuffer's pixel format.
        """
        ...

    def rect(self, x: int, y: int, w: int, h: int, color: int, fill: bool = False, /) -> None:
        """
        Outline or fill a rectangle.

        Arguments:
            x:
                Top-left x-coordinate.
            y:
                Top-left y-coordinate.
            w:
                Width of the rectangle.
            h:
                Height of the rectangle.
            color:
                An integer in the FrameBuffer's pixel format.
            fill:
                Optionally set to ``True`` to fill the rectangle. Otherwise a
                one-pixel outline is drawn.
        """
        ...

    def ellipse(self, x: int, y: int, xr: int, yr: int, color: int, fill: bool = False, mask: int = 0b1111, /) -> None:
        """
        Draw an ellipse with a given centre and radii. To draw a circle, set the two radii to be equal.

        Arguments:
            x:
                Centre x-coordinate.
            y:
                Centre y-coordinate.
            xr:
                Radius in the x-direction.
            yr:
                Radius in the y-direction.
            color:
                An integer in the FrameBuffer's pixel format.
            fill:
                Optionally set to ``True`` to fill the ellipse. Otherwise a
                one-pixel outline is drawn.
            mask:
                Optionally enables drawing to be restricted to certain
                quadrants of the ellipse. The least significant four bits
                determine which quadrants are to be drawn, with bit 0
                specifying Q1, b1 Q2, b2 Q3 and b3 Q4. Quadrants are numbered
                counterclockwise with Q1 being top right.
        """
        ...

    def poly(self, x: int, y: int, coords: array, color: int, fill: bool = False, /) -> None:
        """
        Draw a pre-defined arbitrary (convex or concave) closed polygon at
        the specified offset coordinate.

        Arguments:
            x:
                Offset x-coordinate.
            y:
                Offset y-coordinate.
            coords:
                An `array.array` of pairwise pixel coordinates, e.g.
                ``array('h', [x0, y0, x1, y1, ... xn, yn])``. Can also be a
                `bytes` (or `bytearray`) if the values are less than ``256``.
            color:
                An integer in the FrameBuffer's pixel format.
            fill:
                Optionally set to ``True`` to fill the ellipse. Otherwise a
                one-pixel outline is drawn.
        """
        ...

    def text(self, text: str, x: int, y: int, color: int = 1, /) -> None:
        """
        Draw text to the FrameBuffer with upper-left coordinate ``(x,y)``.

        All characters have dimensions of 8x8 pixels and there is currently no
        way to change the font. Newlines are ignored.

        Arguments:
            x:
                First character x-coordinate.
            y:
                First character y-coordinate.
            color:
                An integer in the FrameBuffer's pixel format, defaulting to
                the value ``1``.

        """
        ...
    def scroll(self, xstep: int, ystep: int, /) -> None:
        """
        Shift the contents of the FrameBuffer by ``(xstep,ystep)``.

        This operation does not clear the region left behind, so may leave a
        footprint of the previous colors in the FrameBuffer.

        Arguments:
            xstep:
                Number of pixels to shift right (positive) or left (negative) by.
            ystep:
                Number of pixels to shift down (positive) or up (negative) by.
        """
        ...

    def blit(self, source: "FrameBuffer", x: int, y: int, key: int=-1, palette: "FrameBuffer"=None, /) -> None:
        """
        Draw another FrameBuffer on top of the current one at the given coordinates.

        The palette argument enables blitting between FrameBuffers with
        differing formats. Typical usage is to render a monochrome or
        grayscale glyph/icon to a color display.

        Arguments:
            source:
                A `FrameBuffer` instance to draw.
            x:
            y:
            key:
                An integer in the FrameBuffer's pixel format that will be
                considered transparent: all pixels with that color value will
                not be drawn.
            palette:
                Optional `FrameBuffer` instance whose format is that of the
                current FrameBuffer. The palette height must be one pixel and
                its width must be the number of available colors in the source
                FrameBuffer. The palette for an N-bit source needs ``2**N``
                pixels; the palette for a monochrome source would have 2
                pixels representing background and foreground colors. The
                application assigns a color to each pixel in the palette.
                The color of the current pixel will be that of that palette
                pixel whose x position is the color of the corresponding
                source pixel.

        Notes:
            If both *key* and *palette* are specified, then the *key* is
            compared to the value from *palette*, not to the value directly
            from *source*.)
        """
        ...

MONO_VLSB: int = 0
"""
Monochrome (1-bit) color format

This defines a mapping where the bits in a byte are vertically mapped with
bit 0 being nearest the top of the screen. Consequently each byte occupies
8 vertical pixels. Subsequent bytes appear at successive horizontal
locations until the rightmost edge is reached. Further bytes are rendered
at locations starting at the leftmost edge, 8 pixels lower.
"""
MONO_HLSB: int = 3
"""
Monochrome (1-bit) color format

This defines a mapping where the bits in a byte are horizontally mapped.
Each byte occupies 8 horizontal pixels with bit 7 being the leftmost.
Subsequent bytes appear at successive horizontal locations until the
rightmost edge is reached. Further bytes are rendered on the next row, one
pixel lower.
"""
MONO_HMSB: int = 4
"""
Monochrome (1-bit) color format

This defines a mapping where the bits in a byte are horizontally mapped.
Each byte occupies 8 horizontal pixels with bit 0 being the leftmost.
Subsequent bytes appear at successive horizontal locations until the
rightmost edge is reached. Further bytes are rendered on the next row, one
pixel lower.
"""
RGB565: int = 1
"""
Red Green Blue (16-bit, 5+6+5) color format

This defines a mapping where each pixel is represented as a 16-bit value
where the first 5 bits are the red channel, next 6 bits are the green
channel, and final 5 bits are the blue channel.
"""
GS2_HMSB: int = 5
"""
Grayscale (2-bit) color format

Similar to the MONO_MHSB format, except each pixel is two bits.
"""
GS4_HMSB: int = 2
"""
Grayscale (4-bit) color format

Similar to the MONO_MHSB format, except each pixel is four bits.
"""
GS8: int = 6
"""
Grayscale (8-bit) color format

This defines a mapping where each pixel is a single byte representing the
greyscale value of the pixel.
"""
