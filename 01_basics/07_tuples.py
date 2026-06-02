"""
TUPLES
======
Immutable, ordered sequences. Covers creation, packing/unpacking,
named tuples, use as dict keys, and comparison with lists.

Run: python 01_basics/07_tuples.py
"""

# ── 1. Creation ───────────────────────────────────────────────────────────────

print("--- Creation ---")
empty    = ()
single   = (42,)          # trailing comma is REQUIRED for a single-element tuple
single2  = 42,            # parentheses are optional — comma makes it a tuple
pair     = (1, 2)
triple   = (1, "two", 3.0)

print(empty, type(empty))
print(single, type(single))
print(42, type(42))        # without comma: just an int, not a tuple

# Implicit packing: right side of assignment creates a tuple
coords = 10, 20, 30
print(coords, type(coords))

# Convert other iterables to tuple
from_list  = tuple([1, 2, 3])
from_range = tuple(range(5))
from_str   = tuple("abc")
print(from_list, from_range, from_str)


# ── 2. Indexing and Slicing ───────────────────────────────────────────────────

print("\n--- Indexing & Slicing ---")
t = (10, 20, 30, 40, 50)

print(t[0])      # 10
print(t[-1])     # 50
print(t[1:4])    # (20, 30, 40)  — slicing returns a tuple
print(t[::-1])   # reversed: (50, 40, 30, 20, 10)

# Tuples are immutable — this would raise TypeError:
# t[0] = 99


# ── 3. Packing and Unpacking ──────────────────────────────────────────────────

print("\n--- Packing & Unpacking ---")
# Packing: multiple values → one tuple
point = 3, 7

# Unpacking: tuple → multiple variables (must match exactly)
x, y = point
print(f"x={x}, y={y}")

# Extended unpacking with *rest
first, *rest = (1, 2, 3, 4, 5)
print(f"first={first}, rest={rest}")   # rest is a list, not a tuple

*head, last = (1, 2, 3, 4, 5)
print(f"head={head}, last={last}")

a, *middle, z = (1, 2, 3, 4, 5)
print(f"a={a}, middle={middle}, z={z}")

# Swap using tuple unpacking (no temp variable needed):
a, b = 10, 20
a, b = b, a
print(f"after swap: a={a}, b={b}")

# Unpacking in for loops:
records = [(1, "Alice", 90), (2, "Bob", 85), (3, "Carol", 92)]
for id_, name, score in records:
    print(f"  {id_}: {name} — {score}")


# ── 4. Methods ────────────────────────────────────────────────────────────────

print("\n--- Methods ---")
# Tuples only have two methods (immutability limits the API):
t = (1, 2, 3, 2, 1)
print(t.count(2))    # 2 — number of times 2 appears
print(t.index(3))    # 2 — index of first 3

# Everything else (in, len, min, max, sorted, reversed) works via builtins:
print(3 in t)
print(len(t))
print(min(t), max(t))


# ── 5. Tuples as Dict Keys ────────────────────────────────────────────────────

print("\n--- As dict keys ---")
# Tuples are hashable (if all their elements are), so they can be dict keys
# and set members. Lists cannot because they are mutable/unhashable.

locations = {
    (40.7128, -74.0060): "New York",
    (51.5074, -0.1278):  "London",
    (35.6762, 139.6503): "Tokyo",
}
print(locations[(40.7128, -74.0060)])   # New York

# Comparison:
# list: unhashable
# set({[1,2]})   → TypeError
s = {(1, 2), (3, 4)}   # tuples in a set — fine
print(s)


# ── 6. Named Tuples ───────────────────────────────────────────────────────────

print("\n--- Named tuples ---")
from collections import namedtuple

# Define a named tuple class (field names given as string or list)
Point    = namedtuple("Point", ["x", "y"])
Employee = namedtuple("Employee", "name age department")  # space-separated string

p = Point(3, 7)
print(p)               # Point(x=3, y=7)
print(p.x, p.y)        # access by name
print(p[0], p[1])      # also accessible by index
x, y = p               # still unpackable

emp = Employee("Alice", 30, "Engineering")
print(emp.name, emp.age)

# Named tuples are still immutable:
# p.x = 10   # AttributeError

# _replace creates a NEW tuple with some fields changed:
p2 = p._replace(x=99)
print(p, p2)

# _asdict converts to an OrderedDict (Python 3.8+: regular dict):
print(emp._asdict())

# _fields lists field names:
print(Point._fields)   # ('x', 'y')


# ── 7. typing.NamedTuple — Class-based (Modern) ───────────────────────────────

print("\n--- typing.NamedTuple ---")
from typing import NamedTuple

class Color(NamedTuple):
    red:   int
    green: int
    blue:  int
    alpha: float = 1.0   # default value

red = Color(255, 0, 0)
print(red)               # Color(red=255, green=0, blue=0, alpha=1.0)
print(red.red)
transparent = Color(0, 0, 255, 0.5)
print(transparent)


# ── 8. Tuples vs Lists — When to Use Which ────────────────────────────────────

print("\n--- Tuple vs List ---")
# Use a TUPLE when:
#   - data is logically immutable (coordinates, RGB, record fields)
#   - you need it as a dict key or in a set
#   - slight memory / speed advantage for fixed-size data

# Use a LIST when:
#   - data may grow/shrink (appending, removing)
#   - you need sort, reverse in-place

import sys
lst  = [1, 2, 3, 4, 5]
tup  = (1, 2, 3, 4, 5)
print(f"list size: {sys.getsizeof(lst)} bytes")   # slightly larger
print(f"tuple size: {sys.getsizeof(tup)} bytes")


print("\nDone: tuples")
