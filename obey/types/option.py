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

from typing import TypeVar

T = TypeVar("T")


class OptionMeta(type):
    TYPE: str = "2d5e1b80700aa5f7feee626bec13643667af0f0f37099909ad8456c43d93a469"

    def __getitem__(self, underlying_type: T) -> T:
        return (underlying_type, self.TYPE)  # type: ignore


class Option(metaclass=OptionMeta):
    pass
