"""
Smoke tests for generate.py.

These tests are intentionally narrow and fast — they validate the rules
that subscribers actually depend on (UID stability, TZID present, TBA
handling, round-trip parse) rather than exercising every code path.
"""

from __future__ import annotations

import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

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


def test_format_eastern_winter_returns_est() -> None:
    """Outside US DST, the printed abbreviation must be EST."""
    melbourne = ZoneInfo("Australia/Melbourne")
    aware = datetime(2026, 3, 8, 15, 0, tzinfo=melbourne)
    # March 8 15:00 AEDT (UTC+11) = March 8 04:00 UTC. US DST begins 07:00 UTC
    # that same day, so at 04:00 UTC NY is still on EST.
    assert g.format_eastern(aware) == "Sat Mar 7, 11:00 PM EST"


def test_format_eastern_summer_returns_edt() -> None:
    """During US DST, the printed abbreviation must be EDT."""
    paris = ZoneInfo("Europe/Paris")
    aware = datetime(2026, 7, 5, 15, 0, tzinfo=paris)
    # July 5 15:00 CEST (UTC+2) = 13:00 UTC = 09:00 EDT.
    assert g.format_eastern(aware) == "Sun Jul 5, 9:00 AM EDT"


def test_resolve_watch_session_overrides_series() -> None:
    series = {"watch_default": {"us_broadcast": "Default Channel"}}
    session = {"watch": {"us_broadcast": "Override Channel"}}
    assert g.resolve_watch(session, series) == {"us_broadcast": "Override Channel"}


def test_resolve_watch_falls_back_to_series_default() -> None:
    series = {"watch_default": {"us_broadcast": "Default Channel"}}
    session = {"type": "Race"}
    assert g.resolve_watch(session, series) == {"us_broadcast": "Default Channel"}


def test_resolve_watch_returns_none_when_neither_provided() -> None:
    assert g.resolve_watch({}, {}) is None


def test_description_includes_eastern_time_for_non_tba_sessions(f1_series, f1_round) -> None:
    event = g.build_session_event(f1_round["sessions"][-1], f1_round, f1_series)  # Race
    description = str(event.get("description"))
    assert "Time in Eastern:" in description
    assert "EST" in description or "EDT" in description


def test_description_uses_series_watch_default_when_session_lacks_one(
    f1_series, f1_round,
) -> None:
    f1_series["watch_default"] = {
        "us_broadcast": "TestNet",
        "us_streaming": "TestStream",
        "confidence": "high",
    }
    event = g.build_session_event(f1_round["sessions"][-1], f1_round, f1_series)
    description = str(event.get("description"))
    assert "Where to watch (US): TestNet | streaming: TestStream (high confidence)" in description


def test_description_session_watch_overrides_series_default(f1_series, f1_round) -> None:
    f1_series["watch_default"] = {"us_broadcast": "DefaultNet", "confidence": "low"}
    f1_round["sessions"][-1]["watch"] = {"us_broadcast": "OverrideNet", "confidence": "high"}
    event = g.build_session_event(f1_round["sessions"][-1], f1_round, f1_series)
    description = str(event.get("description"))
    assert "OverrideNet" in description
    assert "high confidence" in description
    assert "DefaultNet" not in description


def test_description_falls_back_to_tbd_text_when_no_watch_info(f1_series, f1_round) -> None:
    """f1_series fixture lacks watch_default, so subscribers see the TBD text."""
    event = g.build_session_event(f1_round["sessions"][-1], f1_round, f1_series)
    description = str(event.get("description"))
    assert "Where to watch (US): not yet sourced" in description


def test_tba_event_still_includes_watch_line(f1_series, f1_round) -> None:
    """Sessions with TBA times still get a watch line (TBD or resolved)."""
    f1_round["sessions"].append({"type": "FP3", "start": "TBA"})
    tba_event = g.build_session_event(f1_round["sessions"][-1], f1_round, f1_series)
    description = str(tba_event.get("description"))
    assert "Where to watch (US):" in description


def test_tba_event_uses_date_hint_for_anchor_when_no_other_times() -> None:
    """If a round is fully TBA, `date_hint` anchors all-day events correctly."""
    series = {
        "series": "IndyCar Series",
        "slug": "indycar",
        "calendar_name": "IndyCar 2026",
        "description": "Test fixture",
        "timezone_default": "America/New_York",
    }
    round_data = {
        "round": 12,
        "name": "Music City GP",
        "short_name": "Nashville GP",
        "circuit": "Nashville Superspeedway",
        "location": "Lebanon, Tennessee, USA",
        "tz": "America/Chicago",
        "sessions": [
            {"type": "Race", "start": "TBA", "date_hint": "2026-07-19"},
        ],
    }
    event = g.build_session_event(round_data["sessions"][0], round_data, series)
    dtstart = event.get("dtstart").dt
    assert dtstart.isoformat() == "2026-07-19"


# Pattern-based privacy guard. Detects *categories* of leaked data without
# hardcoding any specific person's name/email into a publicly-readable file.
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
NOREPLY_DOMAIN = "users.noreply.github.com"
LOCAL_PATH_SUBSTRINGS = (
    "C:\\Users\\",   # Windows user-home prefix (escaped backslashes in source)
    "/Users/",       # macOS user-home prefix
    "OneDrive",      # OneDrive sync paths are personal-machine-specific
    "/home/runner/work/",  # GitHub Actions runner paths -- shouldn't leak either
)


def test_published_files_contain_no_personal_identifiers(tmp_path, monkeypatch) -> None:
    """
    Privacy guard: regenerated artifacts must contain no non-noreply emails
    and no local-machine file paths.

    Pattern-based on purpose -- this test file ships publicly, so it
    deliberately does not name any specific person's identifiers.
    """
    monkeypatch.setattr(g, "OUTPUT_DIR", tmp_path)
    g.main()

    for path in tmp_path.iterdir():
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8", errors="ignore")

        for match in EMAIL_RE.finditer(content):
            email = match.group(0)
            assert email.endswith("@" + NOREPLY_DOMAIN), (
                f"Non-noreply email '{email}' leaked into {path.name}"
            )

        for substring in LOCAL_PATH_SUBSTRINGS:
            assert substring not in content, (
                f"Local-machine path fragment '{substring}' leaked into {path.name}"
            )


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
