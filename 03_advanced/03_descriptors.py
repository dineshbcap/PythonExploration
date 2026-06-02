"""
DESCRIPTORS
===========
The descriptor protocol (__get__, __set__, __delete__), data vs non-data
descriptors, how property is implemented, and practical use cases
(validation, lazy attributes, type-coercion).

Run: python 03_advanced/03_descriptors.py
"""

# ── 1. The Descriptor Protocol ────────────────────────────────────────────────

print("--- Descriptor Protocol ---")
# A descriptor is an object that defines how attribute ACCESS works.
# Python uses descriptors for: property, classmethod, staticmethod, functions.
#
# Protocol:
#   __get__(self, obj, objtype=None)   → called on attribute READ
#   __set__(self, obj, value)          → called on attribute WRITE
#   __delete__(self, obj)              → called on attribute DELETE
#
# Data descriptor:     defines __set__ (or __delete__) — overrides instance __dict__
# Non-data descriptor: only __get__ — instance __dict__ takes precedence

class SimpleDescriptor:
    """A minimal data descriptor that logs all access."""

    def __set_name__(self, owner, name):
        # Called automatically when the descriptor is assigned in a class body.
        # `owner` is the owning class, `name` is the attribute name.
        self.name = name
        self.storage_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            # Accessed via the CLASS (e.g. MyClass.attr) — return descriptor itself
            return self
        value = obj.__dict__.get(self.storage_name, None)
        print(f"  GET  {self.name} → {value!r}")
        return value

    def __set__(self, obj, value):
        print(f"  SET  {self.name} ← {value!r}")
        obj.__dict__[self.storage_name] = value

    def __delete__(self, obj):
        print(f"  DEL  {self.name}")
        obj.__dict__.pop(self.storage_name, None)


class Person:
    name  = SimpleDescriptor()
    email = SimpleDescriptor()

    def __init__(self, name, email):
        self.name  = name    # triggers __set__
        self.email = email


p = Person("Alice", "alice@example.com")
print(p.name)                       # triggers __get__
p.email = "new@example.com"         # triggers __set__
del p.name                          # triggers __delete__
print(Person.name)                  # obj is None → returns descriptor itself


# ── 2. Validated Descriptor ───────────────────────────────────────────────────

print("\n--- Validated Descriptor ---")

class Validated:
    """Base class for type-checking descriptors."""

    def __set_name__(self, owner, name):
        self.name         = name
        self.storage_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return obj.__dict__.get(self.storage_name)

    def __set__(self, obj, value):
        value = self.validate(value)
        obj.__dict__[self.storage_name] = value

    def validate(self, value):
        raise NotImplementedError


class TypedField(Validated):
    """Enforces a specific type."""
    def __init__(self, expected_type):
        self.expected_type = expected_type

    def validate(self, value):
        if not isinstance(value, self.expected_type):
            raise TypeError(
                f"'{self.name}' expects {self.expected_type.__name__}, "
                f"got {type(value).__name__}"
            )
        return value


class RangedInt(Validated):
    """Enforces an integer within [min_val, max_val]."""
    def __init__(self, min_val, max_val):
        self.min_val = min_val
        self.max_val = max_val

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"'{self.name}' must be int")
        if not (self.min_val <= value <= self.max_val):
            raise ValueError(
                f"'{self.name}' must be {self.min_val}–{self.max_val}, got {value}"
            )
        return value


class Employee:
    name       = TypedField(str)
    department = TypedField(str)
    age        = RangedInt(18, 65)
    salary     = RangedInt(0, 10_000_000)

    def __init__(self, name, department, age, salary):
        self.name       = name
        self.department = department
        self.age        = age
        self.salary     = salary

    def __repr__(self):
        return f"Employee({self.name!r}, {self.age}, ${self.salary})"

emp = Employee("Alice", "Engineering", 30, 95000)
print(emp)

for bad_call in [
    lambda: Employee(42, "Eng", 30, 0),          # name not str
    lambda: Employee("Bob", "Eng", 16, 0),       # age too low
    lambda: Employee("Carol", "Eng", 30, -100),  # salary negative
]:
    try:
        bad_call()
    except (TypeError, ValueError) as e:
        print(f"  Caught: {e}")


# ── 3. Non-Data Descriptor — Lazy Property ────────────────────────────────────

print("\n--- Lazy (non-data) descriptor ---")
# Non-data descriptors (only __get__) are overridden by instance __dict__.
# This is the basis for "lazy" computed attributes: compute once, cache in instance.

class lazy_property:
    """
    Descriptor for lazy attributes: computed on first access,
    then cached in the instance __dict__ (overriding the descriptor).
    """

    def __init__(self, func):
        self.func = func
        self.name = func.__name__

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        # Compute the value and cache it directly in the instance's __dict__.
        # Because this is a NON-data descriptor (no __set__), the instance
        # __dict__ entry will shadow the class-level descriptor on future access.
        value = self.func(obj)
        obj.__dict__[self.name] = value   # cache — future lookups skip this descriptor
        return value


class Circle:
    def __init__(self, radius):
        self.radius = radius

    @lazy_property
    def area(self):
        """Expensive computation — only done once."""
        print("  Computing area...")
        import math
        return math.pi * self.radius ** 2

    @lazy_property
    def circumference(self):
        print("  Computing circumference...")
        import math
        return 2 * math.pi * self.radius

c = Circle(5)
print(c.area)            # "Computing area..." then result
print(c.area)            # result immediately — no recomputation
print(c.circumference)   # "Computing circumference..."
print(c.__dict__)        # {'radius': 5, 'area': ..., 'circumference': ...}


# ── 4. How `property` Is Implemented ─────────────────────────────────────────

print("\n--- Manual property implementation ---")
# `property` is a built-in data descriptor. Here's a simplified version.

class myproperty:
    """Simplified re-implementation of the built-in `property`."""

    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc or (fget.__doc__ if fget else None)

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(f"'{self.name}' is not readable")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError(f"'{self.name}' is read-only")
        self.fset(obj, value)

    def __delete__(self, obj):
        if self.fdel is None:
            raise AttributeError(f"'{self.name}' cannot be deleted")
        self.fdel(obj)

    def getter(self, fget):
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        return type(self)(self.fget, self.fset, fdel, self.__doc__)


class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @myproperty
    def celsius(self):
        """Temperature in Celsius."""
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value

    @myproperty
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

t = Temperature(100)
print(t.celsius)
print(t.fahrenheit)
t.celsius = 0
print(t.celsius)


# ── 5. __set_name__ Deep Dive ─────────────────────────────────────────────────

print("\n--- __set_name__ ---")
# Python 3.6+ calls descriptor.__set_name__(owner_class, attr_name)
# immediately after the class body is executed.

class AutoName:
    """Descriptor that knows its own attribute name automatically."""

    def __set_name__(self, owner, name):
        print(f"  Bound '{name}' to {owner.__name__}")
        self.name = name
        self.private = f"_{name}"

    def __get__(self, obj, cls=None):
        return None if obj is None else obj.__dict__.get(self.private)

    def __set__(self, obj, value):
        obj.__dict__[self.private] = value


class Model:
    # __set_name__ is called for each of these during class creation:
    field_a = AutoName()
    field_b = AutoName()
    field_c = AutoName()

m = Model()
m.field_a = 10
m.field_b = 20
print(m.field_a, m.field_b, m.field_c)


print("\nDone: descriptors")
