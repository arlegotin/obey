"""
Contains Argument type.

Current realization is a workaround which allows to write:

def main(x: Arg[int]):
    assert type(x) == int

where x is recognized as an int in function body,
wherein Obey detects x as an Argument.

Probably I should dig deeper into metaclasses and types
and make this part more elegant.
But right now it work fine.
"""

from typing import TypeVar

T = TypeVar("T")


class ArgMeta(type):
    TYPE: str = "216cbebbe29885ad4a0bf8bfe79d9d7f1fe1e186264c1f1f6d6ce6b111403a0f"

    def __getitem__(self, underlying_type: T) -> T:
        return (underlying_type, self.TYPE)  # type: ignore


class Arg(metaclass=ArgMeta):
    pass
