"""
FUNCTIONAL TOOLS
================
lambda, map, filter, reduce, sorted with key, zip, enumerate,
functools (partial, lru_cache, wraps, reduce), and operator module.

Run: python 02_intermediate/07_functional_tools.py
"""

from functools import reduce, partial, lru_cache, wraps
import operator

# ── 1. lambda — Anonymous Functions ──────────────────────────────────────────

print("--- lambda ---")
# Syntax: lambda params: expression
# One expression only — no statements, no return keyword.

double = lambda x: x * 2
add    = lambda x, y: x + y

print(double(5))      # 10
print(add(3, 4))      # 7

# Best used INLINE (as argument to higher-order functions)
# Don't assign to a variable — just define a regular def instead

numbers = [3, 1, 4, 1, 5, 9, 2, 6, 5]
print(sorted(numbers, key=lambda x: -x))   # descending sort

people  = [("Bob", 30), ("Alice", 25), ("Carol", 35)]
print(sorted(people, key=lambda p: p[1]))  # sort by age

# Conditional lambda:
classify = lambda n: "even" if n % 2 == 0 else "odd"
print([classify(n) for n in range(6)])


# ── 2. map — Apply Function to Every Element ──────────────────────────────────

print("\n--- map ---")
# map(func, iterable) returns a LAZY iterator

nums    = [1, 2, 3, 4, 5]
squares = list(map(lambda x: x**2, nums))
print(squares)   # [1, 4, 9, 16, 25]

# With a named function (cleaner than lambda)
def celsius_to_fahrenheit(c):
    return c * 9/5 + 32

temps_c = [0, 20, 37, 100]
temps_f = list(map(celsius_to_fahrenheit, temps_c))
print(temps_f)

# map with two iterables — pairs elements
a = [1, 2, 3]
b = [10, 20, 30]
sums = list(map(operator.add, a, b))
print(sums)   # [11, 22, 33]

# Modern Python equivalent (usually clearer):
squares_comp = [x**2 for x in nums]   # list comprehension — preferred

# map is preferred when passing an existing function (avoids re-wrapping in lambda):
words = ["hello", "world", "python"]
print(list(map(str.upper, words)))   # no lambda needed — pass method directly


# ── 3. filter — Keep Elements Matching Predicate ──────────────────────────────

print("\n--- filter ---")
# filter(func, iterable) returns a LAZY iterator of elements where func(x) is truthy

nums = range(1, 21)
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)

# filter(None, iterable) — remove falsy values
mixed = [0, 1, "", "hello", None, [], [1, 2], False, True]
truthy_only = list(filter(None, mixed))
print(truthy_only)   # [1, 'hello', [1, 2], True]

# Equivalent comprehension:
evens_comp = [x for x in nums if x % 2 == 0]

# map + filter combined:
even_squares = list(map(lambda x: x**2, filter(lambda x: x % 2 == 0, range(10))))
print(even_squares)   # [0, 4, 16, 36, 64]


# ── 4. reduce — Fold an Iterable to a Single Value ────────────────────────────

print("\n--- reduce ---")
# reduce(func, iterable, initial?)
# Applies func cumulatively: func(func(func(a,b),c),d)...

nums = [1, 2, 3, 4, 5]
total   = reduce(lambda acc, x: acc + x, nums)   # 15
product = reduce(operator.mul, nums)              # 120
print(total, product)

# Custom max using reduce:
maximum = reduce(lambda a, b: a if a > b else b, nums)
print(maximum)   # 5

# With initial value (prepended to sequence):
concat = reduce(lambda acc, x: acc + str(x), nums, "Values: ")
print(concat)   # "Values: 12345"

# Prefer sum(), max(), any(), all() when available — they're clearer and faster


# ── 5. zip — Combine Multiple Iterables ───────────────────────────────────────

