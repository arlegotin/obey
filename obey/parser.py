from __future__ import annotations
from typing import Any, Optional, Union
from .argument import Argument
from re import compile, IGNORECASE, match


class UnexpectedOption(Exception):
    def __init__(self, token: str):
        super().__init__(f'unexpected option "{token}"')


class UnexpectedPositional(Exception):
    def __init__(self, token: str):
        super().__init__(f'unexpected positional "{token}"')


class MissingArgument(Exception):
    def __init__(self, argument: Argument):
        super().__init__(
            f'missing {"positional argument" if not argument.is_option else "option"} {", ".join(argument.option_names)}'
        )


option_re = compile("^-{1,2}[a-z]", IGNORECASE)


class Parser:
    def __init__(self, parsing_map: dict[Union[int, str], Argument]):
        self.parsing_map = parsing_map

        self.fillable_argument: Optional[Argument] = None
        self.positional_counter: int = 0
        self.end_of_options: bool = False

    def reset(self) -> None:
        for arg in self.parsing_map.values():
            arg.reset_value()

        self.fillable_argument = None
        self.positional_counter = 0
        self.end_of_options = False

    @staticmethod
    def token_is_option(token: str) -> bool:
        return bool(match(option_re, token))

    def parse_tokens(self, tokens: list[str]) -> None:
        self.reset()

        for token in tokens:
            self.process_token(token)

    def process_token(self, token: str) -> None:
        if token == "--" and not self.end_of_options:
            self.end_of_options = True
            self.fillable_argument = None
            return

        if not self.end_of_options and self.token_is_option(token):
            self.fillable_argument = None

            if token not in self.parsing_map:
                raise UnexpectedOption(token)

            argument = self.parsing_map[token]

            if argument.is_bool:
                argument.fill_value(True)
            else:
                self.fillable_argument = argument
        else:
            if self.fillable_argument:
                self.fillable_argument.fill_value(token)

                if not self.fillable_argument.can_be_filled:
                    self.fillable_argument = None
            else:
                if self.positional_counter not in self.parsing_map:
                    raise UnexpectedPositional(token)

                argument = self.parsing_map[self.positional_counter]
                self.positional_counter += 1

                argument.fill_value(token)

                if argument.expects_many_values:
                    self.fillable_argument = argument
