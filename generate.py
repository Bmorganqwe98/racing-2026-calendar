"""
generate.py — Build ICS calendar feeds for the 2026 racing season.

Reads one YAML file per series from `data/`, emits per-series and combined
`.ics` feeds plus an `index.html` landing page into `output/`. Designed to
run locally for previews and on GitHub Actions for deployment to GitHub
Pages.

Schema and key behaviors are documented in `.cursor/rules/racing-project-context.mdc`
and the project README. The short version:

- `DTSTART;TZID=<track zone>` is set per session so subscribers see times in
  their own local zone automatically.
- UIDs follow `{series-slug}-2026-r{round}-{session-slug}@racing-cal` so
  regenerated `.ics` files update events in place rather than duplicating.
- Sessions with `start: TBA` emit an all-day event with a description note.
- Default session durations are applied when `duration_minutes` is omitted.

Run locally:
    pip install -r requirements.txt
    python generate.py
    # -> output/*.ics + output/index.html + output/.nojekyll
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, timedelta
from html import escape as html_escape
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple
from zoneinfo import ZoneInfo

import yaml
from icalendar import Calendar, Event

REPO_ROOT = Path(__file__).resolve().parent
DATA_DIR = REPO_ROOT / "data"
OUTPUT_DIR = REPO_ROOT / "output"

# Subscribe URLs are stamped into output/index.html. These are placeholders
# kept under one constant so the find/replace before pushing to GitHub is
# trivial. Once you know your repo, edit the two strings below (or run
# `python generate.py --owner <user> --repo <repo>` once that flag is added).
GITHUB_OWNER = "Bmorganqwe98"
GITHUB_REPO = "racing-2026-calendar"

UID_DOMAIN = "racing-cal"
COMBINED_SLUG = "racing-2026"
COMBINED_NAME = "All Series 2026"
COMBINED_DESCRIPTION = "Combined feed: F1, F2, WEC, IMSA, IndyCar, WRC for the 2026 season."

DEFAULT_DURATIONS_MINUTES: Dict[str, int] = {
    "fp1": 60,
    "fp2": 60,
    "fp3": 60,
    "practice": 60,
    "practice 1": 45,
    "practice 2": 45,
    "qualifying": 60,
    "sprint q": 60,
    "sprint qualifying": 60,
    "sprint shootout": 30,
    "sprint": 30,
    "sprint race": 60,
    "feature race": 90,
    "race": 120,
    "shakedown": 60,
    "podium": 30,
    "hyperpole": 15,
}

FALLBACK_DURATION_MINUTES = 60

TBA_TOKENS = {"tba", "tbc", "tbd"}

EASTERN_TZ = ZoneInfo("America/New_York")

WATCH_TBD_LINE = (
    "Where to watch (US): not yet sourced. "
    "Check official broadcaster listings closer to the event date."
)

VALID_WATCH_CONFIDENCE = {"high", "medium", "low"}

# When DTSTART is TBA, we emit an all-day event on this fallback date so the
# event is visible. Each TBA event also carries a note in DESCRIPTION so the
# user knows the time is unconfirmed.
# We use the round's earliest known session date if available, else fall back
# to the season's notional start.
TBA_FALLBACK_DATE = date(2026, 1, 1)


@dataclass
class SeriesMeta:
    """Metadata about a series, used to render the index page."""

    slug: str
    name: str
    calendar_name: str
    round_count: int
    session_count: int
    ics_filename: str


def slugify(value: str) -> str:
    """
    Lowercase, hyphenate, strip non-alphanumeric characters.

    Used for session-type slugs in UIDs so `Sprint Race` becomes `sprint-race`.

    Args:
        value: Source string.

    Returns:
        URL- and UID-safe slug.
    """
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return cleaned or "session"


def is_tba(start_value: Any) -> bool:
    """Return True if `start_value` is a TBA/TBC/TBD marker."""
    if start_value is None:
        return True
    if isinstance(start_value, str) and start_value.strip().lower() in TBA_TOKENS:
        return True
    return False


def parse_local_start(start_value: Any) -> datetime:
    """
    Parse a YAML `start` value into a naive datetime (no tz).

    Accepts either:
    - A string `"2026-03-08T15:00"` (ISO 8601 without offset),
    - Or a datetime/date already coerced by PyYAML.

    Args:
        start_value: Raw value from YAML.

    Returns:
        A naive datetime; the round's `tz` is applied separately when the
        Event is built.

    Raises:
        ValueError: If the value can't be parsed.
    """
    if isinstance(start_value, datetime):
        return start_value.replace(tzinfo=None) if start_value.tzinfo else start_value
    if isinstance(start_value, date):
        return datetime(start_value.year, start_value.month, start_value.day)
    if isinstance(start_value, str):
        text = start_value.strip()
        return datetime.fromisoformat(text)
    raise ValueError(f"Unrecognized start value: {start_value!r}")


def resolve_duration(session: Dict[str, Any]) -> timedelta:
    """
    Pick the right session duration: explicit value, then series default by
    type, then fallback.

    Args:
        session: Parsed session dict.

    Returns:
        timedelta representing the session length.
    """
    explicit = session.get("duration_minutes")
    if explicit is not None:
        return timedelta(minutes=int(explicit))
    type_key = str(session.get("type", "")).strip().lower()
    minutes = DEFAULT_DURATIONS_MINUTES.get(type_key, FALLBACK_DURATION_MINUTES)
    return timedelta(minutes=minutes)


def build_uid(series_slug: str, round_number: int, session_type: str) -> str:
    """
    Build a stable iCalendar UID for a single race session.

    Format: `{series}-2026-r{round}-{session}@racing-cal`. Stable across
    regenerations so subscribers see updates rather than duplicates.

    Args:
        series_slug: Lowercase series id (e.g. `f1`).
        round_number: 1-based round within the season.
        session_type: Free-text session type from YAML.

    Returns:
        UID string.
    """
    return f"{series_slug}-2026-r{round_number}-{slugify(session_type)}@{UID_DOMAIN}"


def build_summary(series_short: str, round_short_name: str, session_type: str) -> str:
    """SUMMARY shown in calendar clients, e.g. `F1 Australian GP - Race`."""
    return f"{series_short} {round_short_name} - {session_type}"


def series_short_label(series_data: Dict[str, Any]) -> str:
    """Pick a short series label for SUMMARY (e.g. `F1`, `WEC`)."""
    if "calendar_name" in series_data:
        first = series_data["calendar_name"].split()[0]
        return first
    return series_data.get("slug", "").upper() or "Series"


def round_earliest_date(round_data: Dict[str, Any]) -> Optional[date]:
    """Return the earliest known session date in this round (for TBA fallback)."""
    earliest: Optional[datetime] = None
    for session in round_data.get("sessions", []) or []:
        if is_tba(session.get("start")):
            continue
        try:
            dt = parse_local_start(session.get("start"))
        except (ValueError, TypeError):
            continue
        if earliest is None or dt < earliest:
            earliest = dt
    return earliest.date() if earliest else None


def format_eastern(aware_dt: datetime) -> str:
    """
    Render a tz-aware datetime in Eastern time (e.g. 'Sat Mar 7, 11:00 PM EST').

    Always uses America/New_York; the printed abbreviation is whatever the
    zone is at that instant (EST in winter, EDT during DST). This keeps the
    description text honest with what the calendar client will display when
    the user is in the Eastern timezone.
    """
    eastern = aware_dt.astimezone(EASTERN_TZ)
    weekday = eastern.strftime("%a")
    month = eastern.strftime("%b")
    day = eastern.day
    hour_12 = eastern.hour % 12 or 12
    minute = eastern.minute
    am_pm = "AM" if eastern.hour < 12 else "PM"
    abbr = eastern.strftime("%Z")
    return f"{weekday} {month} {day}, {hour_12}:{minute:02d} {am_pm} {abbr}"


def resolve_watch(
    session: Dict[str, Any],
    series_data: Dict[str, Any],
) -> Optional[Dict[str, Any]]:
    """
    Pick US watch info for a session.

    Resolution order (no merging — each level is all-or-nothing):
    1. session-level `watch:` block (most specific override)
    2. series-level `watch_default:` block (fallback for the whole series)
    3. None (caller renders an explicit TBD line)
    """
    session_watch = session.get("watch") if session else None
    if session_watch:
        return session_watch
    series_watch = series_data.get("watch_default") if series_data else None
    if series_watch:
        return series_watch
    return None


def _format_watch_line(watch: Optional[Dict[str, Any]]) -> str:
    """Render the 'Where to watch' line(s) for a session description."""
    if not watch:
        return WATCH_TBD_LINE
    parts: List[str] = []
    if watch.get("us_broadcast"):
        parts.append(str(watch["us_broadcast"]))
    if watch.get("us_streaming"):
        parts.append(f"streaming: {watch['us_streaming']}")
    confidence_raw = str(watch.get("confidence", "")).strip().lower()
    confidence_suffix = (
        f" ({confidence_raw} confidence)"
        if confidence_raw in VALID_WATCH_CONFIDENCE
        else ""
    )
    primary = " | ".join(parts) if parts else "TBD"
    line = f"Where to watch (US): {primary}{confidence_suffix}"
    notes = str(watch.get("notes", "")).strip()
    if notes:
        line += f"\nWatch notes: {notes}"
    return line


def build_session_event(
    session: Dict[str, Any],
    round_data: Dict[str, Any],
    series_data: Dict[str, Any],
) -> Event:
    """
    Build an iCalendar Event for one race session.

    Args:
        session: The session dict (type, start, optional duration_minutes).
        round_data: The parent round dict (round, name, short_name, circuit,
            location, tz, sessions).
        series_data: The whole series dict (series, slug, calendar_name, ...).

    Returns:
        A fully-populated icalendar.Event.
    """
    series_slug = series_data["slug"]
    series_short = series_short_label(series_data)
    round_number = int(round_data["round"])
    round_short = round_data.get("short_name", round_data["name"])
    session_type = str(session["type"])

    event = Event()
    event.add("uid", build_uid(series_slug, round_number, session_type))
    event.add("summary", build_summary(series_short, round_short, session_type))
    event.add("location", _format_location(round_data))
    event.add("categories", [series_data.get("series", series_slug)])

    if is_tba(session.get("start")):
        # All-day placeholder; description flags it so subscribers know it's TBA.
        anchor = round_earliest_date(round_data) or TBA_FALLBACK_DATE
        event.add("dtstart", anchor)
        event.add("dtend", anchor + timedelta(days=1))
        event.add(
            "description",
            _build_description(
                series_data,
                round_data,
                session_type,
                tba=True,
                session=session,
            ),
        )
        return event

    tz_name = round_data.get("tz") or series_data.get("timezone_default") or "UTC"
    tz = ZoneInfo(tz_name)
    naive_start = parse_local_start(session["start"])
    aware_start = naive_start.replace(tzinfo=tz)
    duration = resolve_duration(session)

    event.add("dtstart", aware_start)
    event.add("dtend", aware_start + duration)
    event.add(
        "description",
        _build_description(
            series_data,
            round_data,
            session_type,
            tba=False,
            aware_start=aware_start,
            session=session,
        ),
    )

    return event


def _format_location(round_data: Dict[str, Any]) -> str:
    """LOCATION = `Circuit, City, Country` when available."""
    parts = [
        str(round_data.get("circuit", "")).strip(),
        str(round_data.get("location", "")).strip(),
    ]
    return ", ".join(p for p in parts if p)


def _build_description(
    series_data: Dict[str, Any],
    round_data: Dict[str, Any],
    session_type: str,
    *,
    tba: bool,
    aware_start: Optional[datetime] = None,
    session: Optional[Dict[str, Any]] = None,
) -> str:
    """
    Rich DESCRIPTION text for the event.

    Layout (per line, separated by '\\n' which most calendar clients render
    as paragraph breaks):
        Series: <name>
        Round <n>: <round name>
        Session: <type>
        Time in Eastern: <weekday Mon D, H:MM AM/PM EST/EDT>   (skipped on TBA)
        Time TBA - placeholder all-day...                       (TBA only)
        Where to watch (US): <broadcaster> | streaming: <stream> (<confidence>)
        Watch notes: <free text>                                (only if provided)
        Generated from data/<slug>.yaml. See NOTES.md...
    """
    lines: List[str] = [
        f"Series: {series_data.get('series', series_data['slug'])}",
        f"Round {round_data['round']}: {round_data['name']}",
        f"Session: {session_type}",
    ]
    if tba:
        lines.append(
            "Time TBA - this is a placeholder all-day event. "
            "It will update to the correct time once published."
        )
    elif aware_start is not None:
        lines.append(f"Time in Eastern: {format_eastern(aware_start)}")

    lines.append(_format_watch_line(resolve_watch(session or {}, series_data)))

    lines.append(
        "Generated from data/{slug}.yaml. See NOTES.md for source provenance.".format(
            slug=series_data["slug"]
        )
    )
    return "\n".join(lines)


def build_series_calendar(series_data: Dict[str, Any]) -> Tuple[Calendar, int]:
    """
    Build a per-series Calendar.

    VTIMEZONE blocks for every TZID referenced by the events are appended
    via `add_missing_timezones()` so non-Google clients (Apple, Outlook)
    can resolve the zones without consulting an external database.

    Args:
        series_data: Parsed YAML for one series.

    Returns:
        Tuple of (Calendar, session_count).
    """
    cal = _new_calendar(
        name=series_data.get("calendar_name", series_data["slug"]),
        description=series_data.get("description", ""),
    )
    session_count = 0
    for round_data in series_data.get("rounds", []) or []:
        for session in round_data.get("sessions", []) or []:
            cal.add_component(build_session_event(session, round_data, series_data))
            session_count += 1
    cal.add_missing_timezones()
    return cal, session_count


def build_combined_calendar(all_series: List[Dict[str, Any]]) -> Calendar:
    """Build the all-series combined feed (with VTIMEZONE blocks)."""
    cal = _new_calendar(name=COMBINED_NAME, description=COMBINED_DESCRIPTION)
    for series_data in all_series:
        for round_data in series_data.get("rounds", []) or []:
            for session in round_data.get("sessions", []) or []:
                cal.add_component(
                    build_session_event(session, round_data, series_data)
                )
    cal.add_missing_timezones()
    return cal


def _new_calendar(*, name: str, description: str) -> Calendar:
    """Construct a Calendar with the standard PRODID + display properties."""
    cal = Calendar()
    cal.add("prodid", "-//racing-2026-ics-calendar//generate.py//EN")
    cal.add("version", "2.0")
    cal.add("calscale", "GREGORIAN")
    cal.add("method", "PUBLISH")
    cal.add("x-wr-calname", name)
    if description:
        cal.add("x-wr-caldesc", description)
    return cal


def write_ics(calendar: Calendar, path: Path) -> None:
    """Write a Calendar to disk as bytes (iCalendar format is byte-oriented)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(calendar.to_ical())


