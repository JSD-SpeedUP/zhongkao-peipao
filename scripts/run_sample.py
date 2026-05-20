from __future__ import annotations

import argparse
import json
from pathlib import Path


REQUIRED_FIELDS = {"id", "type", "subject", "stem", "answer", "tags", "difficulty", "source", "evidence"}
SUPPORTED_TYPES = {"choice", "fill_blank", "short_answer", "table", "image", "matching"}
SAFE_SOURCE_KINDS = {"self_made", "public_domain"}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def validate_question(question: dict) -> list[str]:
    problems: list[str] = []
    missing = sorted(REQUIRED_FIELDS - set(question))
    if missing:
        problems.append(f"missing fields: {', '.join(missing)}")

    q_type = question.get("type")
    if q_type not in SUPPORTED_TYPES:
        problems.append(f"unsupported type: {q_type}")

    source = question.get("source") or {}
    if source.get("kind") not in SAFE_SOURCE_KINDS:
        problems.append("red light: source must be self_made or public_domain")

    evidence = question.get("evidence") or {}
    if evidence.get("public_safe") is not True:
        problems.append("red light: evidence.public_safe must be true")

    if q_type == "matching":
        matching = question.get("matching") or {}
        if not matching.get("left") or not matching.get("right") or not matching.get("pairs"):
            problems.append("matching question needs left, right, and pairs")

    if q_type == "image" and not question.get("images"):
        problems.append("image question needs images")

    return problems


def exp_for(question: dict, config: dict) -> int:
    exp_config = config.get("exp", {})
    base = int(exp_config.get("base_per_question", 10))
    multiplier = int(exp_config.get("difficulty_multiplier", 5))
    review_bonus = int(exp_config.get("review_bonus", 3))
    difficulty = int(question.get("difficulty", 1))
    return base + difficulty * multiplier + review_bonus


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the public Zhongkao Peipao sample workflow.")
    parser.add_argument("questions", nargs="?", default="examples/sample-questions.json")
    parser.add_argument("--config", default="config.example.json")
    args = parser.parse_args()

    questions_path = Path(args.questions)
    config_path = Path(args.config)

    questions = load_json(questions_path)
    config = load_json(config_path)

    total_exp = 0
    red_lights: list[str] = []

    print("Zhongkao Peipao public sample")
    print(f"questions: {len(questions)}")

    for question in questions:
        problems = validate_question(question)
        q_exp = exp_for(question, config)
        total_exp += q_exp
        status = "RED" if problems else "OK"
        print(f"- {question.get('id')}: {status}, exp={q_exp}, tags={','.join(question.get('tags', []))}")
        for problem in problems:
            red_lights.append(f"{question.get('id')}: {problem}")

    print(f"total_exp: {total_exp}")

    if red_lights:
        print("red_lights:")
        for item in red_lights:
            print(f"- {item}")
        return 1

    print("evidence_loop: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
