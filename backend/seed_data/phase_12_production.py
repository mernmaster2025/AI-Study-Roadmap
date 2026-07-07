"""Phase 12 — Production AI / MLOps."""

PHASE = {
    "phase_number": 12,
    "title": "Production AI & MLOps",
    "description": (
        "Shipping a model is the beginning, not the end. Batch for throughput, "
        "version releases, monitor for drift, and track error rates — the "
        "engineering that keeps AI alive in production."
    ),
    "estimated_hours": 20,
    "lessons": [
        {
            "title": "Batching for Throughput",
            "description": "Group requests so the GPU works efficiently.",
            "estimated_minutes": 25,
            "content_markdown": """
# Batching for Throughput

GPUs are fastest when they process many inputs at once. **Batching** groups a
stream of items into fixed-size chunks (the last chunk may be smaller).

```python
def batches(items, size):
    return [items[i:i + size] for i in range(0, len(items), size)]

batches([1, 2, 3, 4, 5], 2)   # [[1, 2], [3, 4], [5]]
```

## Key ideas
- Larger batches → higher throughput but more latency and memory.
- The final batch is often ragged — handle it, don't drop it.
- Dynamic batching groups requests that arrive close together in time.

## Why it matters for AI
Inference servers batch incoming requests to maximise GPU utilisation and cut
cost per prediction.
""",
            "examples": [
                {
                    "title": "Chunking a stream",
                    "language": "python",
                    "code": "items = list(range(7))\nprint([items[i:i+3] for i in range(0, 7, 3)])  # [[0,1,2],[3,4,5],[6]]",
                }
            ],
            "challenges": [
                {
                    "title": "Batch a List",
                    "description": (
                        "Implement `batches(items, size)` splitting the list into "
                        "consecutive chunks of at most `size`, preserving order."
                    ),
                    "starter_code": "def batches(items, size):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Step through indices in strides of `size`.", "Slice items[i:i+size] each step."],
                    "solution_code": (
                        "def batches(items, size):\n"
                        "    return [items[i:i + size] for i in range(0, len(items), size)]\n"
                    ),
                    "test_cases": [
                        {"call": "batches([1, 2, 3, 4, 5], 2)", "expected": "[[1, 2], [3, 4], [5]]"},
                        {"call": "batches([1, 2, 3], 3)", "expected": "[[1, 2, 3]]"},
                        {"call": "batches([], 4)", "expected": "[]"},
                    ],
                }
            ],
        },
        {
            "title": "Model Versioning",
            "description": "Parse semantic versions to track model releases.",
            "estimated_minutes": 25,
            "content_markdown": """
# Model Versioning

Ship models with **semantic versions** like `v2.3.1` = (major, minor, patch).
Parsing them into a tuple of integers lets you compare and sort releases.

```python
def parse_semver(s):
    s = s.lstrip("v")
    return tuple(int(part) for part in s.split("."))

parse_semver("v2.3.1")   # (2, 3, 1)
```

## Key ideas
- Tuples compare lexicographically: `(2,0,0) > (1,9,9)`.
- Bump **major** for breaking changes, **minor** for features, **patch** for fixes.
- Version every model artifact so you can roll back a bad deploy.

## Why it matters for AI
Reproducibility demands knowing exactly which model + data + code produced a
prediction. Versioning is the backbone of that audit trail.
""",
            "examples": [
                {
                    "title": "Comparing versions",
                    "language": "python",
                    "code": "print((2, 0, 0) > (1, 9, 9))  # True\nprint(tuple(int(p) for p in '1.4.2'.split('.')))  # (1, 4, 2)",
                }
            ],
            "challenges": [
                {
                    "title": "Parse Semantic Version",
                    "description": (
                        "Implement `parse_semver(s)` returning a tuple of ints from a "
                        "version string like 'v2.3.1' or '1.4.2' (strip a leading 'v')."
                    ),
                    "starter_code": "def parse_semver(s):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["`s.lstrip('v')` removes a leading v.", "Split on '.' and int() each part."],
                    "solution_code": (
                        "def parse_semver(s):\n"
                        "    s = s.lstrip('v')\n"
                        "    return tuple(int(part) for part in s.split('.'))\n"
                    ),
                    "test_cases": [
                        {"call": "parse_semver('1.4.2')", "expected": "(1, 4, 2)"},
                        {"call": "parse_semver('v2.0.1')", "expected": "(2, 0, 1)"},
                        {"call": "parse_semver('10.11.12')", "expected": "(10, 11, 12)"},
                    ],
                }
            ],
        },
        {
            "title": "Monitoring & Drift",
            "description": "Smooth a metric stream to spot changes over time.",
            "estimated_minutes": 30,
            "content_markdown": """
# Monitoring & Drift

Production inputs and model performance **drift** over time. A **moving average**
smooths a noisy metric stream so trends and regressions stand out.

```python
def moving_average(xs, w):
    return [sum(xs[i:i + w]) / w for i in range(len(xs) - w + 1)]

moving_average([1, 2, 3, 4], 2)   # [1.5, 2.5, 3.5]
```

## Key ideas
- A window of `w` produces `len(xs) - w + 1` outputs.
- Bigger windows smooth more but lag further behind changes.
- Alert when the smoothed metric crosses a threshold.

## Why it matters for AI
Dashboards track rolling accuracy, latency, and input statistics. Detecting drift
early is what triggers retraining before users notice.
""",
            "examples": [
                {
                    "title": "Smoothing noisy accuracy",
                    "language": "python",
                    "code": "acc = [0.90, 0.70, 0.92, 0.68]\nprint([sum(acc[i:i+2])/2 for i in range(3)])  # [0.8, 0.81, 0.8]",
                }
            ],
            "challenges": [
                {
                    "title": "Moving Average",
                    "description": (
                        "Implement `moving_average(xs, w)` returning the average of each "
                        "sliding window of width `w`. Output length is len(xs) - w + 1 "
                        "(empty if w > len(xs))."
                    ),
                    "starter_code": "def moving_average(xs, w):\n    pass\n",
                    "difficulty": "medium",
                    "hints": ["Windows start at 0 .. len(xs)-w.", "Average each slice xs[i:i+w]."],
                    "solution_code": (
                        "def moving_average(xs, w):\n"
                        "    return [sum(xs[i:i + w]) / w for i in range(len(xs) - w + 1)]\n"
                    ),
                    "test_cases": [
                        {"call": "moving_average([1, 2, 3, 4], 2)", "expected": "[1.5, 2.5, 3.5]"},
                        {"call": "moving_average([2, 4, 6], 3)", "expected": "[4.0]"},
                        {"call": "moving_average([1, 2], 3)", "expected": "[]"},
                    ],
                }
            ],
        },
        {
            "title": "Tracking Error Rates",
            "description": "Measure the fraction of failing requests.",
            "estimated_minutes": 25,
            "content_markdown": """
# Tracking Error Rates

A core SLO metric: the **error rate** is the fraction of requests that returned a
server error (HTTP status ≥ 500).

```python
def error_rate(statuses):
    if not statuses:
        return 0.0
    errors = sum(1 for s in statuses if s >= 500)
    return errors / len(statuses)
```

## Key ideas
- 5xx = server errors; 4xx = client errors (usually excluded from this metric).
- Error rate feeds SLOs, alerting, and automatic rollbacks.
- Watch it *per model version* to catch a bad deploy fast.

## Why it matters for AI
An ML service that silently 500s on 5% of traffic is broken. Error rate is one of
the first things you put on the on-call dashboard.
""",
            "examples": [
                {
                    "title": "Half the requests errored",
                    "language": "python",
                    "code": "statuses = [200, 200, 500, 503]\nprint(sum(1 for s in statuses if s >= 500) / len(statuses))  # 0.5",
                }
            ],
            "challenges": [
                {
                    "title": "Server Error Rate",
                    "description": (
                        "Implement `error_rate(statuses)` returning the fraction of HTTP "
                        "status codes that are >= 500. Empty input returns 0.0."
                    ),
                    "starter_code": "def error_rate(statuses):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Count statuses >= 500.", "Divide by total; guard the empty list."],
                    "solution_code": (
                        "def error_rate(statuses):\n"
                        "    if not statuses:\n"
                        "        return 0.0\n"
                        "    errors = sum(1 for s in statuses if s >= 500)\n"
                        "    return errors / len(statuses)\n"
                    ),
                    "test_cases": [
                        {"call": "error_rate([200, 200, 500, 503])", "expected": "0.5"},
                        {"call": "error_rate([200, 404, 301])", "expected": "0.0"},
                        {"call": "error_rate([])", "expected": "0.0"},
                    ],
                }
            ],
        },
    ],
}
