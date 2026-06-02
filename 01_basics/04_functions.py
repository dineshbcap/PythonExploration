"""
FUNCTIONS
=========
Defining functions, parameter types (*args, **kwargs), default values,
keyword-only and positional-only parameters, scope (LEGB), closures,
first-class functions, and recursion.

Run: python 01_basics/04_functions.py
"""

# ── 1. Basic Definition ───────────────────────────────────────────────────────

def greet(name):
    """Return a greeting string."""        # docstring — first line of body
    return f"Hello, {name}!"

print(greet("Alice"))
print(greet.__doc__)   # access the docstring

# A function with no return statement implicitly returns None
def say_hello():
    print("Hi!")

result = say_hello()
print(f"Return value: {result}")    # None


# ── 2. Default Parameter Values ──────────────────────────────────────────────

print("\n--- Default values ---")

def power(base, exponent=2):    # exponent is optional; defaults to 2
    return base ** exponent

print(power(3))        # 9    (uses default)
print(power(3, 3))     # 27   (overrides default)

# IMPORTANT: default values are evaluated ONCE at definition time.
# Using a mutable default (list, dict) is a classic bug:
def bad_append(item, lst=[]):
    lst.append(item)
    return lst

print(bad_append(1))   # [1]
print(bad_append(2))   # [1, 2]  ← shared across calls!

# Fix: use None as sentinel, create fresh object inside
def good_append(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(good_append(1))  # [1]
print(good_append(2))  # [2]   ← independent


# ── 3. Positional vs Keyword Arguments ───────────────────────────────────────

print("\n--- Positional vs keyword ---")

def connect(host, port, timeout):
    print(f"Connecting to {host}:{port} (timeout={timeout}s)")

connect("localhost", 5432, 30)                       # positional
connect(host="localhost", port=5432, timeout=30)     # keyword
connect("localhost", timeout=30, port=5432)          # mixed (positional first)


# ── 4. *args — Variable Positional Arguments ──────────────────────────────────

print("\n--- *args ---")

def total(*args):
    # args is a tuple of all extra positional arguments
    return sum(args)

print(total(1, 2, 3))         # 6
print(total(10, 20, 30, 40))  # 100

# Unpacking a list/tuple into positional args using *:
nums = [1, 2, 3, 4]
print(total(*nums))   # equivalent to total(1, 2, 3, 4)


# ── 5. **kwargs — Variable Keyword Arguments ──────────────────────────────────

print("\n--- **kwargs ---")

def profile(**kwargs):
    # kwargs is a dict of all extra keyword arguments
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

profile(name="Alice", age=30, city="NYC")

# Unpacking a dict into keyword args using **:
data = {"name": "Bob", "age": 25}
profile(**data)


# ── 6. Combined Signature ────────────────────────────────────────────────────

print("\n--- Combined signature ---")

def describe(title, *topics, verbose=False, **meta):
    """
    title   — positional (required)
    *topics — extra positionals gathered as tuple
    verbose — keyword-only (comes after *)
    **meta  — extra keywords gathered as dict
    """
    print(f"Title: {title}")
    print(f"Topics: {topics}")
    print(f"Verbose: {verbose}")
    print(f"Meta: {meta}")

describe("Python", "loops", "functions", verbose=True, author="Guido", year=1991)


# ── 7. Positional-Only Parameters (/) — Python 3.8+ ──────────────────────────

print("\n--- Positional-only (/) ---")

def strict_pos(x, y, /, z=0):
    # x and y MUST be passed positionally; they cannot be used as keywords
    return x + y + z

print(strict_pos(1, 2))          # OK
print(strict_pos(1, 2, z=10))    # OK — z can be keyword
# strict_pos(x=1, y=2)           # TypeError


# ── 8. Keyword-Only Parameters (*) ───────────────────────────────────────────

print("\n--- Keyword-only (*) ---")

def create_user(name, *, admin=False, active=True):
    # admin and active MUST be passed as keywords
    print(f"User {name}: admin={admin}, active={active}")

create_user("Alice", admin=True)
# create_user("Bob", True)       # TypeError — admin must be keyword


# ── 9. Scope — LEGB Rule ─────────────────────────────────────────────────────

print("\n--- LEGB Scope ---")
# Python resolves names in this order:
# L = Local (inside current function)
# E = Enclosing (outer function, for nested functions)
# G = Global (module level)
# B = Built-in (builtins module)

x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(f"inner sees: {x}")   # local

    inner()
    print(f"outer sees: {x}")       # enclosing

outer()
print(f"module sees: {x}")          # global

# global keyword — modifies a global variable from inside a function
count = 0
def increment():
    global count
    count += 1

increment(); increment()
print(f"count = {count}")   # 2

# nonlocal keyword — modifies an enclosing (non-global) variable
def make_counter():
    n = 0
    def counter():
        nonlocal n
        n += 1
        return n
    return counter

c = make_counter()
print(c(), c(), c())   # 1 2 3


# ── 10. Closures ──────────────────────────────────────────────────────────────

print("\n--- Closures ---")
# A closure is a function that remembers variables from its enclosing scope
# even after the outer function has returned.

def multiplier(factor):
    def multiply(x):
        return x * factor   # factor is captured from enclosing scope
    return multiply

double = multiplier(2)
triple = multiplier(3)
print(double(5), triple(5))   # 10  15

# Inspect what a closure has captured:
print(double.__closure__[0].cell_contents)   # 2


# ── 11. First-Class Functions ─────────────────────────────────────────────────

print("\n--- First-class functions ---")
# Functions are objects: assign, pass, return, store them.

def square(n): return n ** 2
def cube(n):   return n ** 3

operations = [square, cube]         # store in a list
for op in operations:
    print(f"{op.__name__}(4) = {op(4)}")

def apply(func, value):             # pass as argument
    return func(value)

print(apply(square, 7))   # 49

def make_adder(n):                  # return a function
    def adder(x):
        return x + n
    return adder

add10 = make_adder(10)
print(add10(5))   # 15


# ── 12. Recursion ─────────────────────────────────────────────────────────────

print("\n--- Recursion ---")
# A function calling itself. Requires a base case to prevent infinite recursion.

def factorial(n):
    if n <= 1:        # base case
        return 1
    return n * factorial(n - 1)   # recursive case

print(factorial(5))   # 120
print(factorial(10))  # 3628800

# Python's default recursion limit is 1000:
import sys
print(f"Recursion limit: {sys.getrecursionlimit()}")

# Fibonacci — naive (exponential time), then memoized (linear):
def fib_naive(n):
    if n <= 1:
        return n
    return fib_naive(n - 1) + fib_naive(n - 2)

from functools import lru_cache

@lru_cache(maxsize=None)   # memoizes results automatically
def fib(n):
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])   # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]


# ── 13. Type Hints (preview) ──────────────────────────────────────────────────

print("\n--- Type hints ---")
# Hints are NOT enforced at runtime; they document intent and enable IDE checks.

def add(a: int, b: int) -> int:
    return a + b

def greet_typed(name: str, times: int = 1) -> str:
    return (name + " ") * times

print(add(3, 4))
print(greet_typed("Hi", 3))


print("\nDone: functions")
