"""
DATACLASSES AND TYPING
======================
@dataclass, field(), post_init, frozen, slots, inheritance,
and the typing module (generics, TypeVar, Protocol, Literal, TypedDict, etc.)

Run: python 03_advanced/05_dataclasses_and_typing.py
"""

from dataclasses import dataclass, field, asdict, astuple, replace, KW_ONLY  # noqa: F401
from typing import (
    Any, ClassVar, Final, Generic, Literal, Optional, Protocol,
    Sequence, TypeVar, Union, get_type_hints, overload, runtime_checkable
)

# ── 1. Basic @dataclass ───────────────────────────────────────────────────────

print("--- Basic @dataclass ---")
# @dataclass auto-generates __init__, __repr__, __eq__ from annotated fields.

@dataclass
class Point:
    x: float
    y: float

p1 = Point(3.0, 4.0)
p2 = Point(3.0, 4.0)
p3 = Point(1.0, 2.0)

print(p1)            # Point(x=3.0, y=4.0) — auto __repr__
print(p1 == p2)      # True  — auto __eq__ (compares by field values)
print(p1 == p3)      # False
print(p1 is p2)      # False — different instances


# ── 2. Default Values and field() ────────────────────────────────────────────

print("\n--- field() ---")

@dataclass
class Config:
    host:    str  = "localhost"
    port:    int  = 5432
    timeout: int  = 30
    tags:    list = field(default_factory=list)   # mutable default needs factory
    meta:    dict = field(default_factory=dict)
    # WRONG: tags: list = []  → TypeError — mutable default not allowed directly

    # Fields with default_factory CAN'T precede fields without defaults.

c1 = Config()
c2 = Config()
c1.tags.append("web")
print(c1.tags)   # ["web"]
print(c2.tags)   # [] — independent list, not shared


# ── 3. Post-Init Processing ───────────────────────────────────────────────────

print("\n--- __post_init__ ---")

@dataclass
class Rectangle:
    width:  float
    height: float
    area:   float = field(init=False)   # not a constructor parameter

    def __post_init__(self):
        if self.width <= 0 or self.height <= 0:
            raise ValueError("Dimensions must be positive")
        self.area = self.width * self.height

r = Rectangle(4.0, 6.0)
print(r)            # includes area = 24.0

try:
    Rectangle(-1, 5)
except ValueError as e:
    print(f"Caught: {e}")


# ── 4. frozen=True — Immutable Dataclass ──────────────────────────────────────

print("\n--- frozen=True ---")

@dataclass(frozen=True)   # makes instances hashable and immutable
class ImmutablePoint:
    x: float
    y: float

ip = ImmutablePoint(3, 4)
print(ip)

try:
    ip.x = 10    # raises FrozenInstanceError
except Exception as e:
    print(f"Caught: {type(e).__name__}")

# Frozen dataclasses are hashable — can be used as dict keys or in sets:
cache = {ImmutablePoint(0, 0): "origin", ImmutablePoint(1, 0): "unit-x"}
print(cache[ImmutablePoint(0, 0)])


# ── 5. order=True — Comparison Methods ───────────────────────────────────────

print("\n--- order=True ---")

@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"

v1 = Version(1, 2, 0)
v2 = Version(2, 0, 0)
v3 = Version(1, 2, 1)

print(v1 < v2)   # True
print(sorted([v2, v3, v1]))   # [v1, v3, v2]


# ── 6. Inheritance ────────────────────────────────────────────────────────────

print("\n--- Dataclass Inheritance ---")

@dataclass
class Shape:
    color: str = "red"

    def describe(self):
        return f"{self.__class__.__name__} ({self.color})"

@dataclass
class Circle(Shape):
    radius: float = 1.0

    def area(self):
        import math
        return math.pi * self.radius ** 2

@dataclass
class ColoredCircle(Circle):
    border: str = "black"

cc = ColoredCircle(color="blue", radius=5.0, border="white")
print(cc)
print(cc.describe())
print(f"Area: {cc.area():.2f}")


# ── 7. Utility Functions ──────────────────────────────────────────────────────

print("\n--- asdict / astuple / replace ---")

@dataclass
class Employee:
    name:   str
    age:    int
    salary: float

e = Employee("Alice", 30, 95000.0)

