from __future__ import annotations
from typing import Callable, Optional, Any
import sys

from .collection import Collection
from .parser import Parser
from .const import HELP_OPTIONS
from .help import help_called, compose_collection_help, compose_group_help


class Group:
    def __init__(self, name: str, shared_collection: Optional[Collection] = None):

        # Name displayed in help menu
        self.name = name

        # Collection that will be combined with any other collection during execution
        self.shared_collection: Collection = (
            shared_collection if shared_collection is not None else Collection()
        )

        self.collections: list[Collection] = [Collection()]
        self.subgroups: list[Group] = []

    def sub(self, name: str) -> Group:
        """
        Creates a subgroup
        """
        group = Group(name=" ".join([self.name, name]))
        self.subgroups.append(group)
        return group

    def execute(self, command_line_parameters: list[str]) -> list[Any]:
        has_collections_to_choose_from = len(self.collections) > 2
        has_subgroups_to_choose_from = len(self.subgroups) > 0

        if has_collections_to_choose_from or has_subgroups_to_choose_from:
            return self.execute_one_of_many(command_line_parameters)
        else:
            return self.execute_collection(self.collections[0], command_line_parameters)

    def execute_one_of_many(self, command_line_parameters: list[str]) -> list[Any]:
        if help_called():
            raise RuntimeError(f"add subgroups to help")
            # return [
            #     compose_group_help(self.collections),
            # ]
        else:
            if not command_line_parameters:
                raise RuntimeError(f"no command specified")

            command_name = command_line_parameters.pop(0)

            for c in self.collections:
                if c.name == command_name:
                    return self.execute_collection(c, command_line_parameters)

            for g in self.subgroups:
                if g.name == command_name:
                    return self.execute(command_line_parameters)

            raise RuntimeError(f'unknown command "{command_name}"')

    def execute_collection(self, collection: Collection, command_line_parameters: list[str]) -> list[Any]:
        combined_collection = self.shared_collection + collection

        if help_called():
            return [
                compose_collection_help(combined_collection),
            ]
        else:
            parser = Parser(parsing_map=combined_collection.parsing_map)
            parser.parse_tokens(command_line_parameters)

            return combined_collection.execute()

    @property
    def current_collection(self) -> Collection:
        return self.collections[-1]

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
        self.current_collection.add_parameter_help(arg_name, help_message)

        return lambda fn: fn
