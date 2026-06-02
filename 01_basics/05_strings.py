"""
STRINGS
=======
String creation, immutability, slicing, built-in methods, formatting (%, .format, f-strings),
encoding/decoding, regular expressions, and common patterns.

Run: python 01_basics/05_strings.py
"""

# ── 1. Creation and Immutability ─────────────────────────────────────────────

print("--- Creation ---")
s1 = 'single quotes'
s2 = "double quotes"
s3 = """triple-quoted
multi-line string"""
s4 = r"raw string: \n \t not escaped"   # r-prefix: backslashes are literal
s5 = b"bytes literal"                   # bytes, not str

print(s3)
print(s4)
print(type(s5))   # <class 'bytes'>

# Strings are immutable — you cannot change a character in place
word = "hello"
# word[0] = 'H'   # TypeError
word = "H" + word[1:]   # create a new string instead
print(word)


# ── 2. Indexing and Slicing ───────────────────────────────────────────────────

print("\n--- Indexing & Slicing ---")
s = "Python"
#    P  y  t  h  o  n
#    0  1  2  3  4  5   (forward)
#   -6 -5 -4 -3 -2 -1   (backward)

print(s[0])      # P
print(s[-1])     # n
print(s[2:5])    # tho  (start inclusive, stop exclusive)
print(s[:3])     # Pyt  (omit start → 0)
print(s[3:])     # hon  (omit stop → end)
print(s[::2])    # Pto  (step 2)
print(s[::-1])   # nohtyP  (step -1 reverses the string)

# Extended slice: s[start:stop:step]
print("abcdefgh"[1:7:2])   # bdf


# ── 3. Common String Methods ──────────────────────────────────────────────────

print("\n--- Methods ---")
text = "  Hello, World!  "

# Case methods
print(text.strip())          # remove leading/trailing whitespace
print(text.lower())          # all lowercase
print(text.upper())          # all uppercase
print("hello world".title()) # Title Case
print("hello world".capitalize())  # First letter only

# Search / test
print("world" in text.lower())         # True
print(text.strip().startswith("Hello"))# True
print(text.strip().endswith("!"))      # True
print(text.strip().find("World"))      # 7  (-1 if not found)
print(text.strip().index("World"))     # 7  (raises ValueError if not found)
print(text.strip().count("l"))         # 3

# Modification (returns NEW string — strings are immutable)
print(text.strip().replace("World", "Python"))
print("a,b,c".split(","))              # ['a', 'b', 'c']
print("a,b,,c".split(","))            # ['a', 'b', '', 'c']
print(" ".join(["Hello", "World"]))   # "Hello World"

# Padding
print("42".zfill(5))           # 00042
print("hi".ljust(10, "-"))     # hi--------
print("hi".rjust(10, "-"))     # --------hi
print("hi".center(10, "-"))    # ----hi----

# Type-test methods
print("abc".isalpha())    # True — all alphabetic
print("123".isdigit())    # True — all digits
print("abc123".isalnum()) # True — alphanumeric
print("   ".isspace())    # True — all whitespace


# ── 4. String Formatting ──────────────────────────────────────────────────────

print("\n--- Formatting ---")
name = "Alice"
age  = 30

# Method 1: % formatting (old, C-style)
print("Name: %s, Age: %d" % (name, age))
print("Pi: %.2f" % 3.14159)

# Method 2: str.format()
print("Name: {}, Age: {}".format(name, age))
print("Name: {n}, Age: {a}".format(n=name, a=age))
print("{0} {0} {1}".format("Go", "Python"))

# Method 3: f-strings (Python 3.6+) — fastest and most readable
pi = 3.14159
print(f"Name: {name}, Age: {age}")
print(f"Pi = {pi:.2f}")              # format spec after colon
print(f"{age:05d}")                  # zero-padded int: 00030
print(f"{1_000_000:,}")              # thousands separator: 1,000,000
print(f"{'left':<10}|{'center':^10}|{'right':>10}")  # alignment

# Expressions inside f-strings:
print(f"{2 ** 10 = }")           # Python 3.8+ debug format: 2 ** 10 = 1024
print(f"{name.upper()!r}")       # !r calls repr(); !s calls str(); !a for ascii

# Template strings — safe for user-controlled input (no code execution)
from string import Template
tmpl = Template("Hello, $name! You are $age years old.")
print(tmpl.substitute(name=name, age=age))


# ── 5. Useful Built-in Functions on Strings ──────────────────────────────────

print("\n--- Built-ins ---")
print(len("Python"))        # 6
print(ord("A"))             # 65  — Unicode code point of character
print(chr(65))              # 'A' — character for code point
print(sorted("python"))     # ['h', 'n', 'o', 'p', 't', 'y'] — list of chars
print("".join(sorted("python")))  # 'hnopyt'


# ── 6. Encoding / Decoding ────────────────────────────────────────────────────

print("\n--- Encoding ---")
text = "café"
encoded = text.encode("utf-8")          # str → bytes
print(encoded)                          # b'caf\xc3\xa9'
decoded = encoded.decode("utf-8")       # bytes → str
print(decoded)                          # café

# Different encodings:
print(text.encode("latin-1"))           # b'caf\xe9'
print(text.encode("utf-16"))            # includes BOM


# ── 7. Regular Expressions ────────────────────────────────────────────────────

print("\n--- Regular Expressions ---")
import re

text = "Call us at 555-1234 or 555-5678 for info."

# re.search — find first match anywhere
m = re.search(r"\d{3}-\d{4}", text)
if m:
    print(f"First phone: {m.group()}")      # 555-1234
    print(f"Position: {m.start()}-{m.end()}")

# re.findall — return list of all matches
phones = re.findall(r"\d{3}-\d{4}", text)
print(f"All phones: {phones}")              # ['555-1234', '555-5678']

# re.sub — replace matches
clean = re.sub(r"\d{3}-\d{4}", "XXX-XXXX", text)
print(clean)

# re.match — matches only at the beginning of string
m = re.match(r"\d+", "123abc")
print(m.group() if m else "no match")      # 123

# Groups — capture sub-patterns
m = re.search(r"(\d{3})-(\d{4})", text)
if m:
    print(f"Area: {m.group(1)}, Number: {m.group(2)}")

# Compiled pattern — reuse for performance
pattern = re.compile(r"\b[A-Z][a-z]+\b")   # capitalized words
print(pattern.findall("Hello World from Python"))   # ['Hello', 'World', 'From', 'Python']


# ── 8. String Interning and Identity ──────────────────────────────────────────

print("\n--- Interning ---")
# CPython interns (caches) short strings that look like identifiers.
a = "hello"
b = "hello"
print(a is b)    # True — interned (same object)

c = "hello world"
d = "hello world"
print(c is d)    # May be True or False — implementation dependent
print(c == d)    # Always True — use == for value comparison


print("\nDone: strings")
