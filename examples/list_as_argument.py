from obey import command


@command
def print_out_list(names: list[str]):
    """
    Prints names separated by commas
    """

    return ", ".join(names)