print(asdict(e))      # {'name': 'Alice', 'age': 30, 'salary': 95000.0}
print(astuple(e))     # ('Alice', 30, 95000.0)

# replace() creates a NEW instance with some fields changed (immutable update):
e2 = replace(e, salary=100000.0)
print(e2)    # name/age unchanged, salary updated
print(e)     # original unchanged


# ── 8. slots=True (Python 3.10+) ──────────────────────────────────────────────

print("\n--- slots=True ---")

@dataclass(slots=True)
class FastPoint:
    x: float
    y: float

fp = FastPoint(1.0, 2.0)
print(fp)


# ── 9. ClassVar and InitVar ───────────────────────────────────────────────────

print("\n--- ClassVar / InitVar ---")
from dataclasses import InitVar

@dataclass
class BankAccount:
    owner:         str
    balance:       float = 0.0
    interest_rate: ClassVar[float] = 0.05   # class-level; not an instance field

    # InitVar: passed to __init__ but NOT stored as an instance attribute
    initial_deposit: InitVar[float] = 0.0

    def __post_init__(self, initial_deposit: float):
        self.balance += initial_deposit

acct = BankAccount("Alice", initial_deposit=1000.0)
print(acct)              # no initial_deposit field
print(acct.balance)      # 1000.0
print(BankAccount.interest_rate)   # 0.05


# ── 10. Typing Module ─────────────────────────────────────────────────────────

print("\n--- typing module ---")

# Optional[X] == Union[X, None]
def find_user(user_id: int) -> Optional[str]:
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)

print(find_user(1))    # Alice
print(find_user(99))   # None

# Union[X, Y] — one of several types (Python 3.10+ allows X | Y)
def normalize(value: Union[int, float, str]) -> float:
    return float(value)

# Literal — restrict to specific values
def set_direction(dir: Literal["north", "south", "east", "west"]) -> str:
    return f"Going {dir}"

print(set_direction("north"))

# Final — mark as a constant (not enforced at runtime, only by type checkers)
MAX_RETRIES: Final = 3


# ── 11. TypeVar and Generic ───────────────────────────────────────────────────

print("\n--- TypeVar / Generic ---")
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")

class Stack(Generic[T]):
    """Generic stack — type-safe via type hints."""

    def __init__(self):
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> T:
        return self._items[-1]

    def is_empty(self) -> bool:
        return not self._items

    def __len__(self) -> int:
        return len(self._items)

int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
print(int_stack.pop())   # 2


# ── 12. Protocol — Structural Subtyping ───────────────────────────────────────

print("\n--- Protocol ---")
# Protocol defines an interface by structure (duck typing), not inheritance.

@runtime_checkable
class Drawable(Protocol):
    def draw(self) -> str: ...
    def bounding_box(self) -> tuple[float, float, float, float]: ...

class Circle:
    def __init__(self, x, y, r): self.x = x; self.y = y; self.r = r
    def draw(self): return f"Circle at ({self.x},{self.y}) r={self.r}"
    def bounding_box(self): return (self.x-self.r, self.y-self.r,
                                     self.x+self.r, self.y+self.r)

class Text:
    def __init__(self, x, y, content): self.x=x; self.y=y; self.content=content
    def draw(self): return f"Text '{self.content}' at ({self.x},{self.y})"
    def bounding_box(self): return (self.x, self.y, self.x+100, self.y+20)

# Neither Circle nor Text inherits from Drawable, but they satisfy the protocol:
shapes: list[Drawable] = [Circle(0, 0, 5), Text(10, 20, "Hello")]
for s in shapes:
    print(f"  {s.draw()}")

# runtime_checkable allows isinstance() checks:
print(isinstance(Circle(0,0,1), Drawable))   # True


# ── 13. TypedDict ─────────────────────────────────────────────────────────────

print("\n--- TypedDict ---")
from typing import TypedDict

class Movie(TypedDict):
    title:    str
    year:     int
    rating:   float

m: Movie = {"title": "Inception", "year": 2010, "rating": 8.8}
print(m["title"])

# TypedDict with optional keys via NotRequired (Python 3.11+):
from typing import NotRequired

class Settings(TypedDict):
    host: str
    port: int
    debug: NotRequired[bool]   # optional key

settings: Settings = {"host": "localhost", "port": 8080}
print(f"  Settings: {settings}")


print("\nDone: dataclasses_and_typing")
