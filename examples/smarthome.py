from obey import command
from typing import Literal

@command
def switch(device: Literal['wifi', 'bedroom light', 'heater'], state: bool):
    if state:
        print(f"{device} is turned on")
    else:
        print(f"{device} is turned off")
