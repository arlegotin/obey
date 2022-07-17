from __future__ import annotations
from typing import Callable, Any
import atexit
import sys
from os.path import basename

from .group import Group


class Command:
    """
    A top-level class representing package interface.
    Handles execution process.
    Contains a root Group instance and reflects it's public interface.
    """

    def __init__(self, auto_run: bool = False):
        self.group = Group(name=basename(sys.argv[0]))

        self.auto_run = auto_run

        atexit.register(self.final_call)

    def final_call(self) -> None:
        if self.auto_run:
            self.run()

    def run(self) -> None:
        """
        Executes commands with sys.argv and prints out the results
        """
        returned_values = self.execute(sys.argv[1:])

        for x in returned_values:
            print(x)

    def execute(self, command_line_parameters: list[str]) -> list[Any]:
        try:
            return self.group.execute(command_line_parameters)
        except Exception as e:
            return [
                f"Error: {e}",
            ]

    def if_main(self, name: str) -> Callable:

        self.auto_run = name == "__main__"

        return lambda fn: fn

    # @property
    # def called_from_top(self) -> bool:
    #     """
    #     Returns true if parent function is being called from a top-level script
    #     """
    #     frm = inspect.stack()[2]
    #     mod = inspect.getmodule(frm[0])
    #     return mod.__name__ == "__main__"

    def __call__(self, fn: Callable) -> Callable:
        return self.group(fn)

    def sub(self, name: str) -> Group:
        return self.group.sub(name)

    def for_next(self, fn: Callable) -> Callable:
        return self.group.for_next(fn)

    def for_all(self, fn: Callable) -> Callable:
        return self.group.for_all(fn)

    def help(self, arg_name: str, help_message: str) -> Callable:
        return self.group.help(arg_name, help_message)
