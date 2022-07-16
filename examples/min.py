from obey import command


@command
def find_min(values: list[float]):
    print(f"Min value is {min(values)}")
