from obey.parameter import Parameter
from obey.const import PLACEHOLDER_FOR_DEFAUL_VALUE
import pytest
from typing import Optional, Literal, Callable
from math import inf


def test_default_placeholder():
    arg = Parameter("some_func", "some_arg", int, PLACEHOLDER_FOR_DEFAUL_VALUE)

    assert not arg.has_default
    assert arg.value is None


def test_primitives():
    func_name = "some_func"
    arg_name = "some_arg"

    for arg_type, default, some_other_value in [
        (str, "hi", "hey"),
        (int, 1, 2),
        (float, 2.718, 3.14),
        (complex, complex("3+4j"), complex("5-2j")),
    ]:
        for with_default in [False, True]:
            for is_option in [False, True]:

                if with_default:
                    if is_option:
                        arg = Parameter(func_name, arg_name, Optional[arg_type], default)
                    else:
                        arg = Parameter(func_name, arg_name, arg_type, default)

                    assert arg.value == default
                    arg.validate_value()
                else:
                    if is_option:
                        arg = Parameter(func_name, arg_name, Optional[arg_type])
                    else:
                        arg = Parameter(func_name, arg_name, arg_type)

                    assert arg.value is None

                    with pytest.raises(Exception):
                        arg.validate_value()

                assert arg.fn_name == func_name
                assert arg.original_name == arg_name

                assert arg.has_default == with_default

                assert arg.original_type == arg_type
                assert arg.args_in_type == ()

                assert arg.is_option is is_option

                assert arg.underlying_type == arg_type
                assert arg.is_bool == (arg_type is bool)
                assert not arg.is_list
                assert not arg.is_literal
                assert not arg.is_tuple

                assert arg.expected_values_count == 1
                assert not arg.expects_many_values
                assert arg.can_be_filled

                arg.fill_value(some_other_value)
                assert not arg.can_be_filled
                assert arg.value == some_other_value
                arg.validate_value()


def test_bool():
    func_name = "some_func"
    arg_name = "some_arg"

    for with_default in [False, True]:
        for is_option in [False, True]:

            if with_default:
                if is_option:
                    arg = Parameter(func_name, arg_name, Optional[bool], True)
                    assert arg.has_default
                    assert arg.value == False
                else:
                    arg = Parameter(func_name, arg_name, bool, True)
                    assert arg.has_default
                    assert arg.value == True

                arg.validate_value()
            else:
                if is_option:
                    arg = Parameter(func_name, arg_name, Optional[bool])
                    assert arg.has_default
                    assert arg.value == False
                    arg.validate_value()
                else:
                    arg = Parameter(func_name, arg_name, bool)
                    assert not arg.has_default
                    assert arg.value is None

                    with pytest.raises(Exception):
                        arg.validate_value()

            assert arg.fn_name == func_name
            assert arg.original_name == arg_name

            assert arg.original_type == bool
            assert arg.args_in_type == ()

            assert arg.is_option is is_option

            assert arg.underlying_type == bool
            assert arg.is_bool == True
            assert not arg.is_list
            assert not arg.is_literal
            assert not arg.is_tuple

            assert arg.expected_values_count == 1
            assert not arg.expects_many_values
            assert arg.can_be_filled

            arg.fill_value(True)
            assert not arg.can_be_filled
            assert arg.value == True
            arg.validate_value()


def test_list():
    func_name = "some_func"
    arg_name = "some_arg"

    for t, defaults, values in [
        (str, ["one"], ["two", "three"]),
        (int, [1, 2], [3]),
        (float, [], [0.2, 0.3, 1.4]),
        (complex, [complex("1"), complex("j"), complex("5+4j")], [complex("2")]),
        (bool, [True, False, True], [False, True]),
    ]:
        for is_option in [False, True]:
            for with_default in [False, True]:
                if with_default:
                    if is_option:
                        arg = Parameter(func_name, arg_name, Optional[list[t]], defaults)
                    else:
                        arg = Parameter(func_name, arg_name, list[t], defaults)

                    arg.validate_value()
                    assert arg.value == defaults
                else:
                    if is_option:
                        arg = Parameter(func_name, arg_name, Optional[list[t]])
                    else:
                        arg = Parameter(func_name, arg_name, list[t])

                    with pytest.raises(Exception):
                        arg.validate_value()

                assert arg.original_type == list[t]
                assert arg.args_in_type == (t,)
                assert arg.is_option is is_option

                assert arg.is_list
                assert not arg.is_literal
                assert not arg.is_tuple

                assert arg.underlying_type == t

                assert arg.expected_values_count == inf
                assert arg.expects_many_values
                assert arg.can_be_filled

                for i, value in enumerate(values):
                    arg.fill_value(value)

                    assert arg.value == values[: i + 1]
                    assert arg.can_be_filled

                arg.validate_value()


