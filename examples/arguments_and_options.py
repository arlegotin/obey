from obey import command
from typing import Optional


@command
def weather(
    latitude: float,
    temperature: Optional[float],
    longitude: float = 0.12,
    humidity: Optional[int] = 68,
):
    """
    Prints out weather in given coordinates
    """
    return f"At {latitude}° N, {longitude}° W temperature is {temperature}°C, humidity is {humidity}%"
