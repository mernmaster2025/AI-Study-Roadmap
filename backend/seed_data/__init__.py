"""Curriculum content source.

The full 12-phase curriculum lives in ``curriculum.json`` (one object per phase)
and is loaded here as ``PHASES``. It was authored by a multi-agent workflow and
every challenge's ``solution_code`` is verified to pass its own ``test_cases``.

Schema of each phase::

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
          "examples":   [{"title": str, "language": str, "code": str}],
          "challenges": [{"title","description","starter_code","difficulty",
                          "hints":[str],"solution_code",
                          "test_cases":[{"call","expected"}]}],
          "quiz":       [{"type","text","options":[str],"correct_answer",
                          "explanation"}]
        }
      ]
    }

To edit content, change ``curriculum.json`` and re-run ``python seed.py``.
"""
import json
from pathlib import Path

_DATA_FILE = Path(__file__).with_name("curriculum.json")

if not _DATA_FILE.exists():
    raise FileNotFoundError(
        f"{_DATA_FILE} is missing. The curriculum content is required to seed "
        "the database."
    )

PHASES = json.loads(_DATA_FILE.read_text(encoding="utf-8"))
