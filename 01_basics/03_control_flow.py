"""
CONTROL FLOW
============
if/elif/else, for loops, while loops, break, continue, pass,
loop else clauses, and match/case (Python 3.10+).

Run: python 01_basics/03_control_flow.py
"""

# ── 1. if / elif / else ───────────────────────────────────────────────────────

print("--- if/elif/else ---")
score = 72

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
else:
    grade = "F"

print(f"Score {score} → Grade {grade}")   # Grade C

# Ternary (conditional expression):
status = "pass" if score >= 60 else "fail"
print(f"Status: {status}")

# Truthiness in conditions — no need to write `if x == True` or `if len(x) > 0`:
items = [1, 2, 3]
if items:          # truthy because list is non-empty
    print(f"Has {len(items)} items")

name = ""
if not name:       # falsy because empty string
    print("Name is empty")


# ── 2. for Loop ──────────────────────────────────────────────────────────────

print("\n--- for loop ---")
# Iterates over any iterable (list, tuple, str, dict, generator, ...)

fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(f"  {fruit}")

# range(start, stop, step) — generates integers, does NOT create a list
print("Squares:")
for i in range(1, 6):
    print(f"  {i}^2 = {i ** 2}")

# Counting down
for i in range(5, 0, -1):
    print(i, end=" ")
print()

# enumerate — gives index AND value together
print("Indexed fruits:")
for idx, fruit in enumerate(fruits, start=1):   # start=1 offsets index
    print(f"  {idx}. {fruit}")

# zip — iterate two sequences in lockstep
names   = ["Alice", "Bob", "Carol"]
scores  = [88, 92, 75]
for name, score in zip(names, scores):
    print(f"  {name}: {score}")

# Iterating over a dict
config = {"host": "localhost", "port": 5432, "db": "myapp"}
print("Config:")
for key, value in config.items():
    print(f"  {key} = {value}")


# ── 3. while Loop ────────────────────────────────────────────────────────────

print("\n--- while loop ---")
n = 1
while n <= 5:
    print(n, end=" ")
    n += 1
print()

# Classic input-until-valid pattern:
import random
random.seed(42)
target = random.randint(1, 10)
attempt = 0
guess = 0
while guess != target:
    guess = random.randint(1, 10)   # simulated guesses
    attempt += 1
    if attempt > 50:               # safety — avoid infinite loop in demo
        break
print(f"Found {target} in {attempt} attempts")


# ── 4. break, continue, pass ─────────────────────────────────────────────────

print("\n--- break ---")
for i in range(10):
    if i == 5:
        print(f"Breaking at {i}")
        break
    print(i, end=" ")
print()

print("\n--- continue ---")
for i in range(10):
    if i % 2 == 0:
        continue    # skip even numbers, resume at top of loop
    print(i, end=" ")
print()

print("\n--- pass ---")
# pass is a no-op placeholder; required when a block would otherwise be empty
for _ in range(3):
    pass    # loop body — nothing to do yet

class Stub:
    pass    # placeholder class body

def todo():
    pass    # not implemented yet


# ── 5. Loop else Clause ────────────────────────────────────────────────────

print("\n--- loop else ---")
# The else block runs if the loop completed WITHOUT hitting break.
# Useful for "search and report not found" patterns.

def find_prime_factor(n):
    for i in range(2, n):
        if n % i == 0:
            print(f"{n} is divisible by {i}")
            break
    else:
        # Only reaches here if break was never hit
        print(f"{n} is prime")

find_prime_factor(7)    # prime
find_prime_factor(12)   # divisible by 2

# Same pattern with while:
i = 0
while i < 5:
    if i == 10:    # never true → else runs
        break
    i += 1
else:
    print("while completed without break")


# ── 6. Nested Loops ──────────────────────────────────────────────────────────

print("\n--- Nested loops ---")
for row in range(1, 4):
    for col in range(1, 4):
        print(f"{row*col:3}", end="")
    print()   # newline after each row

# Breaking out of nested loops using a flag:
found = False
for i in range(5):
    for j in range(5):
        if i + j == 7:
            found = True
            break
    if found:
        break
print(f"Found i={i}, j={j} where i+j=7")


# ── 7. match / case  (Python 3.10+) ──────────────────────────────────────────

print("\n--- match/case ---")
import sys

if sys.version_info >= (3, 10):
    # match/case is a syntax feature — must be compiled at runtime on 3.9
    exec("""
def describe_point(point):
    match point:
        case (0, 0):
            return "Origin"
        case (x, 0):
            return f"On x-axis at x={x}"
        case (0, y):
            return f"On y-axis at y={y}"
        case (x, y):
            return f"Point at ({x}, {y})"

def classify_number(n):
    match n:
        case int(x) if x < 0:
            return "negative int"
        case int(x) if x == 0:
            return "zero"
        case int(x):
            return f"positive int: {x}"
        case float(x):
            return f"float: {x}"
        case _:
            return "unknown"

print(describe_point((0, 0)))    # Origin
print(describe_point((3, 0)))    # On x-axis at x=3
print(describe_point((0, 4)))    # On y-axis at y=4
print(describe_point((2, 5)))    # Point at (2, 5)
print(classify_number(-5))
print(classify_number(0))
print(classify_number(42))
print(classify_number(3.14))
""")
else:
    print(f"  match/case requires Python 3.10+, current: {sys.version_info[:2]}")
    print("  Equivalent using if/elif:")
    def describe_point(point):
        if point == (0, 0):          return "Origin"
        elif point[1] == 0:          return f"On x-axis at x={point[0]}"
        elif point[0] == 0:          return f"On y-axis at y={point[1]}"
        else:                        return f"Point at {point}"
    for pt in [(0,0),(3,0),(0,4),(2,5)]:
        print(f"  {pt} → {describe_point(pt)}")


print("\nDone: control_flow")
