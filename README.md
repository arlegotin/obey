# Obey

> ⚠️ Obey is still in beta. Bugs are possible

Obey is a Python package for creating **command line interfaces**.

Obey leverages Python synthax so developers could keep the code **concise and readable**.

Obey produces **easy to use** CLI: detailed help and autocompletion for all shells.

### Extremely easy start

Install Obey directly from PyPI:
```console
pip install obey
```

Add just two lines of code – import and decorator call – to an existing app:

```python
from obey import command

@command
def hello(name: str, count: int = 1):
    for _ in range(count):
        print(f"Hello, {name}!")
```

### Unhindered growth in complexity

Branch, combine and pipe commands in any form – Obey will take on all the complexity.
Here are some features:
- type validation
- help generation
- command branching
- command combination 
- command piping
  
...and more. Check out [the examples](#).

### Clarity as a basic principle
At every scenario Obey keeps things as simple as possible, exposing no more complexity than needed to complete the task.

Probably, this is one of the reasons [why you should prefer Obey](#) over Typer, Click, Fire or argparse.

Intrigued? So let's dive in.

## Table of contents

1. [Basics](#1-basics)
   - Create the first command
   - Arguments
   - Options
   - Types
     - Primitives
     - Bool
     - Literal
     - List
     - Tuple
   - Returned value
2. Firing
3. Command branching
   - One level
   - To infinity and beyond
4. Command combination
   - Combine with the next
   - Combine with all
5. Command piping
6. Help generation
7. Why should I prefer Obey over Typer, Click, Fire or argparse?
8. More examples
9.  Contribution

## 1. Basics

First, let's see how to make simple script that can take parameters.

### Create the first command

Obey creates commands by decorating functions with `@command` decorator:

```python
# hello.py
from obey import command

@command
def say_hi():
    print("Hello, world!")
```

That's all, we can run it:

```console
python hello.py
Hello, world!
```

Congratulations! We just made our first CLI. It doesn't do much though.

In general script can contain multiple commands.

For now, let's stick with single-command scripts. We'll back to multiple commands [a bit later](#).

Obey commands supports two types of parameters: arguments and options.

### Arguments

Let's make our script a bit more interactive and allow user pass a name.

Script arguments are parsed from the arguments of the decorated function:

```python
@command
def say_hi(name):
    print(f"Hello, {name}!")
```

Let's try to run the script as before:

```console
python hello.py
Argument "name" of "say_hi" is required
Use -h, --help for help
```

Oops. We got an error.

Let's check the help page that Obey [autmatically generated]():

```console
python hello.py -h
Usage:
hello.py [options] <name>

Arguments:
<name>  str  required

Options:
-h  --help  Show this message and exit
```

As we can see, `hello.py` has a reqired argument `<name>` now.

Indeed, since argument `name` is required for the function, it becomes required for the script as well:

```console
python hello.py Brian
Hello, Brian!
```

Of course, the argument can have a default value if we want.

Let's add functionality to our script so it could print the greeting many times:

```python
@command
def say_hi(name, count: int = 1):
    for _ in range(count):
        print(f"Hello, {name}!")
```

And call it:

```console
python hello.py Brian
Hello, Brian!

python hello.py Brian 3
Hello, Brian!
Hello, Brian!
Hello, Brian!
```

As you can see, `say_hi` uses the default value for `count` if it was not passed into command. And help page confirms it:

```console
python hello.py -h
Usage:
hello.py [options] <name> [<count>]

Arguments:
<name>   str  required
<count>  int  default: 1

Options:
-h  --help  Show this message and exit
```

You might also notice that in addition to the default value we added a type hint `int`.

This is because by default Obey interprets all arguments as a strings. We should provide a proper type hint for the argument if we don't want to get an exeption in runtime.

Argument value is validated within it's type:
```console
python hello.py Brian three
Argument "count" of "say_hi" cannot be casted from "three"
```

We'll discuss types in more detail [below]().

### Options

Options are similar to arguments. The difference is that option value must be preceded by its it's name when the command is being called. Like so:

```console
git commit -m "Hotfix"
ffmpeg -i /path/to/the/video.mp4
ls -a
```

`-m`, `-i` and `-a` are options in these examples.

Let's rewrite our previous command so it could accept options. We'll use `obey.Option` for that:

```python
from obey import command, Option

def say_hi(name: Option[str], count: Option[int] = 1):
    for _ in range(count):
        print(f"Hello, {name}!")
```

Let's check help page to see how to use this command now:

```console
python hello.py -h
Usage:
hello.py [options]

Options:
-n  --name   str  required
-c  --count  int  default: 1
-h  --help                    Show this message and exit
```

As we can see, Obey has parsed option names and make it possible to address them with a short name `-n` along with a long name `--name`.

All right, let's try it:

```console
python hello.py -n Brian
Hello, Brian!

python hello.py -n Brian -c 3
Hello, Brian!
Hello, Brian!
Hello, Brian!
```

We can address options with short and long names in any order:
```console
python hello.py --name Emmy
Hello, Emmy!

python hello.py --count 3 -n Emmy
Hello, Emmy!
Hello, Emmy!
Hello, Emmy!
```

And of course, options, like arguments, are also validated:
```console
python hello.py
Option "name" of "say_hi" is required

python hello.py -n Emmy -c ten
Option "count" of "say_hi" cannot be casted from "ten"
```

### Types

As we have seen, it's a good practice to provide type hints for arguments and options, avoiding manual casting and runtime exceptions.

Let's see what types commands can take.

#### Primitives

Any argument or option can have one of this types:
- `str`
- `int`
- `float`
- `complex`
- `bool`

And it works as straight forward as it sounds:
  
```python
@command
def add(x: float, y: float):
    return x + y

@command
def pow(x: float, n: int = 2):
    return x ** n

@command
def multiply_complex(x: complex, y: complex):
    return x * y

@command
def set_logging_level(debug: Option[bool]):
    if debug:
        logger.setLevel(logging.DEBUG)
```

The only exeption here is `bool`, that has a slightly different behavior.

#### Bool argument

Unlike other primitives, argument bool can be casted from a wider range of values:
`yes`, `y`, `true`, `t`, `on`, `1` for `True`,
`no`, `n`, `false`, `f`, `off`, `0` for `False`:

```python
# turing_test.py

@command
def are_you_human(are_you: bool):
    if are_you:
        print("You are human")
    else:
        print("You are robot")
```

```
python turing_test.py yes
You are human

python turing_test.py 1
You are human

python turing_test.py n
You are robot

python turing_test.py off
You are robot
```

#### Bool option

The second difference is that option bool acts like a flag.

In other words, it always has a default value `False`. And option will take a value `True` whenever flag is specified.

Let's take a look a quick example:

```python
@command
def do_something(verbose: Option[bool]):
    if verbose:
        print("I'm doing something add telling you about it")
```

Let's check help menu:

```console
python do_something.py -h
Usage:
do_something.py [options]

Options:
-v  --verbose
-h  --help     Show this message and exit
```

And try to call it:

```console
python do_something.py

python do_something.py -v
I'm doing something add telling you about it
```

Notice that attempt to specify a value for a bool option `-v yes` or `-v no` will raise exeption.

#### Literal

It is also possible that we want to limit the range of values for our option or argument.

In this case we'll use Python built-in `typing.Literal`:

```python
# smarthome.py
from obey import command
from typing import Literal

@command
def switch(device: Literal['wifi', 'bedroom light', 'heater'], state: bool):
    if state:
        print(f"{device}")
```

Let's check how to use out smarthome app:
```console
Usage:
smarthome.py [options] <device> <state>

Arguments:
<device>  {wifi|bedroom light|heater}  required
<state>   y/n                          required

Options:
-h  --help  Show this message and exit
```

And it work as expected:
```console
python smarthome.py wifi on
wifi is turned on

python smarthome.py "bedroom light" off
bedroom light is turned off

python smarthome.py heater 1
heater is turned on

python smarthome.py kettle on
Argument "device" of "switch" got "kettle", but should be {wifi|bedroom light|heater}
```

Currently Obey does not support Literal with different types. Argument type `Literal["hello", 1]` will raise an exception.

#### List

We can provide an indefinite number of values for one option or argument using Python `list`:

```python
@command
def min(values: list[float]):
    print(f"Min. value is {min(values)}")
```
```console
python min.py 0.618 1 2.718 3.14
Min. value is 0.618
```

Notice that list cannot be empty:
```console
python min.py
Argument "values" of "min" is required
```

If the absence of values is the expected behavior, we can handle it by providing a default value:
```python
@command
def sum_numbers(values: list[float] = []):
    if not list:
        print("Sum is zero")

    print(f"Sum is {sum(values)}")
```

```console
python sum.py
Sum is zero

python sum.py 1 2 3
Sum is 6.0
```

#### Tuple

We can provide a fixed number of values for one option or argument using Python `tuple`:

```python
@command
def cross_product(a: tuple[float, float, float], b: tuple[float, float, float]):
    a1, a2, a3 = a
    b1, b2, b3 = b

    c = [a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1]

    return f"a × b = {c}"
```

```console
python cross_product.py -h
cross_product.py [options] <a> <b>

Arguments:
<a>  [float, float, float]  required
<b>  [float, float, float]  required

Options:
-h  --help  Show this message and exit
```

As we can see, vector product is defined only for three-dimensional vectors (which is true):

```console
python cross_product.py 1 2 3 4 5 6
a × b = [-3.0, 6.0, -3.0]

python cross_product.py 1 2 3 4 5
Argument "b" of "cross_product" got 2 values, but expects 3

python cross_product.py 1 2 3 4 5 6 7
Unexpected positional "7"
```

Currently Obey does not support tuples with different types. Argument type `tuple[float, string]` will raise an exception.

### Returned value
So far, all commands that we saw displayed the result using `print`. Which is not always a good idea: those functions are hard to test.

It would be nice if our commands could be testable, while CLI user could see the result on the screen.

That's why Obey takes a function execution result, validates it according to the function returning type and prints it out:

```python
@command
def sum_numbers(values: list[float] = []) -> float:
    if not list:
        return 0

    return sum(values)
```

For CLI user our command works as expected:
```console
python sum.py 1 2 3
6.0
```
While developer can import this function to test it:
```python
# tests/test_sum.py
from my_package import sum_numbers

def test_sum_numbers():
    assert sum_numbers([1, 2, 3]) == 6
```

## Firing

As you probably already noticed, Obey executes commands without checking `__name__ == '__main__'` or so. This is bacause Obey tries to determine when to run the command and when not.

For most cases this is the most natural and handy behavior. And of course, this behavior can be changed.

Let's see how it works and how we can control it.

Assume we have a file `app.py` containing a single command:

```python
# app.py
from obey import command

@command
def do_it(task: str) -> str:
    return f"I'm doing {task}"
```

When we execute `app.py` Obey will automatically call function `do_it`:

```console
python app.py well
I'm doing well
```

But what if in some cases we'd like to reuse `do_it`? Let's make an extension for our app:
```python
# extended_app.py
from .app import do_it
from obey import command

@command
def do_it_multiple(task: str, count: int = 1) -> str:
    return ", ".join([do_it(task) for _ in range(count)])
        
```
And call it:
```console
python extended_app.py "my part" 3
I'm doing my part, I'm doing my part, I'm doing my part
```

As we can see, Obey ignored command `do_it` from `app.py` and called only `do_it_multiple` from `extended_app.py`.

It's also possible to reuse decorated command in other parts of our application, which are not intended for CLI. For example in tests:

```python
# tests/test_all.py

from my_package.app import do_it
from my_package.extended_app import do_it_multiple

def test_do_it():
    assert do_it("fine!") == "I'm doing fine!"

def do_it_multiple():
    assert do_it_multiple("my job", 2) == "I'm doing my job, I'm doing my job"
```