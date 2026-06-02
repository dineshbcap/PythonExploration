"""
SETS
====
Unordered collections of unique, hashable elements.
Covers creation, CRUD, set algebra, frozen sets, and use cases.

Run: python 01_basics/08_sets.py
"""

# ── 1. Creation ───────────────────────────────────────────────────────────────

print("--- Creation ---")
empty   = set()           # NOT {} — that creates an empty dict
numbers = {1, 2, 3, 4, 5}
mixed   = {1, "hello", 3.14, True}   # True and 1 are the SAME element (1 == True)

# From other iterables — duplicates are silently removed
from_list  = set([1, 2, 2, 3, 3, 3])
from_str   = set("banana")            # {'b', 'a', 'n'} — only unique chars
from_range = set(range(5))

print(numbers)
print(from_list)   # {1, 2, 3}
print(from_str)    # {'b', 'a', 'n'} (unordered)
print(mixed)       # True and 1 — only one survives: {1, 'hello', 3.14}


# ── 2. Membership Testing ─────────────────────────────────────────────────────

print("\n--- Membership (O(1) average) ---")
primes = {2, 3, 5, 7, 11, 13}
print(7 in primes)     # True
print(4 in primes)     # False
print(4 not in primes) # True

# Sets shine here: O(1) average vs O(n) for lists
import timeit
lst  = list(range(100_000))
s    = set(lst)
t1 = timeit.timeit(lambda: 99_999 in lst, number=1000)
t2 = timeit.timeit(lambda: 99_999 in s,   number=1000)
print(f"list lookup: {t1:.4f}s vs set lookup: {t2:.6f}s")


# ── 3. Adding and Removing ────────────────────────────────────────────────────

print("\n--- CRUD ---")
s = {1, 2, 3}

s.add(4)         # add one element — no-op if already present
s.add(2)         # still {1, 2, 3, 4} — no duplicate
print(s)

s.update([5, 6, 7])    # add multiple elements (from any iterable)
print(s)

s.remove(7)            # raises KeyError if element not found
s.discard(99)          # SAFE remove — no error if element absent
print(s)

popped = s.pop()       # removes and returns AN ARBITRARY element (sets are unordered)
print(f"Popped: {popped}, remaining: {s}")

s.clear()              # remove all elements
print(s)


# ── 4. Set Algebra ────────────────────────────────────────────────────────────

print("\n--- Set Algebra ---")
A = {1, 2, 3, 4, 5}
B = {4, 5, 6, 7, 8}

# Union — elements in A OR B (or both)
print(f"A | B   = {A | B}")
print(f"union() = {A.union(B)}")            # same result

# Intersection — elements in BOTH A and B
print(f"A & B           = {A & B}")
print(f"intersection()  = {A.intersection(B)}")

# Difference — elements in A but NOT in B
print(f"A - B           = {A - B}")
print(f"difference()    = {A.difference(B)}")

# Symmetric difference — elements in either but NOT both
print(f"A ^ B                    = {A ^ B}")
print(f"symmetric_difference()   = {A.symmetric_difference(B)}")

# In-place versions:
s = {1, 2, 3}
s |= {4, 5};   print(s)    # {1, 2, 3, 4, 5}
s &= {2, 3, 4};print(s)    # {2, 3, 4}
s -= {2};      print(s)    # {3, 4}
s ^= {3, 5};   print(s)    # {4, 5}


# ── 5. Subset / Superset / Disjoint ──────────────────────────────────────────

print("\n--- Relationships ---")
A = {1, 2, 3}
B = {1, 2, 3, 4, 5}
C = {10, 11}

print(A.issubset(B))       # True  — every element of A is in B
print(A <= B)              # same

print(B.issuperset(A))     # True  — B contains all elements of A
print(B >= A)              # same

print(A < B)               # True  — proper subset (A <= B and A != B)
print(A <= A)              # True  — every set is a subset of itself
print(A < A)               # False — not proper

print(A.isdisjoint(C))     # True  — no elements in common


# ── 6. Set Comprehension ──────────────────────────────────────────────────────

print("\n--- Set Comprehension ---")
squares = {x ** 2 for x in range(10)}
print(squares)

# Deduplication via set comprehension:
words = ["hello", "world", "hello", "python", "world"]
unique_upper = {w.upper() for w in words}
print(unique_upper)


# ── 7. frozenset ──────────────────────────────────────────────────────────────

print("\n--- frozenset ---")
# Immutable set — hashable, so it can be a dict key or element of another set

fs = frozenset([1, 2, 3])
print(fs)
print(type(fs))

# fs.add(4)   # AttributeError — frozenset is immutable

# Use as dict key:
cache = {frozenset([1, 2]): "pair", frozenset([3, 4, 5]): "triple"}
print(cache[frozenset([1, 2])])   # "pair"

# Set of frozensets:
sets_collection = {frozenset([1, 2]), frozenset([3, 4]), frozenset([1, 2])}
print(sets_collection)   # only 2 unique frozensets


# ── 8. Common Patterns ────────────────────────────────────────────────────────

print("\n--- Common Patterns ---")

# Deduplicate a list while preserving order (Python 3.7+ dicts maintain order):
dupes = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
deduped = list(dict.fromkeys(dupes))   # preserves order
print(deduped)   # [3, 1, 4, 5, 9, 2, 6]

# Simple dedup (order not guaranteed via set):
print(list(set(dupes)))

# Find items in list1 but not list2:
list1 = [1, 2, 3, 4, 5]
list2 = [3, 4, 5, 6, 7]
only_in_1 = set(list1) - set(list2)
print(only_in_1)   # {1, 2}

# Common items:
common = set(list1) & set(list2)
print(common)   # {3, 4, 5}


print("\nDone: sets")
