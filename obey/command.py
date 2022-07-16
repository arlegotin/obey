from __future__ import annotations
from typing import Callable, Optional
import atexit
import sys
import inspect

from .collection import Collection
from .parser import Parser
from .const import HELP_OPTIONS
from .help import help_called, compose_collection_help, compose_group_help


class Command:
    def __init__(self, shared_collection: Optional[Collection] = None, auto_run=False):
        self.shared_collection = (
            shared_collection if shared_collection is not None else Collection()
        )
        self.collections: list[Collection] = []
        self.auto_run = auto_run

        atexit.register(self.final_call)

    def final_call(self):
        if self.auto_run:
            self.execute()

    def if_main(self, name: str) -> Callable:

        self.auto_run = name == "__main__"

        return lambda fn: fn

    def execute(self) -> None:
        try:
            if len(self.collections) > 2:
                self.execute_one_of_many()
            else:
                self.execute_collection(self.collections[0])
        except Exception as e:
            print(e)

            if HELP_OPTIONS:
                print(f"Use {', '.join(HELP_OPTIONS)} for help")

    def execute_one_of_many(self):
        if help_called():
            print(compose_group_help(self.collections))
        else:
            if len(sys.argv) < 2:
                raise RuntimeError(f"No command specified")

            command_name = sys.argv.pop(1)

            for c in self.collections:
                if c.name == command_name:
                    self.execute_collection(c)
                    return

            raise RuntimeError(f'Unknown command "{command_name}"')

    def execute_collection(self, collection: Collection):
        combined_collection = self.shared_collection + collection

        if help_called():
            print(compose_collection_help(combined_collection))
        else:
            parser = Parser(parsing_map=combined_collection.parsing_map)
            parser.parse_tokens(sys.argv[1:])

            returned_values = combined_collection.execute()
            message_to_print = "\n".join(
                [str(v) for v in returned_values if v is not None]
            )

            if message_to_print:
                print(message_to_print)

    @property
    def current_collection(self) -> Collection:
        if not self.collections:
            self.collections.append(Collection())

        return self.collections[-1]

    @property
    def called_from_top(self) -> bool:
        """
        Returns true if parent function is being called from a top-level script
        """
        frm = inspect.stack()[2]
        mod = inspect.getmodule(frm[0])
        return mod.__name__ == "__main__"

    def __call__(self, fn: Callable) -> Callable:
        self.current_collection.add_fn(fn)
        self.collections.append(Collection())

        return fn

    def for_next(self, fn: Callable) -> Callable:
        self.current_collection.add_fn(fn)

        return fn

    def for_all(self, fn: Callable) -> Callable:
        self.shared_collection.add_fn(fn)

        return fn

    def help(self, arg_name: str, help_message: str) -> Callable:
        self.current_collection.add_argument_help(arg_name, help_message)

        return lambda fn: fn
