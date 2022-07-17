from obey.parameter import Parameter
from obey.const import NO_VALUE
import pytest
from math import inf

@pytest.fixture
def fn_name():
    return "some_function"


@pytest.fixture
def name():
    return "some_parameter"


@pytest.fixture
def strings():
    return ["hello", "goodbye"]


@pytest.fixture
def primitives():
    return [
        (str, ["hello", "Goodbye", "good morning", "BIG", "", "2022", "-1.4142"], ["Sunday", "short", "", "-6", "London", "New-York"]),
        (int, [-1, 0, 9, 102, 88914, 4e3], [-2000, 0, 33, 64, 2e2]),
        (float, [-1.618, -1, 0, 0.618, 2.718, 314.15, 10012], [-.004, 5.6, 10, 111]),
        (complex, [-1, 0, 1.6, complex("1"), complex("1j"), complex(".5-4j"), complex("5+0.4j")], [complex("-3"), 1, 10, complex("-9.3+4.57j")]),
    ]


def test_names(fn_name, name):
    param = Parameter(fn_name, name, str)

    assert param.fn_name == fn_name
    assert param.name == name


def test_value_placeholder(fn_name, name):
    param = Parameter(fn_name, name, str)
    assert not param.has_default

    param = Parameter(fn_name, name, str, NO_VALUE)
    assert not param.has_default

    param = Parameter(fn_name, name, str, "hello")
    assert param.has_default


def test_primitives(fn_name, name, primitives):

    for type, values, default_values in primitives:
        for with_default in [False, True]:
            for dv in default_values:
                if with_default:
                    param = Parameter(fn_name, name, type, dv)

                    assert param.is_option
                    assert param.has_default
                    assert param.value == dv
                else:
                    param = Parameter(fn_name, name, type)

                    assert not param.is_option
                    assert not param.has_default
                    assert param.value == NO_VALUE

                assert param.original_type == type
                assert param.underlying_type == type

                assert not param.is_bool
                assert not param.is_list
                assert not param.is_literal
                assert not param.is_tuple

                assert param.expected_values_count == 1
                assert not param.expects_many_values

                for value in values:
                    assert param.can_be_filled

                    param.fill_value(value)
                    assert param.value == value
                    assert not param.can_be_filled

                    param.validate_value()

                    with pytest.raises(Exception):
                        param.fill_value(values[1])

                    param.reset_value()


def test_bool_argument(fn_name, name):
    param = Parameter(fn_name, name, bool)

    assert not param.is_option
    assert not param.has_default
    assert param.value == NO_VALUE

    assert param.original_type == bool
    assert param.underlying_type == bool

    assert param.is_bool
    assert not param.is_list
    assert not param.is_literal
    assert not param.is_tuple

    assert param.expected_values_count == 1
    assert not param.expects_many_values

    for value in [True, False]:
        assert param.can_be_filled

        param.fill_value(value)
        assert param.value == value
        assert not param.can_be_filled

        param.validate_value()

        with pytest.raises(Exception):
            param.fill_value(value)

        param.reset_value()

def test_bool_option(fn_name, name):
    for dv in [False, True]:
        param = Parameter(fn_name, name, bool, dv)

        assert param.is_option
        assert param.has_default
        assert param.value == False


def test_list(fn_name, name, primitives):
    for type, values, default_values in primitives:
        for with_default in [False, True]:
            if with_default:
                param = Parameter(fn_name, name, list[type], default_values)

                assert param.is_option
                assert param.has_default
                assert param.value == default_values
            else:
                param = Parameter(fn_name, name, list[type])

                assert not param.is_option
                assert not param.has_default
                assert param.value == NO_VALUE

            assert param.original_type == list[type]
            assert param.underlying_type == type

            assert not param.is_bool
            assert param.is_list
            assert not param.is_literal
            assert not param.is_tuple

            assert param.expected_values_count == inf
            assert param.expects_many_values

            for i, value in enumerate(values):
                assert param.can_be_filled

                param.fill_value(value)
                assert param.value == values[:i+1]
                assert param.can_be_filled
