from obey.command import Command
from typing import Optional


def test_empty():
    command = Command()

    assert not command.auto_run
    assert not command.collections
    assert command.shared_collection.parsing_map.keys() == {}.keys()


def test_empty_fn():
    command = Command()

    @command
    def empty_1():
        pass

    assert len(command.collections) == 2

    @command
    def empty_2():
        pass

    assert len(command.collections) == 3


def test_positional_fn():
    command = Command()

    @command
    def pos(count: int):
        pass

    assert command.collections[0].parsing_map.keys() == {0: None}.keys()


def test_option_fn():
    command = Command()

    @command
    def opt(count: Optional[int]):
        pass

    assert (
        command.collections[0].parsing_map.keys()
        == {
            "-c": None,
            "--count": None,
        }.keys()
    )


def test_for_next():
    command = Command()

    @command.for_next
    def opt_1(name: str, value: Optional[float]):
        pass

    @command
    def opt_2(name: str, count: Optional[int]):
        pass

    assert (
        command.collections[0].parsing_map.keys()
        == {
            0: None,
            "-v": None,
            "--value": None,
            1: None,
            "-c": None,
            "--count": None,
        }.keys()
    )
