"""
DESIGN PATTERNS
===============
Classic GoF patterns implemented idiomatically in Python:
Creational (Singleton, Factory, Builder), Structural (Adapter, Decorator,
Proxy, Composite), Behavioural (Observer, Strategy, Command, Iterator,
Template Method, Chain of Responsibility).

Run: python 03_advanced/10_design_patterns.py
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from functools import wraps
from typing import Callable

# ══════════════════════════════════════════════════════════════════════════════
#  CREATIONAL PATTERNS
# ══════════════════════════════════════════════════════════════════════════════

print("=" * 60)
print("CREATIONAL PATTERNS")
print("=" * 60)

# ── 1. Singleton ─────────────────────────────────────────────────────────────

print("\n--- Singleton ---")
# Guarantees a class has exactly one instance.

class SingletonMeta(type):
    _instances: dict = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class AppConfig(metaclass=SingletonMeta):
    def __init__(self):
        self.debug   = False
        self.db_url  = "postgresql://localhost/mydb"

c1 = AppConfig()
c2 = AppConfig()
c1.debug = True
print(f"Same instance: {c1 is c2}")   # True
print(f"c2.debug = {c2.debug}")       # True — same object


# ── 2. Factory Method ─────────────────────────────────────────────────────────

print("\n--- Factory Method ---")
# Defines an interface for creating an object, but lets subclasses decide the type.

class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None: ...

class EmailNotification(Notification):
    def __init__(self, address): self.address = address
    def send(self, message):
        print(f"  [Email → {self.address}] {message}")

class SMSNotification(Notification):
    def __init__(self, number): self.number = number
    def send(self, message):
        print(f"  [SMS → {self.number}] {message}")

class PushNotification(Notification):
    def __init__(self, token): self.token = token
    def send(self, message):
        print(f"  [Push → {self.token[:8]}...] {message}")

def notification_factory(channel: str, target: str) -> Notification:
    creators = {
        "email": EmailNotification,
        "sms":   SMSNotification,
        "push":  PushNotification,
    }
    if channel not in creators:
        raise ValueError(f"Unknown channel: {channel!r}")
    return creators[channel](target)

for channel, target in [("email", "user@example.com"), ("sms", "+1555-1234")]:
    n = notification_factory(channel, target)
    n.send("Your order has shipped!")


# ── 3. Builder ────────────────────────────────────────────────────────────────

print("\n--- Builder ---")
# Separates construction of a complex object from its representation.
# Allows step-by-step construction and fluent chaining.

@dataclass
class QueryConfig:
    table:      str = ""
    conditions: list = field(default_factory=list)
    columns:    list = field(default_factory=list)
    order_by:   str  = ""
    limit:      int  = 0

class QueryBuilder:
    def __init__(self):
        self._config = QueryConfig()

    def from_table(self, table: str) -> "QueryBuilder":
        self._config.table = table
        return self   # return self for fluent chaining

    def select(self, *columns) -> "QueryBuilder":
        self._config.columns.extend(columns)
        return self

    def where(self, condition: str) -> "QueryBuilder":
        self._config.conditions.append(condition)
        return self

    def order_by(self, column: str) -> "QueryBuilder":
        self._config.order_by = column
        return self

    def limit(self, n: int) -> "QueryBuilder":
        self._config.limit = n
        return self

    def build(self) -> str:
        cols  = ", ".join(self._config.columns) or "*"
        sql   = f"SELECT {cols} FROM {self._config.table}"
        if self._config.conditions:
            sql += " WHERE " + " AND ".join(self._config.conditions)
        if self._config.order_by:
            sql += f" ORDER BY {self._config.order_by}"
        if self._config.limit:
            sql += f" LIMIT {self._config.limit}"
        return sql

query = (QueryBuilder()
         .from_table("users")
         .select("name", "email")
         .where("active = true")
         .where("age >= 18")
         .order_by("name")
         .limit(10)
         .build())

print(f"  SQL: {query}")


# ══════════════════════════════════════════════════════════════════════════════
#  STRUCTURAL PATTERNS
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("STRUCTURAL PATTERNS")
print("=" * 60)

# ── 4. Adapter ────────────────────────────────────────────────────────────────

print("\n--- Adapter ---")
# Allows incompatible interfaces to work together.

class LegacyPrinter:
    """Old API we cannot modify."""
    def print_document(self, text: str):
        print(f"  [Legacy] printing: {text}")

class ModernPrinter(ABC):
    """New interface the rest of the app expects."""
    @abstractmethod
    def render(self, content: str) -> None: ...

class LegacyPrinterAdapter(ModernPrinter):
    """Wraps LegacyPrinter so it satisfies ModernPrinter."""
    def __init__(self, legacy: LegacyPrinter):
        self._legacy = legacy

    def render(self, content: str) -> None:
        self._legacy.print_document(content)   # translate the call

def print_report(printer: ModernPrinter, report: str):
    printer.render(report)

adapter = LegacyPrinterAdapter(LegacyPrinter())
print_report(adapter, "Q4 Financials")


# ── 5. Decorator Pattern ──────────────────────────────────────────────────────

print("\n--- Decorator Pattern (structural) ---")
# Adds responsibilities to an object dynamically without subclassing.
# Different from Python's @decorator syntax (though same concept).

class Coffee(ABC):
    @abstractmethod
    def cost(self) -> float: ...
    @abstractmethod
    def description(self) -> str: ...

class SimpleCoffee(Coffee):
    def cost(self): return 1.00
    def description(self): return "Coffee"

class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    def cost(self):        return self._coffee.cost()
    def description(self): return self._coffee.description()

class Milk(CoffeeDecorator):
    def cost(self):        return self._coffee.cost() + 0.25
    def description(self): return self._coffee.description() + ", Milk"

class Sugar(CoffeeDecorator):
    def cost(self):        return self._coffee.cost() + 0.10
    def description(self): return self._coffee.description() + ", Sugar"

class Vanilla(CoffeeDecorator):
    def cost(self):        return self._coffee.cost() + 0.50
    def description(self): return self._coffee.description() + ", Vanilla"

my_coffee = Vanilla(Sugar(Milk(SimpleCoffee())))
print(f"  {my_coffee.description()} → ${my_coffee.cost():.2f}")


# ── 6. Proxy ──────────────────────────────────────────────────────────────────

print("\n--- Proxy ---")
# A surrogate that controls access to another object.

class DataService:
    def fetch(self, key: str) -> str:
        return f"data-for-{key}"

class CachingProxy:
    """Adds caching in front of DataService without modifying it."""
    def __init__(self, service: DataService):
        self._service = service
        self._cache: dict = {}

    def fetch(self, key: str) -> str:
        if key not in self._cache:
            print(f"  [Proxy] cache miss for {key!r}")
            self._cache[key] = self._service.fetch(key)
        else:
            print(f"  [Proxy] cache hit for {key!r}")
        return self._cache[key]

proxy = CachingProxy(DataService())
print(proxy.fetch("user:1"))
print(proxy.fetch("user:1"))   # served from cache
print(proxy.fetch("user:2"))


# ── 7. Composite ──────────────────────────────────────────────────────────────

print("\n--- Composite ---")
# Treat individual objects and compositions uniformly.

class FileSystemItem(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def size(self) -> int: ...

    def display(self, indent: int = 0) -> None:
        print(" " * indent + str(self))

class File(FileSystemItem):
    def __init__(self, name, size):
        super().__init__(name)
        self._size = size

    def size(self):
        return self._size

    def __str__(self):
        return f"📄 {self.name} ({self._size}B)"

class Directory(FileSystemItem):
    def __init__(self, name):
        super().__init__(name)
        self._children: list[FileSystemItem] = []

    def add(self, item: FileSystemItem):
        self._children.append(item)
        return self

    def size(self):
        return sum(c.size() for c in self._children)

    def display(self, indent: int = 0):
        print(" " * indent + f"📁 {self.name}/ ({self.size()}B)")
        for child in self._children:
            child.display(indent + 2)

root = Directory("project")
src  = Directory("src").add(File("main.py", 4096)).add(File("utils.py", 1024))
docs = Directory("docs").add(File("README.md", 512))
root.add(src).add(docs).add(File("setup.py", 256))
root.display()


# ══════════════════════════════════════════════════════════════════════════════
#  BEHAVIOURAL PATTERNS
# ══════════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 60)
print("BEHAVIOURAL PATTERNS")
print("=" * 60)

# ── 8. Observer ───────────────────────────────────────────────────────────────

print("\n--- Observer ---")

class EventEmitter:
    """Minimal pub/sub event emitter."""
    def __init__(self):
        self._listeners: dict[str, list[Callable]] = {}

    def on(self, event: str, handler: Callable) -> None:
        self._listeners.setdefault(event, []).append(handler)

    def emit(self, event: str, *args, **kwargs) -> None:
        for handler in self._listeners.get(event, []):
            handler(*args, **kwargs)

class InventorySystem(EventEmitter):
    def __init__(self):
        super().__init__()
        self._stock: dict = {}

    def update_stock(self, item: str, qty: int):
        self._stock[item] = qty
        self.emit("stock_updated", item=item, qty=qty)
        if qty == 0:
            self.emit("out_of_stock", item=item)

inv = InventorySystem()
inv.on("stock_updated", lambda item, qty: print(f"  [Logger] {item}: {qty} units"))
inv.on("out_of_stock",  lambda item:      print(f"  [Alert] {item!r} is OUT OF STOCK!"))

inv.update_stock("apples", 50)
inv.update_stock("apples", 0)


# ── 9. Strategy ───────────────────────────────────────────────────────────────

print("\n--- Strategy ---")
# Defines a family of algorithms, encapsulates each one, makes them interchangeable.

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: list) -> list: ...

class BubbleSort(SortStrategy):
    def sort(self, data):
        d = data[:]
        for i in range(len(d)):
            for j in range(len(d)-i-1):
                if d[j] > d[j+1]: d[j], d[j+1] = d[j+1], d[j]
        return d

class QuickSort(SortStrategy):
    def sort(self, data):
        if len(data) <= 1: return data
        pivot = data[len(data)//2]
        left  = [x for x in data if x < pivot]
        mid   = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + mid + self.sort(right)

class Sorter:
    def __init__(self, strategy: SortStrategy):
        self.strategy = strategy

    def sort(self, data):
        return self.strategy.sort(data)

data = [3, 1, 4, 1, 5, 9, 2, 6]
print(Sorter(BubbleSort()).sort(data))
print(Sorter(QuickSort()).sort(data))

# In Python, you can also pass callables directly instead of strategy objects:
def merge_sort(data):
    if len(data) <= 1: return data
    mid   = len(data) // 2
    left  = merge_sort(data[:mid])
    right = merge_sort(data[mid:])
    return sorted(left + right)   # simplified merge

sorter = Sorter(type("Fn", (SortStrategy,), {"sort": lambda self, d: merge_sort(d)})())
print(sorter.sort(data))


# ── 10. Command ───────────────────────────────────────────────────────────────

print("\n--- Command ---")
# Encapsulates a request as an object, supports undo/redo.

class Command(ABC):
    @abstractmethod
    def execute(self): ...
    @abstractmethod
    def undo(self): ...

class TextEditor:
    def __init__(self):
        self.text = ""
        self._history: list[Command] = []

    def apply(self, command: Command):
        command.execute()
        self._history.append(command)

    def undo(self):
        if self._history:
            self._history.pop().undo()

class InsertText(Command):
    def __init__(self, editor, text):
        self.editor = editor
        self.text   = text
    def execute(self):
        self.editor.text += self.text
    def undo(self):
        self.editor.text = self.editor.text[:-len(self.text)]

class DeleteLast(Command):
    def __init__(self, editor, n):
        self.editor  = editor
        self.n       = n
        self._deleted = ""
    def execute(self):
        self._deleted = self.editor.text[-self.n:]
        self.editor.text = self.editor.text[:-self.n]
    def undo(self):
        self.editor.text += self._deleted

ed = TextEditor()
ed.apply(InsertText(ed, "Hello"))
ed.apply(InsertText(ed, ", World!"))
print(f"  After inserts: {ed.text!r}")
ed.undo()
print(f"  After undo: {ed.text!r}")
ed.undo()
print(f"  After undo: {ed.text!r}")


# ── 11. Template Method ───────────────────────────────────────────────────────

print("\n--- Template Method ---")
# Base class defines the skeleton of an algorithm; subclasses fill in specific steps.

class DataPipeline(ABC):
    def run(self):   # Template method — defines the algorithm skeleton
        data = self.extract()
        data = self.transform(data)
        self.load(data)

    @abstractmethod
    def extract(self) -> list: ...

    def transform(self, data: list) -> list:
        return data   # default: no-op; subclasses can override

    @abstractmethod
    def load(self, data: list) -> None: ...

class CSVToDatabase(DataPipeline):
    def extract(self):
        return [{"name": "Alice", "score": "85"}, {"name": "Bob", "score": "92"}]

    def transform(self, data):
        return [{"name": r["name"], "score": int(r["score"])} for r in data]

    def load(self, data):
        print(f"  Inserting into DB: {data}")

CSVToDatabase().run()


# ── 12. Chain of Responsibility ───────────────────────────────────────────────

print("\n--- Chain of Responsibility ---")
# Pass a request along a chain of handlers; each handles or forwards.

class Handler(ABC):
    def __init__(self):
        self._next: "Handler | None" = None

    def set_next(self, handler: "Handler") -> "Handler":
        self._next = handler
        return handler   # allows chaining: h1.set_next(h2).set_next(h3)

    def handle(self, request: int) -> str:
        if self._next:
            return self._next.handle(request)
        return f"Unhandled: {request}"

class SmallHandler(Handler):
    def handle(self, request):
        if request < 10:
            return f"Small({request})"
        return super().handle(request)

class MediumHandler(Handler):
    def handle(self, request):
        if 10 <= request < 100:
            return f"Medium({request})"
        return super().handle(request)

class LargeHandler(Handler):
    def handle(self, request):
        return f"Large({request})"

h1 = SmallHandler()
h1.set_next(MediumHandler()).set_next(LargeHandler())

for value in [5, 50, 500]:
    print(f"  {value} → {h1.handle(value)}")


print("\nDone: design_patterns")
