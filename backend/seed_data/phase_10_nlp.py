"""Phase 10 — Natural Language Processing."""

PHASE = {
    "phase_number": 10,
    "title": "Natural Language Processing",
    "description": (
        "Turn text into numbers a model can use: tokenize, weight terms, measure "
        "similarity, and build n-grams. The classic NLP toolkit, from scratch."
    ),
    "estimated_hours": 22,
    "lessons": [
        {
            "title": "Tokenization",
            "description": "Split raw text into clean, lowercase tokens.",
            "estimated_minutes": 30,
            "content_markdown": """
# Tokenization

**Tokenization** breaks text into units (tokens). A simple word tokenizer
lowercases the text and splits on anything that isn't a letter or digit.

```python
def tokenize(text):
    cleaned = "".join(c.lower() if c.isalnum() else " " for c in text)
    return cleaned.split()

tokenize("Hello, World!")   # ['hello', 'world']
```

## Key ideas
- Lowercasing collapses "The" and "the" into one token.
- Punctuation is usually stripped (or kept as its own token).
- Modern LLMs use **subword** tokenizers (BPE) instead of whole words.

## Why it matters for AI
Tokenization is step 0 of every NLP pipeline. Bad tokenization silently caps a
model's quality.
""",
            "examples": [
                {
                    "title": "Punctuation becomes a separator",
                    "language": "python",
                    "code": "text = 'AI & ML: cool!'\ncleaned = ''.join(c.lower() if c.isalnum() else ' ' for c in text)\nprint(cleaned.split())  # ['ai', 'ml', 'cool']",
                }
            ],
            "challenges": [
                {
                    "title": "Word Tokenizer",
                    "description": (
                        "Implement `tokenize(text)`: lowercase, treat any non-alphanumeric "
                        "character as a separator, and return the list of tokens."
                    ),
                    "starter_code": "def tokenize(text):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["`c.isalnum()` tests letters/digits.", "Replace non-alnum with spaces, then `.split()`."],
                    "solution_code": (
                        "def tokenize(text):\n"
                        "    cleaned = ''.join(c.lower() if c.isalnum() else ' ' for c in text)\n"
                        "    return cleaned.split()\n"
                    ),
                    "test_cases": [
                        {"call": "tokenize('Hello, World!')", "expected": "['hello', 'world']"},
                        {"call": "tokenize('AI & ML')", "expected": "['ai', 'ml']"},
                        {"call": "tokenize('')", "expected": "[]"},
                    ],
                }
            ],
        },
        {
            "title": "Term Frequency",
            "description": "Represent a document by how often each word appears.",
            "estimated_minutes": 30,
            "content_markdown": """
# Term Frequency

**Term frequency (TF)** turns a token list into a vector: each token's count
divided by the total number of tokens (its relative frequency).

$$ \\text{tf}(t) = \\frac{\\text{count}(t)}{\\text{total tokens}} $$

```python
def term_frequency(tokens):
    n = len(tokens)
    tf = {}
    for t in tokens:
        tf[t] = tf.get(t, 0) + 1 / n
    return tf
```

## Key ideas
- TF is the "bag of words" model — order is discarded.
- Normalising by length lets you compare documents of different sizes.
- TF-IDF extends this by down-weighting words common across *all* documents.

## Why it matters for AI
Bag-of-words / TF-IDF vectors powered NLP for decades and are still strong,
interpretable baselines before you reach for embeddings.
""",
            "examples": [
                {
                    "title": "Counts to frequencies",
                    "language": "python",
                    "code": "tokens = ['a', 'b', 'a']\nn = len(tokens)\ntf = {}\nfor t in tokens:\n    tf[t] = tf.get(t, 0) + 1/n\nprint(tf)  # {'a': 0.666..., 'b': 0.333...}",
                }
            ],
            "challenges": [
                {
                    "title": "Term Frequency",
                    "description": (
                        "Implement `term_frequency(tokens)` returning a dict mapping each "
                        "token to count/total. Empty input returns an empty dict."
                    ),
                    "starter_code": "def term_frequency(tokens):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Count occurrences first.", "Divide each count by the total token count."],
                    "solution_code": (
                        "def term_frequency(tokens):\n"
                        "    n = len(tokens)\n"
                        "    if n == 0:\n"
                        "        return {}\n"
                        "    counts = {}\n"
                        "    for t in tokens:\n"
                        "        counts[t] = counts.get(t, 0) + 1\n"
                        "    return {t: c / n for t, c in counts.items()}\n"
                    ),
                    "test_cases": [
                        {"call": "term_frequency(['a', 'b', 'a'])", "expected": "{'a': 0.6666666666666666, 'b': 0.3333333333333333}"},
                        {"call": "term_frequency(['x', 'x', 'x', 'x'])", "expected": "{'x': 1.0}"},
                        {"call": "term_frequency([])", "expected": "{}"},
                    ],
                }
            ],
        },
        {
            "title": "Cosine Similarity",
            "description": "Measure how similar two vectors are by their angle.",
            "estimated_minutes": 30,
            "content_markdown": """
# Cosine Similarity

**Cosine similarity** compares two vectors by the cosine of the angle between
them — ignoring magnitude, focusing on direction:

$$ \\cos(a, b) = \\frac{a \\cdot b}{\\lVert a\\rVert\\,\\lVert b\\rVert} $$

Range: `-1` (opposite) to `1` (identical direction).

```python
import math
def cosine_similarity(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return 0.0 if na == 0 or nb == 0 else dot / (na * nb)
```

## Key ideas
- Length-independent: `[1,1]` and `[2,2]` are perfectly similar (`1.0`).
- The workhorse metric for comparing embeddings.
- A zero vector has no direction → define similarity as 0.

## Why it matters for AI
Semantic search, RAG retrieval, and recommendation all rank items by cosine
similarity of their embedding vectors.
""",
            "examples": [
                {
                    "title": "Direction, not size",
                    "language": "python",
                    "code": "import math\ndef cos(a,b):\n    d=sum(x*y for x,y in zip(a,b))\n    return d/(math.sqrt(sum(x*x for x in a))*math.sqrt(sum(y*y for y in b)))\nprint(cos([1,1],[2,2]))  # 1.0",
                }
            ],
            "challenges": [
                {
                    "title": "Cosine Similarity",
                    "description": (
                        "Implement `cosine_similarity(a, b)` for two equal-length vectors. "
                        "If either vector is all zeros, return 0.0."
                    ),
                    "starter_code": "import math\n\ndef cosine_similarity(a, b):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Compute dot product and both norms.", "Guard against a zero norm."],
                    "solution_code": (
                        "import math\n\n"
                        "def cosine_similarity(a, b):\n"
                        "    dot = sum(x * y for x, y in zip(a, b))\n"
                        "    na = math.sqrt(sum(x * x for x in a))\n"
                        "    nb = math.sqrt(sum(y * y for y in b))\n"
                        "    if na == 0 or nb == 0:\n"
                        "        return 0.0\n"
                        "    return dot / (na * nb)\n"
                    ),
                    "test_cases": [
                        {"call": "cosine_similarity([1, 0], [1, 0])", "expected": "1.0"},
                        {"call": "cosine_similarity([1, 0], [0, 1])", "expected": "0.0"},
                        {"call": "cosine_similarity([1, 1], [2, 2])", "expected": "1.0"},
                        {"call": "cosine_similarity([0, 0], [1, 1])", "expected": "0.0"},
                    ],
                }
            ],
        },
        {
            "title": "N-grams",
            "description": "Capture local word order with sliding windows.",
            "estimated_minutes": 25,
            "content_markdown": """
# N-grams

An **n-gram** is a contiguous run of `n` tokens. They add a little word-order
information that bag-of-words throws away.

```python
def ngrams(tokens, n):
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]

ngrams(["the", "cat", "sat"], 2)   # [('the','cat'), ('cat','sat')]
```

## Key ideas
- Bigrams (`n=2`) and trigrams (`n=3`) are the most common.
- When `n > len(tokens)`, there are no n-grams (empty list).
- Bigger `n` captures more context but explodes the vocabulary.

## Why it matters for AI
N-gram language models predicted the next word long before neural nets, and the
idea survives in tokenizer statistics and evaluation metrics like BLEU.
""",
            "examples": [
                {
                    "title": "Bigrams of a sentence",
                    "language": "python",
                    "code": "toks = ['i', 'love', 'ai']\nprint([tuple(toks[i:i+2]) for i in range(len(toks)-1)])\n# [('i','love'), ('love','ai')]",
                }
            ],
            "challenges": [
                {
                    "title": "N-grams",
                    "description": (
                        "Implement `ngrams(tokens, n)` returning a list of n-token tuples "
                        "in order. If `n` exceeds the token count, return an empty list."
                    ),
                    "starter_code": "def ngrams(tokens, n):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Windows start at 0 .. len(tokens)-n.", "Wrap each slice in tuple()."],
                    "solution_code": (
                        "def ngrams(tokens, n):\n"
                        "    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]\n"
                    ),
                    "test_cases": [
                        {"call": "ngrams(['a', 'b', 'c'], 2)", "expected": "[('a', 'b'), ('b', 'c')]"},
                        {"call": "ngrams(['a', 'b', 'c'], 1)", "expected": "[('a',), ('b',), ('c',)]"},
                        {"call": "ngrams(['a'], 2)", "expected": "[]"},
                    ],
                }
            ],
        },
    ],
}
