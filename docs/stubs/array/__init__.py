"""
This module provides a type that allows for efficient and compact
representation of lists of numeric values. They work like lists, except all
elements must be of the same numeric type, and they also implement the
:term:`buffer protocol`.

The supported format codes are ``b``, ``B``, ``h``, ``H``, ``i``, ``I``,
``l``, ``L``, ``q``, ``Q``,

This documentation uses `int` as a placeholder for the numeric type. If
floating point support is enabled, the array type may also hold floating-point
values elements (corresponding to type codes ``f`` and ``d``).
"""

from typing import Iterable, overload
from annotations import availability, overload_availability, cpython_stdlib, Level

cpython_stdlib("array")


@availability(Level.CORE_FEATURES)
class array:
    """
    Creates an array with elements of given numeric type.

    Arguments:
        typecode:
            A single character from the list above defining the numeric type
            for elements in this array.
        initializer:
            An object that can be iterated to generate the initial values for
            this array. For example, a `list`, `tuple`, `bytes`, or other
            sequence. If the initializer is not provided, then the array will
            be empty.
    """

    def __init__(self, typecode, initializer: Iterable[int]=None) -> None:
        ...

    def append(self, val: int) -> None:
        """
        Append new element *val* to the end of array, growing it.
        """
        ...

    def extend(self, source: Iterable[int]) -> None:
        """
        Append new elements from *source* to the end of array, growing it.
        """
        ...

    @overload
    def __getitem__(self, index: int) -> int:
        ...

    @overload
    def __getitem__(self, index: slice) -> "array":
        ...

    def __getitem__(self, index):
        """
        Implements the subscript operator with both integer and slice
        arguments to get a single element or a range of elements.

        Returns:
            Either a numeric value or an array containing the range of
            elements.
        """
        ...

    @overload
    def __setitem__(self, index: slice, value: "array") -> None:
        ...

    @overload
    def __setitem__(self, index: int, value: int) -> None:
        ...

    @overload_availability(Level.EXTRA_FEATURES, details="slice")
    def __setitem__(self, index, value):
        """
        Implements the subscript operator with both integer and slice
        arguments to set either a single element or a range of elements.
        """
        ...

    def __len__(self) -> int:
        """
        Supports the ``len(a)`` operator.

        Returns:
            The number of elements in the array.
        """
        ...

    def __add__(self, other: "array") -> "array":
        """
        Array instances can be concatenated together using the ``+`` operator.

        Parameters:
            other: An `array.array` instance.

        Returns:
            The concatenation of the two arrays.

        Notes:
            This is implemented by concatenating the underlying bytes, which
            may produce unexpected results if the numeric types of the two
            arrays are different.
        """
        ...

    def __iadd__(self, other: "array") -> "array":
        """
        Array instances can be concatenated in-place using the ``+=`` operator.

        Parameters:
            other: An `array.array` instance.

        Returns:
            The array instance that has now been extended with the items from
            *other*.

        Notes:
            This is implemented by concatenating the underlying bytes, which
            may produce unexpected results if the numeric types of the two
            arrays are different.
        """
        ...

    def __repr__(self) -> str:
        """
        Supports the ``repr(a)`` operator.

        Returns:
            The string representation of the array in the form
            ``"array(<type>, [<elements>])"``, where ``<type>`` is the type
            code letter for the array and ``<elements>`` is a comma separated
            list of the elements of the array.
        """
        ...
