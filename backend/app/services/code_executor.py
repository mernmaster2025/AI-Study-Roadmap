"""Run user-submitted Python and grade it against a challenge's test cases.

======================================================================
SECURITY WARNING
======================================================================
This executor runs untrusted code in a subprocess with only a wall-clock
timeout. That is fine for LOCAL DEVELOPMENT of this slice, but it is NOT a
real sandbox: the code can read/write files, open sockets, and spin the CPU
up to the timeout. Before exposing this to real users, run each submission
inside a locked-down boundary — a Docker container with no network, dropped
capabilities, a read-only FS and a memory cap; nsjail/firejail; or move
execution to the browser with Pyodide. Keep the harness contract below; just
swap where it runs.
======================================================================

Test-case contract
-------------------
Each challenge stores ``test_cases`` as a list of objects:

    {"call": "add(2, 3)", "expected": "5"}

The harness runs the learner's code, then for each case evaluates ``call``
and compares it (``==``) to ``eval(expected)``. Using a call expression rather
than a fixed ``main(...)`` signature lets each challenge name its own function.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path

from app.config import get_settings

settings = get_settings()

_SENTINEL = "___TEST_RESULTS_JSON___"

_HARNESS_TEMPLATE = '''\
import json as _json
import math as _math

def _approx_equal(a, b):
    """Compare results, tolerating float rounding, recursively into containers."""
    if isinstance(a, bool) or isinstance(b, bool):
        return a is b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return _math.isclose(a, b, rel_tol=1e-6, abs_tol=1e-9)
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_approx_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_approx_equal(a[k], b[k]) for k in a)
    return a == b

# ---- learner code ----
{user_code}
# ---- end learner code ----

_tests = _json.loads({tests_literal!r})
_results = []
for _i, _t in enumerate(_tests):
    try:
        _actual = eval(_t["call"])
        _expected = eval(_t["expected"])
        _results.append({{
            "test_number": _i + 1,
            "passed": _approx_equal(_actual, _expected),
            "expected": repr(_expected),
            "actual": repr(_actual),
        }})
    except Exception as _e:  # noqa: BLE001 - report any failure to the learner
        _results.append({{
            "test_number": _i + 1,
            "passed": False,
            "error": "{{}}: {{}}".format(type(_e).__name__, _e),
        }})

print({sentinel!r} + _json.dumps(_results))
'''


def execute_with_tests(code: str, test_cases: list[dict]) -> dict:
    """Execute ``code`` and grade it against ``test_cases``.

    Returns a dict matching schemas.ExecuteCodeResponse.
    """
    result = {
        "output": "",
        "error": None,
        "test_results": [],
        "all_tests_passed": False,
        "execution_time": 0.0,
        "score": 0,
    }

    if len(code) > settings.max_code_length:
        result["error"] = "Submission exceeds the maximum allowed length."
        return result

    harness = _HARNESS_TEMPLATE.format(
        user_code=code,
        tests_literal=json.dumps(test_cases),
        sentinel=_SENTINEL,
    )

    start = time.time()
    tmp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(
            "w", suffix=".py", delete=False, encoding="utf-8"
        ) as fh:
            fh.write(harness)
            tmp_path = Path(fh.name)

        proc = subprocess.run(
            [sys.executable, "-I", str(tmp_path)],  # -I: isolated mode
            capture_output=True,
            text=True,
            timeout=settings.code_timeout_seconds,
        )

        stdout = proc.stdout
        if _SENTINEL in stdout:
            user_output, _, results_json = stdout.partition(_SENTINEL)
            result["output"] = user_output.rstrip("\n")
            try:
                result["test_results"] = json.loads(results_json)
            except json.JSONDecodeError:
                result["error"] = "Failed to parse test results."
        else:
            # Harness crashed before emitting results (usually a syntax/runtime
            # error in the learner's code) — surface stdout + stderr.
            result["output"] = stdout.rstrip("\n")
            result["error"] = (proc.stderr or "Execution failed.").strip()

        tests = result["test_results"]
        if tests:
            result["all_tests_passed"] = all(t.get("passed") for t in tests)
            result["score"] = 100 if result["all_tests_passed"] else 0

    except subprocess.TimeoutExpired:
        result["error"] = (
            f"Code execution timed out (> {settings.code_timeout_seconds}s)."
        )
    except Exception as exc:  # noqa: BLE001
        result["error"] = str(exc)
    finally:
        result["execution_time"] = round(time.time() - start, 4)
        if tmp_path is not None:
            tmp_path.unlink(missing_ok=True)

    return result
