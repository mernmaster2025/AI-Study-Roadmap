"""Phase 11 — Large Language Models & Generative AI."""

PHASE = {
    "phase_number": 11,
    "title": "LLMs & Generative AI",
    "description": (
        "The machinery behind modern LLMs: softmax, scaled dot-product attention, "
        "temperature sampling, and embedding retrieval for RAG — each reduced to "
        "the core computation you can implement yourself."
    ),
    "estimated_hours": 26,
    "lessons": [
        {
            "title": "Softmax",
            "description": "Turn a vector of scores into a probability distribution.",
            "estimated_minutes": 30,
            "content_markdown": """
# Softmax

**Softmax** converts a vector of real scores (logits) into probabilities that
are positive and sum to 1:

$$ \\text{softmax}(z)_i = \\frac{e^{z_i}}{\\sum_j e^{z_j}} $$

```python
import math
def softmax(z):
    m = max(z)                      # subtract max for numerical stability
    exps = [math.exp(x - m) for x in z]
    total = sum(exps)
    return [e / total for e in exps]
```

## Key ideas
- Subtracting `max(z)` avoids `exp` overflow — mathematically identical.
- Larger logits get exponentially more probability mass.
- Equal logits → uniform distribution.

## Why it matters for AI
Softmax produces the next-token probability distribution at the output of every
LLM, and the attention weights inside it.
""",
            "examples": [
                {
                    "title": "Equal scores → uniform",
                    "language": "python",
                    "code": "import math\ndef softmax(z):\n    e=[math.exp(x-max(z)) for x in z]; s=sum(e)\n    return [x/s for x in e]\nprint(softmax([0, 0]))  # [0.5, 0.5]",
                }
            ],
            "challenges": [
                {
                    "title": "Softmax",
                    "description": (
                        "Implement `softmax(z)` returning a probability list that sums to 1. "
                        "Subtract the max for numerical stability."
                    ),
                    "starter_code": "import math\n\ndef softmax(z):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Exponentiate (x - max(z)).", "Divide each exp by the sum of exps."],
                    "solution_code": (
                        "import math\n\n"
                        "def softmax(z):\n"
                        "    m = max(z)\n"
                        "    exps = [math.exp(x - m) for x in z]\n"
                        "    total = sum(exps)\n"
                        "    return [e / total for e in exps]\n"
                    ),
                    "test_cases": [
                        {"call": "softmax([0, 0])", "expected": "[0.5, 0.5]"},
                        {"call": "softmax([1, 1, 1])", "expected": "[0.3333333333333333, 0.3333333333333333, 0.3333333333333333]"},
                        {"call": "[round(p, 5) for p in softmax([0, 1])]", "expected": "[0.26894, 0.73106]"},
                    ],
                }
            ],
        },
        {
            "title": "Scaled Dot-Product Attention",
            "description": "How a token decides which other tokens to attend to.",
            "estimated_minutes": 40,
            "content_markdown": """
# Scaled Dot-Product Attention

Attention scores a **query** against each **key** with a dot product, scales by
`1/sqrt(d)` to keep magnitudes stable, and softmaxes the scores into weights:

$$ \\text{weights} = \\text{softmax}\\!\\left(\\frac{q \\cdot k_i}{\\sqrt{d}}\\right) $$

```python
import math
def attention_weights(query, keys):
    d = len(query)
    scores = [sum(q * k for q, k in zip(query, key)) / math.sqrt(d) for key in keys]
    # ... softmax(scores)
```

## Key ideas
- The `1/sqrt(d)` scaling prevents huge dot products from saturating softmax.
- Weights are a probability distribution over the keys.
- The output is a weighted sum of value vectors (not computed here).

## Why it matters for AI
This single formula, stacked and parallelised, *is* the Transformer. Everything
GPT-style is built on it.
""",
            "examples": [
                {
                    "title": "Identical keys → equal attention",
                    "language": "python",
                    "code": "# query=[1,1], keys=[[1,1],[1,1]]  ->  equal scores  ->  weights [0.5, 0.5]",
                }
            ],
            "challenges": [
                {
                    "title": "Attention Weights",
                    "description": (
                        "Implement `attention_weights(query, keys)`: compute each key's "
                        "scaled dot-product score `dot(query, key)/sqrt(len(query))`, then "
                        "softmax the scores into a weight list."
                    ),
                    "starter_code": "import math\n\ndef attention_weights(query, keys):\n    pass\n",
                    "difficulty": "hard",
                    "hints": ["Scale each score by 1/sqrt(len(query)).", "Softmax the score list (subtract max for stability)."],
                    "solution_code": (
                        "import math\n\n"
                        "def attention_weights(query, keys):\n"
                        "    d = len(query)\n"
                        "    scores = [sum(q * k for q, k in zip(query, key)) / math.sqrt(d)\n"
                        "              for key in keys]\n"
                        "    m = max(scores)\n"
                        "    exps = [math.exp(s - m) for s in scores]\n"
                        "    total = sum(exps)\n"
                        "    return [e / total for e in exps]\n"
                    ),
                    "test_cases": [
                        {"call": "attention_weights([1, 1], [[1, 1], [1, 1]])", "expected": "[0.5, 0.5]"},
                        {"call": "[round(w, 4) for w in attention_weights([1, 0], [[1, 0], [0, 1]])]", "expected": "[0.6698, 0.3302]"},
                        {"call": "round(sum(attention_weights([2, 1], [[1, 1], [0, 2], [3, 0]])), 6)", "expected": "1.0"},
                    ],
                }
            ],
        },
        {
            "title": "Temperature Sampling",
            "description": "Control how random the model's next-token choice is.",
            "estimated_minutes": 30,
            "content_markdown": """
# Temperature Sampling

Before softmax, dividing the logits by a **temperature** `T` reshapes the
distribution:

$$ p_i = \\text{softmax}(z_i / T) $$

- `T < 1` sharpens (more confident, more deterministic).
- `T > 1` flattens (more random, more creative).
- `T → 0` approaches greedy argmax.

```python
def softmax_with_temperature(logits, T):
    scaled = [z / T for z in logits]
    # ... softmax(scaled)
```

## Key ideas
- Temperature is applied to logits, *before* the exponentials.
- It trades off coherence (low T) against diversity (high T).
- Often combined with top-k / top-p (nucleus) filtering.

## Why it matters for AI
Temperature is the main knob you turn when calling an LLM API to make it more
factual or more imaginative.
""",
            "examples": [
                {
                    "title": "High T flattens the distribution",
                    "language": "python",
                    "code": "# logits [2, 0]:\n#   T=0.5 -> sharper (e.g. [0.982, 0.018])\n#   T=2.0 -> flatter (e.g. [0.731, 0.269])",
                }
            ],
            "challenges": [
                {
                    "title": "Softmax with Temperature",
                    "description": (
                        "Implement `softmax_with_temperature(logits, T)`: divide the logits "
                        "by T, then apply a numerically-stable softmax."
                    ),
                    "starter_code": "import math\n\ndef softmax_with_temperature(logits, T):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Scale logits by 1/T first.", "Then softmax as usual."],
                    "solution_code": (
                        "import math\n\n"
                        "def softmax_with_temperature(logits, T):\n"
                        "    scaled = [z / T for z in logits]\n"
                        "    m = max(scaled)\n"
                        "    exps = [math.exp(s - m) for s in scaled]\n"
                        "    total = sum(exps)\n"
                        "    return [e / total for e in exps]\n"
                    ),
                    "test_cases": [
                        {"call": "softmax_with_temperature([0, 0], 1.0)", "expected": "[0.5, 0.5]"},
                        {"call": "[round(p, 4) for p in softmax_with_temperature([2, -2], 2.0)]", "expected": "[0.8808, 0.1192]"},
                        {"call": "round(sum(softmax_with_temperature([1, 2, 3], 0.7)), 6)", "expected": "1.0"},
                    ],
                }
            ],
        },
        {
            "title": "Embeddings & RAG Retrieval",
            "description": "Find the most relevant document by embedding similarity.",
            "estimated_minutes": 35,
            "content_markdown": """
# Embeddings & RAG Retrieval

**Retrieval-Augmented Generation (RAG)** grounds an LLM in your data: embed the
query and every document as vectors, then retrieve the document whose embedding
is **most similar** (highest cosine similarity) to the query.

```python
def nearest_neighbor(query, docs):
    best_i, best_sim = 0, float("-inf")
    for i, d in enumerate(docs):
        sim = cosine_similarity(query, d)
        if sim > best_sim:
            best_i, best_sim = i, sim
    return best_i
```

## Key ideas
- Embeddings place semantically similar text close together in vector space.
- Retrieval = nearest-neighbour search over those vectors.
- Real systems use approximate NN indexes (FAISS, HNSW) for millions of docs.

## Why it matters for AI
RAG is how chatbots answer from private/company data without retraining — the
dominant pattern for production LLM apps.
""",
            "examples": [
                {
                    "title": "Pick the closest document",
                    "language": "python",
                    "code": "# query=[1,0]; docs=[[0,1],[1,0],[1,1]]\n# similarities: 0.0, 1.0, 0.707  ->  best index = 1",
                }
            ],
            "challenges": [
                {
                    "title": "Nearest Neighbor Retrieval",
                    "description": (
                        "Implement `nearest_neighbor(query, docs)` returning the index of "
                        "the document (a list of vectors) with the highest cosine "
                        "similarity to `query`. On ties, return the earliest index."
                    ),
                    "starter_code": "import math\n\ndef nearest_neighbor(query, docs):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Reuse cosine similarity.", "Track the best index; use strict > so ties keep the earlier one."],
                    "solution_code": (
                        "import math\n\n"
                        "def _cos(a, b):\n"
                        "    dot = sum(x * y for x, y in zip(a, b))\n"
                        "    na = math.sqrt(sum(x * x for x in a))\n"
                        "    nb = math.sqrt(sum(y * y for y in b))\n"
                        "    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)\n\n"
                        "def nearest_neighbor(query, docs):\n"
                        "    best_i, best_sim = 0, float('-inf')\n"
                        "    for i, d in enumerate(docs):\n"
                        "        sim = _cos(query, d)\n"
                        "        if sim > best_sim:\n"
                        "            best_i, best_sim = i, sim\n"
                        "    return best_i\n"
                    ),
                    "test_cases": [
                        {"call": "nearest_neighbor([1, 0], [[0, 1], [1, 0], [1, 1]])", "expected": "1"},
                        {"call": "nearest_neighbor([1, 1], [[1, 0], [0, 1]])", "expected": "0"},
                        {"call": "nearest_neighbor([0, 2], [[2, 0], [0, 5]])", "expected": "1"},
                    ],
                }
            ],
        },
    ],
}
