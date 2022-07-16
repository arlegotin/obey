"""
Contains Option type.

Current realization is a workaround which allows to write:

def main(x: Option[int]):
    assert type(x) == int

where x is recognized as an int in function body,
wherein Obey detects x as an Option.

Probably I should dig deeper into metaclasses and types
and make this part more elegant.
But right now it work fine.
"""

from typing import Any, TypeVar


T = TypeVar("T")


class OptionMeta(type):
    TYPE: str = "option type: value that I hope no one will ever type $&*~!@#"

    def __getitem__(self, underlying_type: T) -> T:
        return (underlying_type, self.TYPE)  # type: ignore


class Option(metaclass=OptionMeta):
    pass
