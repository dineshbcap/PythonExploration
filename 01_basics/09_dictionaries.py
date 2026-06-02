"""
DICTIONARIES
============
Mutable key-value mappings. Python 3.7+ guarantees insertion order.
Covers creation, CRUD, iteration, merging, defaultdict, Counter,
OrderedDict, and common idioms.

Run: python 01_basics/09_dictionaries.py
"""

from collections import defaultdict, OrderedDict, Counter

# ── 1. Creation ───────────────────────────────────────────────────────────────

print("--- Creation ---")
empty  = {}
person = {"name": "Alice", "age": 30, "city": "NYC"}

# Constructor forms:
d1 = dict(name="Bob", age=25)           # keyword args
d2 = dict([("x", 1), ("y", 2)])         # list of (key, value) pairs
d3 = dict.fromkeys(["a", "b", "c"], 0)  # all keys, same default value

print(person)
print(d1)
print(d2)
print(d3)

# Keys must be hashable (immutable): str, int, float, bool, tuple, frozenset
valid = {(1, 2): "point", 42: "answer", True: "yes"}
# {[1,2]: "oops"}  # TypeError — lists are unhashable


# ── 2. Accessing Values ───────────────────────────────────────────────────────

print("\n--- Access ---")
d = {"a": 1, "b": 2, "c": 3}

print(d["a"])           # 1 — KeyError if key absent
print(d.get("b"))       # 2 — returns None if key absent (safe)
print(d.get("z"))       # None
print(d.get("z", 99))   # 99 — return default if key absent

# Check existence before access:
if "a" in d:
    print(d["a"])


# ── 3. Adding and Updating ────────────────────────────────────────────────────

print("\n--- Adding & Updating ---")
d = {"a": 1}

d["b"] = 2            # add new key
d["a"] = 99           # overwrite existing key
print(d)

d.update({"c": 3, "d": 4})   # merge another dict
d.update(e=5, f=6)            # keyword arguments
print(d)

# setdefault — set only if key ABSENT; returns current value
d.setdefault("g", 0)
d.setdefault("a", 0)   # "a" already exists — unchanged
print(d)


# ── 4. Removing ───────────────────────────────────────────────────────────────

print("\n--- Removing ---")
d = {"a": 1, "b": 2, "c": 3, "d": 4}

val = d.pop("b")          # remove by key, return value; KeyError if absent
print(f"popped: {val}, d={d}")

val = d.pop("z", None)    # safe version with default
print(f"missing pop: {val}")

key, val = d.popitem()    # remove and return LAST inserted key-value pair (LIFO)
print(f"popitem: {key}={val}, d={d}")

del d["a"]                # delete by key — KeyError if absent
print(d)

d.clear()
print(d)


# ── 5. Iteration ──────────────────────────────────────────────────────────────

print("\n--- Iteration ---")
config = {"host": "localhost", "port": 5432, "db": "myapp"}

# Keys (default iteration)
for key in config:
    print(f"  key: {key}")

# Values
for value in config.values():
    print(f"  value: {value}")

# Key-value pairs — most common
for key, value in config.items():
    print(f"  {key} = {value}")

# Keys/values/items return VIEW objects — they reflect live changes
keys_view = config.keys()
config["new_key"] = "new_val"
print(keys_view)   # includes "new_key" — it's a live view


# ── 6. Dictionary Comprehension ───────────────────────────────────────────────

print("\n--- Dict Comprehension ---")
squares = {n: n**2 for n in range(1, 6)}
print(squares)

# Filter + transform:
raw = {"alice": 85, "bob": 92, "carol": 78, "dave": 88}
passed = {name: score for name, score in raw.items() if score >= 80}
print(passed)

# Invert a dict (swap keys and values — only safe if values are unique):
inverted = {v: k for k, v in squares.items()}
print(inverted)

# Conditional value:
grades = {name: "pass" if score >= 80 else "fail" for name, score in raw.items()}
print(grades)


# ── 7. Merging Dicts ──────────────────────────────────────────────────────────

print("\n--- Merging ---")
defaults = {"color": "red",  "size": "M", "qty": 1}
overrides = {"color": "blue", "qty": 5}

# Method 1: unpack with **  (Python 3.5+)
merged = {**defaults, **overrides}   # later dict wins on duplicate keys
print(merged)

# Method 2: | operator (Python 3.9+)
merged = defaults | overrides
print(merged)

# In-place merge with |=
defaults |= overrides
print(defaults)

# Method 3: update() modifies in place
d = {"a": 1}
d.update({"b": 2, "a": 99})
print(d)


# ── 8. defaultdict ────────────────────────────────────────────────────────────

print("\n--- defaultdict ---")
# Never raises KeyError; automatically creates a default value for new keys.

# Group words by their first letter:
words = ["apple", "banana", "avocado", "blueberry", "cherry", "apricot"]
groups = defaultdict(list)   # default factory: list()
for word in words:
    groups[word[0]].append(word)
print(dict(groups))

# Count occurrences without initializing:
counter = defaultdict(int)   # default factory: int() → 0
for word in words:
    counter[word[0]] += 1
print(dict(counter))

# Nested defaultdict:
graph = defaultdict(set)
edges = [(1, 2), (1, 3), (2, 3), (3, 4)]
for u, v in edges:
    graph[u].add(v)
    graph[v].add(u)
print({k: sorted(v) for k, v in graph.items()})


# ── 9. Counter ────────────────────────────────────────────────────────────────

print("\n--- Counter ---")
# Specialized dict for counting hashable elements.
from collections import Counter

text = "the quick brown fox jumps over the lazy dog"
word_freq = Counter(text.split())
print(word_freq.most_common(3))   # top 3 most common words

char_freq = Counter(text)
print(char_freq.most_common(5))

# Arithmetic on Counters:
c1 = Counter("aab")
c2 = Counter("abc")
print(c1 + c2)    # add counts
print(c1 - c2)    # subtract (drops negatives/zeros)
print(c1 & c2)    # min of each
print(c1 | c2)    # max of each


# ── 10. OrderedDict ───────────────────────────────────────────────────────────

print("\n--- OrderedDict ---")
# In Python 3.7+ regular dicts maintain insertion order.
# OrderedDict is still useful for move_to_end() and LRU cache implementations.

od = OrderedDict([("a", 1), ("b", 2), ("c", 3)])
od.move_to_end("a")          # move "a" to the last position
print(od)

od.move_to_end("c", last=False)  # move "c" to the FIRST position
print(od)


# ── 11. Common Idioms ─────────────────────────────────────────────────────────

print("\n--- Idioms ---")
inventory = {"apple": 10, "banana": 0, "cherry": 5}

# Filter out zero-stock items
in_stock = {k: v for k, v in inventory.items() if v > 0}
print(in_stock)

# Increment count (three styles):
d = {}
key = "hits"
# Style 1: get with default
d[key] = d.get(key, 0) + 1
# Style 2: setdefault
d.setdefault(key, 0)
d[key] += 1
# Style 3: defaultdict (preferred for frequent counting)
dd = defaultdict(int)
dd[key] += 1
dd[key] += 1

# Nested dict access without KeyError chains:
data = {"user": {"profile": {"name": "Alice"}}}
name = data.get("user", {}).get("profile", {}).get("name", "Unknown")
print(name)


print("\nDone: dictionaries")
