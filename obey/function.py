from functools import cached_property
from typing import Callable, Any
from types import GeneratorType
from inspect import getfullargspec
from .parameter import Parameter
from .context import Context
from sys import stdout
from warnings import warn
from inspect import cleandoc
from .const import PLACEHOLDER_FOR_DEFAUL_VALUE


class Function:
    def __init__(self, fn: Callable):
        self.fn = fn

    @cached_property
    def doc(self) -> str:
        if self.fn.__doc__ is None:
            return ""

        return cleandoc(self.fn.__doc__)

    @cached_property
    def name(self) -> str:
        return self.fn.__name__

    @cached_property
    def parameters(self) -> list[Parameter]:
        # Get function specifications
        spec = getfullargspec(self.fn)
        # print(spec)

        # Retrieve function argument names
        names = spec.args

        # Retrieve function argument defaults and pad non-defaults
        defaults = [] if spec.defaults is None else [*spec.defaults]
        defaults = [PLACEHOLDER_FOR_DEFAUL_VALUE] * (
            len(names) - len(defaults)
        ) + defaults

        # Create Argument instances for each function argument
        parameters = []

        for (name, default) in zip(names, defaults):
            if name in spec.annotations:
                its_type = spec.annotations[name]
            else:
                its_type = str

                # warn(
                #     f'No type specified for argument "{name}" of "{self.name}". It will be interpreted as string'
                # )

            variable = Parameter(self.name, name, its_type, default)

            parameters.append(variable)

        return parameters

    def execute(self) -> Any:
        for arg in self.parameters:
            arg.validate_value()

        kwargs = {arg.original_name: arg.value for arg in self.parameters}

        result = self.fn(**kwargs)

        if isinstance(result, GeneratorType):
            return [x for x in result]
        else:
            return result

    @cached_property
    def has_options(self) -> bool:
        return any([arg.is_option for arg in self.parameters])

    @cached_property
    def has_positionals(self) -> bool:
        return any([not arg.is_option for arg in self.parameters])
