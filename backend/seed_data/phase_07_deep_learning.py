"""Phase 7 — Deep Learning Fundamentals."""

PHASE = {
    "phase_number": 7,
    "title": "Deep Learning Fundamentals",
    "description": (
        "Neurons, activations, forward propagation and loss — build a neural "
        "network's machinery by hand so the frameworks in Phase 8 feel obvious."
    ),
    "estimated_hours": 24,
    "lessons": [
        {
            "title": "The Perceptron",
            "description": "A single neuron: weighted sum, bias, and a threshold.",
            "estimated_minutes": 30,
            "content_markdown": """
# The Perceptron

A **perceptron** is one neuron. It computes a weighted sum of inputs, adds a
**bias**, and fires (`1`) if the result clears a threshold, else stays off (`0`).

$$ \\text{output} = \\begin{cases} 1 & w \\cdot x + b \\ge 0 \\\\ 0 & \\text{otherwise} \\end{cases} $$

```python
def perceptron(weights, inputs, bias):
    z = sum(w * x for w, x in zip(weights, inputs)) + bias
    return 1 if z >= 0 else 0
```

## Key ideas
- The weights say how much each input matters; the bias shifts the threshold.
- A single perceptron can only separate **linearly separable** data.
- Stacking neurons into layers removes that limitation.

## Why it matters for AI
Every unit in a deep net is this same weighted-sum-plus-activation. Understand
one neuron and you understand a billion of them.
""",
            "examples": [
                {
                    "title": "An AND gate as a perceptron",
                    "language": "python",
                    "code": "def perceptron(w, x, b):\n    return 1 if sum(wi*xi for wi,xi in zip(w,x)) + b >= 0 else 0\n\nprint(perceptron([1,1],[1,1],-1.5))  # 1 (1+1-1.5>=0)\nprint(perceptron([1,1],[1,0],-1.5))  # 0",
                }
            ],
            "challenges": [
                {
                    "title": "Perceptron Output",
                    "description": (
                        "Implement `perceptron(weights, inputs, bias)` returning 1 if "
                        "`dot(weights, inputs) + bias >= 0`, else 0."
                    ),
                    "starter_code": "def perceptron(weights, inputs, bias):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Compute the weighted sum with zip.", "Compare to zero with >=."],
                    "solution_code": (
                        "def perceptron(weights, inputs, bias):\n"
                        "    z = sum(w * x for w, x in zip(weights, inputs)) + bias\n"
                        "    return 1 if z >= 0 else 0\n"
                    ),
                    "test_cases": [
                        {"call": "perceptron([1, 1], [2, 3], -4)", "expected": "1"},
                        {"call": "perceptron([1, 1], [1, 1], -3)", "expected": "0"},
                        {"call": "perceptron([1], [0], 0)", "expected": "1"},
                    ],
                }
            ],
        },
        {
            "title": "Activation Functions (ReLU)",
            "description": "The non-linearity that lets deep nets learn complex shapes.",
            "estimated_minutes": 25,
            "content_markdown": """
# Activation Functions (ReLU)

Without a non-linear **activation**, stacking layers just makes another linear
function. **ReLU** (Rectified Linear Unit) is the modern default:

$$ \\text{ReLU}(x) = \\max(0, x) $$

```python
def relu(x):
    return x if x > 0 else 0
```

## Key ideas
- ReLU passes positives through and zeroes negatives.
- It's cheap, and its gradient is a clean 0 or 1 — good for deep nets.
- Sigmoid/tanh saturate (tiny gradients); ReLU mostly doesn't.

## Why it matters for AI
ReLU (and cousins like GELU) is in nearly every modern network, from CNNs to the
feed-forward blocks of Transformers.
""",
            "examples": [
                {
                    "title": "ReLU clips negatives",
                    "language": "python",
                    "code": "vals = [-3, -1, 0, 2, 5]\nprint([v if v > 0 else 0 for v in vals])  # [0, 0, 0, 2, 5]",
                }
            ],
            "challenges": [
                {
                    "title": "ReLU",
                    "description": "Implement `relu(x)` = max(0, x).",
                    "starter_code": "def relu(x):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Return x when positive, else 0.", "`max(0, x)` works too."],
                    "solution_code": "def relu(x):\n    return x if x > 0 else 0\n",
                    "test_cases": [
                        {"call": "relu(5)", "expected": "5"},
                        {"call": "relu(-3)", "expected": "0"},
                        {"call": "relu(0)", "expected": "0"},
                        {"call": "relu(2.5)", "expected": "2.5"},
                    ],
                }
            ],
        },
        {
            "title": "Forward Propagation",
            "description": "Push inputs through a dense layer of neurons.",
            "estimated_minutes": 35,
            "content_markdown": """
# Forward Propagation

A **dense layer** applies several neurons to the same inputs. Neuron `j` has its
own weight vector and bias; its output is `ReLU(w_j · x + b_j)`.

```python
def layer_forward(inputs, weights, biases):
    out = []
    for w, b in zip(weights, biases):
        z = sum(wi * xi for wi, xi in zip(w, inputs)) + b
        out.append(z if z > 0 else 0)   # ReLU
    return out
```

## Key ideas
- `weights` is a list of weight vectors, one per neuron.
- The layer turns an input vector into a new vector (the activations).
- Chaining layers = repeatedly calling this on the previous output.

## Why it matters for AI
The forward pass *is* inference. Training then measures its error and adjusts the
weights — but prediction is just forward propagation.
""",
            "examples": [
                {
                    "title": "One layer, three neurons",
                    "language": "python",
                    "code": "inputs = [1, 2]\nweights = [[1, 0], [0, 1], [1, 1]]\nbiases  = [0, 0, -5]\n# outputs: relu(1), relu(2), relu(-2) = [1, 2, 0]",
                }
            ],
            "challenges": [
                {
                    "title": "Dense Layer Forward Pass",
                    "description": (
                        "Implement `layer_forward(inputs, weights, biases)` where `weights` "
                        "is a list of weight vectors (one per neuron). Return the list of "
                        "ReLU-activated outputs."
                    ),
                    "starter_code": "def layer_forward(inputs, weights, biases):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Loop over (weight_vector, bias) pairs.", "Each output is relu(dot(w, inputs) + b)."],
                    "solution_code": (
                        "def layer_forward(inputs, weights, biases):\n"
                        "    out = []\n"
                        "    for w, b in zip(weights, biases):\n"
                        "        z = sum(wi * xi for wi, xi in zip(w, inputs)) + b\n"
                        "        out.append(z if z > 0 else 0)\n"
                        "    return out\n"
                    ),
                    "test_cases": [
                        {"call": "layer_forward([1, 2], [[1, 0], [0, 1], [1, 1]], [0, 0, -5])", "expected": "[1, 2, 0]"},
                        {"call": "layer_forward([1, 1], [[1, 1]], [-3])", "expected": "[0]"},
                        {"call": "layer_forward([2, 2], [[0.5, 0.5]], [1])", "expected": "[3.0]"},
                    ],
                }
            ],
        },
        {
            "title": "Loss: Binary Cross-Entropy",
            "description": "How wrong a probability prediction is.",
            "estimated_minutes": 30,
            "content_markdown": """
# Loss: Binary Cross-Entropy

For a probability prediction `p` and true label `y ∈ {0, 1}`, **binary
cross-entropy** measures the surprise:

$$ L = -\\big(y \\log p + (1-y)\\log(1-p)\\big) $$

```python
import math
def bce(y, p):
    return -(y * math.log(p) + (1 - y) * math.log(1 - p))
```

## Key ideas
- Confident and right → loss near 0; confident and wrong → loss explodes.
- It pairs naturally with the sigmoid output.
- In practice `p` is clipped away from exactly 0 or 1 to avoid `log(0)`.

## Why it matters for AI
Cross-entropy is *the* classification loss, from logistic regression to the
next-token prediction that trains large language models.
""",
            "examples": [
                {
                    "title": "Being right is cheap",
                    "language": "python",
                    "code": "import math\nprint(round(-math.log(0.99), 4))  # 0.01 — tiny loss when confident & correct",
                }
            ],
            "challenges": [
                {
                    "title": "Binary Cross-Entropy",
                    "description": (
                        "Implement `bce(y, p)` for a single example, with `y` in {0, 1} and "
                        "`0 < p < 1`."
                    ),
                    "starter_code": "import math\n\ndef bce(y, p):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Use math.log.", "L = -(y*log(p) + (1-y)*log(1-p))."],
                    "solution_code": (
                        "import math\n\n"
                        "def bce(y, p):\n"
                        "    return -(y * math.log(p) + (1 - y) * math.log(1 - p))\n"
                    ),
                    "test_cases": [
                        {"call": "round(bce(1, 0.9), 5)", "expected": "0.10536"},
                        {"call": "round(bce(0, 0.1), 5)", "expected": "0.10536"},
                        {"call": "round(bce(1, 0.5), 5)", "expected": "0.69315"},
                    ],
                }
            ],
        },
    ],
}
