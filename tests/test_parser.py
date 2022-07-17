import pytest
from obey.parameter import Parameter
from obey.collection import Collection
from obey.parser import Parser
from obey.const import NO_DEFAUL_VALUE
from typing import Optional, Literal, Union


def one_positional(count: int):
    pass


def two_positionals(one: float, two: float):
    pass


def one_default_positional(x: str = "hello"):
    pass


def two_default_positional(x: float = 0.5, y: float = 0.7):
    pass


def two_positionals_with_one_default(x: float, y: str = "hello"):
    pass


def one_option(age: Optional[float]):
    pass


def two_options(name: Optional[str], height: Optional[float]):
    pass


def two_options_with_one_default(filename: Optional[str], size: Optional[int] = 128):
    pass


def positional_and_two_options_with_default(
    city: str,
    population: Optional[int],
    size: float = 99,
    distance: Optional[float] = 50,
):
    pass


def positional_list(values: list[int]):
    pass


def positional_list_before_another_positional(values: list[int], x: int):
    pass


def positional_list_after_another_positional(x: int, values: list[int]):
    pass


def positional_tuple(coords: tuple[float, float, float]):
    pass


def option_list(values: Optional[list[float]]):
    pass


def option_tuple(coords2d: Optional[tuple[float, float]]):
    pass


def test_empty_collection():
    for tokens in [["1"], ["-c", "1"]]:
        collection = Collection()

        parser = Parser(parsing_map=collection.parsing_map)

        with pytest.raises(Exception):
            parser.parse_tokens(tokens)


def positional_and_option(names: list[str], values: Optional[list[float]]):
    pass


def test_empty_tokens():
    collection = Collection()

    collection.add_fn(one_positional)

    parser = Parser(parsing_map=collection.parsing_map)

    parser.parse_tokens([])

    with pytest.raises(Exception):
        collection.execute()


def test_empty_collection_and_tokens():
    collection = Collection()

    parser = Parser(parsing_map=collection.parsing_map)

    parser.parse_tokens([])


def test_one_positional():
    collection = Collection()

    collection.add_fn(one_positional)

    parser = Parser(parsing_map=collection.parsing_map)

    parser.parse_tokens(["1"])

    assert collection.parameters[0].value == 1


def test_two_positionals():
    collection = Collection()

    collection.add_fn(two_positionals)

    parser = Parser(parsing_map=collection.parsing_map)

    parser.parse_tokens([])

    with pytest.raises(Exception):
        collection.execute()

    parser.parse_tokens(["2.5"])

    with pytest.raises(Exception):
        collection.execute()

    parser.parse_tokens(["2.5", "3.5"])
    collection.execute()

    assert collection.parameters[0].value == 2.5
    assert collection.parameters[1].value == 3.5


def test_one_default_positional():
    collection = Collection()

    collection.add_fn(one_default_positional)

    parser = Parser(parsing_map=collection.parsing_map)

    assert collection.parameters[0].value == "hello"

    parser.parse_tokens(["bye"])

    assert collection.parameters[0].value == "bye"


def test_two_default_positional():
    collection = Collection()

    collection.add_fn(two_default_positional)

    parser = Parser(parsing_map=collection.parsing_map)

    assert collection.parameters[0].value == 0.5
    assert collection.parameters[1].value == 0.7

    parser.parse_tokens([".1"])

    assert collection.parameters[0].value == 0.1
    assert collection.parameters[1].value == 0.7

    parser.parse_tokens([".3", "-.8"])

    assert collection.parameters[0].value == 0.3
    assert collection.parameters[1].value == -0.8


def test_two_positionals_with_one_default():
    collection = Collection()

    collection.add_fn(two_positionals_with_one_default)

    parser = Parser(parsing_map=collection.parsing_map)

    assert collection.parameters[0].value == NO_DEFAUL_VALUE
    assert collection.parameters[1].value == "hello"

    parser.parse_tokens([])

    with pytest.raises(Exception):
        collection.execute()

    parser.parse_tokens([".99"])
    collection.execute()

    assert collection.parameters[0].value == 0.99
    assert collection.parameters[1].value == "hello"

    parser.parse_tokens([".99", "bye"])
    collection.execute()

    assert collection.parameters[0].value == 0.99
    assert collection.parameters[1].value == "bye"


