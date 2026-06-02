"""
EXCEPTION HANDLING
==================
try/except/else/finally, exception hierarchy, custom exceptions,
exception chaining, context managers for cleanup, and best practices.

Run: python 02_intermediate/05_exception_handling.py
"""

# ── 1. Basic try/except ───────────────────────────────────────────────────────

print("--- Basic try/except ---")

try:
    x = int("not a number")
except ValueError:
    print("Caught ValueError: couldn't convert string to int")

# Multiple except clauses — most specific first
def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("  Error: division by zero")
        return None
    except TypeError as e:
        print(f"  Error: wrong type — {e}")
        return None
    else:
        # Runs ONLY if no exception was raised in try
        print(f"  {a} / {b} = {result}")
        return result
    finally:
        # ALWAYS runs, exception or not — use for cleanup
        print("  (safe_divide finished)")

safe_divide(10, 2)
safe_divide(10, 0)
safe_divide(10, "x")


# ── 2. Catching Multiple Exceptions in One Clause ────────────────────────────

print("\n--- Multiple in one clause ---")

def parse(text):
    try:
        return int(text)
    except (ValueError, TypeError):
        return None

print(parse("42"))    # 42
print(parse("hi"))    # None
print(parse(None))    # None


# ── 3. Exception Hierarchy ────────────────────────────────────────────────────

print("\n--- Exception Hierarchy ---")
# BaseException
#  ├── SystemExit
#  ├── KeyboardInterrupt
#  ├── GeneratorExit
#  └── Exception
#       ├── ArithmeticError
#       │    ├── ZeroDivisionError
#       │    └── OverflowError
#       ├── LookupError
#       │    ├── IndexError
#       │    └── KeyError
#       ├── ValueError
#       ├── TypeError
#       ├── AttributeError
#       ├── FileNotFoundError
#       ├── OSError (IOError, EnvironmentError)
#       ├── RuntimeError
#       └── StopIteration

# Catch by base class to catch all subclasses:
try:
    d = {}
    _ = d["missing"]
except LookupError as e:
    print(f"LookupError caught: {type(e).__name__}: {e}")


# ── 4. The `as` Keyword — Accessing the Exception Object ──────────────────────

print("\n--- Exception object ---")

try:
    lst = [1, 2, 3]
    lst[10]
except IndexError as e:
    print(f"Type:    {type(e).__name__}")
    print(f"Message: {e}")
    print(f"Args:    {e.args}")


# ── 5. Re-raising Exceptions ──────────────────────────────────────────────────

print("\n--- Re-raise ---")

def process(data):
    try:
        return 100 / data
    except ZeroDivisionError:
        print("  Logging error...")
        raise   # re-raise the SAME exception with original traceback

try:
    process(0)
except ZeroDivisionError as e:
    print(f"  Caller caught: {e}")


# ── 6. Exception Chaining ────────────────────────────────────────────────────

print("\n--- Exception Chaining ---")

def read_config(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError as e:
        # raise X from Y — sets __cause__, shows both in traceback
        raise RuntimeError(f"Config file not found: {path}") from e

try:
    read_config("/nonexistent/config.json")
except RuntimeError as e:
    print(f"Caught: {e}")
    print(f"Caused by: {e.__cause__}")

# raise X from None — suppress the original exception from the traceback
def load(key):
    internal = {"x": 1}
    try:
        return internal[key]
    except KeyError:
        raise ValueError(f"Invalid key: {key!r}") from None

try:
    load("z")
except ValueError as e:
    print(f"Clean error: {e}, __cause__={e.__cause__}")  # None


# ── 7. Custom Exceptions ──────────────────────────────────────────────────────

print("\n--- Custom Exceptions ---")

class AppError(Exception):
    """Base exception for all application errors."""
    pass

class ValidationError(AppError):
    """Raised when input fails validation."""
    def __init__(self, field: str, message: str):
        self.field   = field
        self.message = message
        super().__init__(f"Validation failed on '{field}': {message}")

class DatabaseError(AppError):
    """Raised on database failures."""
    def __init__(self, operation: str, original: Exception = None):
        self.operation = operation
        super().__init__(f"Database error during {operation!r}")
        if original:
            self.__cause__ = original

def create_user(name: str, age: int):
    if not name:
        raise ValidationError("name", "cannot be empty")
    if not (0 < age < 150):
        raise ValidationError("age", f"must be 0-150, got {age}")
    return {"name": name, "age": age}

# Catch the specific custom exception:
for test in [("", 25), ("Alice", -5), ("Alice", 30)]:
    try:
        user = create_user(*test)
        print(f"  Created: {user}")
    except ValidationError as e:
        print(f"  {e}")


# ── 8. except* — Exception Groups (Python 3.11+) ─────────────────────────────

print("\n--- ExceptionGroup (Python 3.11+) ---")
import sys
if sys.version_info >= (3, 11):
    # except* and ExceptionGroup are syntax/runtime features of 3.11+
    exec("""
try:
    raise ExceptionGroup("multiple errors", [
        ValueError("bad value"),
        TypeError("bad type"),
        ValueError("another bad value"),
    ])
except* ValueError as eg:
    print(f"  ValueErrors: {[str(e) for e in eg.exceptions]}")
except* TypeError as eg:
    print(f"  TypeErrors: {[str(e) for e in eg.exceptions]}")
""")
else:
    print(f"  Python {sys.version_info[:2]} — ExceptionGroup/except* is Python 3.11+")
    print("  Concept: ExceptionGroup bundles multiple exceptions raised concurrently")
    print("  (e.g. from asyncio.gather or TaskGroup when several tasks fail)")
    print("  except* matches and splits the group by exception type")


# ── 9. finally and Context Managers ──────────────────────────────────────────

print("\n--- finally patterns ---")

# finally always runs — ideal for releasing resources
def risky_operation():
    resource = "acquired"
    try:
        print(f"  Using {resource}")
        raise RuntimeError("something broke")
    except RuntimeError:
        print("  Handling error")
        raise
    finally:
        print(f"  Releasing {resource}")   # ALWAYS runs

try:
    risky_operation()
except RuntimeError:
    print("  Caller handled it")


# ── 10. Best Practices ────────────────────────────────────────────────────────

print("\n--- Best practices ---")

# BAD: catching bare Exception (hides bugs, catches everything)
# try: ...
# except Exception: pass   # silently swallows all errors

# GOOD: catch the most specific exception you expect
def safe_open(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError:
        return ""    # expected case: file might not exist yet
    except PermissionError as e:
        raise RuntimeError(f"Cannot read {path}: permission denied") from e
    # Any other OSError propagates — we don't know how to handle it

# BAD: using exception flow as normal control flow (slow, unreadable)
# try: return d[key]
# except KeyError: return default

# GOOD: check first (LBYL) or use .get() (EAFP with no overhead)
d = {"a": 1}
# EAFP-style (Python prefers this when exception is rare):
try:
    val = d["b"]
except KeyError:
    val = 0
# Simpler:
val = d.get("b", 0)


print("\nDone: exception_handling")
