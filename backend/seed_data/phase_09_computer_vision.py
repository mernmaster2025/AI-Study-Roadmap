"""Phase 9 — Computer Vision."""

PHASE = {
    "phase_number": 9,
    "title": "Computer Vision",
    "description": (
        "Images are just arrays of numbers. Build the core CV operations — "
        "grayscale conversion, convolution, pooling — and learn how CNN output "
        "shapes are computed."
    ),
    "estimated_hours": 22,
    "lessons": [
        {
            "title": "Images as Arrays",
            "description": "Pixels, channels, and converting colour to grayscale.",
            "estimated_minutes": 30,
            "content_markdown": """
# Images as Arrays

A colour image is a grid of pixels, each with red, green and blue channels
(0–255). To convert to **grayscale** we take a weighted sum that matches human
brightness perception (the eye is most sensitive to green):

$$ \\text{gray} = 0.299R + 0.587G + 0.114B $$

```python
def grayscale(r, g, b):
    return 0.299 * r + 0.587 * g + 0.114 * b
```

## Key ideas
- Shape convention: `(height, width, channels)`.
- Green dominates the luminance weights.
- Grayscale drops 3 channels to 1 — less data, often enough signal.

## Why it matters for AI
Many classic CV pipelines start in grayscale, and understanding pixels-as-arrays
is the bridge from images to tensors.
""",
            "examples": [
                {
                    "title": "White and black endpoints",
                    "language": "python",
                    "code": "def gray(r,g,b): return 0.299*r + 0.587*g + 0.114*b\nprint(gray(255,255,255))  # 255.0\nprint(gray(0,0,0))        # 0.0",
                }
            ],
            "challenges": [
                {
                    "title": "Grayscale a Pixel",
                    "description": "Implement `grayscale(r, g, b)` using the luminance weights 0.299, 0.587, 0.114.",
                    "starter_code": "def grayscale(r, g, b):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["It's a weighted sum.", "Green has the largest weight."],
                    "solution_code": "def grayscale(r, g, b):\n    return 0.299 * r + 0.587 * g + 0.114 * b\n",
                    "test_cases": [
                        {"call": "grayscale(255, 255, 255)", "expected": "255.0"},
                        {"call": "grayscale(0, 0, 0)", "expected": "0.0"},
                        {"call": "round(grayscale(255, 0, 0), 3)", "expected": "76.245"},
                    ],
                }
            ],
        },
        {
            "title": "Convolution",
            "description": "Slide a kernel over a signal to detect local patterns.",
            "estimated_minutes": 35,
            "content_markdown": """
# Convolution

A **convolution** (technically cross-correlation, as used in deep learning)
slides a small **kernel** across the input, computing a dot product at each
position. In 1-D with 'valid' padding, the output has length
`len(signal) - len(kernel) + 1`.

```python
def convolve1d(signal, kernel):
    k = len(kernel)
    return [sum(signal[i + j] * kernel[j] for j in range(k))
            for i in range(len(signal) - k + 1)]
```

## Key ideas
- The kernel's weights define what pattern it responds to (edges, blurs…).
- 'Valid' padding shrinks the output; 'same' padding keeps its size.
- CNNs *learn* the kernel weights instead of hand-designing them.

## Why it matters for AI
Convolution is the core operation of every CNN — the reason they excel at images
while using far fewer parameters than dense nets.
""",
            "examples": [
                {
                    "title": "An averaging (blur) kernel",
                    "language": "python",
                    "code": "signal = [2, 4, 6, 8]\nkernel = [0.5, 0.5]           # average of each adjacent pair\n# outputs: [3.0, 5.0, 7.0]",
                }
            ],
            "challenges": [
                {
                    "title": "1-D Convolution",
                    "description": (
                        "Implement `convolve1d(signal, kernel)` with 'valid' padding: "
                        "output[i] = sum of signal[i+j]*kernel[j]. Output length is "
                        "len(signal) - len(kernel) + 1."
                    ),
                    "starter_code": "def convolve1d(signal, kernel):\n    pass\n",
                    "difficulty": "hard",
                    "hints": ["Slide the kernel start i from 0 to len(signal)-len(kernel).", "At each i, dot the window with the kernel."],
                    "solution_code": (
                        "def convolve1d(signal, kernel):\n"
                        "    k = len(kernel)\n"
                        "    return [sum(signal[i + j] * kernel[j] for j in range(k))\n"
                        "            for i in range(len(signal) - k + 1)]\n"
                    ),
                    "test_cases": [
                        {"call": "convolve1d([1, 2, 3, 4], [1, 0])", "expected": "[1, 2, 3]"},
                        {"call": "convolve1d([1, 2, 3], [1, 1])", "expected": "[3, 5]"},
                        {"call": "convolve1d([2, 4, 6, 8], [0.5, 0.5])", "expected": "[3.0, 5.0, 7.0]"},
                    ],
                }
            ],
        },
        {
            "title": "Max Pooling",
            "description": "Downsample by keeping the strongest response per window.",
            "estimated_minutes": 25,
            "content_markdown": """
# Max Pooling

**Max pooling** shrinks a signal by taking the maximum over non-overlapping
windows. It keeps the strongest activation and discards precise location, adding
a little translation invariance.

```python
def max_pool1d(signal, size):
    return [max(signal[i:i + size]) for i in range(0, len(signal), size)]
```

## Key ideas
- Reduces resolution → fewer computations downstream.
- 'Max' keeps peaks; 'average' pooling smooths instead.
- Common window/stride is 2, halving the length.

## Why it matters for AI
Pooling layers are how CNNs progressively compress spatial detail into abstract
features.
""",
            "examples": [
                {
                    "title": "Halving with a window of 2",
                    "language": "python",
                    "code": "signal = [1, 3, 2, 4]\nprint([max(signal[i:i+2]) for i in range(0, 4, 2)])  # [3, 4]",
                }
            ],
            "challenges": [
                {
                    "title": "1-D Max Pooling",
                    "description": (
                        "Implement `max_pool1d(signal, size)`: split into non-overlapping "
                        "windows of `size` and return the max of each. Assume len is "
                        "divisible by size."
                    ),
                    "starter_code": "def max_pool1d(signal, size):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Step through the signal in strides of `size`.", "Take max of each window slice."],
                    "solution_code": (
                        "def max_pool1d(signal, size):\n"
                        "    return [max(signal[i:i + size]) for i in range(0, len(signal), size)]\n"
                    ),
                    "test_cases": [
                        {"call": "max_pool1d([1, 3, 2, 4], 2)", "expected": "[3, 4]"},
                        {"call": "max_pool1d([5, 1, 2, 9, 7, 3], 3)", "expected": "[5, 9]"},
                        {"call": "max_pool1d([1, 2, 3, 4], 4)", "expected": "[4]"},
                    ],
                }
            ],
        },
        {
            "title": "CNN Output Shapes",
            "description": "Predict a conv layer's output size from its hyperparameters.",
            "estimated_minutes": 25,
            "content_markdown": """
# CNN Output Shapes

For a 1-D conv (or one spatial dimension of a 2-D conv), the output size is:

$$ \\left\\lfloor \\frac{W - K + 2P}{S} \\right\\rfloor + 1 $$

where `W` = input size, `K` = kernel size, `P` = padding, `S` = stride.

```python
def conv_output_size(w, k, stride, padding):
    return (w - k + 2 * padding) // stride + 1
```

## Key ideas
- Padding adds border pixels so edges get covered ('same' padding).
- Stride > 1 downsamples, shrinking the output.
- Getting this wrong is the source of endless shape-mismatch errors.

## Why it matters for AI
You'll compute these by hand constantly when designing CNNs to make layers line
up before the classifier head.
""",
            "examples": [
                {
                    "title": "Same padding keeps the size",
                    "language": "python",
                    "code": "def out(w,k,s,p): return (w - k + 2*p)//s + 1\nprint(out(5, 3, 1, 1))  # 5 — 'same' padding\nprint(out(5, 3, 1, 0))  # 3 — 'valid'",
                }
            ],
            "challenges": [
                {
                    "title": "Convolution Output Size",
                    "description": "Implement `conv_output_size(w, k, stride, padding)` using the standard formula.",
                    "starter_code": "def conv_output_size(w, k, stride, padding):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Numerator is w - k + 2*padding.", "Integer-divide by stride, then add 1."],
                    "solution_code": (
                        "def conv_output_size(w, k, stride, padding):\n"
                        "    return (w - k + 2 * padding) // stride + 1\n"
                    ),
                    "test_cases": [
                        {"call": "conv_output_size(5, 3, 1, 0)", "expected": "3"},
                        {"call": "conv_output_size(5, 3, 1, 1)", "expected": "5"},
                        {"call": "conv_output_size(7, 3, 2, 0)", "expected": "3"},
                    ],
                }
            ],
        },
    ],
}
