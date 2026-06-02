"""
ABSTRACT BASE CLASSES (ABCs)
=============================
abc.ABC, @abstractmethod, abstract properties/class methods,
virtual subclasses (__subclasshook__), and built-in ABCs from collections.abc.

Run: python 03_advanced/06_abstract_base_classes.py
"""

from abc import ABC, ABCMeta, abstractmethod, abstractclassmethod
import collections.abc

# ── 1. Basic ABC ──────────────────────────────────────────────────────────────

print("--- Basic ABC ---")
# ABC prevents instantiation of a class that has unimplemented abstract methods.

class Shape(ABC):
    """Abstract base for all 2-D shapes."""

    @abstractmethod
    def area(self) -> float:
        """Return the area of the shape."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        """Return the perimeter of the shape."""
        ...

    # Non-abstract method — shared implementation available to all subclasses
    def describe(self) -> str:
        return (f"{type(self).__name__}: "
                f"area={self.area():.2f}, perimeter={self.perimeter():.2f}")

# Direct instantiation raises TypeError:
try:
    s = Shape()
except TypeError as e:
    print(f"Cannot instantiate: {e}")

# Must implement all abstract methods:
class Circle(Shape):
    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        import math
        return math.pi * self.radius ** 2

    def perimeter(self) -> float:
        import math
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    def __init__(self, w: float, h: float):
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

    def perimeter(self):
        return 2 * (self.w + self.h)

shapes = [Circle(5), Rectangle(4, 6)]
for s in shapes:
    print(s.describe())


# ── 2. Abstract Properties and Class Methods ──────────────────────────────────

print("\n--- Abstract properties ---")

class Animal(ABC):

    @property
    @abstractmethod
    def sound(self) -> str:
        """The sound the animal makes."""
        ...

    @classmethod
    @abstractmethod
    def kingdom(cls) -> str:
        """Biological kingdom (must be class method)."""
        ...

    @staticmethod
    @abstractmethod
    def breath_type() -> str:
        """How the animal breathes."""
        ...

    def speak(self):
        return f"{type(self).__name__} says: {self.sound}"


class Dog(Animal):
    @property
    def sound(self):
        return "Woof"

    @classmethod
    def kingdom(cls):
        return "Animalia"

    @staticmethod
    def breath_type():
        return "lungs"

d = Dog()
print(d.speak())
print(Dog.kingdom())
print(Dog.breath_type())


# ── 3. Partial Concrete Class ─────────────────────────────────────────────────

print("\n--- Partial concrete class ---")
# A class can implement SOME abstract methods; remaining ones stay abstract.

class Polygon(Shape):
    """Partially implements Shape — perimeter is concrete, area is still abstract."""

    def __init__(self, sides: list[float]):
        self.sides = sides

    def perimeter(self) -> float:
        return sum(self.sides)   # concrete implementation

    # area() is still abstract — Polygon is still abstract

    # Attempting to instantiate Polygon still raises TypeError
    # because area() is unimplemented.

class RegularPolygon(Polygon):
    """Concrete: knows how to compute area for a regular polygon."""

    def __init__(self, n: int, side: float):
        import math
        super().__init__([side] * n)
        self.n    = n
        self.side = side

    def area(self) -> float:
        import math
        return (self.n * self.side**2) / (4 * math.tan(math.pi / self.n))

rp = RegularPolygon(6, 5)   # regular hexagon with side 5
print(rp.describe())


# ── 4. Virtual Subclasses with __subclasshook__ ───────────────────────────────

print("\n--- Virtual subclasses ---")
# register() and __subclasshook__ let you declare a class as a subclass
# of an ABC WITHOUT it actually inheriting from it.
# This is the formal foundation of duck typing.

class Sizeable(ABC):
    """Anything with a __len__ method is considered Sizeable."""

    @classmethod
    def __subclasshook__(cls, C):
        # Return True  → C is treated as a virtual subclass of Sizeable
        # Return False → C is NOT
        # Return NotImplemented → fall back to normal subclass check
        if cls is Sizeable:
            if any("__len__" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented

class MyList:
    def __init__(self, items):
        self._items = list(items)
    def __len__(self):
        return len(self._items)

ml = MyList([1, 2, 3])

# MyList never inherited from Sizeable, but isinstance returns True:
print(isinstance(ml, Sizeable))      # True  — __len__ found
print(isinstance([1, 2], Sizeable))  # True  — list has __len__
print(isinstance(42, Sizeable))      # False — int has no __len__

# register() — explicitly declare an existing class as a virtual subclass:
class LegacyContainer:
    """Old class we cannot modify that happens to be Sizeable."""
    def __len__(self): return 0

# Even without __subclasshook__ matching, explicit registration works:
Sizeable.register(LegacyContainer)
print(isinstance(LegacyContainer(), Sizeable))  # True


# ── 5. ABCMeta Directly ────────────────────────────────────────────────────────

print("\n--- ABCMeta directly ---")
# ABC is just `class ABC(metaclass=ABCMeta): pass`.
# You can use ABCMeta directly when you already have a custom metaclass.

class Printable(metaclass=ABCMeta):
    @abstractmethod
    def to_string(self) -> str: ...

class Document(Printable):
    def __init__(self, text):
        self.text = text
    def to_string(self):
        return self.text

d = Document("Hello, World!")
print(d.to_string())


# ── 6. Built-in ABCs from collections.abc ────────────────────────────────────

print("\n--- collections.abc ---")
# The standard library defines many ABCs for common protocols.

# Iterable — requires __iter__
class NumberRange(collections.abc.Iterable):
    def __init__(self, start, stop):
        self.start = start
        self.stop  = stop

    def __iter__(self):
        return iter(range(self.start, self.stop))

for n in NumberRange(3, 7):
    print(n, end=" ")
print()

# Mapping — requires __getitem__, __len__, __iter__; provides get, keys, values, etc.
class FrozenDict(collections.abc.Mapping):
    def __init__(self, d):
        self._d = dict(d)

    def __getitem__(self, key):   return self._d[key]
    def __len__(self):            return len(self._d)
    def __iter__(self):           return iter(self._d)

fd = FrozenDict({"a": 1, "b": 2})
print(dict(fd))
print(fd.get("a"))       # .get() provided for FREE by Mapping
print(list(fd.keys()))   # .keys() provided for FREE
print("a" in fd)         # __contains__ provided for FREE

# MutableSequence — provide 5 abstract methods, get 18 mixin methods for free:
class LimitedList(collections.abc.MutableSequence):
    def __init__(self, maxlen):
        self._data = []
        self.maxlen = maxlen

    def __getitem__(self, idx):
        return self._data[idx]

    def __setitem__(self, idx, value):
        self._data[idx] = value

    def __delitem__(self, idx):
        del self._data[idx]

    def __len__(self):
        return len(self._data)

    def insert(self, idx, value):
        if len(self._data) >= self.maxlen:
            raise OverflowError(f"Max size {self.maxlen} reached")
        self._data.insert(idx, value)

ll = LimitedList(3)
ll.append(1)     # append() is a free mixin method built on insert()
ll.append(2)
ll.append(3)
print(list(ll))
try:
    ll.append(4)
except OverflowError as e:
    print(f"Caught: {e}")

# Key collections.abc ABCs:
# Container      — __contains__
# Iterable       — __iter__
# Iterator       — __next__, __iter__
# Sized          — __len__
# Callable       — __call__
# Sequence       — immutable sequence (+ mixin methods)
# MutableSequence
# Set
# MutableSet
# Mapping
# MutableMapping
# Awaitable, Coroutine, AsyncIterable, etc.

# Quick isinstance checks:
print(isinstance([1,2,3], collections.abc.MutableSequence))  # True
print(isinstance((1,2),   collections.abc.Sequence))         # True
print(isinstance({},      collections.abc.MutableMapping))   # True
print(isinstance(set(),   collections.abc.MutableSet))       # True


print("\nDone: abstract_base_classes")
