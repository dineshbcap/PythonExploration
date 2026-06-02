"""
ITERATORS AND GENERATORS
========================
The iterator protocol (__iter__/__next__), custom iterators,
generator functions (yield), yield from, generator pipelines,
send()/throw()/close(), and itertools.

Run: python 02_intermediate/04_iterators_generators.py
"""

import itertools

# ── 1. The Iterator Protocol ──────────────────────────────────────────────────

print("--- Iterator Protocol ---")
# An ITERABLE has __iter__() that returns an iterator.
# An ITERATOR has __next__() that returns the next value or raises StopIteration.

lst = [1, 2, 3]
it  = iter(lst)       # calls lst.__iter__()

print(next(it))   # 1
print(next(it))   # 2
print(next(it))   # 3
try:
    print(next(it))   # StopIteration
except StopIteration:
    print("Iterator exhausted")

# for loops are sugar over the iterator protocol:
#   it = iter(lst)
#   while True:
#       try: item = next(it)
#       except StopIteration: break
#       ... do something with item ...


# ── 2. Custom Iterator Class ──────────────────────────────────────────────────

print("\n--- Custom Iterator ---")

class CountUp:
    """Iterates integers from start to stop (inclusive)."""

    def __init__(self, start: int, stop: int):
        self.current = start
        self.stop    = stop

    def __iter__(self):
        return self   # the object itself is its own iterator

    def __next__(self):
        if self.current > self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value

for n in CountUp(1, 5):
    print(n, end=" ")
print()

# Works with all iteration tools:
print(list(CountUp(1, 5)))
print(sum(CountUp(1, 100)))   # 5050


class Fibonacci:
    """Generates Fibonacci numbers up to a given count."""

    def __init__(self, count: int):
        self.count = count
        self.a, self.b = 0, 1
        self.n = 0

    def __iter__(self): return self

    def __next__(self):
        if self.n >= self.count:
            raise StopIteration
        value = self.a
        self.a, self.b = self.b, self.a + self.b
        self.n += 1
        return value

print(list(Fibonacci(10)))


# ── 3. Generator Functions ────────────────────────────────────────────────────

print("\n--- Generator Functions ---")
# A function with `yield` returns a generator object (lazy iterator).
# Execution suspends at each yield and resumes on the next next() call.

def count_up(start: int, stop: int):
    """Generator equivalent of CountUp class above — much simpler."""
    current = start
    while current <= stop:
        yield current    # pause here, return value to caller
        current += 1     # resume here on next next()

gen = count_up(1, 5)
print(type(gen))         # <class 'generator'>
print(next(gen))         # 1
print(list(gen))         # [2, 3, 4, 5] — continues from where we left off


def fibonacci():
    """Infinite Fibonacci generator — generates forever."""
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

# Take first 10 from infinite generator using itertools.islice:
print(list(itertools.islice(fibonacci(), 10)))


# ── 4. Generator State — yield Saves Frame ────────────────────────────────────

print("\n--- Generator state ---")

def verbose_gen():
    print("  [start]")
    yield 1
    print("  [after 1]")
    yield 2
    print("  [after 2]")
    yield 3
    print("  [end]")

g = verbose_gen()
print("Calling next() 3 times:")
print(next(g))
print(next(g))
print(next(g))


# ── 5. yield from ────────────────────────────────────────────────────────────

print("\n--- yield from ---")
# Delegates to a sub-iterable; transparently forwards values (and send/throw).

def chain(*iterables):
    """Equivalent of itertools.chain."""
    for it in iterables:
        yield from it   # yield each item from sub-iterable

print(list(chain([1, 2], [3, 4], [5])))

# Recursive generator using yield from:
def flatten(nested):
    """Recursively flatten arbitrarily nested lists."""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)   # recurse into nested lists
        else:
            yield item

data = [1, [2, [3, 4], 5], [6, 7]]
print(list(flatten(data)))   # [1, 2, 3, 4, 5, 6, 7]


# ── 6. Two-way Communication: send() ─────────────────────────────────────────

