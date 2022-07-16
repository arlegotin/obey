from obey import command, Option


@command
def hello(name: Option[str], count: Option[int] = 1):
    """
    Prints out greeting for given name given number of times
    """
    for _ in range(count):
        print(f"Hello, {name}!")
