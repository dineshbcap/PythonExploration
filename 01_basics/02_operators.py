"""
OPERATORS
=========
Python operators: arithmetic, comparison, logical, bitwise, identity,
membership, assignment, and the walrus operator (:=).

Run: python 01_basics/02_operators.py
"""

# ── 1. Arithmetic Operators ──────────────────────────────────────────────────

print("--- Arithmetic ---")
a, b = 17, 5

print(f"{a} + {b}  = {a + b}")    # 22  — addition
print(f"{a} - {b}  = {a - b}")    # 12  — subtraction
print(f"{a} * {b}  = {a * b}")    # 85  — multiplication
print(f"{a} / {b}  = {a / b}")    # 3.4 — true division (always float)
print(f"{a} // {b} = {a // b}")   # 3   — floor division (truncates toward -∞)
print(f"{a} % {b}  = {a % b}")    # 2   — modulo (remainder)
print(f"{a} ** {b} = {a ** b}")   # 1419857 — exponentiation

# Floor division edge case with negatives:
print(-17 // 5)   # -4, not -3 (floors toward negative infinity)
print(-17 % 5)    # 3  (always has same sign as divisor)

# Operator on non-numbers:
print("ab" * 3)   # "ababab" — repetition
print([1] + [2])  # [1, 2]   — concatenation


# ── 2. Comparison Operators ──────────────────────────────────────────────────

print("\n--- Comparison ---")
x, y = 10, 20
print(x == y)    # False — equal
print(x != y)    # True  — not equal
print(x < y)     # True  — less than
print(x > y)     # False — greater than
print(x <= 10)   # True  — less than or equal
print(x >= 10)   # True  — greater than or equal

# Chained comparisons (Python-specific, reads naturally):
age = 25
print(18 <= age < 65)        # True — both conditions checked
print(1 < 2 < 3 < 4)         # True

# Comparing different types:
print(1 == 1.0)    # True — value equality across int/float
print(1 == True)   # True — bool is int subtype


# ── 3. Logical Operators ─────────────────────────────────────────────────────

print("\n--- Logical ---")
# and, or, not evaluate with short-circuit logic

print(True and False)   # False
print(True or False)    # True
print(not True)         # False

# Short-circuit: right side not evaluated if left determines the outcome
def side_effect():
    print("  side_effect() called")
    return True

print("and short-circuit (False and ...):")
False and side_effect()    # side_effect never called

print("or short-circuit (True or ...):")
True or side_effect()      # side_effect never called

# Truthiness rules — these are all falsy:
falsy_values = [0, 0.0, "", [], {}, set(), None, False]
for v in falsy_values:
    print(f"  bool({v!r}) = {bool(v)}")

# and/or return one of their operands (not necessarily True/False):
print("a" or "b")    # "a" — first truthy value
print("" or "b")     # "b" — skips falsy ""
print("" and "b")    # ""  — first falsy value
print("a" and "b")   # "b" — returns last if all truthy


# ── 4. Assignment Operators ──────────────────────────────────────────────────

print("\n--- Assignment ---")
n = 10
n += 5;  print(n)    # 15  +=
n -= 3;  print(n)    # 12  -=
n *= 2;  print(n)    # 24  *=
n //= 5; print(n)    # 4   //=
n **= 3; print(n)    # 64  **=
n %= 10; print(n)    # 4   %=


# ── 5. Walrus Operator := (Python 3.8+) ──────────────────────────────────────

print("\n--- Walrus Operator ---")
# Assigns AND returns a value in a single expression.
# Useful to avoid evaluating something twice.

import re
data = "User: Alice, Age: 30"

if m := re.search(r"Age: (\d+)", data):
    print(f"Found age: {m.group(1)}")   # "30"

# In a while loop to avoid reading twice:
import io
stream = io.StringIO("line1\nline2\nline3\n")
while chunk := stream.readline():
    print(f"  chunk: {chunk!r}")


# ── 6. Identity Operators ────────────────────────────────────────────────────

print("\n--- Identity ---")
a = [1, 2]
b = [1, 2]
c = a

print(a is c)    # True  — same object
print(a is b)    # False — equal but different objects
print(a is not b)# True

# CPython caches small integers (-5 to 256) and interned strings,
# so these may be True despite being separate literals:
x = 100; y = 100
print(x is y)    # True (cached small int)
x = 1000; y = 1000
print(x is y)    # False in most contexts (not cached)


# ── 7. Membership Operators ──────────────────────────────────────────────────

print("\n--- Membership ---")
fruits = ["apple", "banana", "cherry"]
print("apple" in fruits)         # True
print("mango" not in fruits)     # True

text = "Hello, World!"
print("World" in text)           # True — works on strings too

# in on dict checks keys:
d = {"a": 1, "b": 2}
print("a" in d)      # True
print(1 in d)        # False — 1 is a value, not a key
print(1 in d.values())  # True


# ── 8. Bitwise Operators ─────────────────────────────────────────────────────

print("\n--- Bitwise ---")
#  Operate on the binary representation of integers.
x = 0b1010   # 10
y = 0b1100   # 12

print(f"x & y  = {x & y:04b} ({x & y})")    # AND  → 1000 (8)
print(f"x | y  = {x | y:04b} ({x | y})")    # OR   → 1110 (14)
print(f"x ^ y  = {x ^ y:04b} ({x ^ y})")    # XOR  → 0110 (6)
print(f"~x     = {~x}")                       # NOT  → -11 (inverts bits, two's complement)
print(f"x << 1 = {x << 1}")                  # Left shift  → 20 (multiply by 2)
print(f"x >> 1 = {x >> 1}")                  # Right shift → 5  (divide by 2)

# Common use: checking/setting flags
READ    = 0b001   # 1
WRITE   = 0b010   # 2
EXECUTE = 0b100   # 4

perms = READ | WRITE          # combine
print(bool(perms & READ))     # True — has READ
print(bool(perms & EXECUTE))  # False — no EXECUTE
perms |= EXECUTE              # add EXECUTE
print(bin(perms))             # 0b111


# ── 9. Operator Precedence (highest to lowest, abbreviated) ──────────────────

print("\n--- Precedence ---")
# **  >  unary +/-/~  >  * / // %  >  + -  >  << >>  >  &  >  ^  >  |
# > comparison  >  not  >  and  >  or  >  := (walrus)

result = 2 + 3 * 4 ** 2   # 4**2=16, *3=48, +2=50
print(result)              # 50
print(2 + (3 * (4 ** 2)))  # same — explicit parens always win

print("\nDone: operators")
