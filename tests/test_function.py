from obey.function import Function
from obey.const import NO_DEFAUL_VALUE
import pytest
from typing import Optional, Literal
from math import inf


def empty():
    pass


def one_unspecified(idk):
    return idk


def one_required_positional(count: int):
    return count * 2


def one_positional(value: float = 2.718):
    return value - 1


def one_required_optional(name: Optional[str]):
    return name + " with postfix"


def one_optional(z: Optional[complex] = complex("3+4j")):
    return (z.real**2 + z.imag**2) ** 0.5


def one_literal(action: Literal["on", "off"]):
    return action.upper()


def one_tuple(values: tuple[float, float, float] = (1.0, 2.5, 3.1)):
    return sum(values)


def one_optional_list(names: Optional[list[str]]):
    return (", ").join(names)


def one_positional_list(names: list[str]):
    return (", ").join(names)


def mixed(
    value: float,
    name: Optional[str],
    debug: bool,
    modes: Optional[Literal["yes", "no"]],
    count: int = 3,
    z: Optional[complex] = complex("1-2j"),
):
    pass


def test_empty():
    fn = Function(empty)

    assert not fn.has_options
    assert not fn.has_positionals

    assert len(fn.parameters) == 0


def test_names():
    fn = Function(one_required_positional)

    assert fn.name == "one_required_positional"

    arg = fn.parameters[0]

    assert arg.fn_name == "one_required_positional"
    assert arg.original_name == "count"


def test_one_unspecified():
    fn = Function(one_unspecified)

    assert not fn.has_options
    assert fn.has_positionals

    assert len(fn.parameters) == 1

    arg = fn.parameters[0]

    assert arg.original_type == str

    with pytest.raises(Exception):
        fn.execute()

    arg.fill_value("23")
    assert fn.execute() == "23"


def test_one_required_positional():
    fn = Function(one_required_positional)

    assert not fn.has_options
    assert fn.has_positionals

    assert len(fn.parameters) == 1

    arg = fn.parameters[0]

    assert arg.original_type == int
    assert not arg.has_default
    assert not arg.is_option
    assert arg.underlying_type == int
    assert not arg.is_bool
    assert not arg.is_list
    assert not arg.is_literal
    assert not arg.is_tuple
    assert arg.expected_values_count == 1
    assert not arg.expects_many_values

    with pytest.raises(Exception):
        fn.execute()

    arg.fill_value(7)
    assert fn.execute() == 14


def test_one_positional():
    fn = Function(one_positional)

    assert not fn.has_options
    assert fn.has_positionals

    assert len(fn.parameters) == 1

    arg = fn.parameters[0]

    assert arg.original_type == float
    assert arg.has_default
    assert arg.value == 2.718
    assert not arg.is_option
    assert arg.underlying_type == float
    assert not arg.is_bool
    assert not arg.is_list
    assert not arg.is_literal
    assert not arg.is_tuple
    assert arg.expected_values_count == 1
    assert not arg.expects_many_values

    assert fn.execute() == 1.718
    arg.fill_value(3.14)
    assert fn.execute() == 2.14


def test_one_required_optional():
    fn = Function(one_required_optional)

    assert fn.has_options
    assert not fn.has_positionals

    assert len(fn.parameters) == 1

    arg = fn.parameters[0]

    assert arg.original_type == str
    assert not arg.has_default
    assert arg.is_option
    assert arg.underlying_type == str
    assert not arg.is_bool
    assert not arg.is_list
    assert not arg.is_literal
    assert not arg.is_tuple
    assert arg.expected_values_count == 1
    assert not arg.expects_many_values

    with pytest.raises(Exception):
        fn.execute()

    arg.fill_value("some line")
    assert fn.execute() == "some line with postfix"


def test_one_optional():
    fn = Function(one_optional)

    assert fn.has_options
    assert not fn.has_positionals

    assert len(fn.parameters) == 1

    arg = fn.parameters[0]

    assert arg.original_type == complex
    assert arg.has_default
    assert arg.value == complex("3+4j")
    assert arg.is_option
    assert arg.underlying_type == complex
    assert not arg.is_bool
    assert not arg.is_list
    assert not arg.is_literal
    assert not arg.is_tuple
    assert arg.expected_values_count == 1
    assert not arg.expects_many_values

    assert fn.execute() == 5
    arg.fill_value(complex("1j"))
    assert fn.execute() == 1


def test_one_literal():
    fn = Function(one_literal)

    assert not fn.has_options
    assert fn.has_positionals

    assert len(fn.parameters) == 1

    arg = fn.parameters[0]

    assert arg.original_type == Literal["on", "off"]
    assert not arg.has_default
    assert not arg.is_option
    assert arg.underlying_type == str
    assert not arg.is_bool
    assert not arg.is_list
    assert arg.is_literal
    assert not arg.is_tuple
    assert arg.expected_values_count == 1
    assert not arg.expects_many_values

    arg.fill_value("on")
    assert fn.execute() == "ON"

    arg.reset_value()
    arg.fill_value("off")
    assert fn.execute() == "OFF"


