"""
FILE HANDLING
=============
open(), file modes, context managers, reading/writing text and binary files,
pathlib, csv, json, and pickle.

Run: python 02_intermediate/06_file_handling.py
"""

import csv
import json
import pickle
import tempfile
import os
from pathlib import Path

# ── 1. Basic File Operations ─────────────────────────────────────────────────

print("--- Basic open() ---")
# Use a temporary directory so this script has no side effects
tmpdir = Path(tempfile.mkdtemp())

sample_path = tmpdir / "sample.txt"

# Writing
with open(sample_path, "w", encoding="utf-8") as f:
    f.write("Line 1\n")
    f.write("Line 2\n")
    f.writelines(["Line 3\n", "Line 4\n"])

print(f"Wrote to: {sample_path}")

# Reading — whole file
with open(sample_path, "r", encoding="utf-8") as f:
    content = f.read()
print(repr(content))

# Reading — line by line (memory-efficient for large files)
with open(sample_path, "r", encoding="utf-8") as f:
    for lineno, line in enumerate(f, start=1):
        print(f"  {lineno}: {line.rstrip()}")

# Reading — list of lines
with open(sample_path, "r", encoding="utf-8") as f:
    lines = f.readlines()
print(f"Lines list: {lines}")

# readline() — one line at a time
with open(sample_path, "r", encoding="utf-8") as f:
    first  = f.readline()
    second = f.readline()
print(f"first={first!r}, second={second!r}")


# ── 2. File Modes ─────────────────────────────────────────────────────────────

print("\n--- File Modes ---")
# "r"  — read (default); FileNotFoundError if missing
# "w"  — write; creates or TRUNCATES existing file
# "a"  — append; creates if missing, never truncates
# "x"  — exclusive create; FileExistsError if file already exists
# "b"  — binary mode (combine: "rb", "wb")
# "+"  — read+write (combine: "r+", "w+")

# Append mode:
with open(sample_path, "a", encoding="utf-8") as f:
    f.write("Line 5 (appended)\n")

# Read+write without truncating:
with open(sample_path, "r+", encoding="utf-8") as f:
    f.seek(0)           # move to start
    original = f.read()
    f.seek(0)           # back to start
    f.write(original.upper())   # overwrite with uppercase version

with open(sample_path, "r") as f:
    print(f.read())


# ── 3. Binary Files ───────────────────────────────────────────────────────────

print("\n--- Binary files ---")
bin_path = tmpdir / "data.bin"

# Write raw bytes
with open(bin_path, "wb") as f:
    f.write(b"\x89PNG\r\n\x1a\n")   # PNG magic bytes
    f.write((1024).to_bytes(4, "big"))  # write int as 4-byte big-endian

with open(bin_path, "rb") as f:
    magic = f.read(8)
    width = int.from_bytes(f.read(4), "big")
print(f"magic={magic!r}, width={width}")

# seek() / tell() — random access
with open(sample_path, "rb") as f:
    f.seek(0, 2)              # seek to end (offset=0, whence=2)
    size = f.tell()           # current position = file size
    print(f"File size: {size} bytes")
    f.seek(0)                 # back to beginning


# ── 4. pathlib — Modern Path Handling ─────────────────────────────────────────

print("\n--- pathlib ---")
# pathlib.Path is the modern, cross-platform alternative to os.path

p = Path("/usr/local/bin/python3")
print(p.name)       # "python3"       — filename with extension
print(p.stem)       # "python3"       — filename without extension
print(p.suffix)     # ""              — extension (e.g. ".py")
print(p.parent)     # Path("/usr/local/bin")
print(p.parts)      # ('/', 'usr', 'local', 'bin', 'python3')

# Building paths with / operator:
home    = Path.home()
config  = home / ".config" / "myapp" / "settings.json"
print(config)

# Working with our temp files:
for fp in tmpdir.iterdir():
    print(f"  {fp.name} — {fp.stat().st_size} bytes")

# Read/write directly via Path:
text_path = tmpdir / "via_pathlib.txt"
text_path.write_text("Hello from pathlib!\n", encoding="utf-8")
print(text_path.read_text(encoding="utf-8"))

# glob patterns:
py_files = list(Path(".").glob("**/*.py"))
print(f"Found {len(py_files)} .py files in current directory tree")

# Existence checks:
print(text_path.exists())
print(text_path.is_file())
print(tmpdir.is_dir())


# ── 5. CSV Files ──────────────────────────────────────────────────────────────

print("\n--- CSV ---")
csv_path = tmpdir / "employees.csv"

rows = [
    ["name",  "department",  "salary"],
    ["Alice", "Engineering", 95000],
    ["Bob",   "Marketing",   72000],
    ["Carol", "Engineering", 88000],
]

# Writing CSV
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

# Reading CSV as lists
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
        print(f"  {row}")

# DictReader — each row is a dict keyed by header
with open(csv_path, "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    employees = list(reader)

for emp in employees:
    print(f"  {emp['name']} ({emp['department']}): ${emp['salary']}")

# DictWriter — write dicts
json_csv = tmpdir / "settings.csv"
with open(json_csv, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["key", "value"])
    writer.writeheader()
    writer.writerows([{"key": "host", "value": "localhost"},
                       {"key": "port", "value": "5432"}])


# ── 6. JSON Files ─────────────────────────────────────────────────────────────

print("\n--- JSON ---")
data = {
    "name": "Alice",
    "age": 30,
    "scores": [95, 87, 91],
    "address": {"city": "NYC", "zip": "10001"},
    "active": True,
    "note": None
}

json_path = tmpdir / "user.json"

# Write JSON — indent for human-readable output
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print(json_path.read_text())

# Read JSON
with open(json_path, "r", encoding="utf-8") as f:
    loaded = json.load(f)

print(loaded["name"], loaded["scores"])

# Serialize/deserialize to/from string:
s = json.dumps(data, sort_keys=True)
d = json.loads(s)
print(d["age"])

# Custom serializer for types not supported by default (e.g. datetime):
import datetime
def json_default(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

obj = {"created": datetime.datetime.now()}
print(json.dumps(obj, default=json_default))


# ── 7. Pickle — Binary Serialization ─────────────────────────────────────────

print("\n--- Pickle ---")
# Pickle serializes ANY Python object — but output is NOT human-readable,
# NOT portable across Python versions, and NOT safe for untrusted input.

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point({self.x}, {self.y})"

pkl_path = tmpdir / "point.pkl"

p = Point(3, 7)
with open(pkl_path, "wb") as f:
    pickle.dump(p, f, protocol=pickle.HIGHEST_PROTOCOL)

with open(pkl_path, "rb") as f:
    loaded_p = pickle.load(f)

print(f"Loaded: {loaded_p}")

# In-memory pickle:
data = {"key": [1, 2, 3], "nested": {"a": 1}}
b = pickle.dumps(data)
print(pickle.loads(b))


# ── 8. Cleanup ────────────────────────────────────────────────────────────────

import shutil
shutil.rmtree(tmpdir)   # remove temp directory and all its contents
print(f"\nCleaned up temp dir: {tmpdir}")


print("\nDone: file_handling")