def write_nojekyll(output_dir: Path) -> None:
    """Tell GitHub Pages not to apply Jekyll processing to .ics files."""
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")


def write_index_html(metas: List[SeriesMeta], output_dir: Path) -> None:
    """
    Render output/index.html with subscribe URLs per series + combined feed.

    Both `https://` (for browsers) and `webcal://` (for one-click subscribe
    in most calendar apps) URLs are listed.
    """
    base_https = (
        f"https://{GITHUB_OWNER}.github.io/{GITHUB_REPO}"
        if GITHUB_OWNER and GITHUB_REPO
        else "https://<YOUR-USERNAME>.github.io/<YOUR-REPO>"
    )
    base_webcal = base_https.replace("https://", "webcal://", 1)

    rows = []
    combined_meta = SeriesMeta(
        slug=COMBINED_SLUG,
        name=COMBINED_NAME,
        calendar_name=COMBINED_NAME,
        round_count=sum(m.round_count for m in metas),
        session_count=sum(m.session_count for m in metas),
        ics_filename=f"{COMBINED_SLUG}.ics",
    )
    for meta in [combined_meta, *metas]:
        https_url = f"{base_https}/{meta.ics_filename}"
        webcal_url = f"{base_webcal}/{meta.ics_filename}"
        rows.append(
            "<tr>"
            f"<td><strong>{html_escape(meta.calendar_name)}</strong></td>"
            f"<td>{meta.round_count}</td>"
            f"<td>{meta.session_count}</td>"
            f"<td><a href=\"{html_escape(https_url)}\"><code>{html_escape(https_url)}</code></a></td>"
            f"<td><a href=\"{html_escape(webcal_url)}\">subscribe</a></td>"
            "</tr>"
        )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Racing 2026 Calendar Feeds</title>
