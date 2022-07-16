from obey import command


@command
def hello(name: str, count: int = 1):
    """
    Greets <name> given number of times
    """
    for _ in range(count):
        print(f"Hello, {name}!")
