"""
METACLASSES
===========
type(), custom metaclasses, __new__ vs __init__, class creation hooks,
__prepare__, __init_subclass__, and practical use cases.

Run: python 03_advanced/04_metaclasses.py
"""

# ── 1. Everything is an Object — Including Classes ────────────────────────────

print("--- Classes are objects ---")

class MyClass:
    x = 42

# A class is an instance of its metaclass.
print(type(42))        # <class 'int'>
print(type("hello"))   # <class 'str'>
print(type(MyClass))   # <class 'type'> — MyClass is an instance of type
print(type(type))      # <class 'type'> — type is its own metaclass

# Every class you define has `type` as its metaclass (unless overridden).
print(MyClass.__class__)    # <class 'type'>
print(MyClass.__bases__)    # (<class 'object'>,)


# ── 2. type() as a Class Factory ──────────────────────────────────────────────

print("\n--- type() as class factory ---")
# type(name, bases, namespace) creates a new class dynamically.
# This is what `class` statements do under the hood.

# Equivalent to:
#   class Dog(Animal):
#       species = "canine"
#       def bark(self): return "Woof"

Animal  = type("Animal", (), {"can_breathe": True})
Dog     = type("Dog", (Animal,), {
    "species": "canine",
    "bark": lambda self: f"{self.__class__.__name__} says Woof",
})

d = Dog()
print(d.bark())
print(d.can_breathe)   # inherited


# ── 3. Custom Metaclass ───────────────────────────────────────────────────────

print("\n--- Custom metaclass ---")
# A metaclass controls how classes are CREATED (not how instances are created).
# Use metaclass= keyword in class definition.

class LoggingMeta(type):
    """Metaclass that logs every class it creates."""

    def __new__(mcs, name, bases, namespace):
        # mcs  = the metaclass (LoggingMeta)
        # name = name of the class being created ("MyModel", etc.)
        # bases = tuple of base classes
        # namespace = dict of class attributes and methods
        print(f"  Creating class: {name!r}, bases={[b.__name__ for b in bases]}")
        cls = super().__new__(mcs, name, bases, namespace)
        return cls

    def __init__(cls, name, bases, namespace):
        # Called after __new__ — cls is already created
        super().__init__(name, bases, namespace)
        print(f"  Initialized class: {name!r}")


class Base(metaclass=LoggingMeta):
    pass

class Derived(Base):   # inherits metaclass LoggingMeta
    x = 42


# ── 4. __new__ vs __init__ in Metaclasses ─────────────────────────────────────

print("\n--- __new__ vs __init__ ---")
# __new__(mcs, name, bases, namespace) — CREATES the class object
# __init__(cls, name, bases, namespace) — INITIALIZES it after creation

# Use __new__ when you need to modify the namespace before the class is built,
# or return a different class entirely.

class SingletonMeta(type):
    """Metaclass that makes a class a singleton."""
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        # __call__ is invoked when you instantiate the class (e.g. MyClass())
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class Config(metaclass=SingletonMeta):
    def __init__(self):
        self.data = {}

c1 = Config()
c2 = Config()
print(c1 is c2)   # True — same instance every time


# ── 5. __prepare__ — Customize the Class Namespace ────────────────────────────

print("\n--- __prepare__ ---")
# Called before the class body executes; returns the mapping to use as namespace.
# Used to give the namespace special behavior (ordered, insert default values, etc.)

class OrderedMeta(type):
    """Records the ORDER in which class attributes were defined."""

    @classmethod
    def __prepare__(mcs, name, bases, **kwargs):
        # Return a plain dict — in Python 3.7+ dicts maintain order anyway,
        # but this is where you'd return a custom mapping.
        print(f"  __prepare__ called for {name!r}")
        return {}   # could return collections.OrderedDict() for older Python

    def __new__(mcs, name, bases, namespace, **kwargs):
        cls = super().__new__(mcs, name, bases, namespace)
        # Record definition order (excluding dunder names)
        cls._field_order = [k for k in namespace if not k.startswith("_")]
        return cls

class Form(metaclass=OrderedMeta):
    first_name = "str"
    last_name  = "str"
    email      = "str"
    age        = "int"

print(f"Field order: {Form._field_order}")


# ── 6. Metaclass for Interface Enforcement ────────────────────────────────────

print("\n--- Interface enforcement ---")

class InterfaceMeta(type):
    """Ensures all subclasses implement required methods."""

    REQUIRED = set()

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        # Collect required methods from the class hierarchy
        required = set()
        for base in bases:
            required |= getattr(base, "_required_methods", set())
        # Check that each required method is implemented (not just inherited as abstract)
        missing = required - set(namespace.keys())
        if missing and bases:   # skip the base class itself
            raise TypeError(
                f"Class {name!r} must implement: {', '.join(sorted(missing))}"
            )
        return cls


class IPlugin(metaclass=InterfaceMeta):
    _required_methods = {"initialize", "execute", "teardown"}

    def initialize(self): raise NotImplementedError
    def execute(self):    raise NotImplementedError
    def teardown(self):   raise NotImplementedError

try:
    class BadPlugin(IPlugin):
        def initialize(self): pass
        # Missing execute and teardown!
except TypeError as e:
    print(f"  Caught: {e}")

class GoodPlugin(IPlugin):
    def initialize(self): print("  init")
    def execute(self):    print("  run")
    def teardown(self):   print("  stop")

GoodPlugin().execute()


# ── 7. Metaclass for Auto-Registration ────────────────────────────────────────

print("\n--- Auto-registration ---")

class PluginRegistry(type):
    """Automatically registers every subclass in a global registry."""
    _registry: dict = {}

    def __new__(mcs, name, bases, namespace):
        cls = super().__new__(mcs, name, bases, namespace)
        # Don't register the base class itself
        if bases:
            plugin_name = namespace.get("name", name.lower())
            mcs._registry[plugin_name] = cls
            print(f"  Registered: {plugin_name!r}")
        return cls


class BaseHandler(metaclass=PluginRegistry):
    """Base for all handlers."""
    name = "base"   # not registered (no bases before it)

class JSONHandler(BaseHandler):
    name = "json"
    def handle(self, data): return f"JSON: {data}"

class CSVHandler(BaseHandler):
    name = "csv"
    def handle(self, data): return f"CSV: {data}"

print(PluginRegistry._registry)
handler = PluginRegistry._registry["json"]()
print(handler.handle({"key": "value"}))


# ── 8. __init_subclass__ — Lighter Alternative ────────────────────────────────

print("\n--- __init_subclass__ (lighter) ---")
# In many cases __init_subclass__ (Python 3.6+) achieves the same as a metaclass
# without the metaclass complexity.

class Base:
    _subclasses: list = []

    def __init_subclass__(cls, category=None, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.category = category or cls.__name__.lower()
        Base._subclasses.append(cls)
        print(f"  Registered subclass: {cls.__name__!r} (category={cls.category!r})")

class Alpha(Base, category="algorithms"):
    pass

class Beta(Base):
    pass

print([c.__name__ for c in Base._subclasses])


print("\nDone: metaclasses")
