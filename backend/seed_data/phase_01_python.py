"""Phase 1 — Python Fundamentals."""

PHASE = {
    "phase_number": 1,
    "title": "Python Fundamentals",
    "description": (
        "Variables, control flow, functions and collections — the foundation "
        "every later phase builds on. If you can read and write these, you can "
        "read almost any AI codebase."
    ),
    "estimated_hours": 12,
    "lessons": [
        {
            "title": "Variables & Data Types",
            "description": "Store values and understand Python's core built-in types.",
            "estimated_minutes": 25,
            "content_markdown": """
# Variables & Data Types

A **variable** is a name bound to a value. Python is *dynamically typed*: you
never declare a type — the type comes from the value you assign.

```python
name = "Ada"      # str
age = 36           # int
height = 1.68      # float
is_admin = True    # bool
nothing = None     # NoneType
```

## Key ideas
- Inspect any value's type with `type(x)`.
- `int` and `float` are numeric; mixing them yields a `float` (`3 + 0.0 == 3.0`).
- Strings are **immutable** — operations build *new* strings.
- `None` represents "no value" and is its own type.

## Why it matters for AI
Every dataset is ultimately numbers and strings. Knowing when something is an
`int` vs `float` vs `str` is the difference between a model that trains and a
`TypeError` at 2 a.m.
""",
            "examples": [
                {
                    "title": "Inspecting types",
                    "language": "python",
                    "code": "print(type(42))      # <class 'int'>\nprint(type(3.14))    # <class 'float'>\nprint(type('hi'))    # <class 'str'>\nprint(type(True))    # <class 'bool'>",
                },
                {
                    "title": "f-strings for formatting",
                    "language": "python",
                    "code": "name, acc = 'model_v2', 0.9137\nprint(f'{name} reached {acc:.1%} accuracy')  # model_v2 reached 91.4% accuracy",
                },
            ],
            "challenges": [
                {
                    "title": "Sum Two Numbers",
                    "description": "Implement `add(a, b)` that returns the sum of its two arguments.",
                    "starter_code": "def add(a, b):\n    # Return the sum of a and b\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["The `+` operator adds two numbers.", "Use `return`, not `print`."],
                    "solution_code": "def add(a, b):\n    return a + b\n",
                    "test_cases": [
                        {"call": "add(2, 3)", "expected": "5"},
                        {"call": "add(-1, 1)", "expected": "0"},
                        {"call": "add(100, 250)", "expected": "350"},
                        {"call": "add(2.5, 0.5)", "expected": "3.0"},
                    ],
                }
            ],
        },
        {
            "title": "Control Flow & Loops",
            "description": "Branch with if/elif/else and repeat work with loops.",
            "estimated_minutes": 30,
            "content_markdown": """
# Control Flow & Loops

Programs make decisions with `if` and repeat work with loops.

```python
for i in range(3):
    if i % 2 == 0:
        print(i, "even")
    else:
        print(i, "odd")
```

## Key ideas
- `range(n)` yields `0 .. n-1`; `range(a, b)` yields `a .. b-1`.
- `%` is the modulo (remainder) operator — the workhorse of "every k-th" logic.
- Accumulate results in a variable or list as you loop.
- `break` exits a loop early; `continue` skips to the next iteration.

## Why it matters for AI
Training loops, epochs, mini-batches — deep learning *is* loops. You'll write
`for epoch in range(num_epochs):` more times than you can count.
""",
            "examples": [
                {
                    "title": "Accumulating a sum",
                    "language": "python",
                    "code": "total = 0\nfor i in range(1, 6):\n    total += i\nprint(total)  # 15",
                }
            ],
            "challenges": [
                {
                    "title": "FizzBuzz Value",
                    "description": (
                        "Implement `fizzbuzz(n)`: return 'Fizz' if `n` is divisible by 3, "
                        "'Buzz' if divisible by 5, 'FizzBuzz' if divisible by both, else "
                        "`str(n)`."
                    ),
                    "starter_code": "def fizzbuzz(n):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Check divisibility by both (15) first.", "`n % 3 == 0` tests divisibility by 3."],
                    "solution_code": (
                        "def fizzbuzz(n):\n"
                        "    if n % 15 == 0:\n"
                        "        return 'FizzBuzz'\n"
                        "    if n % 3 == 0:\n"
                        "        return 'Fizz'\n"
                        "    if n % 5 == 0:\n"
                        "        return 'Buzz'\n"
                        "    return str(n)\n"
                    ),
                    "test_cases": [
                        {"call": "fizzbuzz(3)", "expected": "'Fizz'"},
                        {"call": "fizzbuzz(5)", "expected": "'Buzz'"},
                        {"call": "fizzbuzz(15)", "expected": "'FizzBuzz'"},
                        {"call": "fizzbuzz(7)", "expected": "'7'"},
                    ],
                }
            ],
        },
        {
            "title": "Functions & Scope",
            "description": "Package logic into reusable functions with parameters and return values.",
            "estimated_minutes": 30,
            "content_markdown": """
# Functions & Scope

A **function** packages logic behind a name so you can reuse it.

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Ada")                 # 'Hello, Ada!'
greet("Ada", greeting="Hi")  # 'Hi, Ada!'
```

## Key ideas
- Parameters can have **defaults** (`greeting="Hello"`).
- Pass arguments **positionally** or **by keyword**.
- Variables created inside a function are **local** — they don't leak out.
- A function without an explicit `return` returns `None`.

## Why it matters for AI
Loss functions, activation functions, data transforms — they're all just
functions. Clean functions are what make ML code testable instead of a
1,000-line script.
""",
            "examples": [
                {
                    "title": "Default and keyword arguments",
                    "language": "python",
                    "code": "def scale(x, factor=2):\n    return x * factor\n\nprint(scale(5))            # 10\nprint(scale(5, factor=3))  # 15",
                }
            ],
            "challenges": [
                {
                    "title": "Factorial",
                    "description": "Implement `factorial(n)` returning n! (with `factorial(0) == 1`).",
                    "starter_code": "def factorial(n):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Multiply the numbers 1..n.", "0! is defined as 1."],
                    "solution_code": (
                        "def factorial(n):\n"
                        "    result = 1\n"
                        "    for i in range(2, n + 1):\n"
                        "        result *= i\n"
                        "    return result\n"
                    ),
                    "test_cases": [
                        {"call": "factorial(0)", "expected": "1"},
                        {"call": "factorial(1)", "expected": "1"},
                        {"call": "factorial(5)", "expected": "120"},
                        {"call": "factorial(7)", "expected": "5040"},
                    ],
                }
            ],
        },
        {
            "title": "Collections & Comprehensions",
            "description": "Lists, dicts, sets, and the comprehension syntax that makes them sing.",
            "estimated_minutes": 35,
            "content_markdown": """
# Collections & Comprehensions

Python's built-in containers cover most data-wrangling needs:

```python
nums   = [1, 2, 3]            # list  — ordered, mutable
counts = {"a": 1, "b": 2}     # dict  — key -> value
seen   = {1, 2, 3}            # set   — unique, unordered
point  = (10, 20)            # tuple — ordered, immutable
```

## Comprehensions
A compact way to build a collection from an iterable:

```python
squares = [x * x for x in range(5)]          # [0, 1, 4, 9, 16]
evens   = [x for x in range(10) if x % 2 == 0]
lookup  = {w: len(w) for w in ["ai", "ml"]}   # {'ai': 2, 'ml': 2}
```

## Why it matters for AI
Feature dictionaries, vocabularies, one-hot maps, batching — you'll live in
lists and dicts. Comprehensions turn 5-line loops into 1 readable line.
""",
            "examples": [
                {
                    "title": "Counting with a dict",
                    "language": "python",
                    "code": "words = ['ai', 'ml', 'ai', 'dl', 'ai']\ncounts = {}\nfor w in words:\n    counts[w] = counts.get(w, 0) + 1\nprint(counts)  # {'ai': 3, 'ml': 1, 'dl': 1}",
                }
            ],
            "challenges": [
                {
                    "title": "Word Frequencies",
                    "description": (
                        "Implement `word_count(text)` returning a dict mapping each "
                        "whitespace-separated word to how many times it appears. "
                        "Assume input is already lowercased and clean."
                    ),
                    "starter_code": "def word_count(text):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["`text.split()` splits on whitespace.", "Use `dict.get(word, 0) + 1`."],
                    "solution_code": (
                        "def word_count(text):\n"
                        "    counts = {}\n"
                        "    for w in text.split():\n"
                        "        counts[w] = counts.get(w, 0) + 1\n"
                        "    return counts\n"
                    ),
                    "test_cases": [
                        {"call": "word_count('a b a')", "expected": "{'a': 2, 'b': 1}"},
                        {"call": "word_count('ml ml ml')", "expected": "{'ml': 3}"},
                        {"call": "word_count('')", "expected": "{}"},
                    ],
                },
                {
                    "title": "Unique, Order-Preserving",
                    "description": (
                        "Implement `unique_in_order(items)` returning the items with "
                        "duplicates removed, keeping the first occurrence order."
                    ),
                    "starter_code": "def unique_in_order(items):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Track what you've already seen in a set.", "Append only the first time you meet a value."],
                    "solution_code": (
                        "def unique_in_order(items):\n"
                        "    seen = set()\n"
                        "    out = []\n"
                        "    for x in items:\n"
                        "        if x not in seen:\n"
                        "            seen.add(x)\n"
                        "            out.append(x)\n"
                        "    return out\n"
                    ),
                    "test_cases": [
                        {"call": "unique_in_order([1, 1, 2, 3, 3, 1])", "expected": "[1, 2, 3]"},
                        {"call": "unique_in_order(['a', 'b', 'a'])", "expected": "['a', 'b']"},
                        {"call": "unique_in_order([])", "expected": "[]"},
                    ],
                },
            ],
        },
    ],
}
