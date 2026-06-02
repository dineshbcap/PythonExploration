"""
LISTS
=====
The most versatile mutable sequence. Covers creation, CRUD operations, slicing,
sorting, searching, copying, nested lists, and performance characteristics.

Run: python 01_basics/06_lists.py
"""

# ── 1. Creation ───────────────────────────────────────────────────────────────

print("--- Creation ---")
empty   = []
nums    = [1, 2, 3, 4, 5]
mixed   = [42, "hello", True, 3.14, None]     # can mix types
nested  = [[1, 2], [3, 4], [5, 6]]
from_range = list(range(1, 11))                # [1, 2, 3, ..., 10]
from_str   = list("abc")                       # ['a', 'b', 'c']

print(nums)
print(mixed)
print(from_range)


# ── 2. Indexing and Slicing ───────────────────────────────────────────────────

print("\n--- Indexing & Slicing ---")
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

print(fruits[0])       # apple
print(fruits[-1])      # elderberry
print(fruits[1:3])     # ['banana', 'cherry']
print(fruits[::2])     # ['apple', 'cherry', 'elderberry']
print(fruits[::-1])    # reversed list

# Slice assignment — replace a sub-range with new elements
fruits[1:3] = ["blueberry", "coconut", "durian"]
print(fruits)

# Delete a slice
del fruits[1:3]
print(fruits)


# ── 3. Adding Elements ────────────────────────────────────────────────────────

print("\n--- Adding ---")
lst = [1, 2, 3]

lst.append(4)           # add to end — O(1) amortized
lst.insert(1, 99)       # insert at index — O(n), shifts elements right
lst.extend([5, 6, 7])   # extend with another iterable — O(k)
lst += [8, 9]           # same as extend but creates new list then assigns
print(lst)

# + creates a new list
new_lst = lst + [10, 11]
print(new_lst)
print(lst is not new_lst)   # True — different objects


# ── 4. Removing Elements ──────────────────────────────────────────────────────

print("\n--- Removing ---")
lst = [1, 2, 3, 2, 4, 2]

lst.remove(2)     # removes the FIRST occurrence of value 2
print(lst)        # [1, 3, 2, 4, 2]

popped = lst.pop()    # removes and returns LAST element — O(1)
print(popped, lst)

popped = lst.pop(1)   # removes and returns element at index — O(n)
print(popped, lst)

del lst[0]        # delete by index — O(n)
print(lst)

lst.clear()       # remove all elements
print(lst)


# ── 5. Searching ──────────────────────────────────────────────────────────────

print("\n--- Searching ---")
nums = [10, 20, 30, 20, 40]

print(20 in nums)           # True — O(n) linear scan
print(nums.index(20))       # 1   — index of FIRST occurrence (ValueError if absent)
print(nums.count(20))       # 2   — count of all occurrences


# ── 6. Sorting ────────────────────────────────────────────────────────────────

print("\n--- Sorting ---")
nums = [3, 1, 4, 1, 5, 9, 2, 6]

# sorted() — returns a NEW sorted list; original unchanged
print(sorted(nums))
print(sorted(nums, reverse=True))

# list.sort() — sorts IN PLACE; returns None
nums.sort()
print(nums)
nums.sort(reverse=True)
print(nums)

# Custom sort with key function:
words = ["banana", "apple", "cherry", "date"]
print(sorted(words, key=len))          # sort by string length
print(sorted(words, key=str.lower))    # case-insensitive sort

people = [("Alice", 30), ("Bob", 25), ("Carol", 35)]
print(sorted(people, key=lambda p: p[1]))          # sort by age
print(sorted(people, key=lambda p: p[0].lower())) # sort by name

# Stable sort — elements with equal keys keep their original relative order
grades = [("B", 88), ("A", 95), ("B", 91), ("A", 92)]
print(sorted(grades, key=lambda g: g[0]))  # ties in grade maintain position


# ── 7. Reversing ──────────────────────────────────────────────────────────────

print("\n--- Reversing ---")
lst = [1, 2, 3, 4, 5]
lst.reverse()           # in-place, returns None
print(lst)
print(list(reversed(lst)))  # reversed() returns an iterator, not a list


# ── 8. Copying ────────────────────────────────────────────────────────────────

print("\n--- Copying ---")
original = [1, [2, 3], 4]

# Shallow copy — top-level is independent, but nested objects are shared
shallow = original.copy()           # or: original[:]  or list(original)
shallow[0] = 99
shallow[1].append(99)               # mutates the shared inner list
print(f"original: {original}")      # [1, [2, 3, 99], 4] — inner list changed!
print(f"shallow:  {shallow}")       # [99, [2, 3, 99], 4]

import copy
original = [1, [2, 3], 4]
deep = copy.deepcopy(original)      # fully independent at all depths
deep[1].append(99)
print(f"original after deepcopy: {original}")  # [1, [2, 3], 4] — unchanged
print(f"deep: {deep}")                          # [1, [2, 3, 99], 4]


# ── 9. Nested Lists (2-D matrix) ──────────────────────────────────────────────

print("\n--- Nested lists ---")
# Creating a 3×3 matrix of zeros — MUST use list comprehension, not * trick
matrix = [[0] * 3 for _ in range(3)]   # each row is a separate list
matrix[0][0] = 9
print(matrix)    # [[9, 0, 0], [0, 0, 0], [0, 0, 0]]

# Wrong way — all rows are the SAME object:
bad_matrix = [[0] * 3] * 3
bad_matrix[0][0] = 9
print(bad_matrix)  # [[9, 0, 0], [9, 0, 0], [9, 0, 0]] — all changed!

# Flatten a 2-D list
flat = [x for row in matrix for x in row]
print(flat)


# ── 10. Performance Notes ─────────────────────────────────────────────────────

print("\n--- Performance ---")
# Operation      Time complexity
# append(x)      O(1) amortized
# pop()          O(1)  (from end)
# pop(i)         O(n)  (shift needed)
# insert(i, x)   O(n)
# x in lst       O(n)  (linear scan)
# lst[i]         O(1)
# len(lst)       O(1)

# When membership tests are frequent, use a set instead:
lst = list(range(1_000_000))
s   = set(lst)
import timeit
print("list 'in' (1M items):", timeit.timeit(lambda: 999_999 in lst, number=100))
print("set  'in' (1M items):", timeit.timeit(lambda: 999_999 in s,   number=100))


# ── 11. Miscellaneous Useful Functions ───────────────────────────────────────

print("\n--- Misc ---")
nums = [4, 1, 7, 3, 9]
print(f"min={min(nums)}, max={max(nums)}, sum={sum(nums)}")
print(f"len={len(nums)}")
print(list(enumerate(nums)))    # [(0, 4), (1, 1), ...]
print(list(zip(nums, nums)))    # [(4,4), (1,1), ...]

# any() / all()
print(any(n > 8 for n in nums))    # True  — at least one > 8
print(all(n > 0 for n in nums))    # True  — all positive


print("\nDone: lists")
