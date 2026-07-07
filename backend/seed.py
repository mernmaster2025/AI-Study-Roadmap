"""Seed the database with Phase 1 (Python Fundamentals) content.

Run:  python seed.py
Idempotent — clears and re-inserts the seeded rows each run so you can iterate
on content. It does NOT delete users or their submissions.
"""
from sqlalchemy import delete, select

from app.database import Base, SessionLocal, engine
from app.models import Challenge, Lesson, Phase


def reset_content(db):
    # Order matters for FK integrity (challenges -> lessons -> phases).
    db.execute(delete(Challenge))
    db.execute(delete(Lesson))
    db.execute(delete(Phase))
    db.commit()


def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        reset_content(db)

        phase = Phase(
            phase_number=1,
            title="Python Fundamentals",
            description=(
                "Variables, data types, control flow, functions and collections — "
                "the foundation everything else in the roadmap builds on."
            ),
            estimated_hours=12,
            order=1,
        )
        db.add(phase)
        db.flush()  # assign phase.id

        # ---- Lesson 1 ----
        lesson1 = Lesson(
            phase_id=phase.id,
            lesson_number=1,
            title="Variables & Data Types",
            description="Store values and understand Python's core built-in types.",
            estimated_minutes=25,
            order=1,
            content_markdown=(
                "# Variables & Data Types\n\n"
                "A **variable** is a name bound to a value. Python is dynamically "
                "typed, so you don't declare types — the type comes from the value.\n\n"
                "```python\n"
                "name = \"Ada\"      # str\n"
                "age = 36           # int\n"
                "height = 1.68      # float\n"
                "is_admin = True    # bool\n"
                "```\n\n"
                "## Key ideas\n"
                "- Use `type(x)` to inspect a value's type.\n"
                "- Strings are immutable; you build new ones rather than editing in place.\n"
                "- `int` and `float` are numeric; mixing them yields a `float`.\n"
            ),
            examples=[
                {
                    "title": "Inspecting types",
                    "language": "python",
                    "code": "x = 42\nprint(type(x))       # <class 'int'>\nprint(type(3.14))    # <class 'float'>\nprint(type('hi'))    # <class 'str'>",
                },
                {
                    "title": "String formatting",
                    "language": "python",
                    "code": "name = 'Ada'\nage = 36\nprint(f'{name} is {age} years old')",
                },
            ],
        )
        db.add(lesson1)
        db.flush()

        db.add(
            Challenge(
                lesson_id=lesson1.id,
                title="Sum Two Numbers",
                description=(
                    "Implement a function `add(a, b)` that returns the sum of its "
                    "two arguments."
                ),
                starter_code="def add(a, b):\n    # Return the sum of a and b\n    pass\n",
                difficulty="easy",
                hints=["The `+` operator adds two numbers.", "Use `return`, not `print`."],
                solution_code="def add(a, b):\n    return a + b\n",
                order=1,
                test_cases=[
                    {"call": "add(2, 3)", "expected": "5"},
                    {"call": "add(-1, 1)", "expected": "0"},
                    {"call": "add(100, 250)", "expected": "350"},
                    {"call": "add(0, 0)", "expected": "0"},
                ],
            )
        )

        # ---- Lesson 2 ----
        lesson2 = Lesson(
            phase_id=phase.id,
            lesson_number=2,
            title="Control Flow & Loops",
            description="Branch with if/elif/else and repeat work with loops.",
            estimated_minutes=30,
            order=2,
            content_markdown=(
                "# Control Flow & Loops\n\n"
                "Programs make decisions with `if` and repeat work with loops.\n\n"
                "```python\n"
                "for i in range(3):\n"
                "    if i % 2 == 0:\n"
                "        print(i, 'even')\n"
                "    else:\n"
                "        print(i, 'odd')\n"
                "```\n\n"
                "## Key ideas\n"
                "- `range(n)` yields `0 .. n-1`.\n"
                "- `%` is the modulo (remainder) operator.\n"
                "- Accumulate results in a variable or list as you loop.\n"
            ),
            examples=[
                {
                    "title": "Summing a range",
                    "language": "python",
                    "code": "total = 0\nfor i in range(1, 6):\n    total += i\nprint(total)  # 15",
                }
            ],
        )
        db.add(lesson2)
        db.flush()

        db.add(
            Challenge(
                lesson_id=lesson2.id,
                title="FizzBuzz Value",
                description=(
                    "Implement `fizzbuzz(n)` that returns the string 'Fizz' if `n` is "
                    "divisible by 3, 'Buzz' if divisible by 5, 'FizzBuzz' if divisible "
                    "by both, and the number itself (as a string) otherwise."
                ),
                starter_code="def fizzbuzz(n):\n    # Return 'Fizz', 'Buzz', 'FizzBuzz', or str(n)\n    pass\n",
                difficulty="medium",
                hints=[
                    "Check divisibility by both 3 and 5 first.",
                    "`n % 3 == 0` tests divisibility by 3.",
                ],
                solution_code=(
                    "def fizzbuzz(n):\n"
                    "    if n % 15 == 0:\n"
                    "        return 'FizzBuzz'\n"
                    "    if n % 3 == 0:\n"
                    "        return 'Fizz'\n"
                    "    if n % 5 == 0:\n"
                    "        return 'Buzz'\n"
                    "    return str(n)\n"
                ),
                order=1,
                test_cases=[
                    {"call": "fizzbuzz(3)", "expected": "'Fizz'"},
                    {"call": "fizzbuzz(5)", "expected": "'Buzz'"},
                    {"call": "fizzbuzz(15)", "expected": "'FizzBuzz'"},
                    {"call": "fizzbuzz(7)", "expected": "'7'"},
                ],
            )
        )

        db.commit()

        phase_count = db.scalar(select(Phase.id))
        print("Seeded Phase 1 with 2 lessons and 2 challenges.")
        print(f"  Phase id: {phase.id}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
