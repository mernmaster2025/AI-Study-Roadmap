"""Full 12-phase AI study curriculum.

Each phase lives in its own module exposing a ``PHASE`` dict with this shape::

    {
      "phase_number": int,
      "title": str,
      "description": str,
      "estimated_hours": int,
      "lessons": [
        {
          "title": str,
          "description": str,
          "estimated_minutes": int,
          "content_markdown": str,
          "examples": [{"title": str, "language": str, "code": str}],
          "challenges": [
            {
              "title": str,
              "description": str,
              "starter_code": str,
              "difficulty": "easy" | "medium" | "hard",
              "hints": [str, ...],
              "solution_code": str,
              # Each test evaluates ``call`` and compares (approx) to eval(expected).
              "test_cases": [{"call": str, "expected": str}, ...],
            },
            ...
          ],
        },
        ...
      ],
    }

``seed.py`` consumes ``PHASES`` and derives ordering from list position, so the
content modules never hard-code ``order`` fields.
"""
from seed_data import (
    phase_01_python,
    phase_02_dsa,
    phase_03_math,
    phase_04_data,
    phase_05_viz,
    phase_06_ml,
    phase_07_deep_learning,
    phase_08_frameworks,
    phase_09_computer_vision,
    phase_10_nlp,
    phase_11_llms,
    phase_12_production,
)

PHASES = [
    phase_01_python.PHASE,
    phase_02_dsa.PHASE,
    phase_03_math.PHASE,
    phase_04_data.PHASE,
    phase_05_viz.PHASE,
    phase_06_ml.PHASE,
    phase_07_deep_learning.PHASE,
    phase_08_frameworks.PHASE,
    phase_09_computer_vision.PHASE,
    phase_10_nlp.PHASE,
    phase_11_llms.PHASE,
    phase_12_production.PHASE,
]
