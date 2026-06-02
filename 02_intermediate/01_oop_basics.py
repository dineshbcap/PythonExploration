"""
OOP BASICS
==========
Classes, __init__, instance attributes, class attributes, instance methods,
class methods, static methods, properties, __repr__/__str__, and dunder methods.

Run: python 02_intermediate/01_oop_basics.py
"""

# ── 1. Defining a Class ───────────────────────────────────────────────────────

class Dog:
    """A simple model of a dog."""

    # Class attribute — shared by ALL instances
    species = "Canis lupus familiaris"
    count   = 0   # tracks how many Dog objects were created

    # __init__ is the initializer (not the constructor; __new__ is)
    def __init__(self, name: str, breed: str, age: int):
        # Instance attributes — unique to each object
        self.name  = name
        self.breed = breed
        self.age   = age
        Dog.count += 1   # access class attribute via class name

    # Instance method — receives `self` (the instance)
    def bark(self) -> str:
        return f"{self.name} says: Woof!"

    def birthday(self):
        self.age += 1
        return self.age

    # __repr__ — unambiguous representation for developers
    # Called by repr() and as fallback for str() in containers
    def __repr__(self) -> str:
        return f"Dog(name={self.name!r}, breed={self.breed!r}, age={self.age})"

    # __str__ — human-readable representation
    # Called by print() and str()
    def __str__(self) -> str:
        return f"{self.name} ({self.breed}, {self.age} yrs)"


# ── 2. Creating Instances ─────────────────────────────────────────────────────

print("--- Instances ---")
rex   = Dog("Rex",   "German Shepherd", 4)
buddy = Dog("Buddy", "Labrador",        2)

print(rex)          # uses __str__
print(repr(rex))    # uses __repr__
print(f"{rex!r}")   # explicit __repr__ in f-string

print(rex.bark())
print(buddy.bark())

# Access class attribute through instance or class:
print(rex.species)
print(Dog.species)
print(f"Total dogs: {Dog.count}")   # 2


# ── 3. Class Methods ──────────────────────────────────────────────────────────

print("\n--- Class Methods ---")

class Circle:
    PI = 3.14159265

    def __init__(self, radius: float):
        self.radius = radius

    @classmethod
    def from_diameter(cls, diameter: float) -> "Circle":
        """Alternative constructor — creates Circle from diameter."""
        return cls(diameter / 2)   # cls is the class (Circle), not instance

    @classmethod
    def unit_circle(cls) -> "Circle":
        return cls(1.0)

    def area(self) -> float:
        return self.PI * self.radius ** 2

    def __repr__(self) -> str:
        return f"Circle(radius={self.radius})"

c1 = Circle(5)
c2 = Circle.from_diameter(10)   # alternative constructor
c3 = Circle.unit_circle()

print(c1, c2, c3)
print(f"Area of c1: {c1.area():.2f}")


# ── 4. Static Methods ─────────────────────────────────────────────────────────

print("\n--- Static Methods ---")

class MathUtils:
    """Utility class — groups related functions, no instance state needed."""

    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if n is a prime number."""
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Euclidean algorithm for greatest common divisor."""
        while b:
            a, b = b, a % b
        return a

print(MathUtils.is_prime(17))    # True
print(MathUtils.is_prime(18))    # False
print(MathUtils.gcd(48, 18))     # 6


# ── 5. Properties ─────────────────────────────────────────────────────────────

print("\n--- Properties ---")

class Temperature:
    """Demonstrates @property for controlled attribute access."""

    def __init__(self, celsius: float):
        self._celsius = celsius   # leading _ signals "private by convention"

    @property
    def celsius(self) -> float:
        """Getter — accessed as temperature.celsius (no call parentheses)."""
        return self._celsius

    @celsius.setter
    def celsius(self, value: float):
        """Setter — enforces validation on assignment."""
        if value < -273.15:
            raise ValueError(f"Temperature {value}°C is below absolute zero")
        self._celsius = value

    @celsius.deleter
    def celsius(self):
        """Deleter — runs on `del temperature.celsius`."""
        del self._celsius

    @property
    def fahrenheit(self) -> float:
        """Computed property — no setter, read-only."""
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value: float):
        self.celsius = (value - 32) * 5/9   # delegates to celsius setter

    def __repr__(self):
        return f"Temperature({self._celsius}°C / {self.fahrenheit}°F)"

t = Temperature(100)
print(t)
print(t.celsius)
print(t.fahrenheit)

t.celsius = 0         # setter
print(t)

t.fahrenheit = 32     # fahrenheit setter → celsius setter
print(t)

try:
    t.celsius = -300  # triggers ValueError
except ValueError as e:
    print(f"Caught: {e}")


# ── 6. Key Dunder (Magic) Methods ─────────────────────────────────────────────

print("\n--- Dunder methods ---")

class Vector:
    """2-D vector demonstrating operator overloading."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __add__(self, other):        # v1 + v2
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):        # v1 - v2
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):       # v * 3
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):      # 3 * v  (reflected — when left operand fails)
        return self.__mul__(scalar)

    def __neg__(self):               # -v
        return Vector(-self.x, -self.y)

    def __abs__(self):               # abs(v) — magnitude
        return (self.x**2 + self.y**2) ** 0.5

    def __eq__(self, other):         # v1 == v2
        return self.x == other.x and self.y == other.y

    def __hash__(self):              # must define if __eq__ is defined
        return hash((self.x, self.y))

    def __len__(self):               # len(v)
        return 2

    def __bool__(self):              # truth value: bool(v)
        return self.x != 0 or self.y != 0

    def __iter__(self):              # for component in v
        yield self.x
        yield self.y

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)      # Vector(4, 6)
print(v1 - v2)      # Vector(-2, -2)
print(v1 * 3)       # Vector(3, 6)
print(3 * v1)       # Vector(3, 6)
print(-v1)          # Vector(-1, -2)
print(abs(v2))      # 5.0
print(v1 == v2)     # False
print(len(v1))      # 2
print(list(v1))     # [1, 2]
print(bool(Vector(0, 0)))   # False
print(bool(v1))             # True


# ── 7. __slots__ ──────────────────────────────────────────────────────────────

print("\n--- __slots__ ---")

class Point:
    """
    __slots__ prevents the per-instance __dict__, saving memory.
    Only the listed attributes are allowed; dynamically adding new ones raises AttributeError.
    """
    __slots__ = ("x", "y")

    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
print(p.x, p.y)
# p.z = 5   # AttributeError — not in __slots__

import sys
class PointDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

print(f"with __slots__: {sys.getsizeof(p)} bytes")
print(f"with __dict__:  {sys.getsizeof(PointDict(3,4))} bytes")


print("\nDone: oop_basics")