def test_one_tuple():
    fn = Function(one_tuple)

    assert not fn.has_options
    assert fn.has_positionals

    assert len(fn.parameters) == 1

    arg = fn.parameters[0]

    assert arg.original_type == tuple[float, float, float]
    assert arg.has_default
    assert arg.value == (1.0, 2.5, 3.1)
    assert not arg.is_option
    assert arg.underlying_type == float
    assert not arg.is_bool
    assert not arg.is_list
    assert not arg.is_literal
    assert arg.is_tuple
    assert arg.expected_values_count == 3
    assert arg.expects_many_values

    assert fn.execute() == 6.6

    arg.fill_value(1)

    with pytest.raises(Exception):
        fn.execute()

    arg.fill_value(2)

    with pytest.raises(Exception):
        fn.execute()

    arg.fill_value(3)

    assert fn.execute() == 6


def test_one_optional_list():
    fn = Function(one_optional_list)

    assert fn.has_options
    assert not fn.has_positionals

    assert len(fn.parameters) == 1

    arg = fn.parameters[0]

    assert arg.original_type == list[str]
    assert not arg.has_default
    assert arg.is_option
    assert arg.underlying_type == str
    assert not arg.is_bool
    assert arg.is_list
    assert not arg.is_literal
    assert not arg.is_tuple
    assert arg.expected_values_count == inf
    assert arg.expects_many_values

    with pytest.raises(Exception):
        fn.execute()

    arg.fill_value("one")
    assert fn.execute() == "one"

    arg.fill_value("two")
    assert fn.execute() == "one, two"

    arg.fill_value("three")
    assert fn.execute() == "one, two, three"

    arg.fill_value("four")
    assert fn.execute() == "one, two, three, four"


def test_one_positional_list():
    fn = Function(one_positional_list)

    assert not fn.has_options
    assert fn.has_positionals

    assert len(fn.parameters) == 1

    arg = fn.parameters[0]

    assert arg.original_type == list[str]
    assert not arg.has_default
    assert not arg.is_option
    assert arg.underlying_type == str
    assert not arg.is_bool
    assert arg.is_list
    assert not arg.is_literal
    assert not arg.is_tuple
    assert arg.expected_values_count == inf
    assert arg.expects_many_values

    with pytest.raises(Exception):
        fn.execute()

    arg.fill_value("one")
    assert fn.execute() == "one"

    arg.fill_value("two")
    assert fn.execute() == "one, two"

    arg.fill_value("three")
    assert fn.execute() == "one, two, three"

    arg.fill_value("four")
    assert fn.execute() == "one, two, three, four"


def test_mixed():
    fn = Function(mixed)

    assert fn.has_options
    assert fn.has_positionals

    assert len(fn.parameters) == 6

    value, name, debug, modes, count, z = fn.parameters

    assert value.original_type == float
    assert not value.has_default
    assert not value.is_option
    assert value.underlying_type == float
    assert not value.is_bool
    assert not value.is_list
    assert not value.is_literal
    assert not value.is_tuple
    assert value.expected_values_count == 1
    assert not value.expects_many_values

    assert name.original_type == str
    assert not name.has_default
    assert name.is_option
    assert name.underlying_type == str
    assert not name.is_bool
    assert not name.is_list
    assert not name.is_literal
    assert not name.is_tuple
    assert name.expected_values_count == 1
    assert not name.expects_many_values

    assert debug.original_type == bool
    assert not debug.has_default
    assert not debug.is_option
    assert debug.underlying_type == bool
    assert debug.is_bool
    assert not debug.is_list
    assert not debug.is_literal
    assert not debug.is_tuple
    assert debug.expected_values_count == 1
    assert not debug.expects_many_values

    assert modes.original_type == Literal["yes", "no"]
    assert not modes.has_default
    assert modes.is_option
    assert modes.underlying_type == str
    assert not modes.is_bool
    assert not modes.is_list
    assert modes.is_literal
    assert not modes.is_tuple
    assert modes.expected_values_count == 1
    assert not modes.expects_many_values

    assert count.original_type == int
    assert count.has_default
    assert count.value == 3
    assert not count.is_option
    assert count.underlying_type == int
    assert not count.is_bool
    assert not count.is_list
    assert not count.is_literal
    assert not count.is_tuple
    assert count.expected_values_count == 1
    assert not count.expects_many_values

    assert z.original_type == complex
    assert z.has_default
    assert z.value == complex("1-2j")
    assert z.is_option
    assert z.underlying_type == complex
    assert not z.is_bool
    assert not z.is_list
    assert not z.is_literal
    assert not z.is_tuple
    assert z.expected_values_count == 1
    assert not z.expects_many_values
