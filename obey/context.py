from typing import Any


class Context:
    def __setattr__(self, name: str, value: Any) -> None:
        self.__dict__[name] = value

    def __getattr__(self, name) -> Any:
        if name not in self.__dict__:
            raise AttributeError(f'Context has no attribute "{name}"')

        return self.attrs[name]
