# Obey

> ⚠️ Obey is still in beta. Bugs are possible

Obey is a Python package for creating command line interfaces.

Obey leverages Python synthax so developers could keep their code concise and clear.

Obey produces easy to use CLI: detailed help and autocompletion for all shells.

### Extremely easy start

Add just two lines of code to an existing app: import and decorator call:

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
  
...and more. Check out [the examples](./examples/).

## Table of contents

1. Input and output
   1. Arguments
   2. Options
   3. Types
   4. Defaults
   5. Returned values
2. Firing
3. Command branching
   1. One level
   2. Too infinity and beyond
4. Command combination
   1. Combine with the next
   2. Combine with all
5. Command piping
6. Examples
7.  Contribution