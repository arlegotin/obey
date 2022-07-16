from typing import Optional, Any, Literal, Union, get_origin, get_args
from functools import cached_property
from math import inf
from .utils import (
    str_to_bool,
    decompose_optional,
    type_is_valid,
    get_underlying_types,
    name_is_valid,
)
from .const import PLACEHOLDER_FOR_DEFAUL_VALUE


class Argument:
    def __init__(
        self, fn_name: str, name: str, its_type: Any, default: Optional[Any] = None
    ):
        if not name_is_valid(name):
            raise NameError(f'Invalid argument name "{name}" of "{fn_name}"')

        self.fn_name = fn_name
        self.original_name = name

        if not type_is_valid(its_type):
            raise ArgumentError(self, f'has invalid type "{its_type}"')

        self.original_type, self.is_option = decompose_optional(its_type)
        self.underlying_type = get_underlying_types(its_type)[0]

        if default == PLACEHOLDER_FOR_DEFAUL_VALUE:
            default = None

        if self.original_type is bool and self.is_option and default is None:
            default = False

        self.default = default
        self.filled_value: Any = None

    def cast(self, value: Any) -> Any:
        if self.is_bool:
            return str_to_bool(value)

        try:
            value = self.underlying_type(value)
        except ValueError:
            raise ArgumentError(self, f'cannot be casted from "{value}"')

        if self.is_literal:
            if value not in self.args_in_type:
                raise ArgumentError(
                    self, f'got "{value}", but should be {self.type_description}'
                )

        return value

    @property
    def can_be_filled(self) -> bool:
        if self.filled_value is None:
            return True

        if self.expects_many_values:
            return len(self.filled_value) < self.expected_values_count

        return False

    def reset_value(self) -> None:
        self.filled_value = None

    def fill_value(self, value: Any) -> None:
        if not self.can_be_filled:
            raise ArgumentError(self, f"already has a value")

        if self.expects_many_values:
            if self.filled_value is None:
                self.filled_value = []

            self.filled_value.append(self.cast(value))

        else:
            self.filled_value = self.cast(value)

    def validate_value(self) -> None:
        if not self.has_default and self.value is None:
            raise ArgumentError(self, "is required")

        if 1 < self.expected_values_count < inf:
            if len(self.value) != self.expected_values_count:
                raise ArgumentError(
                    self,
                    f"got {len(self.value)} values, but expects {self.expected_values_count}",
                )

    @property
    def value(self) -> Any:
        if self.filled_value is not None:
            return self.filled_value

        if self.has_default:
            return self.default

        return None

    def __repr__(self) -> str:
        parts = []

        if not self.has_default:
            parts.append("required")

        parts.append("positional" if not self.is_option else "option")

        if self.has_default:
            parts.append(f"{self.original_name}:{self.type_description}={self.default}")
        else:
            parts.append(f"{self.original_name}:{self.type_description}")

        if self.expects_many_values:
            if self.expected_values_count == inf:
                parts.append("takes any number of values")
            else:
                parts.append(f"takes {self.expected_values_count} values")

        return " ".join(parts)

    @cached_property
    def type_origin(self) -> Any:
        return get_origin(self.original_type)

    @cached_property
    def is_literal(self) -> bool:
        return self.type_origin is Literal

    @cached_property
    def is_tuple(self) -> bool:
        return self.type_origin is tuple

    @cached_property
    def is_list(self) -> bool:
        return self.type_origin is list

    @cached_property
    def is_bool(self) -> bool:
        return self.underlying_type is bool

    @cached_property
    def args_in_type(self) -> tuple[Any, ...]:
        return get_args(self.original_type)

    @cached_property
    def has_default(self) -> bool:
        return self.default is not None

    @cached_property
    def type_description(self) -> str:
        if self.is_literal:
            possible_values = [str(x) for x in self.args_in_type]
            return "{" + "|".join(possible_values) + "}"

        if self.is_tuple:
            possible_values = [self.underlying_type.__name__ for _ in self.args_in_type]
            return f'[{", ".join(possible_values)}]'

        if self.is_list:
            return f"[{self.underlying_type.__name__}, ...]"

        if self.is_bool:
            return "y/n"

        return self.underlying_type.__name__

    @cached_property
    def value_description(self) -> str:
        if self.has_default:
            if self.is_bool:
                return f"default: {'y' if self.value else 'n'}"
            else:
                return f"default: {self.value}"

        return "required"

    @cached_property
    def expected_values_count(self) -> Union[int, float]:
        if self.is_tuple:
            return len(self.args_in_type)

        if self.is_list:
            return inf

        return 1

    @cached_property
    def expects_many_values(self) -> bool:
        return self.expected_values_count > 1


class ArgumentError(Exception):
    def __init__(self, arg: Argument, message: str):
        prefix = f'{"Option" if arg.is_option else "Argument"} "{arg.original_name}" of "{arg.fn_name}"'
        super().__init__(f"{prefix} {message}")
