from obey import command
from typing import Optional


@command
def print_out_list(names: Optional[list[str]]):
    """
    Prints names separated by commas
    """
    return ", ".join(names)
