import pytest
from obey.parameter import Parameter
from obey.collection import Collection
from typing import Optional, Literal, Union


def map_to_keys(parsing_map: dict[Union[int, str], Parameter]) -> list[Union[int, str]]:
    return list(parsing_map.keys())


def map_to_arg_names(
    parsing_map: dict[Union[int, str], Parameter]
) -> list[Union[int, str]]:
    return [arg.original_name for arg in parsing_map.values()]


def empty():
    pass


def one_unspecified(idk):
    pass


def one_positional(count: int):
    pass


def two_positionals(count: int, value: float):
    pass


def one_option(count: Optional[int]):
    pass


def two_options(count: Optional[int], value: Optional[float]):
    pass


def two_similar_options(value: Optional[float], verbose: Optional[bool]):
    pass


def three_similar_options(
    value: Optional[float], verbose: Optional[bool], volume: Optional[float]
):
    pass


def mixed(
    name: str, age: Optional[int], sex: Literal[0, 1, 2], height: Optional[float]
):
    pass


def test_empty_1():
    collection = Collection()

    assert collection.parsing_map.keys() == {}.keys()


def test_empty_2():
    collection = Collection()

    collection.add_fn(empty)

    assert collection.parsing_map.keys() == {}.keys()


def test_one_positional():
    collection = Collection()

    collection.add_fn(one_positional)

    assert collection.parsing_map.keys() == {0: None}.keys()


def test_two_positionals():
    collection = Collection()

    collection.add_fn(two_positionals)

    assert collection.parsing_map.keys() == {0: None, 1: None}.keys()

    assert map_to_arg_names(collection.parsing_map) == ["count", "value"]


def test_one_option():
    collection = Collection()

    collection.add_fn(one_option)

    assert collection.parsing_map.keys() == {"-c": None, "--count": None}.keys()


def test_two_options():
    collection = Collection()

    collection.add_fn(two_options)

    assert (
        collection.parsing_map.keys()
        == {"-c": None, "--count": None, "-v": None, "--value": None}.keys()
    )

    assert map_to_arg_names(collection.parsing_map) == [
        "count",
        "count",
        "value",
        "value",
    ]


def test_two_similar_options():
    collection = Collection()

    collection.add_fn(two_similar_options)

    assert (
        collection.parsing_map.keys()
        == {"-v": None, "--value": None, "-V": None, "--verbose": None}.keys()
    )

    assert map_to_arg_names(collection.parsing_map) == [
        "value",
        "value",
        "verbose",
        "verbose",
    ]


def test_three_similar_options():
    collection = Collection()

    collection.add_fn(three_similar_options)

    assert (
        collection.parsing_map.keys()
        == {
            "-v": None,
            "--value": None,
            "-V": None,
            "--verbose": None,
            "--volume": None,
        }.keys()
    )

    assert map_to_arg_names(collection.parsing_map) == [
        "value",
        "value",
        "verbose",
        "verbose",
        "volume",
    ]


def test_mixed():
    collection = Collection()

    collection.add_fn(mixed)

    assert (
        collection.parsing_map.keys()
        == {
            0: None,
            "-a": None,
            "--age": None,
            1: None,
            "-H": None,
            "--height": None,
        }.keys()
    )

    assert map_to_arg_names(collection.parsing_map) == [
        "name",
        "age",
        "age",
        "sex",
        "height",
        "height",
    ]


def test_combination_1():
    collection = Collection()

    collection.add_fn(empty)
    collection.add_fn(one_positional)

    assert collection.parsing_map.keys() == {0: None}.keys()


def test_combination_2():
    collection = Collection()

    collection.add_fn(one_positional)
    collection.add_fn(two_positionals)

    assert collection.parsing_map.keys() == {0: None, 1: None, 2: None}.keys()

    assert map_to_arg_names(collection.parsing_map) == ["count", "count", "value"]


def test_combination_3():
    collection = Collection()

    collection.add_fn(two_positionals)
    collection.add_fn(two_options)

    assert (
        collection.parsing_map.keys()
        == {
            0: None,
            1: None,
            "-c": None,
            "--count": None,
            "-v": None,
            "--value": None,
        }.keys()
    )

    assert map_to_arg_names(collection.parsing_map) == [
        "count",
        "value",
        "count",
        "count",
        "value",
        "value",
    ]


def test_combination_4():
    collection = Collection()

    collection.add_fn(mixed)
    collection.add_fn(two_positionals)
    collection.add_fn(two_options)

    assert (
        collection.parsing_map.keys()
        == {
            0: None,
            "-a": None,
            "--age": None,
            1: None,
            "-H": None,
            "--height": None,
            2: None,
            3: None,
            "-c": None,
            "--count": None,
            "-v": None,
            "--value": None,
        }.keys()
    )

    assert map_to_arg_names(collection.parsing_map) == [
        "name",
        "age",
        "age",
        "sex",
        "height",
        "height",
        "count",
        "value",
        "count",
        "count",
        "value",
        "value",
    ]


def test_combination_5():
    collection = Collection()

    collection.add_fn(two_options)
    collection.add_fn(two_options)

    with pytest.raises(Exception):
        collection.parsing_map


def test_addition():
    collection_a = Collection()
    collection_b = Collection()

    collection_a.add_fn(two_positionals)
    collection_b.add_fn(two_options)

    collection_c = collection_a + collection_b

    assert (
        collection_c.parsing_map.keys()
        == {
            0: None,
            1: None,
            "-c": None,
            "--count": None,
            "-v": None,
            "--value": None,
        }.keys()
    )

    assert map_to_arg_names(collection_c.parsing_map) == [
        "count",
        "value",
        "count",
        "count",
        "value",
        "value",
    ]
