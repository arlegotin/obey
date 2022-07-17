from __future__ import annotations
from typing import Any, Optional, Union
from .parameter import Parameter
from re import compile, IGNORECASE, match


class UnexpectedOption(Exception):
    def __init__(self, token: str):
        super().__init__(f'unexpected option "{token}"')


class UnexpectedPositional(Exception):
    def __init__(self, token: str):
        super().__init__(f'unexpected positional "{token}"')


class MissingParameter(Exception):
    def __init__(self, parameter: Parameter):
        super().__init__(f'missing {"option" if parameter.is_option else "argument"}')


option_re = compile("^-{1,2}[a-z]", IGNORECASE)


class Parser:
    def __init__(self, parsing_map: dict[Union[int, str], Parameter]):
        self.parsing_map = parsing_map

        self.fillable_parameter: Optional[Parameter] = None
        self.positional_counter: int = 0
        self.end_of_options: bool = False

    def reset(self) -> None:
        for arg in self.parsing_map.values():
            arg.reset_value()

        self.fillable_parameter = None
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
            self.fillable_parameter = None
            return

        if not self.end_of_options and self.token_is_option(token):
            self.fillable_parameter = None

            if token not in self.parsing_map:
                raise UnexpectedOption(token)

            parameter = self.parsing_map[token]

            if parameter.is_bool:
                parameter.fill_value(True)
            else:
                self.fillable_parameter = parameter
        else:
            if self.fillable_parameter:
                self.fillable_parameter.fill_value(token)

                if not self.fillable_parameter.can_be_filled:
                    self.fillable_parameter = None
            else:
                if self.positional_counter not in self.parsing_map:
                    raise UnexpectedPositional(token)

                parameter = self.parsing_map[self.positional_counter]
                self.positional_counter += 1

                parameter.fill_value(token)

                if parameter.expects_many_values:
                    self.fillable_parameter = parameter
