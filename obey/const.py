# Options for calling help menu
HELP_OPTIONS: list[str] = ["-h", "--help"]

# This value is used to determine whether user has provided default value or not.
# I don't want to use None because None may become a valid value in the future.
PLACEHOLDER_FOR_DEFAUL_VALUE: str = (
    "~~~ !@# value that I hope no one will ever type $&* ~~~"
)
