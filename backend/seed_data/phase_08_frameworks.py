"""Phase 8 — Deep Learning Frameworks (PyTorch / TensorFlow)."""

PHASE = {
    "phase_number": 8,
    "title": "Deep Learning Frameworks",
    "description": (
        "PyTorch and TensorFlow give you tensors, autograd, and reusable layers. "
        "We map each framework idea to the plain-Python mechanics you already "
        "built, so the API stops being magic."
    ),
    "estimated_hours": 20,
    "lessons": [
        {
            "title": "Tensors & Reshaping",
            "description": "The n-dimensional array at the centre of every framework.",
            "estimated_minutes": 30,
            "content_markdown": """
# Tensors & Reshaping

A **tensor** is an n-dimensional array (scalars, vectors, matrices, and up).
**Reshaping** reinterprets the same values under a new shape without changing
their order.

```python
import torch
t = torch.arange(6)          # tensor([0,1,2,3,4,5])
t.reshape(2, 3)              # [[0,1,2],[3,4,5]]
```

## Key ideas
- Total element count must stay constant: `2 * 3 == 6`.
- Reshaping is a *view* — cheap, no data copied.
- `flatten()` collapses everything back to 1-D (common before a dense layer).

## Why it matters for AI
Batching images `(N, C, H, W)`, flattening for a classifier head, and aligning
shapes for matmul are all reshapes. Shape errors are the #1 framework paper-cut.
""",
            "examples": [
                {
                    "title": "Flatten then reshape",
                    "language": "python",
                    "code": "flat = [0, 1, 2, 3, 4, 5]\nrows, cols = 2, 3\nprint([flat[r*cols:(r+1)*cols] for r in range(rows)])  # [[0,1,2],[3,4,5]]",
                }
            ],
            "challenges": [
                {
                    "title": "Reshape a Flat List",
                    "description": (
                        "Implement `reshape(flat, rows, cols)` returning a list of `rows` "
                        "lists each of length `cols`, filled row-major. Assume "
                        "`rows * cols == len(flat)`."
                    ),
                    "starter_code": "def reshape(flat, rows, cols):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Row r spans indices r*cols .. (r+1)*cols.", "Slice the flat list per row."],
                    "solution_code": (
                        "def reshape(flat, rows, cols):\n"
                        "    return [flat[r * cols:(r + 1) * cols] for r in range(rows)]\n"
                    ),
                    "test_cases": [
                        {"call": "reshape([1, 2, 3, 4, 5, 6], 2, 3)", "expected": "[[1, 2, 3], [4, 5, 6]]"},
                        {"call": "reshape([1, 2, 3, 4], 4, 1)", "expected": "[[1], [2], [3], [4]]"},
                        {"call": "reshape([1, 2], 1, 2)", "expected": "[[1, 2]]"},
                    ],
                }
            ],
        },
        {
            "title": "Autograd & the Chain Rule",
            "description": "How frameworks compute gradients through many operations.",
            "estimated_minutes": 35,
            "content_markdown": """
# Autograd & the Chain Rule

**Automatic differentiation** works by the **chain rule**: the derivative of
composed functions is the *product* of the local derivatives.

$$ \\frac{dy}{dx} = \\frac{dy}{du}\\cdot\\frac{du}{dx} $$

```python
# y = f(g(x));  dy/dx = f'(g(x)) * g'(x)
locals_ = [2.0, 3.0, 4.0]     # local derivatives along the chain
grad = 1.0
for d in locals_:
    grad *= d                   # 24.0
```

## Key ideas
- Backprop multiplies local gradients from output back to each input.
- Frameworks record every op in a graph, then replay it in reverse.
- `loss.backward()` in PyTorch is exactly this product, automated.

## Why it matters for AI
Autograd is why you never hand-derive gradients anymore. Understanding the chain
rule explains vanishing/exploding gradients (products of many small/large terms).
""",
            "examples": [
                {
                    "title": "PyTorch does the product for you",
                    "language": "python",
                    "code": "import torch\nx = torch.tensor(2.0, requires_grad=True)\ny = (x ** 2) * 3      # dy/dx = 6x = 12 at x=2\ny.backward()\nprint(x.grad)         # tensor(12.)",
                }
            ],
            "challenges": [
                {
                    "title": "Chain Rule",
                    "description": (
                        "Implement `chain_rule(local_grads)` returning the product of a "
                        "list of local derivatives. An empty list yields 1.0."
                    ),
                    "starter_code": "def chain_rule(local_grads):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Start an accumulator at 1.0.", "Multiply through the list."],
                    "solution_code": (
                        "def chain_rule(local_grads):\n"
                        "    grad = 1.0\n"
                        "    for d in local_grads:\n"
                        "        grad *= d\n"
                        "    return grad\n"
                    ),
                    "test_cases": [
                        {"call": "chain_rule([2, 3, 4])", "expected": "24.0"},
                        {"call": "chain_rule([0.5, 0.5])", "expected": "0.25"},
                        {"call": "chain_rule([])", "expected": "1.0"},
                    ],
                }
            ],
        },
        {
            "title": "Counting Model Parameters",
            "description": "Size a network from its layer widths.",
            "estimated_minutes": 25,
            "content_markdown": """
# Counting Model Parameters

Between two dense layers of sizes `a` and `b` there are `a*b` weights plus `b`
biases. Summing over consecutive layers gives the model's parameter count.

```python
sizes = [3, 4, 2]
# (3*4 + 4) + (4*2 + 2) = 16 + 10 = 26
```

## Key ideas
- Each connection is one weight; each neuron in a layer adds one bias.
- Parameter count drives memory and (roughly) capacity.
- `sum(p.numel() for p in model.parameters())` is the PyTorch one-liner.

## Why it matters for AI
"How big is this model?" is a parameter count. It's how we compare a 7B vs 70B
LLM and budget GPU memory.
""",
            "examples": [
                {
                    "title": "PyTorch parameter count",
                    "language": "python",
                    "code": "import torch.nn as nn\nmodel = nn.Linear(3, 4)   # 3*4 weights + 4 biases = 16\nprint(sum(p.numel() for p in model.parameters()))  # 16",
                }
            ],
            "challenges": [
                {
                    "title": "Count Parameters",
                    "description": (
                        "Implement `count_params(layer_sizes)`: for a fully-connected net "
                        "with the given layer widths, return total weights + biases. A "
                        "single-layer list has 0 parameters."
                    ),
                    "starter_code": "def count_params(layer_sizes):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Walk consecutive pairs (a, b).", "Each pair contributes a*b + b."],
                    "solution_code": (
                        "def count_params(layer_sizes):\n"
                        "    total = 0\n"
                        "    for a, b in zip(layer_sizes, layer_sizes[1:]):\n"
                        "        total += a * b + b\n"
                        "    return total\n"
                    ),
                    "test_cases": [
                        {"call": "count_params([3, 4, 2])", "expected": "26"},
                        {"call": "count_params([2, 1])", "expected": "3"},
                        {"call": "count_params([10])", "expected": "0"},
                    ],
                }
            ],
        },
        {
            "title": "The Training Loop",
            "description": "Average the batch losses to report an epoch's loss.",
            "estimated_minutes": 25,
            "content_markdown": """
# The Training Loop

Frameworks don't hide the loop — you write it. Each **epoch** iterates over
mini-batches, and you report the epoch's loss as the **average** of the batch
losses.

```python
for epoch in range(epochs):
    batch_losses = []
    for xb, yb in loader:
        optimizer.zero_grad()
        loss = criterion(model(xb), yb)
        loss.backward()
        optimizer.step()
        batch_losses.append(loss.item())
    print(sum(batch_losses) / len(batch_losses))
```

## Key ideas
- `zero_grad → forward → loss → backward → step` is the sacred five-step order.
- Report the **mean** batch loss, not the last one.
- Watch train vs validation loss to catch overfitting.

## Why it matters for AI
This loop is the same for a 2-parameter regressor and a giant Transformer. Master
its shape once.
""",
            "examples": [
                {
                    "title": "Mean of batch losses",
                    "language": "python",
                    "code": "losses = [0.9, 0.7, 0.5, 0.3]\nprint(sum(losses) / len(losses))  # 0.6",
                }
            ],
            "challenges": [
                {
                    "title": "Epoch Loss",
                    "description": (
                        "Implement `epoch_loss(batch_losses)` returning the mean of the "
                        "list. Return 0.0 for an empty list."
                    ),
                    "starter_code": "def epoch_loss(batch_losses):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Guard the empty case.", "Mean = sum / count."],
                    "solution_code": (
                        "def epoch_loss(batch_losses):\n"
                        "    if not batch_losses:\n"
                        "        return 0.0\n"
                        "    return sum(batch_losses) / len(batch_losses)\n"
                    ),
                    "test_cases": [
                        {"call": "epoch_loss([1.0, 2.0, 3.0])", "expected": "2.0"},
                        {"call": "epoch_loss([0.9, 0.7, 0.5, 0.3])", "expected": "0.6"},
                        {"call": "epoch_loss([])", "expected": "0.0"},
                    ],
                }
            ],
        },
    ],
}
