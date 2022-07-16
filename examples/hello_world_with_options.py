from obey import command
from typing import Optional


@command
def hello(name: Optional[str], count: Optional[int] = 1):
    """
    Prints out greeting for given name given number of times
    """
    for _ in range(count):
        print(f"Hello, {name}!")
