from obey.utils import (
    get_underlying_types,
    str_to_bool,
    decompose_optional,
    type_is_valid,
    name_is_valid,
)
import pytest
from typing import Optional, Literal, Callable, Union, Any


def test_name_is_valid():
    assert not name_is_valid(" ")
    assert not name_is_valid("    ")
    assert not name_is_valid("")
    assert not name_is_valid("-")
    assert not name_is_valid("--")
    assert not name_is_valid("_")
    assert not name_is_valid("__")
    assert not name_is_valid("&")
    assert not name_is_valid("1")
    assert not name_is_valid("23")
    assert not name_is_valid("-h")
    assert not name_is_valid("--k")
    assert not name_is_valid("_o")
    assert not name_is_valid("__p")
    assert name_is_valid("a")
    assert name_is_valid("ab")
    assert name_is_valid("ijk")
    assert name_is_valid("d_h")
    assert name_is_valid("some_body")


def test_decompose_optional():
    for t in [str, int, float, complex, bool]:
        assert decompose_optional(t) == (t, False)
        assert decompose_optional(list[t]) == (list[t], False)
        assert decompose_optional(Optional[t]) == (t, True)
        assert decompose_optional(Optional[list[t]]) == (list[t], True)

    assert decompose_optional(Literal[1, 2]) == (Literal[1, 2], False)
    assert decompose_optional(Optional[Literal[1, 2]]) == (Literal[1, 2], True)

    assert decompose_optional(tuple[complex, str, float]) == (
        tuple[complex, str, float],
        False,
    )
    assert decompose_optional(Optional[tuple[str, bool, complex]]) == (
        tuple[str, bool, complex],
        True,
    )


def test_get_underlying_types():
    for t, values in [
        (str, ("one", "two")),
        (int, (1, 2)),
        (float, (0.2, 1.3)),
        (
            complex,
            (complex("2-2j"), complex("3j")),
        ),
        (bool, (False, True)),
    ]:
        assert get_underlying_types(t) == [t]
        assert get_underlying_types(Optional[t]) == [t]
        assert get_underlying_types(list[t]) == [t]
        assert get_underlying_types(Optional[list[t]]) == [t]
        assert get_underlying_types(tuple[t]) == [t]
        assert get_underlying_types(Optional[tuple[t]]) == [t]
        assert get_underlying_types(Literal[values]) == [t, t]
        assert get_underlying_types(Optional[Literal[values]]) == [t, t]

    assert get_underlying_types(tuple[int, float, str, complex, bool]) == [
        int,
        float,
        str,
        complex,
        bool,
    ]

    assert get_underlying_types(Literal[1, 2, 1, 3, 2, 1]) == [int, int, int]

    assert get_underlying_types(Optional) == []
    assert get_underlying_types(Literal) == []
    assert get_underlying_types(list) == []
    assert get_underlying_types(Optional[list]) == []
    assert get_underlying_types(tuple) == []
    assert get_underlying_types(Optional[tuple]) == []


def test_type_is_valid():
    for t, values in [
        (str, ("one", "two", "Three")),
        (int, (1, 2, 5)),
        (float, (0.2, 1.3, 2.2)),
        (
            complex,
            (complex("4-2j"), complex("3j"), complex("1")),
        ),
        (bool, (False, True)),
    ]:
        assert type_is_valid(t)
        assert type_is_valid(Optional[t])
        assert type_is_valid(list[t])
        assert type_is_valid(Optional[list[t]])
        assert type_is_valid(Literal[values])
        assert type_is_valid(Optional[Literal[values]])

    assert type_is_valid(tuple[int])
    assert type_is_valid(tuple[float, float])
    assert type_is_valid(tuple[str, str, str])
    assert not type_is_valid(tuple[int, float])
    assert not type_is_valid(tuple[str, complex, complex])

    assert not type_is_valid(Optional)
    assert not type_is_valid(Literal)
    assert not type_is_valid(list)
    assert not type_is_valid(Optional[list])
    assert not type_is_valid(tuple)
    assert not type_is_valid(Optional[tuple])
    assert not type_is_valid(Any)
    assert not type_is_valid(Callable)
    assert not type_is_valid(Optional[Callable])
    assert not type_is_valid(Callable[[str], int])


def test_str_to_bool():
    for v in ["1", "y", "yes", "true", "t", "on"]:
        assert str_to_bool(v)

    for v in ["0", "n", "no", "false", "f", "off"]:
        assert not str_to_bool(v)

    for v in ["", "a", "bb", "-", "__"]:
        with pytest.raises(Exception):
            str_to_bool(v)
