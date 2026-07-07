"""Phase 2 — Data Structures & Algorithms."""

PHASE = {
    "phase_number": 2,
    "title": "Data Structures & Algorithms",
    "description": (
        "Stacks, hashing, recursion and search. The vocabulary of efficient code "
        "— and the interview gate for almost every AI/ML role."
    ),
    "estimated_hours": 16,
    "lessons": [
        {
            "title": "Stacks & Queues",
            "description": "LIFO and FIFO structures, and the problems they unlock.",
            "estimated_minutes": 30,
            "content_markdown": """
# Stacks & Queues

A **stack** is last-in-first-out (LIFO); a **queue** is first-in-first-out
(FIFO). In Python a `list` is a ready-made stack:

```python
stack = []
stack.append(1)   # push
stack.append(2)
stack.pop()        # -> 2  (pop the top)
```

## Key ideas
- Stacks shine for *matching* problems: brackets, undo history, call frames.
- For queues, prefer `collections.deque` (O(1) pops from the left).
- The **call stack** is why deep recursion can overflow.

## Why it matters for AI
Tree/graph search, expression parsing, and beam search in NLP all lean on
stacks and queues.
""",
            "examples": [
                {
                    "title": "A deque as a queue",
                    "language": "python",
                    "code": "from collections import deque\nq = deque()\nq.append('a'); q.append('b')\nprint(q.popleft())  # 'a'",
                }
            ],
            "challenges": [
                {
                    "title": "Balanced Brackets",
                    "description": (
                        "Implement `is_balanced(s)` returning True if every '(', '[', "
                        "'{' has a correct matching close in the right order."
                    ),
                    "starter_code": "def is_balanced(s):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Push opening brackets; pop on closing.", "A close with an empty/mismatched stack means unbalanced."],
                    "solution_code": (
                        "def is_balanced(s):\n"
                        "    pairs = {')': '(', ']': '[', '}': '{'}\n"
                        "    stack = []\n"
                        "    for c in s:\n"
                        "        if c in '([{':\n"
                        "            stack.append(c)\n"
                        "        elif c in pairs:\n"
                        "            if not stack or stack.pop() != pairs[c]:\n"
                        "                return False\n"
                        "    return not stack\n"
                    ),
                    "test_cases": [
                        {"call": "is_balanced('()')", "expected": "True"},
                        {"call": "is_balanced('([{}])')", "expected": "True"},
                        {"call": "is_balanced('(]')", "expected": "False"},
                        {"call": "is_balanced('(()')", "expected": "False"},
                    ],
                }
            ],
        },
        {
            "title": "Dictionaries & Hashing",
            "description": "O(1) lookups and the classic problems they make trivial.",
            "estimated_minutes": 30,
            "content_markdown": """
# Dictionaries & Hashing

A dict (hash map) gives **average O(1)** insert and lookup by key. That single
property collapses many O(n^2) brute-force solutions to O(n).

```python
prices = {"gpu": 1500, "cpu": 300}
prices["gpu"]            # 1500  (O(1))
"tpu" in prices          # False (O(1))
```

## Key ideas
- Keys must be **hashable** (immutable): str, int, tuple — not list/dict.
- Use a dict to remember "have I seen this, and where?".
- `dict.get(k, default)` avoids `KeyError`.

## Why it matters for AI
Vocabularies (token -> id), feature maps, caches, and memoization tables are all
dicts. The "two sum" trick below is the same idea behind fast nearest-lookup.
""",
            "examples": [
                {
                    "title": "Remembering seen values",
                    "language": "python",
                    "code": "seen = set()\nfor x in [3, 1, 3, 2]:\n    if x in seen:\n        print('dup', x)\n    seen.add(x)",
                }
            ],
            "challenges": [
                {
                    "title": "Two Sum",
                    "description": (
                        "Implement `two_sum(nums, target)` returning a tuple of the two "
                        "**indices** whose values add to target (earliest such pair, "
                        "left index first). Assume exactly one solution exists."
                    ),
                    "starter_code": "def two_sum(nums, target):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Store value -> index as you scan.", "For each x, check if `target - x` was already seen."],
                    "solution_code": (
                        "def two_sum(nums, target):\n"
                        "    seen = {}\n"
                        "    for i, x in enumerate(nums):\n"
                        "        if target - x in seen:\n"
                        "            return (seen[target - x], i)\n"
                        "        seen[x] = i\n"
                    ),
                    "test_cases": [
                        {"call": "two_sum([2, 7, 11, 15], 9)", "expected": "(0, 1)"},
                        {"call": "two_sum([3, 2, 4], 6)", "expected": "(1, 2)"},
                        {"call": "two_sum([3, 3], 6)", "expected": "(0, 1)"},
                    ],
                }
            ],
        },
        {
            "title": "Recursion",
            "description": "Functions that call themselves — divide and conquer.",
            "estimated_minutes": 30,
            "content_markdown": """
# Recursion

A **recursive** function solves a problem by calling itself on a smaller input,
stopping at a **base case**.

```python
def countdown(n):
    if n == 0:          # base case
        return
    print(n)
    countdown(n - 1)     # recursive step
```

## Key ideas
- Every recursion needs a base case, or it overflows the stack.
- Think: "assume it works for `n-1`; combine that with the current step."
- Some recursions repeat work — **memoize** to fix it (see the dict lesson).

## Why it matters for AI
Tree models (decision trees), recursive tokenizers, and backprop through
computation graphs are all naturally recursive.
""",
            "examples": [
                {
                    "title": "Memoized Fibonacci",
                    "language": "python",
                    "code": "from functools import lru_cache\n\n@lru_cache\ndef fib(n):\n    return n if n < 2 else fib(n - 1) + fib(n - 2)\n\nprint(fib(30))  # 832040 — instant thanks to caching",
                }
            ],
            "challenges": [
                {
                    "title": "Fibonacci",
                    "description": "Implement `fib(n)` where `fib(0)=0`, `fib(1)=1`, `fib(n)=fib(n-1)+fib(n-2)`.",
                    "starter_code": "def fib(n):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Handle n < 2 as the base case.", "Iterating with two rolling variables avoids stack overflow."],
                    "solution_code": (
                        "def fib(n):\n"
                        "    a, b = 0, 1\n"
                        "    for _ in range(n):\n"
                        "        a, b = b, a + b\n"
                        "    return a\n"
                    ),
                    "test_cases": [
                        {"call": "fib(0)", "expected": "0"},
                        {"call": "fib(1)", "expected": "1"},
                        {"call": "fib(10)", "expected": "55"},
                        {"call": "fib(20)", "expected": "6765"},
                    ],
                }
            ],
        },
        {
            "title": "Sorting & Binary Search",
            "description": "Order data, then exploit that order for logarithmic search.",
            "estimated_minutes": 35,
            "content_markdown": """
# Sorting & Binary Search

Sorting arranges data; **binary search** then finds an item in O(log n) by
repeatedly halving the search range — but only works on **sorted** input.

```python
nums = sorted([5, 2, 9, 1])   # [1, 2, 5, 9]
```

## Key ideas
- Python's `sorted()` is O(n log n) and stable.
- Binary search maintains a `[lo, hi]` window and compares the midpoint.
- Off-by-one bugs live here — be precise about `lo`, `hi`, and `mid`.

## Why it matters for AI
Retrieval, ranking, k-NN, and hyperparameter grids all rely on ordering and
fast lookup. Understanding O(log n) vs O(n) is core to scaling.
""",
            "examples": [
                {
                    "title": "Sorting by a key",
                    "language": "python",
                    "code": "records = [('a', 3), ('b', 1), ('c', 2)]\nprint(sorted(records, key=lambda r: r[1]))\n# [('b', 1), ('c', 2), ('a', 3)]",
                }
            ],
            "challenges": [
                {
                    "title": "Binary Search",
                    "description": (
                        "Implement `binary_search(nums, target)` on a sorted ascending "
                        "list. Return the index of target, or -1 if absent."
                    ),
                    "starter_code": "def binary_search(nums, target):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Track `lo` and `hi` inclusive.", "`mid = (lo + hi) // 2`; move the bound that can't contain target."],
                    "solution_code": (
                        "def binary_search(nums, target):\n"
                        "    lo, hi = 0, len(nums) - 1\n"
                        "    while lo <= hi:\n"
                        "        mid = (lo + hi) // 2\n"
                        "        if nums[mid] == target:\n"
                        "            return mid\n"
                        "        if nums[mid] < target:\n"
                        "            lo = mid + 1\n"
                        "        else:\n"
                        "            hi = mid - 1\n"
                        "    return -1\n"
                    ),
                    "test_cases": [
                        {"call": "binary_search([1, 3, 5, 7, 9], 7)", "expected": "3"},
                        {"call": "binary_search([1, 3, 5, 7, 9], 1)", "expected": "0"},
                        {"call": "binary_search([1, 3, 5, 7, 9], 4)", "expected": "-1"},
                        {"call": "binary_search([], 1)", "expected": "-1"},
                    ],
                }
            ],
        },
    ],
}
