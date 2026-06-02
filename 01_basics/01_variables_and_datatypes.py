"""
VARIABLES AND DATA TYPES
========================
Python is dynamically typed: variables hold references to objects, not values.
Every object has a type, an identity (memory address), and a value.

Run: python 01_basics/01_variables_and_datatypes.py
"""

# ── 1. Variable Assignment ──────────────────────────────────────────────────

x = 10          # integer
name = "Alice"  # string
pi = 3.14       # float
active = True   # boolean

# Multiple assignment in one line
a, b, c = 1, 2, 3

# Swap without a temp variable (Python-specific idiom)
a, b = b, a
print(f"After swap: a={a}, b={b}")   # a=2, b=1

# Augmented assignment shorthand
counter = 0
counter += 1   # same as counter = counter + 1
print(f"Counter: {counter}")


# ── 2. Built-in Scalar Types ────────────────────────────────────────────────

print("\n--- Integers ---")
n = 1_000_000          # underscores allowed for readability
big = 10 ** 18         # Python ints have arbitrary precision (no overflow)
negative = -42
print(n, big, negative)
print(f"Type: {type(n)}")          # <class 'int'>

print("\n--- Floats ---")
f = 3.14
sci = 2.5e-3           # scientific notation: 0.0025
print(f, sci)
print(f"Type: {type(f)}")         # <class 'float'>

# Floating-point precision warning:
print(0.1 + 0.2)                  # 0.30000000000000004 — IEEE 754 artefact
from decimal import Decimal
print(Decimal("0.1") + Decimal("0.2"))  # 0.3 — exact decimal arithmetic

print("\n--- Booleans ---")
# bool is a subclass of int; True == 1, False == 0
print(True + True)    # 2
print(False * 99)     # 0
print(isinstance(True, int))  # True

print("\n--- None ---")
nothing = None        # represents the absence of a value
print(nothing, type(nothing))

print("\n--- Complex ---")
z = 2 + 3j
print(z.real, z.imag, abs(z))  # 2.0, 3.0, magnitude


# ── 3. Strings ──────────────────────────────────────────────────────────────

print("\n--- Strings ---")
single = 'hello'
double = "world"
multi  = """Line one
Line two"""           # triple-quoted spans multiple lines

# Strings are sequences and immutable
print(single[0])      # 'h'
print(single[-1])     # 'o'  (negative index counts from the end)
# single[0] = 'H'     # TypeError — strings are immutable


# ── 4. Bytes vs str ─────────────────────────────────────────────────────────

print("\n--- Bytes ---")
raw = b"hello"        # bytes literal (each element is 0-255)
text = raw.decode("utf-8")    # bytes → str
back = text.encode("utf-8")   # str   → bytes
print(raw, text, back)


# ── 5. type() and isinstance() ──────────────────────────────────────────────

print("\n--- Type Checking ---")
values = [42, 3.14, "hi", True, None, b"raw"]
for v in values:
    print(f"  {v!r:15} → type={type(v).__name__}, isinstance int: {isinstance(v, int)}")

# isinstance is preferred over type() equality because it respects inheritance
print(isinstance(True, bool))   # True
print(isinstance(True, int))    # True — bool IS an int


# ── 6. Identity vs Equality ─────────────────────────────────────────────────

print("\n--- Identity vs Equality ---")
p = [1, 2, 3]
q = [1, 2, 3]
r = p

print(p == q)    # True  — same value
print(p is q)    # False — different objects in memory
print(p is r)    # True  — same object (r is an alias for p)

# id() returns the memory address (CPython implementation)
print(f"id(p)={id(p)}, id(q)={id(q)}, id(r)={id(r)}")


# ── 7. Mutability ───────────────────────────────────────────────────────────

print("\n--- Mutability ---")
# Immutable: int, float, bool, str, tuple, frozenset, bytes
# Mutable:   list, dict, set, bytearray, most user-defined objects

immutable_str = "hello"
# immutable_str[0] = "H"   # TypeError

mutable_list = [1, 2, 3]
mutable_list[0] = 99       # OK — lists are mutable
print(mutable_list)

# Mutable default argument pitfall (classic Python gotcha):
def append_item(item, container=[]):   # container is created ONCE
    container.append(item)
    return container

print(append_item(1))   # [1]
print(append_item(2))   # [1, 2]  — not [2]! container persists between calls
# Fix: use None as default, create new list inside
def safe_append(item, container=None):
    if container is None:
        container = []
    container.append(item)
    return container


# ── 8. Type Conversion (Casting) ────────────────────────────────────────────

print("\n--- Type Conversion ---")
print(int("42"))        # str → int
print(float("3.14"))    # str → float
print(str(100))         # int → str
print(bool(0))          # 0 is falsy → False
print(bool(""))         # empty string is falsy → False
print(bool("hi"))       # non-empty string is truthy → True
print(list("abc"))      # str → list of chars: ['a', 'b', 'c']
print(tuple([1, 2]))    # list → tuple


# ── 9. Constants Convention ─────────────────────────────────────────────────

# Python has no true constants; use ALL_CAPS as a convention
MAX_RETRIES = 3
DEFAULT_TIMEOUT = 30.0


print("\nDone: variables_and_datatypes")
