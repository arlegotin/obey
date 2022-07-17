from __future__ import annotations
from typing import Any, Callable, Optional, Union
from functools import reduce
from collections.abc import Generator

from .parameter import Parameter, ParameterError
from .function import Function
from .context import Context
from .const import HELP_OPTIONS


def get_main_option_name(arg: Parameter) -> Optional[str]:
    if len(arg.name) == 1:
        return None

    return "--" + arg.name.replace("_", "-")


def get_short_options(arg: Parameter) -> list[str]:
    return [
        "-" + arg.name[0],
        "-" + arg.name[0].capitalize(),
    ]


class Collection:
    def __init__(
        self,
        functions: Optional[list[Function]] = None,
        help_messages: Optional[dict[str, str]] = None,
    ):
        """
        For God's sake why can't I just write `my_func(items: list = [])` ?!
        I debugged this goddamn bug for an hour!
        WHY? (╯°□°）╯︵ ┻━┻
        There is no reason at all that it wouldn't be possible or reasonable
        to have default arguments evaluated each time the function is called.
        I'm done with this shit and switching back to JS
        """
        self.functions: list[Function] = functions if functions is not None else []
        self.help_messages_for_parameters: dict[str, str] = (
            help_messages if help_messages is not None else {}
        )

    def add_parameter_help(self, arg_name: str, help_message: str) -> None:
        self.help_messages_for_parameters[arg_name] = help_message

    def get_help_message_for_parameter(self, arg: Parameter) -> str:
        return self.help_messages_for_parameters.get(arg.name, "")

    def add_fn(self, fn: Callable) -> None:
        self.functions.append(Function(fn))

    @property
    def parameters(self) -> list[Parameter]:
        return reduce(
            lambda args, fn: args + [arg for arg in fn.parameters],
            self.functions,
            [],
        )

    @property
    def parsing_map(self) -> dict[Union[int, str], Parameter]:

        parsing_map: dict[Union[int, str], Parameter] = {}

        positional_counter: int = 0
        there_was_positional_list = False

        for arg in self.parameters:
            if arg.is_option:
                main_name = get_main_option_name(arg)

                if main_name:
                    if main_name in HELP_OPTIONS:
                        raise ParameterError(
                            arg, f"conflicts with {', '.join(HELP_OPTIONS)}"
                        )

                    if main_name in parsing_map:
                        raise ParameterError(arg, "has a conflicting name")

                    parsing_map[main_name] = arg

                for short_name in get_short_options(arg):
                    if short_name not in parsing_map and short_name not in HELP_OPTIONS:
                        parsing_map[short_name] = arg
                        break
            else:
                if there_was_positional_list:
                    raise ParameterError(arg, "cannot follow positional list")

                if arg.is_list:
                    there_was_positional_list = True

                parsing_map[positional_counter] = arg
                positional_counter += 1

        return parsing_map

    def get_option_names(self, opt: Parameter) -> list[str]:
        names: list[str] = []

        for name, arg in self.parsing_map.items():
            if arg == opt:
                names.append(str(name))

        return sorted(names, key=len)

    def execute(self) -> list[Any]:
        returned_values = []

        for fn in self.functions:
            returned_value = fn.execute()
            returned_values.append(returned_value)

        return returned_values

    def __add__(self, another_collection: Collection) -> Collection:
        return Collection(
            functions=self.functions + another_collection.functions,
            help_messages=self.help_messages_for_parameters
            | another_collection.help_messages_for_parameters,
        )

    def __str__(self) -> str:
        if not self.functions:
            return "Collection is empty"

        return "Collection of: " + ", ".join([fn.name for fn in self.functions])

    def __bool__(self) -> bool:
        return len(self.functions) > 0

    @property
    def doc_lines(self) -> list[str]:
        return list(filter(len, [fn.doc for fn in self.functions]))

    @property
    def name(self) -> str:
        if not self.functions:
            return ""

        return (self.functions[-1].name).replace("_", "-")
