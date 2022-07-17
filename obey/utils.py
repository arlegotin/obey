from typing import Any, Literal, Union, get_origin, get_args
from re import compile, match, IGNORECASE
from .types.option import Option

PRIMITIVE_TYPES = [str, int, float, complex, bool]


name_re = compile("^[A-Z]", IGNORECASE)


def arg_name_is_valid(name: str) -> bool:
    return bool(match(name_re, name))


def get_underlying_types(its_type: Any) -> list[Any]:
    """
    Ruturns types which constitutes given type
    """
    # its_type, _ = decompose_optional(its_type)

    if its_type in PRIMITIVE_TYPES:
        return [its_type]

    origin = get_origin(its_type)

    if origin is tuple or origin is list:
        return [x for x in get_args(its_type)]

    if origin is Literal:
        return [type(x) for x in get_args(its_type)]

    return []


def type_is_valid(its_type: Any) -> bool:
    """
    Returns True if type is valid and False if not
    """
    # its_type, _ = decompose_optional(its_type)

    if its_type in PRIMITIVE_TYPES:
        return True

    underlying_types = get_underlying_types(its_type)

    if not underlying_types:
        return False

    if any(t not in PRIMITIVE_TYPES for t in underlying_types):
        return False

    if any(t != underlying_types[0] for t in underlying_types):
        return False

    return True


def str_to_bool(v):
    """
    Converts string token into bool.
    Raises exception for invalid tokens
    """
    true_values = ("yes", "y", "true", "t", "on", "1")
    false_values = ("no", "n", "false", "f", "off", "0")

    # ( ͡° ͜ʖ ͡°)
    hidden_false_values = ("well_yes_but_actually_no", "well-yes-but-actually-no")

    if isinstance(v, bool):
        return v

    v = v.lower()

    if v in true_values:
        return True

    if v in false_values or v in hidden_false_values:
        return False

    raise RuntimeError(f'expected {"/".join(true_values)} or {"/".join(false_values)}')


def decompose_optional(given_type: Any) -> tuple[Any, bool]:
    """
    Function decomposes given type into tuple[underlying_type, True] if type is Optional.
    And decomposes into tuple[given_type, False] if type is not Optional:

    x -> x, False
    Optional[x] -> x, True

    Works with typing.Optional and obey.types.Option
    """
    if get_origin(given_type) is Union:
        parts_of_union = get_args(given_type)

        if len(parts_of_union) == 2:
            type_behind, presumably_none = parts_of_union
            if type_behind != type(None) and presumably_none == type(None):
                return type_behind, True

    if isinstance(given_type, tuple):
        if len(given_type) == 2:
            type_behind, type_name = given_type

            if type_name == Option.TYPE:
                return type_behind, True

    return given_type, False
