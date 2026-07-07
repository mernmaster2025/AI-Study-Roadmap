"""Phase 3 — Math for AI."""

PHASE = {
    "phase_number": 3,
    "title": "Math for AI",
    "description": (
        "Linear algebra, probability, statistics and calculus — implemented in "
        "pure Python so the formulas stop being abstract. This is the language "
        "models are written in."
    ),
    "estimated_hours": 20,
    "lessons": [
        {
            "title": "Vectors & the Dot Product",
            "description": "Vectors as lists of numbers, and the operation at the heart of every neural net.",
            "estimated_minutes": 35,
            "content_markdown": """
# Vectors & the Dot Product

A **vector** is just an ordered list of numbers: `[3, 4]`. The **dot product**
multiplies matching components and sums them:

$$ a \\cdot b = \\sum_i a_i b_i $$

```python
a = [1, 2, 3]
b = [4, 5, 6]
dot = sum(x * y for x, y in zip(a, b))   # 1*4 + 2*5 + 3*6 = 32
```

## Key ideas
- The dot product measures how much two vectors point the same way.
- A vector's **length** (norm) is `sqrt(dot(v, v))`.
- Zip pairs up components: `zip([1,2],[3,4]) -> (1,3),(2,4)`.

## Why it matters for AI
A single neuron computes `dot(weights, inputs) + bias`. Attention scores,
similarity search, and embeddings are all dot products at scale.
""",
            "examples": [
                {
                    "title": "Vector norm",
                    "language": "python",
                    "code": "import math\nv = [3, 4]\nprint(math.sqrt(sum(x * x for x in v)))  # 5.0",
                }
            ],
            "challenges": [
                {
                    "title": "Dot Product",
                    "description": "Implement `dot(a, b)`, the dot product of two equal-length vectors (lists).",
                    "starter_code": "def dot(a, b):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Pair components with `zip(a, b)`.", "Sum the products."],
                    "solution_code": "def dot(a, b):\n    return sum(x * y for x, y in zip(a, b))\n",
                    "test_cases": [
                        {"call": "dot([1, 2, 3], [4, 5, 6])", "expected": "32"},
                        {"call": "dot([1, 0], [0, 1])", "expected": "0"},
                        {"call": "dot([2.0, 2.0], [0.5, 0.5])", "expected": "2.0"},
                    ],
                }
            ],
        },
        {
            "title": "Matrices & Multiplication",
            "description": "Grids of numbers and the matmul that powers every dense layer.",
            "estimated_minutes": 40,
            "content_markdown": """
# Matrices & Multiplication

A **matrix** is a list of rows. Multiplying an (m×n) matrix `A` by an (n×p)
matrix `B` gives an (m×p) matrix where entry `(i, j)` is the dot product of
row `i` of A and column `j` of B.

```python
A = [[1, 2],
     [3, 4]]
B = [[5, 6],
     [7, 8]]
# (A @ B)[0][0] = 1*5 + 2*7 = 19
```

## Key ideas
- Inner dimensions must match: (m×**n**)·(**n**×p).
- Column `j` of B is `[row[j] for row in B]`.
- Order matters: `A·B != B·A` in general.

## Why it matters for AI
`output = inputs @ weights` is the forward pass of a linear layer. GPUs exist
largely to do matmul fast.
""",
            "examples": [
                {
                    "title": "Extracting a column",
                    "language": "python",
                    "code": "B = [[5, 6], [7, 8]]\ncol0 = [row[0] for row in B]\nprint(col0)  # [5, 7]",
                }
            ],
            "challenges": [
                {
                    "title": "Matrix Multiply",
                    "description": (
                        "Implement `matmul(A, B)` for two matrices (lists of rows) with "
                        "compatible shapes. Return the product as a list of rows."
                    ),
                    "starter_code": "def matmul(A, B):\n    pass\n",
                    "difficulty": "hard",
                    "hints": ["Result shape is len(A) x len(B[0]).", "Entry (i,j) = sum over k of A[i][k]*B[k][j]."],
                    "solution_code": (
                        "def matmul(A, B):\n"
                        "    n = len(B)\n"
                        "    p = len(B[0])\n"
                        "    return [[sum(A[i][k] * B[k][j] for k in range(n))\n"
                        "             for j in range(p)]\n"
                        "            for i in range(len(A))]\n"
                    ),
                    "test_cases": [
                        {"call": "matmul([[1, 2], [3, 4]], [[5, 6], [7, 8]])", "expected": "[[19, 22], [43, 50]]"},
                        {"call": "matmul([[1, 0], [0, 1]], [[9, 8], [7, 6]])", "expected": "[[9, 8], [7, 6]]"},
                        {"call": "matmul([[2]], [[3]])", "expected": "[[6]]"},
                    ],
                }
            ],
        },
        {
            "title": "Statistics: Mean, Variance, Std",
            "description": "Summarise data with its centre and spread.",
            "estimated_minutes": 30,
            "content_markdown": """
# Statistics: Mean, Variance, Std

The **mean** is the average; **variance** is the average squared distance from
the mean; **standard deviation** is its square root (back in the original units).

$$ \\mu = \\frac{1}{n}\\sum_i x_i \\qquad \\sigma^2 = \\frac{1}{n}\\sum_i (x_i - \\mu)^2 $$

```python
xs = [2, 4, 4, 4, 5, 5, 7, 9]
mean = sum(xs) / len(xs)                       # 5.0
var  = sum((x - mean) ** 2 for x in xs) / len(xs)  # 4.0
```

## Key ideas
- This is the **population** variance (divide by `n`). Sample variance divides
  by `n-1`.
- Std has the same units as the data; variance is squared units.

## Why it matters for AI
Standardizing features (subtract mean, divide by std) is one of the most common
preprocessing steps and often decides whether a model trains well.
""",
            "examples": [
                {
                    "title": "Standardizing a value (z-score)",
                    "language": "python",
                    "code": "mean, std = 5.0, 2.0\nx = 9\nprint((x - mean) / std)  # 2.0 (2 std above the mean)",
                }
            ],
            "challenges": [
                {
                    "title": "Population Standard Deviation",
                    "description": (
                        "Implement `std(xs)`: the population standard deviation of a "
                        "non-empty list of numbers (divide the variance by n)."
                    ),
                    "starter_code": "def std(xs):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Compute the mean first.", "Variance = mean of squared deviations; std = sqrt(variance)."],
                    "solution_code": (
                        "import math\n\n"
                        "def std(xs):\n"
                        "    mean = sum(xs) / len(xs)\n"
                        "    var = sum((x - mean) ** 2 for x in xs) / len(xs)\n"
                        "    return math.sqrt(var)\n"
                    ),
                    "test_cases": [
                        {"call": "std([2, 4, 4, 4, 5, 5, 7, 9])", "expected": "2.0"},
                        {"call": "std([1, 1, 1, 1])", "expected": "0.0"},
                        {"call": "round(std([1, 2, 3, 4, 5]), 4)", "expected": "1.4142"},
                    ],
                }
            ],
        },
        {
            "title": "Calculus: Gradients Numerically",
            "description": "The derivative as a slope — and how to estimate it with arithmetic.",
            "estimated_minutes": 35,
            "content_markdown": """
# Calculus: Gradients Numerically

A **derivative** is the slope of a function — how fast its output changes as you
nudge its input. We can approximate it with a tiny step `h`:

$$ f'(x) \\approx \\frac{f(x+h) - f(x-h)}{2h} $$

```python
def deriv(f, x, h=1e-5):
    return (f(x + h) - f(x - h)) / (2 * h)

deriv(lambda x: x ** 2, 3)   # ~6.0  (since d/dx x^2 = 2x)
```

## Key ideas
- The **central difference** above is more accurate than a one-sided step.
- Gradient = the vector of partial derivatives for multi-input functions.
- Too-small `h` causes floating-point noise; `1e-5` is a good default.

## Why it matters for AI
Training = follow the gradient of the loss downhill. Frameworks compute
gradients automatically (autograd), but numeric gradients are how you *check*
them.
""",
            "examples": [
                {
                    "title": "Slope of sin at 0 is 1",
                    "language": "python",
                    "code": "import math\nh = 1e-5\nprint((math.sin(0 + h) - math.sin(0 - h)) / (2 * h))  # ~1.0",
                }
            ],
            "challenges": [
                {
                    "title": "Numerical Derivative",
                    "description": (
                        "Implement `numerical_derivative(f, x, h=1e-5)` using the central "
                        "difference formula. `f` is a single-argument function."
                    ),
                    "starter_code": "def numerical_derivative(f, x, h=1e-5):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Evaluate f at x+h and x-h.", "Divide the difference by 2h."],
                    "solution_code": (
                        "def numerical_derivative(f, x, h=1e-5):\n"
                        "    return (f(x + h) - f(x - h)) / (2 * h)\n"
                    ),
                    "test_cases": [
                        {"call": "round(numerical_derivative(lambda x: x * x, 3), 3)", "expected": "6.0"},
                        {"call": "round(numerical_derivative(lambda x: 2 * x + 1, 10), 3)", "expected": "2.0"},
                        {"call": "round(numerical_derivative(lambda x: x ** 3, 2), 2)", "expected": "12.0"},
                    ],
                }
            ],
        },
    ],
}
