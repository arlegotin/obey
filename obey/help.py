from tabulate import tabulate
import sys
from os.path import basename

from .collection import Collection
from .const import HELP_OPTIONS

CALLED_SCRIPT_NAME = basename(sys.argv[0])


def format_table(rows: list[list[str]]) -> str:
    """
    Converts rows of strings into printable table.
    Also Removes empty columns.
    """
    columns = zip(*rows)

    filled_columns = [any(c) for c in columns]

    rows = [[x for i, x in enumerate(row) if filled_columns[i]] for row in rows]

    return tabulate(rows, tablefmt="plain")


def help_called() -> bool:
    """
    Returns true when user calls help menu
    """
    return len(sys.argv) == 2 and sys.argv[1] in HELP_OPTIONS


def combine_lines_to_string(help_lines: list[str]) -> str:
    """
    Combines lines of help into final text
    """
    return "\n".join(help_lines) + "\n"


def compose_collection_help(collection: Collection) -> str:
    """
    Composes help menu for given collection
    """

    help_lines: list[str] = []

    positionals = [arg for arg in collection.arguments if not arg.is_option]
    options = [arg for arg in collection.arguments if arg.is_option]

    # Usage
    call_parts: list[str] = [CALLED_SCRIPT_NAME]

    if options or HELP_OPTIONS:
        call_parts.append("[options]")

    required = [arg for arg in positionals if not arg.has_default]
    for arg in required:
        call_parts.append(collection.format_arg_name(arg))

    not_required = [arg for arg in positionals if arg.has_default]
    if not_required:
        not_required_part = (
            "["
            + " [".join([collection.format_arg_name(arg) for arg in not_required])
            + "]" * len(not_required)
        )
        call_parts.append(not_required_part)

    help_lines += ["Usage:", " ".join(call_parts)]

    # Functions doc
    if collection.doc_lines:
        help_lines.append("")
        help_lines += collection.doc_lines

    # Arguments
    argument_parts: list[list[str]] = []
    for arg in positionals:
        line_parts = [
            collection.format_arg_name(arg),
            arg.type_description,
        ]

        line_parts.append(arg.value_description)

        line_parts.append(collection.get_help_message_for_argument(arg))

        argument_parts.append(line_parts)

    if argument_parts:
        help_lines += ["", "Arguments:"] + [format_table(argument_parts)]

    # Options
    option_parts: list[list[str]] = []
    for arg in options:
        line_parts = [
            *collection.get_option_names(arg),
            arg.type_description,
        ]

        line_parts.append(arg.value_description)

        line_parts.append(collection.get_help_message_for_argument(arg))

        option_parts.append(line_parts)

    if HELP_OPTIONS:
        option_parts.append(
            [*HELP_OPTIONS, "", "", "Show this message and exit"],
        )

    if option_parts:
        help_lines += ["", "Options:"] + [format_table(option_parts)]

    return combine_lines_to_string(help_lines)


def compose_group_help(collections: list[Collection]) -> str:
    """
    Composes help menu for group of collections
    """

    help_lines: list[str] = []

    help_lines += ["Usage:", f"{CALLED_SCRIPT_NAME} <command>"]
    help_lines += ["", "Commands:"]

    help_lines += [
        tabulate(
            [[c.name, ". ".join(c.doc_lines)] for c in collections if c],
            tablefmt="plain",
        )
    ]

    help_lines += [
        "",
        f"Use {CALLED_SCRIPT_NAME} <command> {' / '.join(HELP_OPTIONS)} for help",
    ]

    return combine_lines_to_string(help_lines)