print("\n--- send() ---")
# yield can also RECEIVE a value via generator.send(value).

def running_average():
    """
    Coroutine-style generator that maintains state between calls.
    First send must be None (to advance to the first yield).
    """
    total = 0.0
    count = 0
    average = None
    while True:
        value = yield average   # receive sent value, yield current average
        if value is None:
            break
        total += value
        count += 1
        average = total / count

avg = running_average()
next(avg)                        # prime the generator (advance to first yield)
print(avg.send(10))   # 10.0
print(avg.send(20))   # 15.0
print(avg.send(30))   # 20.0


# ── 7. throw() and close() ───────────────────────────────────────────────────

print("\n--- throw() and close() ---")

def safe_gen():
    try:
        for i in range(100):
            yield i
    except GeneratorExit:
        print("  Generator closed (cleanup here)")
    except ValueError as e:
        print(f"  Caught in generator: {e}")
        yield -1

g = safe_gen()
print(next(g))          # 0
print(next(g))          # 1
print(g.throw(ValueError, "oops"))  # triggers exception inside generator
g.close()               # sends GeneratorExit


# ── 8. Generator Pipeline ────────────────────────────────────────────────────

print("\n--- Generator Pipeline ---")
# Chain generators for memory-efficient stream processing.

def read_numbers(n):
    """Source: generate numbers 1..n."""
    for i in range(1, n + 1):
        yield i

def filter_even(numbers):
    """Stage: keep only even numbers."""
    for n in numbers:
        if n % 2 == 0:
            yield n

def square(numbers):
    """Stage: square each number."""
    for n in numbers:
        yield n * n

# Build pipeline — no data flows until we consume:
pipeline = square(filter_even(read_numbers(20)))
print(list(pipeline))  # [4, 16, 36, 64, 100, 144, 196, 256, 324, 400]
# Only ONE number exists in memory at a time throughout the pipeline!


# ── 9. itertools — Standard Library Generators ───────────────────────────────

print("\n--- itertools ---")

# Infinite iterators
counter = itertools.count(start=1, step=2)      # 1, 3, 5, 7, ...
print(list(itertools.islice(counter, 5)))       # [1, 3, 5, 7, 9]

cycle  = itertools.cycle(["R", "G", "B"])
print(list(itertools.islice(cycle, 7)))         # ['R','G','B','R','G','B','R']

repeat = itertools.repeat("x", 4)
print(list(repeat))                             # ['x','x','x','x']

# Combining iterators
print(list(itertools.chain([1, 2], [3, 4], [5])))         # flatten
print(list(itertools.chain.from_iterable([[1,2],[3,4]])))  # from nested

a = [1, 2, 3]
b = [10, 20, 30]
print(list(itertools.starmap(lambda x, y: x * y, zip(a, b))))  # [10, 40, 90]

# Selecting elements
print(list(itertools.takewhile(lambda x: x < 5, [1, 2, 3, 6, 7, 2])))  # [1,2,3]
print(list(itertools.dropwhile(lambda x: x < 5, [1, 2, 3, 6, 7, 2])))  # [6,7,2]
print(list(itertools.compress("ABCDE", [1, 0, 1, 0, 1])))               # [A,C,E]

# Combinatoric iterators
print(list(itertools.permutations("AB", 2)))   # [('A','B'),('B','A')]
print(list(itertools.combinations("ABC", 2)))  # [('A','B'),('A','C'),('B','C')]
print(list(itertools.product("AB", repeat=2))) # cartesian product

# Grouping (input must be sorted by key!)
data = sorted(["apple","avocado","banana","blueberry","cherry"], key=lambda x: x[0])
for letter, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"  {letter}: {list(group)}")

# Accumulate
print(list(itertools.accumulate([1, 2, 3, 4, 5])))            # running sum
print(list(itertools.accumulate([1, 2, 3, 4, 5], max)))       # running max
import operator
print(list(itertools.accumulate([1, 2, 3, 4, 5], operator.mul))) # factorial!


print("\nDone: iterators_generators")
