# Python: Basic to Advanced — Complete Reference Project

A structured, self-contained Python learning project organized from fundamentals to advanced internals.
Each file is a standalone, runnable module with inline explanations.

---

## Project Structure

```
PythonExploration/
├── 01_basics/
│   ├── 01_variables_and_datatypes.py     # Built-in types, type(), id(), mutability
│   ├── 02_operators.py                   # Arithmetic, comparison, logical, bitwise, walrus
│   ├── 03_control_flow.py                # if/elif/else, for, while, break/continue/pass
│   ├── 04_functions.py                   # Definitions, args, *args/**kwargs, scope, recursion
│   ├── 05_strings.py                     # Methods, formatting, slicing, encoding
│   ├── 06_lists.py                       # CRUD ops, slicing, sorting, nested lists
│   ├── 07_tuples.py                      # Immutability, packing/unpacking, named tuples
│   ├── 08_sets.py                        # Set operations, frozen sets
│   └── 09_dictionaries.py                # CRUD, iteration, merging, defaultdict, OrderedDict
│
├── 02_intermediate/
│   ├── 01_oop_basics.py                  # Classes, __init__, instance/class/static methods
│   ├── 02_inheritance.py                 # Single, multiple, MRO, super(), mixins
│   ├── 03_comprehensions.py              # List/dict/set comprehensions, generator expressions
│   ├── 04_iterators_generators.py        # __iter__/__next__, yield, yield from, send()
│   ├── 05_exception_handling.py          # try/except/else/finally, custom exceptions, chaining
│   ├── 06_file_handling.py               # open(), modes, context managers, pathlib, csv, json
│   ├── 07_functional_tools.py            # lambda, map, filter, reduce, partial, zip, enumerate
│   └── 08_modules_and_packages.py        # import mechanics, __all__, __name__, packages
│
├── 03_advanced/
│   ├── 01_decorators.py                  # Function/class decorators, stacking, functools.wraps
│   ├── 02_context_managers.py            # __enter__/__exit__, contextlib, nested managers
│   ├── 03_descriptors.py                 # __get__/__set__/__delete__, property internals
│   ├── 04_metaclasses.py                 # type(), __new__, custom metaclasses, __init_subclass__
│   ├── 05_dataclasses_and_typing.py      # @dataclass, field(), type hints, Protocols, TypeVar
│   ├── 06_abstract_base_classes.py       # ABC, @abstractmethod, virtual subclasses, __subclasshook__
│   ├── 07_concurrency_threading.py       # Thread, Lock, RLock, Semaphore, ThreadPoolExecutor
│   ├── 08_multiprocessing.py             # Process, Pool, Queue, Pipe, shared memory
│   ├── 09_asyncio.py                     # async/await, event loop, tasks, gather, streams
│   └── 10_design_patterns.py             # Singleton, Factory, Observer, Strategy, Decorator pattern
│
└── README.md
```

## How to Use

Each file can be run directly:
```bash
python 01_basics/01_variables_and_datatypes.py
```

Files are designed to be read top-to-bottom like a tutorial — output is printed with labels so you
can follow along without an IDE. No external dependencies required (standard library only).

## Learning Path

| Level        | Files                  | Time estimate |
|--------------|------------------------|---------------|
| Beginner     | `01_basics/`           | 2–4 hours     |
| Intermediate | `02_intermediate/`     | 4–6 hours     |
| Advanced     | `03_advanced/`         | 6–10 hours    |
