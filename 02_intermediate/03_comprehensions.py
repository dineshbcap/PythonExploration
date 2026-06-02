"""
COMPREHENSIONS
==============
List, dict, set comprehensions, and generator expressions.
The most Pythonic way to build collections from iterables.

Run: python 02_intermediate/03_comprehensions.py
"""

# ── 1. List Comprehension ─────────────────────────────────────────────────────

print("--- List Comprehension ---")
# Syntax: [expression FOR item IN iterable IF condition]

# Basic: squares of 0-9
squares = [x**2 for x in range(10)]
print(squares)

# With filter: even squares only
even_squares = [x**2 for x in range(10) if x % 2 == 0]
print(even_squares)

# Transform strings
words = ["hello", "world", "python"]
upper = [w.upper() for w in words]
print(upper)

# Conditional expression in the output (ternary):
labels = ["even" if x % 2 == 0 else "odd" for x in range(8)]
print(labels)

# Equivalent for-loop for comparison:
result = []
for x in range(10):
    if x % 2 == 0:
        result.append(x**2)
# [0, 4, 16, 36, 64] — same as even_squares

# Nested: Cartesian product
pairs = [(x, y) for x in range(3) for y in range(3)]
print(pairs)

# Flatten a 2-D list:
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [cell for row in matrix for cell in row]
print(flat)   # [1, 2, 3, 4, 5, 6, 7, 8, 9]


# ── 2. Nested Comprehension (matrix transpose) ───────────────────────────────

print("\n--- Nested comprehension ---")
matrix = [[1, 2, 3],
          [4, 5, 6],
          [7, 8, 9]]

# Transpose: rows become columns
transposed = [[row[i] for row in matrix] for i in range(3)]
for row in transposed:
    print(row)

# Same result with zip(*matrix):
transposed2 = list(map(list, zip(*matrix)))
print(transposed2)


# ── 3. Dictionary Comprehension ──────────────────────────────────────────────

print("\n--- Dict Comprehension ---")
# Syntax: {key_expr: value_expr FOR item IN iterable IF condition}

# Word length map
words = ["apple", "banana", "cherry"]
lengths = {word: len(word) for word in words}
print(lengths)

# Invert a dict (swap keys and values):
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(inverted)

# Filter and transform:
scores = {"Alice": 85, "Bob": 92, "Carol": 73, "Dave": 88}
honor_roll = {name: score for name, score in scores.items() if score >= 85}
print(honor_roll)

# Normalize keys:
raw = {"  Name ": "Alice", "AGE": 30, "city ": "NYC"}
clean = {k.strip().lower(): v for k, v in raw.items()}
print(clean)


# ── 4. Set Comprehension ─────────────────────────────────────────────────────

print("\n--- Set Comprehension ---")
# Syntax: {expression FOR item IN iterable IF condition}
# Automatically deduplicates.

nums = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique_squares = {x**2 for x in nums}
print(unique_squares)

# Unique first characters:
words = ["apple", "avocado", "banana", "cherry", "apricot"]
first_chars = {w[0] for w in words}
print(first_chars)   # {'a', 'b', 'c'}


# ── 5. Generator Expressions ─────────────────────────────────────────────────

print("\n--- Generator Expressions ---")
# Syntax: (expression FOR item IN iterable IF condition)
# LAZY — computes values on demand instead of building a full list in memory.

# A generator expression looks like a list comprehension but uses ()
gen = (x**2 for x in range(10))
print(gen)          # <generator object ...> — not evaluated yet
print(next(gen))    # 0   — computes first value on demand
print(next(gen))    # 1
print(list(gen))    # [4, 9, 16, 25, 36, 49, 64, 81] — rest (0,1 already consumed)

# Generators are SINGLE-USE iterators — once exhausted, they're done
gen2 = (x**2 for x in range(5))
print(sum(gen2))    # 30 — passes each value to sum() without building a list
print(sum(gen2))    # 0  — already exhausted!

# Memory comparison:
import sys
list_comp = [x**2 for x in range(10_000)]
gen_expr  = (x**2 for x in range(10_000))
print(f"list size:  {sys.getsizeof(list_comp):,} bytes")
print(f"gen  size:  {sys.getsizeof(gen_expr):,} bytes")  # tiny regardless of size


# ── 6. Generator Expressions as Function Arguments ────────────────────────────

print("\n--- Generators in functions ---")
# When a generator expression is the only argument, the extra () can be omitted.
data = [1, 3, 5, 7, 9]

total    = sum(x**2 for x in data)           # no double ()
max_val  = max(x for x in data if x > 4)
filtered = list(filter(None, (x % 2 for x in data)))

print(f"sum of squares: {total}")
print(f"max > 4: {max_val}")

# any() and all() with generators — short-circuits:
has_even = any(x % 2 == 0 for x in [1, 3, 4, 7])   # stops at 4
all_pos  = all(x > 0      for x in [1, 2, 3, -1])   # stops at -1
print(has_even, all_pos)


# ── 7. Walrus Operator in Comprehensions (Python 3.8+) ───────────────────────

print("\n--- Walrus in comprehensions ---")
# := lets you compute a value once and both filter AND use it.

import math
results = [y for x in range(20) if (y := math.sqrt(x)) > 3]
print(results[:5])

# Without walrus — redundant computation:
# [math.sqrt(x) for x in range(20) if math.sqrt(x) > 3]  # sqrt called twice


# ── 8. Performance Tips ───────────────────────────────────────────────────────

print("\n--- Performance ---")
import timeit

# List comprehension vs map():
t_comp = timeit.timeit("[x**2 for x in range(1000)]", number=10_000)
t_map  = timeit.timeit("list(map(lambda x: x**2, range(1000)))", number=10_000)
print(f"list comp: {t_comp:.3f}s")
print(f"map():     {t_map:.3f}s")
# Comprehensions are often faster due to fewer function call overheads

# Generator expression for large pipelines (memory-efficient):
total = sum(x**2 for x in range(1_000_000) if x % 2 == 0)
print(f"Sum of even squares (0–999999): {total}")


print("\nDone: comprehensions")
