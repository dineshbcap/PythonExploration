"""
MODULES AND PACKAGES
====================
import mechanics, module attributes (__name__, __file__, __all__),
package structure, relative imports, sys.path, importlib, and
the standard library tour.

Run: python 02_intermediate/08_modules_and_packages.py
"""

import sys
import os
import math
import importlib
import importlib.util
import types

# ── 1. Import Styles ─────────────────────────────────────────────────────────

print("--- Import styles ---")

# 1a. Import the whole module — access names via module.name
import math
print(math.pi)
print(math.sqrt(16))

# 1b. Import specific names — bring into current namespace
from math import pi, sqrt, floor
print(pi)
print(sqrt(16))

# 1c. Import with alias — rename to avoid conflicts or shorten
import collections as col
from datetime import datetime as dt

d = col.deque([1, 2, 3])
print(d)
print(dt.now().year)

# 1d. Import all — (AVOID in production code; pollutes namespace)
# from math import *


# ── 2. Module as a Namespace ─────────────────────────────────────────────────

print("\n--- Module attributes ---")
# Every module is an object with attributes.

print(math.__name__)    # "math"
print(math.__file__)    # path to the .py or .so file
print(math.__doc__[:80])

# dir() lists all names in a module
public_names = [name for name in dir(math) if not name.startswith("_")]
print(f"math has {len(public_names)} public names")


# ── 3. __name__ == "__main__" Pattern ────────────────────────────────────────

print("\n--- __name__ ---")
# When a file is run directly:  __name__ == "__main__"
# When imported as a module:    __name__ == the module's name (e.g. "math")

# Standard pattern to make a file both importable AND runnable:
#
# def main():
#     ...
#
# if __name__ == "__main__":
#     main()
#
# This block runs ONLY when the file is executed directly,
# not when imported by another module.

print(f"This script's __name__: {__name__}")


# ── 4. __all__ — Public API Declaration ──────────────────────────────────────

print("\n--- __all__ ---")
# __all__ is a list that controls what `from module import *` exports.
# It also serves as documentation of a module's intended public API.

# Example module content:
#
# __all__ = ["PublicClass", "public_func"]   # only these are exported by *
#
# def public_func(): ...
# def _private_func(): ...   # underscore signals private by convention
# class PublicClass: ...
# class _InternalClass: ...

# Inspect __all__ on standard library modules:
import json
print(f"json.__all__: {json.__all__}")


# ── 5. sys.path — Module Search Path ─────────────────────────────────────────

print("\n--- sys.path ---")
# When you `import foo`, Python searches these directories in order:
# 1. Current directory (or script's directory)
# 2. PYTHONPATH environment variable entries
# 3. Standard library directories
# 4. site-packages (installed third-party packages)

for path in sys.path[:5]:
    print(f"  {path}")

# Add a custom path programmatically (rarely needed; prefer venv/pip):
# sys.path.insert(0, "/some/custom/path")


# ── 6. Package Structure ─────────────────────────────────────────────────────

print("\n--- Package structure ---")
# A PACKAGE is a directory with __init__.py.
# __init__.py can be empty, or expose a public API.
#
# mypackage/
# ├── __init__.py           # makes it a package; runs on import
# ├── core.py               # mypackage.core
# ├── utils.py              # mypackage.utils
# └── subpkg/
#     ├── __init__.py       # makes subpkg a sub-package
#     └── helpers.py        # mypackage.subpkg.helpers

# Example __init__.py that exposes a clean public API:
#
#   # mypackage/__init__.py
#   from .core  import CoreClass
#   from .utils import helper_func
#   __all__ = ["CoreClass", "helper_func"]
#
# Users can then do: from mypackage import CoreClass
# instead of:        from mypackage.core import CoreClass


# ── 7. Relative Imports ───────────────────────────────────────────────────────

print("\n--- Relative imports ---")
# Inside a package, use dots to import relatively:
#
#   from .utils import helper       # same package
#   from ..core import BaseClass    # parent package
#
# Relative imports only work INSIDE packages (not top-level scripts).


# ── 8. importlib — Dynamic Imports ────────────────────────────────────────────

print("\n--- importlib ---")
# Import a module whose name is only known at runtime.

module_name = "json"
mod = importlib.import_module(module_name)
print(f"Dynamically imported: {mod.__name__}")
print(mod.dumps({"a": 1}))

# Reload a module (useful in interactive sessions after editing it):
# importlib.reload(mod)

# Check if a module is available without importing it:
spam = importlib.util.find_spec("json")
print(f"json spec: {spam.name}")

missing = importlib.util.find_spec("nonexistent_module_xyz")
print(f"nonexistent: {missing}")   # None


# ── 9. Standard Library Highlights ───────────────────────────────────────────

print("\n--- Standard Library Tour ---")

# datetime
from datetime import datetime, date, timedelta
now   = datetime.now()
today = date.today()
delta = timedelta(days=7)
print(f"Now: {now:%Y-%m-%d %H:%M}")
print(f"One week from today: {today + delta}")

# collections
from collections import namedtuple, defaultdict, Counter, deque, OrderedDict
Point = namedtuple("Point", "x y")
p = Point(3, 4)
print(f"Distance: {(p.x**2 + p.y**2)**0.5}")

dq = deque([1, 2, 3], maxlen=3)
dq.appendleft(0)   # evicts rightmost when maxlen exceeded
print(dq)

# random
import random
random.seed(0)
print(random.randint(1, 10))
print(random.choice(["rock", "paper", "scissors"]))
print(random.sample(range(10), 5))   # 5 unique random items

# string
import string
print(string.ascii_letters)
print(string.digits)
print(string.punctuation)

# hashlib
import hashlib
h = hashlib.sha256(b"Hello, Python!").hexdigest()
print(f"SHA-256: {h[:16]}...")

# itertools (already covered in iterators file, brief mention)
import itertools
print(list(itertools.product("AB", repeat=2)))

# contextlib
from contextlib import suppress
with suppress(FileNotFoundError):
    os.remove("/nonexistent/file.txt")   # ignored instead of raising
print("No crash after suppress")

# typing
from typing import List, Dict, Optional, Union, Tuple, Any
def greet(name: str, times: int = 1) -> str:
    return (name + " ") * times
print(greet("hi", 3))

# pathlib
from pathlib import Path
print(Path.cwd())
print(Path(__file__).resolve())

# textwrap
import textwrap
long_text = "Python is a general-purpose, high-level programming language."
print(textwrap.fill(long_text, width=40))
print(textwrap.dedent("""
    def foo():
        pass
""").strip())

# pprint
from pprint import pprint
pprint({"name": "Alice", "scores": [85, 92, 78], "address": {"city": "NYC"}})

# dataclasses (preview — see 03_advanced/05_dataclasses_and_typing.py)
from dataclasses import dataclass

@dataclass
class Point3D:
    x: float
    y: float
    z: float = 0.0

print(Point3D(1, 2))
print(Point3D(1, 2, 3))


print("\nDone: modules_and_packages")
