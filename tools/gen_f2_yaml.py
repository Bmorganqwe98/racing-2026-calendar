"""
Build data/f2.yaml from the FIA F2 2026 calendar (Wikipedia + published sprint/feature dates).

Practice / qualifying times follow the conventional F2 weekend template used at Melbourne 2026:
  Practice and Qualifying on the calendar day before the sprint race (except Baku: Thu setup).

Source cross-check: https://en.wikipedia.org/wiki/2026_Formula_2_Championship (retrieved 2026-05-03).
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

ROUNDS = [
    # rnd, sprint_d, feature_d, tz, full_name, short, circuit, location, baku_style
    (
        1,
        date(2026, 3, 7),
        date(2026, 3, 8),
        "Australia/Melbourne",
        "Melbourne",
        "Melbourne",
        "Albert Park Circuit",
        "Melbourne, Australia",
        False,
    ),
    (
        2,
        date(2026, 5, 2),
        date(2026, 5, 3),
        "America/New_York",
        "Miami",
        "Miami",
        "Miami International Autodrome",
        "Miami Gardens, Florida, USA",
        False,
    ),
    (
        3,
        date(2026, 5, 23),
        date(2026, 5, 24),
        "America/Toronto",
        "Montreal",
        "Montreal",
        "Circuit Gilles Villeneuve",
        "Montreal, Canada",
        False,
    ),
    (
        4,
        date(2026, 6, 6),
        date(2026, 6, 7),
        "Europe/Monaco",
        "Monte Carlo",
        "Monte Carlo",
        "Circuit de Monaco",
        "Monte Carlo, Monaco",
        False,
    ),
    (
        5,
        date(2026, 6, 13),
        date(2026, 6, 14),
        "Europe/Madrid",
        "Barcelona",
        "Barcelona",
        "Circuit de Barcelona-Catalunya",
        "Montmeló, Spain",
        False,
    ),
    (
        6,
        date(2026, 6, 27),
        date(2026, 6, 28),
        "Europe/Vienna",
        "Spielberg",
        "Spielberg",
        "Red Bull Ring",
        "Spielberg, Austria",
        False,
    ),
    (
        7,
        date(2026, 7, 4),
        date(2026, 7, 5),
        "Europe/London",
        "Silverstone",
        "Silverstone",
        "Silverstone Circuit",
        "Silverstone, UK",
        False,
    ),
    (
        8,
        date(2026, 7, 18),
        date(2026, 7, 19),
        "Europe/Brussels",
        "Spa-Francorchamps",
        "Spa-Francorchamps",
        "Circuit de Spa-Francorchamps",
        "Stavelot, Belgium",
        False,
    ),
    (
        9,
        date(2026, 7, 25),
        date(2026, 7, 26),
        "Europe/Budapest",
        "Hungaroring",
        "Hungaroring",
        "Hungaroring",
        "Mogyoród, Hungary",
        False,
    ),
    (
        10,
        date(2026, 9, 5),
        date(2026, 9, 6),
        "Europe/Rome",
        "Monza",
        "Monza",
        "Monza Circuit",
        "Monza, Italy",
        False,
    ),
    (
        11,
        date(2026, 9, 12),
        date(2026, 9, 13),
        "Europe/Madrid",
        "Madrid",
        "Madrid",
        "Madring",
        "Madrid, Spain",
        False,
    ),
    (
        12,
        date(2026, 9, 25),
        date(2026, 9, 26),
        "Asia/Baku",
        "Baku",
        "Baku",
        "Baku City Circuit",
        "Baku, Azerbaijan",
        True,
    ),
    (
        13,
        date(2026, 11, 28),
        date(2026, 11, 29),
        "Asia/Qatar",
        "Lusail",
        "Lusail",
        "Lusail International Circuit",
        "Lusail, Qatar",
        False,
    ),
    (
        14,
        date(2026, 12, 5),
        date(2026, 12, 6),
        "Asia/Dubai",
        "Yas Island",
        "Yas Island",
        "Yas Marina Circuit",
        "Abu Dhabi, UAE",
        False,
    ),
]


def sessions_block(sprint_d: date, feature_d: date, baku: bool) -> str:
    if baku:
        pq = sprint_d - timedelta(days=1)  # Thu before Fri sprint
        lines = [
            f"      - type: Practice\n        start: {pq.isoformat()}T10:00\n        duration_minutes: 45",
            f"      - type: Qualifying\n        start: {pq.isoformat()}T14:30\n        duration_minutes: 30",
            f"      - type: Sprint Race\n        start: {sprint_d.isoformat()}T15:35\n        duration_minutes: 60",
            f"      - type: Feature Race\n        start: {feature_d.isoformat()}T11:35\n        duration_minutes: 80",
        ]
    else:
        pq = sprint_d - timedelta(days=1)
        lines = [
            f"      - type: Practice\n        start: {pq.isoformat()}T10:00\n        duration_minutes: 45",
            f"      - type: Qualifying\n        start: {pq.isoformat()}T14:30\n        duration_minutes: 30",
            f"      - type: Sprint Race\n        start: {sprint_d.isoformat()}T15:35\n        duration_minutes: 60",
            f"      - type: Feature Race\n        start: {feature_d.isoformat()}T11:35\n        duration_minutes: 80",
        ]
    return "\n".join(lines)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "f2.yaml"
    header = """# Formula 2 — 2026 schedule
#
# Sprint / feature race dates from Wikipedia's F2 calendar table; practice and
# qualifying use the template described in tools/gen_f2_yaml.py (same structure
# as the Melbourne opener). Re-verify against https://www.fiaformula2.com/Calendar
# before relying on non-race session times.
#
series: Formula 2
slug: f2
calendar_name: F2 2026
description: FIA Formula 2 Championship 2026 (all sessions in track-local time)
timezone_default: UTC

watch_default:
  us_broadcast: F1 TV Pro (no US linear TV)
  us_streaming: F1 TV Pro
  confidence: high
  notes: >-
    F2 sessions air on F1 TV Pro in the US (support series to Formula 1).

rounds:
"""
    chunks = [header]
    for row in ROUNDS:
        rnd, sprint_d, feature_d, tz, loc_name, short, circuit, location, baku = row
        chunks.append(
            f"  - round: {rnd}\n"
            f"    name: {loc_name} Round\n"
            f"    short_name: {short}\n"
            f"    circuit: {circuit}\n"
            f"    location: {location}\n"
            f"    tz: {tz}\n"
            f"    sessions:\n"
            + sessions_block(sprint_d, feature_d, baku)
            + "\n\n"
        )
    out.write_text("".join(chunks), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