<style>
  :root {{ color-scheme: light dark; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; max-width: 920px; margin: 2rem auto; padding: 0 1rem; line-height: 1.5; }}
  h1 {{ margin-bottom: 0.25rem; }}
  p.lede {{ color: #666; margin-top: 0; }}
  table {{ border-collapse: collapse; width: 100%; margin-top: 1.5rem; }}
  th, td {{ text-align: left; padding: 0.6rem 0.5rem; border-bottom: 1px solid #ddd; vertical-align: top; }}
  th {{ background: rgba(0,0,0,0.04); }}
  code {{ font-size: 0.9em; word-break: break-all; }}
  .footnote {{ color: #888; font-size: 0.9em; margin-top: 2rem; }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #0e0e10; color: #ddd; }}
    th {{ background: rgba(255,255,255,0.06); }}
    th, td {{ border-color: #333; }}
    p.lede, .footnote {{ color: #999; }}
  }}
</style>
</head>
<body>
<h1>Racing 2026 Calendar Feeds</h1>
<p class="lede">Subscribe by URL in Google Calendar, Apple Calendar, or Outlook to get a self-updating 2026 race-weekend calendar in your local time zone.</p>

<h2>How to subscribe (Google Calendar)</h2>
<ol>
  <li>Copy a URL from the table below.</li>
  <li>In Google Calendar: <em>Other calendars &rarr; <strong>+</strong> &rarr; From URL</em>.</li>
  <li>Paste the URL and click <strong>Add calendar</strong>.</li>
</ol>
<p>Each series becomes its own color-coded calendar. Google Calendar refreshes subscribed feeds on its own cadence (typically every 8&ndash;24 hours); Apple Calendar and Outlook refresh more aggressively if you want faster updates.</p>

<h2>Available feeds</h2>
<table>
  <thead>
    <tr><th>Calendar</th><th>Rounds</th><th>Sessions</th><th>HTTPS URL</th><th>One-click</th></tr>
  </thead>
  <tbody>
    {"".join(rows)}
  </tbody>
</table>

<p class="footnote">Source data lives in <code>data/&lt;series&gt;.yaml</code> in the repo. Provenance for every schedule (source URL, retrieval date, confidence, TBA gaps) is logged in <code>NOTES.md</code>.</p>
</body>
</html>
"""
    (output_dir / "index.html").write_text(html, encoding="utf-8")


def load_all_series() -> List[Dict[str, Any]]:
    """Load every YAML file under `data/` in deterministic (sorted) order."""
    paths = sorted(DATA_DIR.glob("*.yaml"))
    series_list: List[Dict[str, Any]] = []
    for path in paths:
        with path.open("r", encoding="utf-8") as fh:
            data = yaml.safe_load(fh)
        if not isinstance(data, dict) or "slug" not in data:
            raise ValueError(f"{path} is missing required 'slug' field.")
        series_list.append(data)
    return series_list


def main() -> None:
    """Build per-series and combined .ics files plus the index page."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_nojekyll(OUTPUT_DIR)

    all_series = load_all_series()
    metas: List[SeriesMeta] = []
    total_sessions = 0

    for series_data in all_series:
        cal, session_count = build_series_calendar(series_data)
        ics_filename = f"{series_data['slug']}.ics"
        write_ics(cal, OUTPUT_DIR / ics_filename)
        round_count = len(series_data.get("rounds", []) or [])
        metas.append(
            SeriesMeta(
                slug=series_data["slug"],
                name=series_data.get("series", series_data["slug"]),
                calendar_name=series_data.get("calendar_name", series_data["slug"]),
                round_count=round_count,
                session_count=session_count,
                ics_filename=ics_filename,
            )
        )
        total_sessions += session_count
        print(f"  wrote output/{ics_filename}  ({round_count} rounds, {session_count} sessions)")

    combined_cal = build_combined_calendar(all_series)
    write_ics(combined_cal, OUTPUT_DIR / f"{COMBINED_SLUG}.ics")
    print(f"  wrote output/{COMBINED_SLUG}.ics  (combined: {total_sessions} sessions)")

    write_index_html(metas, OUTPUT_DIR)
    print(f"  wrote output/index.html  ({len(metas)} series + 1 combined)")
    print(f"  wrote output/.nojekyll")


if __name__ == "__main__":
    main()
