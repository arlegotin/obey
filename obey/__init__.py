__version__ = "0.1.0"

from .command import Command
from .types.option import Option

command = Command(auto_run=True)