def test_one_option():
    collection = Collection()

    collection.add_fn(one_option)

    parser = Parser(parsing_map=collection.parsing_map)

    parser.parse_tokens([])

    for tokens in [[], ["-a"]]:
        parser.parse_tokens(tokens)

        with pytest.raises(Exception):
            collection.execute()

    for tokens in [["-w"], ["-w", "2"], ["-a", "no"]]:

        with pytest.raises(Exception):
            parser.parse_tokens(tokens)

    for tokens in [["-a", "2"], ["--age", "2"]]:

        parser.parse_tokens(tokens)
        collection.execute()

        assert collection.parameters[0].value == 2

    for tokens in [["-a", "-3"], ["--age", "-3.0"], ["-a", "-3."]]:

        parser.parse_tokens(tokens)
        collection.execute()

        assert collection.parameters[0].value == -3


def test_two_options():
    collection = Collection()

    collection.add_fn(two_options)

    parser = Parser(parsing_map=collection.parsing_map)

    with pytest.raises(Exception):
        parser.parse_tokens(["Brian", "176"])

    for tokens in [
        [],
        ["-n"],
        ["-n", "Brian"],
        ["-H"],
        ["-H", "176"],
    ]:
        parser.parse_tokens(tokens)

        with pytest.raises(Exception):
            collection.execute()

    for tokens in [
        ["-n", "Brian", "-H", "176"],
        ["-H", "176", "-n", "Brian"],
        ["--height", "176", "-n", "Brian"],
        ["--height", "176", "--name", "Brian"],
    ]:

        parser.parse_tokens(tokens)

        assert collection.parameters[0].value == "Brian"
        assert collection.parameters[1].value == 176


def test_two_options_with_one_default():
    collection = Collection()

    collection.add_fn(two_options_with_one_default)

    parser = Parser(parsing_map=collection.parsing_map)

    for tokens in [
        [],
        ["-s", "16"],
        ["--size", "256"],
    ]:
        parser.parse_tokens(tokens)

        with pytest.raises(Exception):
            collection.execute()

    for tokens in [
        ["-f", "image.png"],
        ["--filename", "image.png"],
    ]:

        parser.parse_tokens(tokens)

        assert collection.parameters[0].value == "image.png"
        assert collection.parameters[1].value == 128

    for tokens in [
        ["-f", "image.png", "-s", "32"],
        ["-s", "32", "--filename", "image.png"],
        ["--size", "32", "-f", "image.png"],
        ["--filename", "image.png", "--size", "32"],
    ]:

        parser.parse_tokens(tokens)

        assert collection.parameters[0].value == "image.png"
        assert collection.parameters[1].value == 32


def test_positional_and_two_options_with_default():
    collection = Collection()

    collection.add_fn(positional_and_two_options_with_default)

    parser = Parser(parsing_map=collection.parsing_map)

    for tokens in [
        [],
        ["London"],
        ["-p", "10"],
    ]:
        parser.parse_tokens(tokens)

        with pytest.raises(Exception):
            collection.execute()

    for tokens in [
        ["London", "-p", "300"],
    ]:

        parser.parse_tokens(tokens)

        assert collection.parameters[0].value == "London"
        assert collection.parameters[1].value == 300
        assert collection.parameters[2].value == 99
        assert collection.parameters[3].value == 50

    for tokens in [
        ["Canberra", "101", "-p", "600", "-d", "25"],
        ["Canberra", "-p", "600", "101", "-d", "25"],
        ["-d", "25", "Canberra", "-p", "600", "101"],
        ["--distance", "25", "--population", "600", "Canberra", "101"],
    ]:

        parser.parse_tokens(tokens)

        assert collection.parameters[0].value == "Canberra"
        assert collection.parameters[1].value == 600
        assert collection.parameters[2].value == 101
        assert collection.parameters[3].value == 25


def test_combination_1():
    collection = Collection()

    collection.add_fn(two_options_with_one_default)
    collection.add_fn(two_positionals_with_one_default)

    parser = Parser(parsing_map=collection.parsing_map)

    for tokens in [
        ["-f", "video.mp4", "2.2"],
        ["2.2", "-f", "video.mp4"],
    ]:

        parser.parse_tokens(tokens)

        assert collection.parameters[0].value == "video.mp4"
        assert collection.parameters[1].value == 128
        assert collection.parameters[2].value == 2.2
        assert collection.parameters[3].value == "hello"

    for tokens in [
        ["-f", "video.mp4", "2.2", "-s", "10", "bye"],
        ["2.2", "bye", "--size", "10", "--filename", "video.mp4"],
    ]:

        parser.parse_tokens(tokens)

        assert collection.parameters[0].value == "video.mp4"
        assert collection.parameters[1].value == 10
        assert collection.parameters[2].value == 2.2
        assert collection.parameters[3].value == "bye"


