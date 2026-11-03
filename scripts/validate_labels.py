"""Validate the sample label JSONL file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

# Allow direct execution from the repository root.
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from src.labels import validate_label_record


def validate_label_file(path: Path) -> int:
    seen_image_ids: set[str] = set()
    errors: list[str] = []

    try:
        with path.open("r", encoding="utf-8") as handle:
            for line_number, raw_line in enumerate(handle, start=1):
                if not raw_line.strip():
                    errors.append(f"line {line_number}: expected one JSON object")
                    continue
                try:
                    record: Any = json.loads(raw_line)
                    validate_label_record(record, line_number)
                    image_id = record["image_id"]
                    if image_id in seen_image_ids:
                        errors.append(
                            f"line {line_number}, field 'image_id': duplicate value {image_id!r}"
                        )
                    else:
                        seen_image_ids.add(image_id)
                except (json.JSONDecodeError, ValueError) as exc:
                    errors.append(f"{exc}")
    except OSError as exc:
        print(f"无法读取 {path}: {exc}", file=sys.stderr)
        return 2

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"校验失败：{len(errors)} 个错误", file=sys.stderr)
        return 1

    print(f"校验通过：{path}（{len(seen_image_ids)} 条记录）")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="校验标签 JSONL 文件")
    parser.add_argument(
        "labels",
        nargs="?",
        type=Path,
        default=Path("data/sample/labels.jsonl"),
        help="JSONL 标签文件路径（默认：data/sample/labels.jsonl）",
    )
    args = parser.parse_args()
    return validate_label_file(args.labels)


if __name__ == "__main__":
    raise SystemExit(main())
