"""Phase 5 — Data Visualization."""

PHASE = {
    "phase_number": 5,
    "title": "Data Visualization",
    "description": (
        "Turn numbers into pictures with Matplotlib and Seaborn. We focus on the "
        "computations behind the charts — binning, correlation, scaling — so your "
        "plots tell the truth."
    ),
    "estimated_hours": 12,
    "lessons": [
        {
            "title": "Histograms & Binning",
            "description": "See a distribution's shape by counting values into bins.",
            "estimated_minutes": 30,
            "content_markdown": """
# Histograms & Binning

A **histogram** splits the data range into equal-width **bins** and counts how
many values land in each. It's the fastest way to see skew, gaps, and outliers.

```python
import matplotlib.pyplot as plt
plt.hist(data, bins=10)
plt.show()
```

## Key ideas
- Bin width = `(max - min) / k`.
- The value equal to `max` belongs in the **last** bin (right edge inclusive).
- Too few bins hide structure; too many make noise. Try a few.

## Why it matters for AI
Before modelling, plot every feature's histogram. Long tails, spikes at 0, and
"impossible" values jump out immediately.
""",
            "examples": [
                {
                    "title": "Bin edges by hand",
                    "language": "python",
                    "code": "data = [1, 2, 3, 4]\nlo, hi, k = min(data), max(data), 2\nwidth = (hi - lo) / k  # 1.5\nprint(width)",
                }
            ],
            "challenges": [
                {
                    "title": "Histogram Counts",
                    "description": (
                        "Implement `histogram(data, k)`: split the range [min, max] into "
                        "`k` equal-width bins and return a list of `k` counts. Values equal "
                        "to the max go in the last bin. If all values are equal, put them "
                        "all in bin 0."
                    ),
                    "starter_code": "def histogram(data, k):\n    pass\n",
                    "difficulty": "hard",
                    "hints": ["width = (max - min) / k; guard width == 0.", "index = int((x - lo) / width), clamped to k-1."],
                    "solution_code": (
                        "def histogram(data, k):\n"
                        "    lo, hi = min(data), max(data)\n"
                        "    counts = [0] * k\n"
                        "    width = (hi - lo) / k\n"
                        "    if width == 0:\n"
                        "        counts[0] = len(data)\n"
                        "        return counts\n"
                        "    for x in data:\n"
                        "        idx = int((x - lo) / width)\n"
                        "        if idx >= k:\n"
                        "            idx = k - 1\n"
                        "        counts[idx] += 1\n"
                        "    return counts\n"
                    ),
                    "test_cases": [
                        {"call": "histogram([1, 2, 3, 4], 2)", "expected": "[2, 2]"},
                        {"call": "histogram([1, 1, 1], 3)", "expected": "[3, 0, 0]"},
                        {"call": "histogram([0, 1, 2, 3, 4, 5], 3)", "expected": "[2, 2, 2]"},
                    ],
                }
            ],
        },
        {
            "title": "Correlation",
            "description": "Quantify how two variables move together.",
            "estimated_minutes": 30,
            "content_markdown": """
# Correlation

The **Pearson correlation** `r` measures linear association between two
variables, from `-1` (perfect opposite) through `0` (none) to `+1` (perfect
same direction).

$$ r = \\frac{\\sum (x_i-\\bar x)(y_i-\\bar y)}{\\sqrt{\\sum (x_i-\\bar x)^2}\\,\\sqrt{\\sum (y_i-\\bar y)^2}} $$

## Key ideas
- `r` captures *linear* structure only — a U-shape can have `r ≈ 0`.
- Correlation is not causation.
- A correlation **heatmap** across all features reveals redundancy.

## Why it matters for AI
Highly correlated features are often redundant. Spotting them early trims models
and reduces overfitting.
""",
            "examples": [
                {
                    "title": "Seaborn heatmap (conceptual)",
                    "language": "python",
                    "code": "import seaborn as sns\n# sns.heatmap(df.corr(), annot=True)\n# bright cells = strongly correlated feature pairs",
                }
            ],
            "challenges": [
                {
                    "title": "Pearson Correlation",
                    "description": (
                        "Implement `correlation(x, y)` for two equal-length lists. Return "
                        "Pearson's r. If either variable has zero variance, return 0.0."
                    ),
                    "starter_code": "def correlation(x, y):\n    pass\n",
                    "difficulty": "hard",
                    "hints": ["Center both lists by subtracting their means.", "r = sum(dx*dy) / (sqrt(sum dx^2) * sqrt(sum dy^2))."],
                    "solution_code": (
                        "import math\n\n"
                        "def correlation(x, y):\n"
                        "    n = len(x)\n"
                        "    mx = sum(x) / n\n"
                        "    my = sum(y) / n\n"
                        "    dx = [xi - mx for xi in x]\n"
                        "    dy = [yi - my for yi in y]\n"
                        "    num = sum(a * b for a, b in zip(dx, dy))\n"
                        "    den = math.sqrt(sum(a * a for a in dx)) * math.sqrt(sum(b * b for b in dy))\n"
                        "    if den == 0:\n"
                        "        return 0.0\n"
                        "    return num / den\n"
                    ),
                    "test_cases": [
                        {"call": "round(correlation([1, 2, 3], [2, 4, 6]), 6)", "expected": "1.0"},
                        {"call": "round(correlation([1, 2, 3], [6, 4, 2]), 6)", "expected": "-1.0"},
                        {"call": "correlation([1, 2, 3], [5, 5, 5])", "expected": "0.0"},
                    ],
                }
            ],
        },
        {
            "title": "Feature Scaling for Plots",
            "description": "Rescale to [0, 1] so charts and colour maps compare fairly.",
            "estimated_minutes": 25,
            "content_markdown": """
# Feature Scaling for Plots

**Min-max scaling** maps values into `[0, 1]`:

$$ x' = \\frac{x - \\min}{\\max - \\min} $$

It's what heatmaps and colour bars use so every feature shares one colour scale.

```python
xs = [10, 20, 30]
lo, hi = min(xs), max(xs)
scaled = [(x - lo) / (hi - lo) for x in xs]   # [0.0, 0.5, 1.0]
```

## Key ideas
- Min-max is sensitive to outliers (one huge value squashes the rest).
- Unlike standardization, the output range is bounded to `[0, 1]`.
- If `max == min`, the feature is constant — map it to all zeros.

## Why it matters for AI
Beyond plots, min-max scaling is a standard preprocessing step for models
(and image pixels, which are scaled from 0–255 to 0–1).
""",
            "examples": [
                {
                    "title": "Pixel scaling",
                    "language": "python",
                    "code": "pixels = [0, 128, 255]\nprint([p / 255 for p in pixels])  # [0.0, 0.502, 1.0]",
                }
            ],
            "challenges": [
                {
                    "title": "Min-Max Scale",
                    "description": (
                        "Implement `minmax_scale(xs)` mapping values to [0, 1]. If all "
                        "values are equal, return a list of zeros of the same length."
                    ),
                    "starter_code": "def minmax_scale(xs):\n    pass\n",
                    "difficulty": "easy",
                    "hints": ["Find min and max once.", "Guard the max == min case."],
                    "solution_code": (
                        "def minmax_scale(xs):\n"
                        "    lo, hi = min(xs), max(xs)\n"
                        "    if hi == lo:\n"
                        "        return [0.0 for _ in xs]\n"
                        "    return [(x - lo) / (hi - lo) for x in xs]\n"
                    ),
                    "test_cases": [
                        {"call": "minmax_scale([10, 20, 30])", "expected": "[0.0, 0.5, 1.0]"},
                        {"call": "minmax_scale([5, 5, 5])", "expected": "[0.0, 0.0, 0.0]"},
                        {"call": "minmax_scale([-1, 0, 1])", "expected": "[0.0, 0.5, 1.0]"},
                    ],
                }
            ],
        },
    ],
}