print("\n--- zip ---")
names   = ["Alice", "Bob", "Carol"]
scores  = [85, 92, 78]
grades  = ["B", "A", "C"]

# zip stops at the SHORTEST iterable
for name, score, grade in zip(names, scores, grades):
    print(f"  {name}: {score} ({grade})")

# Convert parallel lists to list of tuples:
pairs = list(zip(names, scores))
print(pairs)

# Unzip — use zip with * unpacking:
unzipped_names, unzipped_scores = zip(*pairs)
print(unzipped_names)
print(unzipped_scores)

# zip_longest — fills missing values with fillvalue
from itertools import zip_longest
a = [1, 2, 3]
b = [10, 20]
print(list(zip_longest(a, b, fillvalue=0)))   # [(1,10),(2,20),(3,0)]


# ── 6. enumerate — Index + Value ──────────────────────────────────────────────

print("\n--- enumerate ---")
fruits = ["apple", "banana", "cherry"]

for idx, fruit in enumerate(fruits):
    print(f"  {idx}: {fruit}")

# Custom start index:
for idx, fruit in enumerate(fruits, start=1):
    print(f"  {idx}. {fruit}")

# Building an index lookup dict:
index_map = {fruit: idx for idx, fruit in enumerate(fruits)}
print(index_map)


# ── 7. functools.partial — Partial Application ────────────────────────────────

print("\n--- partial ---")
# Creates a new callable with some arguments pre-filled.

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube   = partial(power, exponent=3)

print(square(5))   # 25
print(cube(3))     # 27

# Partial with positional args:
from functools import partial
multiply = partial(operator.mul, 10)   # pre-fill first arg as 10
print(list(map(multiply, [1, 2, 3, 4])))   # [10, 20, 30, 40]

# Useful for reducing repeated arg boilerplate:
import json
pretty_print = partial(json.dumps, indent=2, sort_keys=True)
print(pretty_print({"b": 2, "a": 1}))


# ── 8. functools.lru_cache — Memoization ──────────────────────────────────────

print("\n--- lru_cache ---")
# Caches function results in a dict; repeated calls with same args return cache hit.

@lru_cache(maxsize=128)   # None = unbounded cache
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])
print(fib.cache_info())   # CacheInfo(hits=..., misses=..., maxsize=128, currsize=...)

# Python 3.9+: @functools.cache is a simpler unbounded version
from functools import cache

@cache
def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)

print(factorial(10))
print(factorial.cache_info())


# ── 9. functools.wraps — Preserve Decorator Metadata ─────────────────────────

print("\n--- wraps ---")
# When writing decorators, @wraps copies the wrapped function's metadata.

def log_call(func):
    @wraps(func)   # preserves __name__, __doc__, __annotations__ of func
    def wrapper(*args, **kwargs):
        print(f"  Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log_call
def add(a: int, b: int) -> int:
    """Adds two numbers."""
    return a + b

print(add(3, 4))
print(add.__name__)   # "add" (not "wrapper" — @wraps preserved it)
print(add.__doc__)    # "Adds two numbers."


# ── 10. operator Module ───────────────────────────────────────────────────────

print("\n--- operator module ---")
# Function equivalents of built-in operators — avoid lambdas for simple ops.

nums = [3, 1, 4, 1, 5]

print(reduce(operator.add, nums))          # 14
print(reduce(operator.mul, nums))          # 60
print(sorted(people, key=operator.itemgetter(1)))  # sort by index 1

# attrgetter — get object attribute by name
class Point:
    def __init__(self, x, y): self.x = x; self.y = y
    def __repr__(self): return f"({self.x},{self.y})"

points = [Point(3, 1), Point(1, 4), Point(2, 2)]
print(sorted(points, key=operator.attrgetter("x")))  # sort by x

# methodcaller — call a method by name
words = ["hello", "WORLD", "Python"]
print(list(map(operator.methodcaller("lower"), words)))   # all lowercase


print("\nDone: functional_tools")
