"""Phase 4 — Data Manipulation (NumPy & Pandas)."""

PHASE = {
    "phase_number": 4,
    "title": "Data Manipulation with NumPy & Pandas",
    "description": (
        "Load, clean, reshape and aggregate data — the 80% of ML work that isn't "
        "modelling. We show the NumPy/Pandas idioms and drill the underlying logic "
        "in pure Python."
    ),
    "estimated_hours": 18,
    "lessons": [
        {
            "title": "NumPy Arrays & Vectorization",
            "description": "Why array math beats Python loops, and the mental model behind it.",
            "estimated_minutes": 35,
            "content_markdown": """
# NumPy Arrays & Vectorization

NumPy stores numbers in a compact array and applies operations to the **whole
array at once** (vectorization) — far faster than a Python loop.

```python
import numpy as np
a = np.array([1, 2, 3])
a * 2          # array([2, 4, 6])   — no loop
a + a          # array([2, 4, 6])
a.mean()       # 2.0
```

## Key ideas
- Elementwise ops (`+ - * /`) apply position-by-position.
- Reductions (`sum`, `mean`, `max`) collapse an array to a summary.
- Vectorized code is both shorter *and* orders of magnitude faster.

## Why it matters for AI
Tensors are NumPy arrays with a GPU and gradients bolted on. Every framework
inherits this "operate on the whole array" model.
""",
            "examples": [
                {
                    "title": "Vectorized vs loop (same result)",
                    "language": "python",
                    "code": "import numpy as np\nx = np.array([1.0, 2.0, 3.0])\n# normalize to unit sum, no explicit loop\nprint(x / x.sum())  # [0.1667 0.3333 0.5]",
                }
            ],
            "challenges": [
                {
                    "title": "Normalize to Sum 1",
                    "description": (
                        "Implement `normalize(xs)` returning a new list where each element "
                        "is divided by the total, so the result sums to 1. Assume a "
                        "non-empty list with a non-zero sum."
                    ),
                    "starter_code": "def normalize(xs):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Compute the total once.", "Divide each element by the total."],
                    "solution_code": (
                        "def normalize(xs):\n"
                        "    total = sum(xs)\n"
                        "    return [x / total for x in xs]\n"
                    ),
                    "test_cases": [
                        {"call": "normalize([1, 1, 2])", "expected": "[0.25, 0.25, 0.5]"},
                        {"call": "normalize([5])", "expected": "[1.0]"},
                        {"call": "round(sum(normalize([3, 7, 10])), 6)", "expected": "1.0"},
                    ],
                }
            ],
        },
        {
            "title": "Standardization & Broadcasting",
            "description": "Rescale features so no single column dominates.",
            "estimated_minutes": 30,
            "content_markdown": """
# Standardization & Broadcasting

**Broadcasting** lets NumPy combine arrays of different shapes by stretching the
smaller one. The classic use is standardizing a column: subtract the mean,
divide by the std.

```python
import numpy as np
col = np.array([10.0, 20.0, 30.0])
z = (col - col.mean()) / col.std()   # broadcasting the scalars
```

## Key ideas
- Standardized data has mean 0 and std 1.
- Broadcasting avoids writing loops to apply a scalar to every element.
- Always fit scaling on *training* data, then apply the same numbers to test.

## Why it matters for AI
Gradient descent converges far faster when features share a scale. Skipping
standardization is a top cause of "my model won't learn".
""",
            "examples": [
                {
                    "title": "Broadcasting a row subtraction",
                    "language": "python",
                    "code": "import numpy as np\nX = np.array([[1, 2], [3, 4]])\nprint(X - X.mean(axis=0))  # subtract each column's mean",
                }
            ],
            "challenges": [
                {
                    "title": "Standardize (z-score)",
                    "description": (
                        "Implement `standardize(xs)` returning a list where each value is "
                        "`(x - mean) / std` using the population std. If std is 0, return "
                        "a list of zeros of the same length."
                    ),
                    "starter_code": "def standardize(xs):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Reuse mean and population std.", "Guard against std == 0."],
                    "solution_code": (
                        "import math\n\n"
                        "def standardize(xs):\n"
                        "    mean = sum(xs) / len(xs)\n"
                        "    var = sum((x - mean) ** 2 for x in xs) / len(xs)\n"
                        "    sd = math.sqrt(var)\n"
                        "    if sd == 0:\n"
                        "        return [0.0 for _ in xs]\n"
                        "    return [(x - mean) / sd for x in xs]\n"
                    ),
                    "test_cases": [
                        {"call": "standardize([1, 2, 3])", "expected": "[-1.224744871391589, 0.0, 1.224744871391589]"},
                        {"call": "standardize([5, 5, 5])", "expected": "[0.0, 0.0, 0.0]"},
                        {"call": "round(sum(standardize([10, 20, 30, 40])), 6)", "expected": "0.0"},
                    ],
                }
            ],
        },
        {
            "title": "Pandas: Rows, Columns & GroupBy",
            "description": "Tabular data and split-apply-combine aggregation.",
            "estimated_minutes": 35,
            "content_markdown": """
# Pandas: Rows, Columns & GroupBy

Pandas gives you a **DataFrame** — a table with named columns. The killer
feature is **groupby**: split rows into groups, apply a function, combine the
results.

```python
import pandas as pd
df = pd.DataFrame({"team": ["a", "b", "a"], "score": [10, 5, 20]})
df.groupby("team")["score"].sum()   # a -> 30, b -> 5
```

## Key ideas
- A DataFrame is columns of aligned Series.
- `groupby(key).agg(...)` is split-apply-combine.
- Most "how do I summarise this table" questions are a groupby.

## Why it matters for AI
Feature engineering is mostly grouping and aggregating raw events into per-user
or per-item features.
""",
            "examples": [
                {
                    "title": "Group averages",
                    "language": "python",
                    "code": "import pandas as pd\ndf = pd.DataFrame({'k': ['x','y','x'], 'v': [2,4,4]})\nprint(df.groupby('k')['v'].mean().to_dict())  # {'x': 3.0, 'y': 4.0}",
                }
            ],
            "challenges": [
                {
                    "title": "Group Sum",
                    "description": (
                        "Implement `group_sum(rows)` where `rows` is a list of "
                        "`(key, value)` tuples. Return a dict mapping each key to the sum "
                        "of its values."
                    ),
                    "starter_code": "def group_sum(rows):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Iterate the tuples.", "Accumulate with `d.get(key, 0) + value`."],
                    "solution_code": (
                        "def group_sum(rows):\n"
                        "    out = {}\n"
                        "    for key, value in rows:\n"
                        "        out[key] = out.get(key, 0) + value\n"
                        "    return out\n"
                    ),
                    "test_cases": [
                        {"call": "group_sum([('a', 10), ('b', 5), ('a', 20)])", "expected": "{'a': 30, 'b': 5}"},
                        {"call": "group_sum([])", "expected": "{}"},
                        {"call": "group_sum([('x', 1), ('x', 2), ('x', 3)])", "expected": "{'x': 6}"},
                    ],
                }
            ],
        },
        {
            "title": "Handling Missing Data",
            "description": "Detect and fill gaps before they crash your model.",
            "estimated_minutes": 25,
            "content_markdown": """
# Handling Missing Data

Real data has holes. A common, defensible fix is **mean imputation**: replace
missing entries with the mean of the values that are present.

```python
xs = [1.0, None, 3.0, None, 5.0]
present = [x for x in xs if x is not None]     # [1.0, 3.0, 5.0]
mean = sum(present) / len(present)              # 3.0
filled = [x if x is not None else mean for x in xs]
```

## Key ideas
- Decide *why* a value is missing before choosing a fill strategy.
- Mean imputation is simple but shrinks variance — note that trade-off.
- Alternatives: median (robust to outliers), forward-fill (time series), or a
  learned model.

## Why it matters for AI
Most estimators reject `NaN`/`None`. Imputation is often the first cell in every
training pipeline.
""",
            "examples": [
                {
                    "title": "Pandas fillna",
                    "language": "python",
                    "code": "import pandas as pd\ns = pd.Series([1.0, None, 3.0])\nprint(s.fillna(s.mean()).tolist())  # [1.0, 2.0, 3.0]",
                }
            ],
            "challenges": [
                {
                    "title": "Mean Imputation",
                    "description": (
                        "Implement `fill_missing(xs)`: replace every `None` in the list "
                        "with the mean of the non-None values, and return the new list. "
                        "Assume at least one value is present."
                    ),
                    "starter_code": "def fill_missing(xs):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Filter out None to compute the mean.", "Rebuild the list, substituting the mean for None."],
                    "solution_code": (
                        "def fill_missing(xs):\n"
                        "    present = [x for x in xs if x is not None]\n"
                        "    mean = sum(present) / len(present)\n"
                        "    return [mean if x is None else x for x in xs]\n"
                    ),
                    "test_cases": [
                        {"call": "fill_missing([1.0, None, 3.0])", "expected": "[1.0, 2.0, 3.0]"},
                        {"call": "fill_missing([None, 4.0, None, 8.0])", "expected": "[6.0, 4.0, 6.0, 8.0]"},
                        {"call": "fill_missing([5.0])", "expected": "[5.0]"},
                    ],
                }
            ],
        },
    ],
}
