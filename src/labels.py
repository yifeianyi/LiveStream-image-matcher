"""Validation for the label-record JSON contract."""

from __future__ import annotations

from datetime import date
from pathlib import PurePosixPath, PureWindowsPath
from typing import Any, Mapping


ALLOWED_FIELDS = {"image_id", "path", "session_id", "date"}
REQUIRED_FIELDS = ALLOWED_FIELDS


def _fail(line_number: int, field: str, message: str) -> None:
    raise ValueError(f"line {line_number}, field {field!r}: {message}")


def _is_safe_relative_path(value: str) -> bool:
    """Return whether value is a non-empty, platform-independent relative path."""
    if not value or "\x00" in value:
        return False

    # Check both syntaxes so validation has the same result across operating systems.
    windows_path = PureWindowsPath(value)
    posix_path = PurePosixPath(value.replace("\\", "/"))
    if windows_path.is_absolute() or windows_path.drive:
        return False
    if posix_path.is_absolute():
        return False

    components = value.replace("\\", "/").split("/")
    return ".." not in components


def _validate_date(value: Any, line_number: int) -> None:
    if value is None:
        return
    if not isinstance(value, str):
        _fail(line_number, "date", "must be a YYYY-MM-DD string or null")
    try:
        parsed = date.fromisoformat(value)
    except ValueError:
        _fail(line_number, "date", "must be a valid YYYY-MM-DD date or null")
    if parsed.isoformat() != value:
        _fail(line_number, "date", "must use the exact YYYY-MM-DD format")


def validate_label_record(record: Mapping[str, Any], line_number: int) -> Mapping[str, Any]:
    """Validate one label record and return it unchanged.

    ``line_number`` is included in every error so JSONL callers can locate the
    invalid row. This function does not access the image path or any database.
    """
    if not isinstance(record, Mapping):
        raise ValueError(f"line {line_number}: record must be a JSON object")

    unknown_fields = set(record) - ALLOWED_FIELDS
    if unknown_fields:
        field = sorted(unknown_fields)[0]
        _fail(line_number, field, "unknown field")

    missing_fields = REQUIRED_FIELDS - set(record)
    if missing_fields:
        field = sorted(missing_fields)[0]
        _fail(line_number, field, "required field is missing")

    image_id = record["image_id"]
    if not isinstance(image_id, str) or not image_id:
        _fail(line_number, "image_id", "must be a non-empty string")

    path = record["path"]
    if not isinstance(path, str) or not _is_safe_relative_path(path):
        _fail(line_number, "path", "must be a non-empty safe relative path without '..'")

    session_id = record["session_id"]
    if session_id is not None and not isinstance(session_id, str):
        _fail(line_number, "session_id", "must be a string or null")

    _validate_date(record["date"], line_number)
    return record
