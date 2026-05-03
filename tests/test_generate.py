"""
Smoke tests for generate.py.

These tests are intentionally narrow and fast — they validate the rules
that subscribers actually depend on (UID stability, TZID present, TBA
handling, round-trip parse) rather than exercising every code path.
"""

from __future__ import annotations

import sys
from datetime import date, timedelta
from pathlib import Path

import pytest
from icalendar import Calendar

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

import generate as g  # noqa: E402  (path setup must come first)


@pytest.fixture
def f1_round() -> dict:
    """A representative round used across several tests."""
    return {
        "round": 1,
        "name": "Australian Grand Prix",
        "short_name": "Australian GP",
        "circuit": "Albert Park Circuit",
        "location": "Melbourne, Australia",
        "tz": "Australia/Melbourne",
        "sessions": [
            {"type": "FP1", "start": "2026-03-06T12:30", "duration_minutes": 60},
            {"type": "Race", "start": "2026-03-08T15:00", "duration_minutes": 120},
        ],
    }


@pytest.fixture
def f1_series(f1_round) -> dict:
    return {
        "series": "Formula 1",
        "slug": "f1",
        "calendar_name": "F1 2026",
        "description": "Test fixture",
        "timezone_default": "UTC",
        "rounds": [f1_round],
    }


def test_slugify_normalizes_whitespace_and_punctuation() -> None:
    assert g.slugify("Sprint Race") == "sprint-race"
    assert g.slugify("FP1") == "fp1"
    assert g.slugify("  Day 1!  ") == "day-1"
    assert g.slugify("---") == "session"


def test_uid_is_stable_for_same_inputs() -> None:
    a = g.build_uid("f1", 1, "Race")
    b = g.build_uid("f1", 1, "Race")
    assert a == b == "f1-2026-r1-race@racing-cal"


def test_uid_changes_with_session_type() -> None:
    assert g.build_uid("f1", 1, "Race") != g.build_uid("f1", 1, "Qualifying")


def test_resolve_duration_uses_explicit_value_first() -> None:
    assert g.resolve_duration({"type": "Race", "duration_minutes": 90}) == timedelta(minutes=90)


def test_resolve_duration_falls_back_to_type_default() -> None:
    assert g.resolve_duration({"type": "FP1"}) == timedelta(minutes=60)
    assert g.resolve_duration({"type": "Sprint"}) == timedelta(minutes=30)
    assert g.resolve_duration({"type": "Race"}) == timedelta(minutes=120)


def test_resolve_duration_unknown_type_uses_fallback() -> None:
    assert g.resolve_duration({"type": "Mystery Session"}) == timedelta(
        minutes=g.FALLBACK_DURATION_MINUTES
    )


def test_event_has_tzid_when_session_has_tz(f1_series, f1_round) -> None:
    event = g.build_session_event(f1_round["sessions"][0], f1_round, f1_series)
    ical_text = event.to_ical().decode("utf-8")
    assert "DTSTART;TZID=Australia/Melbourne:20260306T123000" in ical_text


def test_tba_session_emits_all_day_event(f1_series, f1_round) -> None:
    f1_round["sessions"].append({"type": "FP3", "start": "TBA"})
    tba_event = g.build_session_event(f1_round["sessions"][-1], f1_round, f1_series)
    ical_text = tba_event.to_ical().decode("utf-8")
    assert "VALUE=DATE" in ical_text
    assert "Time TBA" in ical_text


def test_full_series_round_trip(tmp_path, f1_series) -> None:
    """Build a calendar, write it to disk, parse it back, expect the same event count."""
    cal, session_count = g.build_series_calendar(f1_series)
    out_path = tmp_path / "f1.ics"
    g.write_ics(cal, out_path)

    reparsed = Calendar.from_ical(out_path.read_bytes())
    events = [c for c in reparsed.walk() if c.name == "VEVENT"]
    assert len(events) == session_count == 2


def test_combined_calendar_includes_every_session(f1_series) -> None:
    f2_series = dict(f1_series)
    f2_series["slug"] = "f2"
    f2_series["calendar_name"] = "F2 2026"
    combined = g.build_combined_calendar([f1_series, f2_series])
    events = [c for c in combined.walk() if c.name == "VEVENT"]
    assert len(events) == 4


def test_load_all_series_finds_six_yaml_files() -> None:
    """The repo ships with one YAML per series (F1, F2, WEC, IMSA, IndyCar, WRC)."""
    series_list = g.load_all_series()
    slugs = {s["slug"] for s in series_list}
    assert slugs == {"f1", "f2", "wec", "imsa", "indycar", "wrc"}


def test_full_pipeline_writes_all_outputs(tmp_path, monkeypatch) -> None:
    """End-to-end: running main() produces every expected output file."""
    monkeypatch.setattr(g, "OUTPUT_DIR", tmp_path)
    g.main()

    expected = {
        "f1.ics",
        "f2.ics",
        "wec.ics",
        "imsa.ics",
        "indycar.ics",
        "wrc.ics",
        "racing-2026.ics",
        "index.html",
        ".nojekyll",
    }
    actual = {p.name for p in tmp_path.iterdir()}
    assert expected.issubset(actual)
