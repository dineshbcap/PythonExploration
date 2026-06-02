# Changelog

All notable changes to this project will be documented here.
Format based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [Unreleased]

---

## [1.0.0] — 2026-06-02

### Added
- `README.md` — project overview, structure, how-to-use, and learning path table
- `requirements.txt` — documents stdlib-only dependency baseline (Python 3.9+)
- `.gitignore` — covers Python bytecode, virtual environments, build artifacts,
  type-checker caches, IDEs, and macOS metadata

#### 01_basics (9 modules)
- `01_variables_and_datatypes.py` — built-in scalar types, identity vs equality, mutability, type conversion
- `02_operators.py` — arithmetic, comparison, logical, bitwise, walrus (`:=`), precedence
- `03_control_flow.py` — if/elif/else, for, while, break/continue/pass, loop else, match/case (3.10+)
- `04_functions.py` — definitions, default values, *args/**kwargs, positional/keyword-only params, LEGB scope, closures, recursion, type hints
- `05_strings.py` — indexing, slicing, methods, f-strings, encoding/decoding, regular expressions
- `06_lists.py` — CRUD, slicing, sorting, shallow vs deep copy, nested lists, performance notes
- `07_tuples.py` — immutability, packing/unpacking, namedtuple, typing.NamedTuple
- `08_sets.py` — set algebra, frozenset, O(1) membership, common patterns
- `09_dictionaries.py` — CRUD, comprehensions, merging, defaultdict, Counter, OrderedDict

#### 02_intermediate (8 modules)
- `01_oop_basics.py` — classes, __init__, instance/class/static methods, properties, dunder methods, __slots__
- `02_inheritance.py` — single/multiple inheritance, MRO, cooperative super(), mixins, ABCs, __init_subclass__
- `03_comprehensions.py` — list/dict/set comprehensions, generator expressions, walrus in comprehensions, performance
- `04_iterators_generators.py` — iterator protocol, custom iterators, yield, yield from, send/throw/close, generator pipelines, itertools
- `05_exception_handling.py` — try/except/else/finally, exception hierarchy, chaining, custom exceptions, ExceptionGroup (3.11+)
- `06_file_handling.py` — open(), modes, binary files, pathlib, csv, json, pickle
- `07_functional_tools.py` — lambda, map, filter, reduce, zip, enumerate, partial, lru_cache, wraps, operator module
- `08_modules_and_packages.py` — import mechanics, __all__, __name__, sys.path, importlib, stdlib tour

#### 03_advanced (10 modules)
- `01_decorators.py` — function/class decorators, @wraps, decorator factories, stacking, real-world patterns
- `02_context_managers.py` — __enter__/__exit__, @contextmanager, contextlib utilities, ExitStack, transactions
- `03_descriptors.py` — __get__/__set__/__delete__, data vs non-data, lazy properties, property internals, __set_name__
- `04_metaclasses.py` — type() as factory, custom metaclasses, __new__ vs __init__, __prepare__, auto-registration
- `05_dataclasses_and_typing.py` — @dataclass, field(), frozen, order, inheritance, asdict/replace, TypeVar, Protocol, TypedDict
- `06_abstract_base_classes.py` — ABC, @abstractmethod, abstract properties, virtual subclasses, collections.abc
- `07_concurrency_threading.py` — Thread, Lock, RLock, Semaphore, Event, Queue, ThreadPoolExecutor, thread-local storage
- `08_multiprocessing.py` — Process, Pool, Queue, Pipe, Value/Array, Manager, ProcessPoolExecutor
- `09_asyncio.py` — async/await, tasks, gather, wait, timeouts, async context managers, async generators, run_in_executor
- `10_design_patterns.py` — Singleton, Factory, Builder, Adapter, Decorator, Proxy, Composite, Observer, Strategy, Command, Template Method, Chain of Responsibility

### Changed
- `README.md` — added GitHub badge and `git clone` snippet

[Unreleased]: https://github.com/dineshbcap/PythonExploration/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/dineshbcap/PythonExploration/releases/tag/v1.0.0