def test_quotes():
    collection = Collection()

    collection.add_fn(one_default_positional)

    parser = Parser(parsing_map=collection.parsing_map)

    parser.parse_tokens(["two words"])

    assert collection.parameters[0].value == "two words"


def test_positional_list():

    collection = Collection()

    collection.add_fn(positional_list)

    parser = Parser(parsing_map=collection.parsing_map)

    values = []
    for i in range(10):
        values.append(i)

        parser.parse_tokens([str(x) for x in values])

        assert collection.parameters[0].value == values


def test_positional_list_before_another_positional():
    collection = Collection()

    collection.add_fn(positional_list_before_another_positional)

    with pytest.raises(Exception):
        collection.parsing_map


def test_positional_list_after_another_positional():
    collection = Collection()

    collection.add_fn(positional_list_after_another_positional)

    parser = Parser(parsing_map=collection.parsing_map)

    values = []
    for i in range(10):
        values.append(i)

        parser.parse_tokens(["20"] + [str(x) for x in values])

        assert collection.parameters[0].value == 20
        assert collection.parameters[1].value == values


def test_positional_tuple():
    collection = Collection()

    collection.add_fn(positional_tuple)

    parser = Parser(parsing_map=collection.parsing_map)

    parser.parse_tokens([])

    with pytest.raises(Exception):
        collection.execute()

    parser.parse_tokens([".2"])

    with pytest.raises(Exception):
        collection.execute()

    parser.parse_tokens([".2", ".3"])

    with pytest.raises(Exception):
        collection.execute()

    parser.parse_tokens([".2", ".3", ".4"])
    assert collection.parameters[0].value == [0.2, 0.3, 0.4]


def test_option_list():
    collection = Collection()

    collection.add_fn(option_list)

    parser = Parser(parsing_map=collection.parsing_map)

    parser.parse_tokens([])

    with pytest.raises(Exception):
        collection.execute()

    with pytest.raises(Exception):
        parser.parse_tokens([".1", "1.", ".0001"])

    parser.parse_tokens(["-v", ".1", "1."])
    assert collection.parameters[0].value == [0.1, 1.0]

    parser.parse_tokens(["-v", ".1", "1.", ".0001"])
    assert collection.parameters[0].value == [0.1, 1.0, 0.0001]

    parser.parse_tokens(["-v", ".1", "1.", ".0001", "999.08"])
    assert collection.parameters[0].value == [0.1, 1.0, 0.0001, 999.08]

    parser.parse_tokens(["-v", "1", "-v", "2", "-v", "3"])
    assert collection.parameters[0].value == [1, 2, 3]


def test_option_tuple():
    collection = Collection()

    collection.add_fn(option_tuple)

    parser = Parser(parsing_map=collection.parsing_map)

    parser.parse_tokens([])

    with pytest.raises(Exception):
        collection.execute()

    with pytest.raises(Exception):
        parser.parse_tokens(["5.5", ".77"])

    parser.parse_tokens(["-c", "5.5"])

    with pytest.raises(Exception):
        collection.execute()

    parser.parse_tokens(["-c", "5.5", ".77"])
    assert collection.parameters[0].value == [5.5, 0.77]

    parser.parse_tokens(["--coords2d", "2", "4"])
    assert collection.parameters[0].value == [2, 4]


def test_positional_and_option():
    collection = Collection()

    collection.add_fn(positional_and_option)

    parser = Parser(parsing_map=collection.parsing_map)

    parser.parse_tokens([])

    with pytest.raises(Exception):
        collection.execute()

    parser.parse_tokens(["Joe"])

    with pytest.raises(Exception):
        collection.execute()

    parser.parse_tokens(["-v"])

    with pytest.raises(Exception):
        collection.execute()

    parser.parse_tokens(["Joe", "-v"])

    with pytest.raises(Exception):
        collection.execute()

    with pytest.raises(Exception):
        parser.parse_tokens(["-v", "Joe"])

    parser.parse_tokens(["Jane", "Joe", "-v", "1"])
    assert collection.parameters[0].value == ["Jane", "Joe"]
    assert collection.parameters[1].value == [1]

    with pytest.raises(Exception):
        parser.parse_tokens(["Jane", "Joe", "--", "-v", "1"])

    with pytest.raises(Exception):
        parser.parse_tokens(["-v", "1", "2", "Jane"])

    parser.parse_tokens(["-v", "1", "2", "--", "Jane"])
    assert collection.parameters[0].value == ["Jane"]
    assert collection.parameters[1].value == [1, 2]
