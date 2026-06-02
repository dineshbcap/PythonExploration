"""
INHERITANCE
===========
Single and multiple inheritance, method resolution order (MRO),
super(), mixins, and abstract base classes (preview).

Run: python 02_intermediate/02_inheritance.py
"""

from abc import ABC, abstractmethod

# ── 1. Single Inheritance ─────────────────────────────────────────────────────

print("--- Single Inheritance ---")

class Animal:
    """Base class for all animals."""

    def __init__(self, name: str, sound: str):
        self.name  = name
        self.sound = sound

    def speak(self) -> str:
        return f"{self.name} says {self.sound}!"

    def describe(self) -> str:
        return f"I am {self.name}"

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name!r})"


class Dog(Animal):
    """Dog inherits from Animal and adds breed-specific behavior."""

    def __init__(self, name: str, breed: str):
        # super() calls the parent class's __init__
        super().__init__(name, sound="Woof")
        self.breed = breed

    def fetch(self, item: str) -> str:
        return f"{self.name} fetches the {item}!"

    # Override parent method:
    def describe(self) -> str:
        base = super().describe()   # call parent version first
        return f"{base}, a {self.breed}"


class Cat(Animal):
    def __init__(self, name: str, indoor: bool = True):
        super().__init__(name, sound="Meow")
        self.indoor = indoor

    def purr(self) -> str:
        return f"{self.name} purrs..."


dog = Dog("Rex", "German Shepherd")
cat = Cat("Whiskers")

print(dog.speak())        # inherited
print(dog.fetch("ball"))  # new method
print(dog.describe())     # overridden

print(cat.speak())
print(cat.purr())

# Check inheritance:
print(isinstance(dog, Dog))     # True
print(isinstance(dog, Animal))  # True — is-a relationship
print(issubclass(Dog, Animal))  # True
print(dog.__class__.__mro__)    # Method Resolution Order


# ── 2. Method Resolution Order (MRO) ─────────────────────────────────────────

print("\n--- MRO ---")

class A:
    def method(self): return "A"

class B(A):
    def method(self): return "B"

class C(A):
    def method(self): return "C"

class D(B, C):    # multiple inheritance
    pass

d = D()
print(d.method())         # "B" — Python uses C3 linearization
print(D.__mro__)          # (D, B, C, A, object)
print([cls.__name__ for cls in D.__mro__])


# ── 3. Multiple Inheritance ───────────────────────────────────────────────────

print("\n--- Multiple Inheritance ---")

class Flyable:
    def fly(self) -> str:
        return f"{self.__class__.__name__} is flying"

class Swimmable:
    def swim(self) -> str:
        return f"{self.__class__.__name__} is swimming"

class Duck(Animal, Flyable, Swimmable):
    def __init__(self, name: str):
        super().__init__(name, sound="Quack")

    def describe(self) -> str:
        return f"{self.name} can fly AND swim"

donald = Duck("Donald")
print(donald.speak())
print(donald.fly())
print(donald.swim())
print(donald.describe())
print([c.__name__ for c in Duck.__mro__])


# ── 4. super() in Multiple Inheritance (Cooperative) ──────────────────────────

print("\n--- Cooperative super() ---")
# With multiple inheritance, super() follows the MRO, not just the direct parent.

class Base:
    def greet(self):
        print("Base.greet")

class Left(Base):
    def greet(self):
        print("Left.greet — before super")
        super().greet()
        print("Left.greet — after super")

class Right(Base):
    def greet(self):
        print("Right.greet — before super")
        super().greet()
        print("Right.greet — after super")

class Child(Left, Right):
    def greet(self):
        print("Child.greet — before super")
        super().greet()
        print("Child.greet — after super")

# MRO: Child → Left → Right → Base → object
c = Child()
c.greet()
# Output shows each class called once in MRO order (no Base duplication)


# ── 5. Mixins ─────────────────────────────────────────────────────────────────

print("\n--- Mixins ---")
# Mixins are small, focused classes that add reusable behavior.
# They are not meant to be instantiated directly.

class JSONMixin:
    """Adds JSON serialization to any class."""
    import json as _json

    def to_json(self) -> str:
        import json
        # __dict__ contains instance attributes
        return json.dumps(self.__dict__, default=str, indent=2)

    @classmethod
    def from_json(cls, json_str: str):
        import json
        data = json.loads(json_str)
        obj = cls.__new__(cls)
        obj.__dict__.update(data)
        return obj


class ReprMixin:
    """Auto-generate __repr__ from instance attributes."""
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{self.__class__.__name__}({attrs})"


class User(JSONMixin, ReprMixin):
    def __init__(self, username: str, email: str, age: int):
        self.username = username
        self.email    = email
        self.age      = age

u = User("alice", "alice@example.com", 30)
print(repr(u))
print(u.to_json())


# ── 6. Abstract Base Classes (Preview) ───────────────────────────────────────

print("\n--- Abstract Base Classes ---")
# Prevent instantiation of base class; enforce subclasses to implement methods.

class Shape(ABC):
    """Abstract base class — cannot be instantiated directly."""

    @abstractmethod
    def area(self) -> float:
        """Subclasses must implement this."""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self) -> str:
        return f"{self.__class__.__name__}: area={self.area():.2f}, perimeter={self.perimeter():.2f}"


class Rectangle(Shape):
    def __init__(self, width: float, height: float):
        self.width  = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height

    def perimeter(self) -> float:
        return 2 * (self.width + self.height)


class Circle(Shape):
    PI = 3.14159

    def __init__(self, radius: float):
        self.radius = radius

    def area(self) -> float:
        return self.PI * self.radius ** 2

    def perimeter(self) -> float:
        return 2 * self.PI * self.radius

# Shape()  ← would raise TypeError: Can't instantiate abstract class

r = Rectangle(4, 6)
c = Circle(5)
print(r.describe())
print(c.describe())

shapes: list[Shape] = [r, c]
for shape in shapes:
    print(f"  {shape.area():.2f}")


# ── 7. __init_subclass__ ──────────────────────────────────────────────────────

print("\n--- __init_subclass__ ---")
# Called whenever a class is subclassed; lets the base class react.

class Plugin:
    _registry: dict = {}

    def __init_subclass__(cls, plugin_name: str = None, **kwargs):
        super().__init_subclass__(**kwargs)
        if plugin_name:
            Plugin._registry[plugin_name] = cls
            print(f"Registered plugin: {plugin_name!r} → {cls.__name__}")

class CSVPlugin(Plugin, plugin_name="csv"):
    def process(self): return "CSV processing"

class JSONPlugin(Plugin, plugin_name="json"):
    def process(self): return "JSON processing"

print(Plugin._registry)
print(Plugin._registry["csv"]().process())


print("\nDone: inheritance")