def test_tuple():
    func_name = "some_func"
    arg_name = "some_arg"

    for t, values, defaults in [
        (str, ("one", "two", "three"), ("four", "five", "six")),
        (int, (1, 2, 3), (-1, 0, -2)),
        (float, (0.2, 1.3, 5.7), (-0.6, 0.0, 40)),
        (
            complex,
            (complex("6+2j"), complex("2-2j"), complex("3j")),
            (complex("3j"), complex("2"), complex("7-1j")),
        ),
        (bool, (False, True, False), (True, True, False)),
    ]:
        for size in [1, 2, 3]:

            for is_option in [False, True]:

                for with_default in [False, True]:

                    args_for_tuple = tuple([t for _ in range(size)])
                    original_tuple = tuple[args_for_tuple]

                    if with_default:
                        if is_option:
                            arg = Parameter(
                                func_name,
                                arg_name,
                                Optional[original_tuple],
                                defaults[:size],
                            )
                        else:
                            arg = Parameter(
                                func_name, arg_name, original_tuple, defaults[:size]
                            )

                        arg.validate_value()
                        assert arg.value == defaults[:size]
                    else:
                        if is_option:
                            arg = Parameter(
                                func_name, arg_name, Optional[original_tuple]
                            )
                        else:
                            arg = Parameter(func_name, arg_name, original_tuple)

                        assert arg.value is None

                        with pytest.raises(Exception):
                            arg.validate_value()

                    assert arg.original_type == original_tuple
                    assert arg.args_in_type == args_for_tuple
                    assert arg.is_option is is_option

                    assert arg.underlying_type == t
                    assert arg.is_bool == (t is bool)
                    assert not arg.is_list
                    assert not arg.is_literal
                    assert arg.is_tuple

                    assert arg.expected_values_count == size
                    assert arg.expects_many_values == (size > 1)
                    assert arg.can_be_filled

                    for i, value in enumerate(values[:size], start=1):
                        arg.fill_value(value)

                        if size > 1:
                            assert arg.value == list(values[:i])
                        else:
                            assert arg.value == values[0]

                        if i < size:
                            assert arg.can_be_filled

                        if 1 < i < size:
                            with pytest.raises(Exception):
                                arg.validate_value()

                    assert not arg.can_be_filled
                    arg.validate_value()


def test_literal():
    func_name = "some_func"
    arg_name = "some_arg"

    args_for_literal = tuple([x for x in [1, 2, 3]])
    original_literal = Literal[args_for_literal]

    for is_option in [False, True]:
        for with_default in [False, True]:
            if with_default:
                if is_option:
                    arg = Parameter(func_name, arg_name, Optional[original_literal], 1)
                else:
                    arg = Parameter(func_name, arg_name, original_literal, 1)
            else:
                if is_option:
                    arg = Parameter(func_name, arg_name, Optional[original_literal])
                else:
                    arg = Parameter(func_name, arg_name, original_literal)

            assert arg.is_literal

            assert arg.original_type == original_literal
            assert arg.args_in_type == args_for_literal
            assert arg.has_default is with_default

            assert arg.is_option is is_option

            assert arg.underlying_type == int
            assert arg.is_bool is False
            assert not arg.is_list
            assert not arg.is_tuple

            assert arg.expected_values_count == 1
            assert not arg.expects_many_values
            assert arg.can_be_filled

            with pytest.raises(Exception):
                arg.fill_value(4)

            arg.fill_value(2)
            assert not arg.can_be_filled
            assert arg.value == 2
            arg.validate_value()


def test_nested_literals():
    arg = Parameter("some_func", "some_arg", Literal[Literal[1, 2], 3])

    assert arg.original_type == Literal[1, 2, 3]
    assert arg.args_in_type == (1, 2, 3)
    assert arg.is_literal

    arg = Parameter("some_func", "some_arg", Literal[1, Literal[Literal[2, 3], 4]])

    assert arg.original_type == Literal[1, 2, 3, 4]
    assert arg.args_in_type == (1, 2, 3, 4)
    assert arg.is_literal


def test_type_description():
    arg = Parameter("some_func", "some_arg", int)
    assert arg.type_description == "int"

    arg = Parameter("some_func", "some_arg", complex)
    assert arg.type_description == "complex"

    arg = Parameter("some_func", "some_arg", Optional[float])
    assert arg.type_description == "float"

    arg = Parameter("some_func", "some_arg", Literal["one", "two"])
    assert arg.type_description == "{one|two}"

    arg = Parameter("some_func", "some_arg", tuple[int, int, int])
    assert arg.type_description == "[int, int, int]"

    arg = Parameter("some_func", "some_arg", tuple[complex, complex])
    assert arg.type_description == "[complex, complex]"

    arg = Parameter("some_func", "some_arg", list[float])
    assert arg.type_description == "[float, ...]"


def test_invalid():
    with pytest.raises(Exception):
        Parameter("some_func", "some_arg", Callable)

    with pytest.raises(Exception):
        Parameter("some_func", "some_arg", tuple[int, float])

    with pytest.raises(Exception):
        Parameter("some_func", "some_arg", Literal)

    with pytest.raises(Exception):
        Parameter("some_func", "some_arg", Optional)


def test_filling():
    arg = Parameter("some_func", "some_arg", int)

    assert arg.value is None
    assert arg.can_be_filled

    arg.fill_value(1)
    assert arg.value == 1
    assert not arg.can_be_filled

    with pytest.raises(Exception):
        arg.fill_value(2)

    arg.reset_value()

    assert arg.value is None
    assert arg.can_be_filled

    arg.fill_value(2)
    assert arg.value == 2
    assert not arg.can_be_filled


def test_literal_filling():
    arg = Parameter("some_func", "some_arg", Literal[2, 3])

    with pytest.raises(Exception):
        arg.fill_value(4)

    arg.fill_value(2)

    assert arg.value == 2
