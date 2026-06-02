"""
DECORATORS
==========
Function decorators, class decorators, decorator factories (with arguments),
stacking decorators, functools.wraps, and common real-world patterns.

Run: python 03_advanced/01_decorators.py
"""

import time
import functools
from functools import wraps

# ── 1. What is a Decorator? ───────────────────────────────────────────────────

print("--- What is a decorator? ---")
# A decorator is a callable that receives a function and returns a new function.
# @syntax is just syntactic sugar:
#
#   @decorator
#   def func(): ...
#
# is exactly:
#   def func(): ...
#   func = decorator(func)

def shout(func):
    """Wraps func so its return value is uppercased."""
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

@shout
def greet(name):
    return f"hello, {name}"

print(greet("alice"))   # HELLO, ALICE

# Without @syntax (equivalent):
def greet2(name): return f"hello, {name}"
greet2 = shout(greet2)
print(greet2("bob"))    # HELLO, BOB


# ── 2. Preserving Metadata with @wraps ────────────────────────────────────────

print("\n--- @wraps ---")

def shout_fixed(func):
    @wraps(func)   # copies __name__, __doc__, __annotations__, __module__, __qualname__
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()
    return wrapper

@shout_fixed
def greet3(name: str) -> str:
    """Returns a greeting for name."""
    return f"hello, {name}"

print(greet3("carol"))
print(greet3.__name__)   # "greet3" (not "wrapper")
print(greet3.__doc__)    # "Returns a greeting for name."


# ── 3. Timing Decorator ───────────────────────────────────────────────────────

print("\n--- Timing decorator ---")

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start  = time.perf_counter()
        result = func(*args, **kwargs)
        end    = time.perf_counter()
        print(f"  {func.__name__} took {end - start:.6f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    """Sum of 0..n using a loop."""
    return sum(range(n))

print(slow_sum(1_000_000))


# ── 4. Logging / Tracing Decorator ───────────────────────────────────────────

print("\n--- Logging decorator ---")

def trace(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        arg_repr = ", ".join([repr(a) for a in args] +
                              [f"{k}={v!r}" for k, v in kwargs.items()])
        print(f"  >> {func.__name__}({arg_repr})")
        result = func(*args, **kwargs)
        print(f"  << {func.__name__} returned {result!r}")
        return result
    return wrapper

@trace
def add(x, y):
    return x + y

add(3, y=4)


# ── 5. Decorator Factory — Decorators with Arguments ──────────────────────────

print("\n--- Decorator factory (with args) ---")
# A decorator factory returns a decorator.
# Three levels: factory → decorator → wrapper.

def repeat(times):
    """Calls the decorated function `times` times."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator   # returns the decorator

@repeat(3)
def say(msg):
    print(f"  {msg}")

say("Hello!")

# Another example: retry on exception
def retry(max_attempts=3, exceptions=(Exception,), delay=0.0):
    """Retries the function on failure."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"  Attempt {attempt} failed: {e}")
                    if attempt == max_attempts:
                        raise
                    if delay:
                        time.sleep(delay)
        return wrapper
    return decorator

attempts = [0]

@retry(max_attempts=3)
def flaky():
    attempts[0] += 1
    if attempts[0] < 3:
        raise ValueError(f"Not ready (attempt {attempts[0]})")
    return "success"

print(flaky())


# ── 6. Stacking Decorators ────────────────────────────────────────────────────

print("\n--- Stacking ---")
# Decorators apply bottom-up (innermost first):
#   @A
#   @B
#   def f(): ...
# is equivalent to: f = A(B(f))

@timer
@trace
def multiply(x, y):
    """Returns x * y."""
    return x * y

multiply(3, 4)
# trace wraps multiply first, then timer wraps that wrapper


# ── 7. Class Decorator ────────────────────────────────────────────────────────

print("\n--- Class decorator ---")
# A class that implements __call__ can be used as a decorator.

class Memoize:
    """Caches results of calls with the same arguments."""

    def __init__(self, func):
        self.func  = func
        self.cache = {}
        wraps(func)(self)   # copy metadata to self

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

@Memoize
def fib(n):
    return n if n <= 1 else fib(n - 1) + fib(n - 2)

print([fib(i) for i in range(10)])
print(fib.cache)


# ── 8. Decorating a Class ────────────────────────────────────────────────────

print("\n--- Decorating a class ---")
# Decorators can also be applied to class definitions.

def singleton(cls):
    """Ensures only one instance of cls is ever created."""
    instances = {}
    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Config:
    def __init__(self):
        self.data = {}
        print("  Config created")

c1 = Config()
c2 = Config()
print(c1 is c2)   # True — same instance


# ── 9. Real-World Patterns ────────────────────────────────────────────────────

print("\n--- Real-world: access control ---")

def require_permission(permission):
    """Checks that the active user has the required permission."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Simulated permission check:
            user_permissions = {"read", "write"}
            if permission not in user_permissions:
                raise PermissionError(f"Requires '{permission}' permission")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@require_permission("admin")
def delete_database():
    return "Database deleted!"

@require_permission("read")
def list_records():
    return ["rec1", "rec2"]

try:
    delete_database()
except PermissionError as e:
    print(f"  Caught: {e}")

print(list_records())

print("\n--- Real-world: validation ---")

def validate_types(**type_map):
    """Validates argument types at call time."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Pair args with parameter names from the type map
            import inspect
            sig    = inspect.signature(func)
            bound  = sig.bind(*args, **kwargs)
            for param, value in bound.arguments.items():
                if param in type_map and not isinstance(value, type_map[param]):
                    raise TypeError(
                        f"{func.__name__}: param '{param}' expected "
                        f"{type_map[param].__name__}, got {type(value).__name__}"
                    )
            return func(*args, **kwargs)
        return wrapper
    return decorator

@validate_types(name=str, age=int)
def register(name, age):
    return f"Registered {name}, age {age}"

print(register("Alice", 30))
try:
    register("Bob", "thirty")   # age is not int
except TypeError as e:
    print(f"  Caught: {e}")


print("\nDone: decorators")
