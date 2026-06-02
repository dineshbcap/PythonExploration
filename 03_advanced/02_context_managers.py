"""
CONTEXT MANAGERS
================
The `with` statement, __enter__/__exit__ protocol, contextlib helpers
(contextmanager, suppress, redirect_stdout, ExitStack), and reentrant managers.

Run: python 03_advanced/02_context_managers.py
"""

import contextlib
import io
import os
import tempfile
import time
from pathlib import Path

# ── 1. Why Context Managers? ──────────────────────────────────────────────────

print("--- Why context managers? ---")
# They guarantee cleanup (releasing resources) whether the body succeeds or fails.
# The with-statement is equivalent to try/finally:
#
#   with open("f") as f:
#       data = f.read()
#
# is equivalent to:
#   f = open("f")
#   try:
#       data = f.read()
#   finally:
#       f.close()

with open(tempfile.mktemp(), "w") as f:
    f.write("test")
    print(f"File open: {not f.closed}")

print(f"File closed after with: {f.closed}")   # True — auto-closed


# ── 2. Class-Based Context Manager ───────────────────────────────────────────

print("\n--- Class-based context manager ---")
# Implement __enter__ (setup) and __exit__ (teardown) in a class.

class Timer:
    """Measures elapsed time of a block."""

    def __enter__(self):
        self._start = time.perf_counter()
        return self   # returned as the `as` variable

    def __exit__(self, exc_type, exc_val, exc_tb):
        # exc_type, exc_val, exc_tb are None if no exception occurred.
        # Returning True suppresses the exception; returning False/None lets it propagate.
        self.elapsed = time.perf_counter() - self._start
        return False   # do not suppress exceptions

with Timer() as t:
    total = sum(range(1_000_000))

print(f"sum={total}, elapsed={t.elapsed:.4f}s")


class ManagedFile:
    """Custom file context manager."""

    def __init__(self, path, mode="r", encoding="utf-8"):
        self.path     = path
        self.mode     = mode
        self.encoding = encoding
        self._file    = None

    def __enter__(self):
        self._file = open(self.path, self.mode, encoding=self.encoding)
        return self._file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file and not self._file.closed:
            self._file.close()
        # Don't return True — let exceptions propagate
        return False

tmp = tempfile.mktemp(suffix=".txt")
with ManagedFile(tmp, "w") as f:
    f.write("Hello!")

with ManagedFile(tmp, "r") as f:
    print(f.read())


# ── 3. Exception Handling in __exit__ ────────────────────────────────────────

print("\n--- __exit__ with exception handling ---")

class Suppressor:
    """Suppresses a specific exception type."""

    def __init__(self, *exception_types):
        self.exception_types = exception_types

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Returning True suppresses the exception
        if exc_type and issubclass(exc_type, self.exception_types):
            print(f"  Suppressing: {exc_type.__name__}: {exc_val}")
            return True
        return False   # re-raise everything else

with Suppressor(ValueError, KeyError):
    d = {}
    _ = d["missing"]   # KeyError — suppressed
print("After suppressor block")

with Suppressor(ValueError):
    x = int("not a number")   # ValueError — suppressed
print("After ValueError suppressor")


# ── 4. @contextmanager — Generator-Based ──────────────────────────────────────

print("\n--- @contextmanager ---")
# contextlib.contextmanager lets you write a context manager as a generator.
# Everything before yield is __enter__; everything after is __exit__.

@contextlib.contextmanager
def timer_cm():
    """Simpler Timer using generator style."""
    start = time.perf_counter()
    try:
        yield   # control passes to the with-block here
    finally:
        elapsed = time.perf_counter() - start
        print(f"  Elapsed: {elapsed:.4f}s")

with timer_cm():
    _ = sum(range(500_000))

# Generator-based managers that handle exceptions:
@contextlib.contextmanager
def managed_resource(name):
    """Acquire/release pattern with exception handling."""
    print(f"  Acquiring {name}")
    resource = {"name": name, "open": True}
    try:
        yield resource
    except ValueError as e:
        print(f"  Handling ValueError: {e}")
        # Don't re-raise — the exception is swallowed
    except Exception:
        print(f"  Unhandled exception — cleaning up {name}")
        raise   # re-raise
    finally:
        resource["open"] = False
        print(f"  Releasing {name}")

