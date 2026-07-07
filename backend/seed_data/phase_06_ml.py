"""Phase 6 — Machine Learning Fundamentals."""

PHASE = {
    "phase_number": 6,
    "title": "Machine Learning Fundamentals",
    "description": (
        "Supervised learning end to end: split data, fit a model, descend the "
        "gradient, classify with logistic regression, and measure it honestly. "
        "Every core idea, implemented from scratch."
    ),
    "estimated_hours": 24,
    "lessons": [
        {
            "title": "Train / Test Split",
            "description": "Why you must evaluate on data the model never saw.",
            "estimated_minutes": 25,
            "content_markdown": """
# Train / Test Split

A model that memorises its training data can look perfect and still fail in the
wild. So we hold out a **test set** and only judge the model on it.

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
```

## Key ideas
- Typical split: 80% train / 20% test (plus a validation set for tuning).
- Never let test data influence training — that's **leakage**.
- Shuffle before splitting unless the data is a time series.

## Why it matters for AI
The gap between train and test performance *is* the definition of overfitting.
No held-out set means no trustworthy number.
""",
            "examples": [
                {
                    "title": "Splitting by index",
                    "language": "python",
                    "code": "data = [10, 20, 30, 40, 50]\ncut = int(len(data) * 0.8)  # 4\nprint(data[:cut], data[cut:])  # [10,20,30,40] [50]",
                }
            ],
            "challenges": [
                {
                    "title": "Train/Test Split",
                    "description": (
                        "Implement `train_test_split(data, train_ratio)` returning a tuple "
                        "`(train, test)` split at `int(len(data) * train_ratio)`, preserving "
                        "order."
                    ),
                    "starter_code": "def train_test_split(data, train_ratio):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Compute the cut index with int().", "Slice the list into two parts."],
                    "solution_code": (
                        "def train_test_split(data, train_ratio):\n"
                        "    cut = int(len(data) * train_ratio)\n"
                        "    return (data[:cut], data[cut:])\n"
                    ),
                    "test_cases": [
                        {"call": "train_test_split([1, 2, 3, 4, 5], 0.8)", "expected": "([1, 2, 3, 4], [5])"},
                        {"call": "train_test_split([1, 2, 3, 4], 0.5)", "expected": "([1, 2], [3, 4])"},
                        {"call": "train_test_split([], 0.8)", "expected": "([], [])"},
                    ],
                }
            ],
        },
        {
            "title": "Linear Regression & MSE",
            "description": "Fit a line and measure its error with mean squared error.",
            "estimated_minutes": 35,
            "content_markdown": """
# Linear Regression & MSE

Linear regression predicts `y = w·x + b`. We measure how wrong it is with
**mean squared error** — the average of squared residuals:

$$ \\text{MSE} = \\frac{1}{n}\\sum_i (y_i - \\hat y_i)^2 $$

```python
def mse(y_true, y_pred):
    n = len(y_true)
    return sum((t - p) ** 2 for t, p in zip(y_true, y_pred)) / n
```

## Key ideas
- Squaring punishes big errors more and keeps everything positive.
- MSE is in *squared* units; its root (RMSE) is back in original units.
- Minimising MSE is what "training" a regressor means.

## Why it matters for AI
MSE is the default loss for regression and a building block of many others.
It's also smooth, so gradient descent loves it.
""",
            "examples": [
                {
                    "title": "A perfect fit scores 0",
                    "language": "python",
                    "code": "y = [1, 2, 3]\nprint(sum((t - p) ** 2 for t, p in zip(y, y)) / len(y))  # 0.0",
                }
            ],
            "challenges": [
                {
                    "title": "Mean Squared Error",
                    "description": "Implement `mse(y_true, y_pred)` for two equal-length lists.",
                    "starter_code": "def mse(y_true, y_pred):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Pair values with zip.", "Average the squared differences."],
                    "solution_code": (
                        "def mse(y_true, y_pred):\n"
                        "    n = len(y_true)\n"
                        "    return sum((t - p) ** 2 for t, p in zip(y_true, y_pred)) / n\n"
                    ),
                    "test_cases": [
                        {"call": "mse([1, 2, 3], [1, 2, 3])", "expected": "0.0"},
                        {"call": "mse([1, 2, 3], [2, 2, 2])", "expected": "0.6666666666666666"},
                        {"call": "mse([0, 0], [3, 4])", "expected": "12.5"},
                    ],
                },
                {
                    "title": "Root Mean Squared Error",
                    "description": (
                        "Implement `rmse(y_true, y_pred)` = the square root of the mean "
                        "squared error, giving an error back in the original units."
                    ),
                    "starter_code": "import math\n\ndef rmse(y_true, y_pred):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Compute the MSE first.", "Return math.sqrt of it."],
                    "solution_code": (
                        "import math\n\n"
                        "def rmse(y_true, y_pred):\n"
                        "    n = len(y_true)\n"
                        "    mse = sum((t - p) ** 2 for t, p in zip(y_true, y_pred)) / n\n"
                        "    return math.sqrt(mse)\n"
                    ),
                    "test_cases": [
                        {"call": "rmse([1, 2, 3], [1, 2, 3])", "expected": "0.0"},
                        {"call": "rmse([0, 0], [3, 4])", "expected": "3.5355339059327378"},
                        {"call": "round(rmse([1, 2], [3, 4]), 4)", "expected": "2.0"},
                    ],
                },
            ],
        },
        {
            "title": "Gradient Descent",
            "description": "The optimisation loop that trains almost every model.",
            "estimated_minutes": 35,
            "content_markdown": """
# Gradient Descent

To minimise a loss, repeatedly step each parameter **against** its gradient:

$$ w \\leftarrow w - \\eta \\cdot \\nabla_w L $$

where `η` (eta) is the **learning rate**.

```python
w = 5.0
lr = 0.1
for _ in range(100):
    grad = 2 * w        # derivative of L = w^2
    w = w - lr * grad    # -> approaches 0, the minimum
```

## Key ideas
- The gradient points **uphill**; we subtract it to go downhill.
- Too-large `lr` overshoots/diverges; too-small crawls.
- One "step" updates every parameter once.

## Why it matters for AI
This four-line loop, scaled to billions of parameters, is how every neural
network learns.
""",
            "examples": [
                {
                    "title": "One step reduces the loss",
                    "language": "python",
                    "code": "w = 5.0\nw = w - 0.1 * (2 * w)  # grad of w^2 is 2w\nprint(w)  # 4.0",
                }
            ],
            "challenges": [
                {
                    "title": "Gradient Descent Step",
                    "description": (
                        "Implement `gd_step(w, grad, lr)` returning the updated parameter "
                        "`w - lr * grad`."
                    ),
                    "starter_code": "def gd_step(w, grad, lr):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["It's a single expression.", "Subtract lr * grad from w."],
                    "solution_code": "def gd_step(w, grad, lr):\n    return w - lr * grad\n",
                    "test_cases": [
                        {"call": "gd_step(5.0, 10.0, 0.1)", "expected": "4.0"},
                        {"call": "gd_step(0.0, 2.0, 0.5)", "expected": "-1.0"},
                        {"call": "gd_step(3.0, 0.0, 0.1)", "expected": "3.0"},
                    ],
                }
            ],
        },
        {
            "title": "Logistic Regression & Sigmoid",
            "description": "Squash a score into a probability for classification.",
            "estimated_minutes": 30,
            "content_markdown": """
# Logistic Regression & Sigmoid

For classification we need a **probability** in `(0, 1)`. The **sigmoid**
squashes any real number into that range:

$$ \\sigma(x) = \\frac{1}{1 + e^{-x}} $$

```python
import math
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

sigmoid(0)    # 0.5
sigmoid(2)    # 0.88...
```

## Key ideas
- `σ(0) = 0.5`; large positive → ~1, large negative → ~0.
- Logistic regression = sigmoid applied to `w·x + b`.
- Threshold the probability (e.g. at 0.5) to get a class label.

## Why it matters for AI
Sigmoid is the original neural-network activation and still the output for
binary classification.
""",
            "examples": [
                {
                    "title": "Probability to label",
                    "language": "python",
                    "code": "p = 0.73\nlabel = 1 if p >= 0.5 else 0\nprint(label)  # 1",
                }
            ],
            "challenges": [
                {
                    "title": "Sigmoid",
                    "description": "Implement `sigmoid(x)` = 1 / (1 + e^(-x)).",
                    "starter_code": "import math\n\ndef sigmoid(x):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Use math.exp.", "sigmoid(0) must equal 0.5."],
                    "solution_code": "import math\n\ndef sigmoid(x):\n    return 1 / (1 + math.exp(-x))\n",
                    "test_cases": [
                        {"call": "sigmoid(0)", "expected": "0.5"},
                        {"call": "round(sigmoid(2), 6)", "expected": "0.880797"},
                        {"call": "round(sigmoid(-2), 6)", "expected": "0.119203"},
                    ],
                }
            ],
        },
        {
            "title": "Classification Metrics",
            "description": "Accuracy, and why it isn't the whole story.",
            "estimated_minutes": 30,
            "content_markdown": """
# Classification Metrics

**Accuracy** is the fraction of predictions that are correct:

$$ \\text{accuracy} = \\frac{\\text{correct}}{\\text{total}} $$

```python
y_true = [1, 0, 1, 1]
y_pred = [1, 0, 0, 1]
acc = sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)  # 0.75
```

## Key ideas
- Accuracy misleads on **imbalanced** data (99% "no" → predict "no" always).
- Precision, recall, and F1 dig into the kinds of mistakes.
- Always compare against a trivial baseline.

## Why it matters for AI
Choosing the wrong metric hides real failures. Fraud, disease, and rare-event
models live and die by recall, not accuracy.
""",
            "examples": [
                {
                    "title": "Booleans sum as 1/0",
                    "language": "python",
                    "code": "print(sum([True, False, True]))  # 2 — True is 1, False is 0",
                }
            ],
            "challenges": [
                {
                    "title": "Accuracy",
                    "description": (
                        "Implement `accuracy(y_true, y_pred)` = fraction of matching "
                        "positions. Return 0.0 for empty input."
                    ),
                    "starter_code": "def accuracy(y_true, y_pred):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Count positions where t == p.", "Divide by the length; guard length 0."],
                    "solution_code": (
                        "def accuracy(y_true, y_pred):\n"
                        "    if not y_true:\n"
                        "        return 0.0\n"
                        "    correct = sum(1 for t, p in zip(y_true, y_pred) if t == p)\n"
                        "    return correct / len(y_true)\n"
                    ),
                    "test_cases": [
                        {"call": "accuracy([1, 0, 1, 1], [1, 0, 0, 1])", "expected": "0.75"},
                        {"call": "accuracy([1, 1, 1], [1, 1, 1])", "expected": "1.0"},
                        {"call": "accuracy([], [])", "expected": "0.0"},
                    ],
                }
            ],
        },
    ],
}
