from obey import command, Option

@command
def do_something(verbose: Option[bool]):
    if verbose:
        print("I'm doing something add telling you about it")