with managed_resource("database") as db:
    print(f"  Using: {db}")
    raise ValueError("query failed")   # caught and swallowed

print("After managed_resource block")


# ── 5. contextlib Utilities ───────────────────────────────────────────────────

print("\n--- contextlib utilities ---")

# suppress — context manager version of "ignore this exception"
with contextlib.suppress(FileNotFoundError):
    os.remove("/tmp/nonexistent_file_xyz.txt")
print("No crash after suppress")

# redirect_stdout — capture or redirect print output
buffer = io.StringIO()
with contextlib.redirect_stdout(buffer):
    print("This goes to the buffer, not the terminal")
captured = buffer.getvalue()
print(f"Captured: {captured!r}")

# redirect_stderr
err_buf = io.StringIO()
with contextlib.redirect_stderr(err_buf):
    import sys
    print("Error message", file=sys.stderr)
print(f"Captured stderr: {err_buf.getvalue()!r}")

# nullcontext — a no-op context manager (useful as a conditional placeholder)
def process(data, lock=None):
    cm = lock if lock is not None else contextlib.nullcontext()
    with cm:
        return [x * 2 for x in data]

print(process([1, 2, 3]))


# ── 6. ExitStack — Dynamic Context Management ─────────────────────────────────

print("\n--- ExitStack ---")
# ExitStack lets you manage a variable number of context managers dynamically.

files = []
with contextlib.ExitStack() as stack:
    for name in ["file1.txt", "file2.txt", "file3.txt"]:
        path = tmpfile = stack.enter_context(
            contextlib.suppress(Exception)   # dummy CM for illustration
        )
    # All entered CMs are exited when the ExitStack exits

# More practical: open many files
tmpdir = Path(tempfile.mkdtemp())
paths  = [tmpdir / f"{i}.txt" for i in range(3)]
for p in paths: p.write_text("data")

with contextlib.ExitStack() as stack:
    opened = [stack.enter_context(open(p)) for p in paths]
    contents = [f.read() for f in opened]
    print(f"Read {len(contents)} files")
# All three files are closed here

# ExitStack.callback — register a cleanup function without a CM:
with contextlib.ExitStack() as stack:
    stack.callback(print, "  Cleanup 1 called")
    stack.callback(print, "  Cleanup 2 called")
    print("  Inside block")
# Callbacks fire in LIFO order when exiting


# ── 7. Reentrant and Thread-Safe Context Managers ────────────────────────────

print("\n--- Reentrant ---")
# contextlib.contextmanager managers are NOT reentrant by default.
# Use threading.Lock() or contextlib.AbstractContextManager for thread safety.

import threading
lock = threading.Lock()

with lock:
    print("  Lock acquired")
    # lock.acquire() again here would deadlock
# Lock released here

# RLock is reentrant:
rlock = threading.RLock()
with rlock:
    with rlock:   # second acquisition OK for the SAME thread
        print("  RLock acquired twice by same thread — no deadlock")


# ── 8. Using Context Managers for Transactions ────────────────────────────────

print("\n--- Transaction pattern ---")

class FakeDB:
    """Demonstrates transaction context manager."""
    def __init__(self):
        self.committed = False
        self.rolled_back = False

    def execute(self, sql):
        print(f"  SQL: {sql}")

    def commit(self):
        self.committed = True
        print("  COMMIT")

    def rollback(self):
        self.rolled_back = True
        print("  ROLLBACK")

@contextlib.contextmanager
def transaction(db):
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise

db = FakeDB()
with transaction(db) as conn:
    conn.execute("INSERT INTO users VALUES ...")
    conn.execute("UPDATE accounts SET ...")

print(f"committed: {db.committed}")

db2 = FakeDB()
try:
    with transaction(db2) as conn:
        conn.execute("DELETE FROM orders WHERE id=1")
        raise ValueError("Constraint violation!")
except ValueError:
    pass
print(f"rolled back: {db2.rolled_back}")


import shutil
shutil.rmtree(tmpdir)
print("\nDone: context_managers")
