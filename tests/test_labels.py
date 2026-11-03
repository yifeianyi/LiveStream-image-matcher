"""Tests for the label data contract."""

import pytest

from src.labels import validate_label_record


VALID_RECORD = {
    "image_id": "img-0001",
    "path": "data/sample/live-a/frame-001.png",
    "session_id": "live-a",
    "date": "2026-05-18",
}


def test_confirmed_record_passes():
    assert validate_label_record(VALID_RECORD, 1) == VALID_RECORD


def test_explicit_null_label_is_preserved():
    record = {**VALID_RECORD, "session_id": None, "date": None}
    assert validate_label_record(record, 2)["date"] is None
    assert validate_label_record(record, 2)["session_id"] is None


def test_missing_required_key_is_rejected():
    record = {key: value for key, value in VALID_RECORD.items() if key != "date"}
    with pytest.raises(ValueError, match="date.*required"):
        validate_label_record(record, 3)


def test_invalid_date_is_rejected():
    with pytest.raises(ValueError, match="date"):
        validate_label_record({**VALID_RECORD, "date": "2026-02-30"}, 4)


def test_absolute_path_is_rejected():
    with pytest.raises(ValueError, match="path"):
        validate_label_record({**VALID_RECORD, "path": "C:/images/frame.png"}, 5)


def test_path_traversal_is_rejected():
    with pytest.raises(ValueError, match="path"):
        validate_label_record({**VALID_RECORD, "path": "data/../secret/frame.png"}, 6)


def test_unknown_field_is_rejected():
    with pytest.raises(ValueError, match="unknown"):
        validate_label_record({**VALID_RECORD, "comment": "guess"}, 7)
