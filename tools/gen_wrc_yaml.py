"""
Generate data/wrc.yaml — collapsed per-day WRC schedule (project convention).

Dates and rally HQ geography from Wikipedia;
clock times reuse the Monte Carlo 2026 editorial template (morning shakedown / evening
opening leg / full days / podium) shifted onto each rally's published start date.

Not stage-accurate — see NOTES.md and racing-project-context.mdc.

Source: https://en.wikipedia.org/wiki/2026_World_Rally_Championship (retrieved 2026-05-03).
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

# (round, rally_name, short_name, circuit_descriptor, location, tz, rally_start_date)
ROUNDS = [
    (1, "Rallye Automobile Monte Carlo", "Monte Carlo", "Monte Carlo / Gap region", "Gap, France", "Europe/Paris", date(2026, 1, 22)),
    (2, "Rally Sweden", "Sweden", "Umeå region", "Umeå, Sweden", "Europe/Stockholm", date(2026, 2, 12)),
    (3, "Safari Rally Kenya", "Kenya", "Nairobi region", "Nairobi, Kenya", "Africa/Nairobi", date(2026, 3, 12)),
    (4, "Croatia Rally", "Croatia", "Rijeka region", "Rijeka, Croatia", "Europe/Zagreb", date(2026, 4, 9)),
    (5, "Rally Islas Canarias", "Canary Islands", "Gran Canaria", "Las Palmas, Spain", "Atlantic/Canary", date(2026, 4, 23)),
    (6, "Rally de Portugal", "Portugal", "Matosinhos / Porto", "Matosinhos, Portugal", "Europe/Lisbon", date(2026, 5, 7)),
    (7, "Rally Japan", "Japan", "Toyota City region", "Toyota, Aichi, Japan", "Asia/Tokyo", date(2026, 5, 28)),
    (8, "Acropolis Rally Greece", "Greece", "Loutraki base", "Loutraki, Greece", "Europe/Athens", date(2026, 6, 25)),
    (9, "Rally Estonia", "Estonia", "Tartu region", "Tartu, Estonia", "Europe/Tallinn", date(2026, 7, 16)),
    (10, "Rally Finland", "Finland", "Jyväskylä region", "Jyväskylä, Finland", "Europe/Helsinki", date(2026, 7, 30)),
    (11, "Rally del Paraguay", "Paraguay", "Encarnación region", "Encarnación, Paraguay", "America/Asuncion", date(2026, 8, 27)),
    (12, "Rally Chile", "Chile", "Concepción region", "Concepción, Chile", "America/Santiago", date(2026, 9, 10)),
    (13, "Rally Italia Sardegna", "Sardegna", "Alghero base", "Alghero, Italy", "Europe/Rome", date(2026, 10, 1)),
    (14, "Rally Saudi Arabia", "Saudi Arabia", "Jeddah region", "Jeddah, Saudi Arabia", "Asia/Riyadh", date(2026, 11, 11)),
]


def sessions_for_start(d0: date) -> str:
    """Collapsed template anchored on WRC Thursday / opening day."""
    d1 = d0 + timedelta(days=1)
    d2 = d0 + timedelta(days=2)
    d3 = d0 + timedelta(days=3)
    return "\n".join(
        [
            f"      - type: Shakedown\n        start: {d0.isoformat()}T09:00\n        duration_minutes: 60",
            f"      - type: Day 1\n        start: {d0.isoformat()}T19:00\n        duration_minutes: 240",
            f"      - type: Day 2\n        start: {d1.isoformat()}T08:00\n        duration_minutes: 600",
            f"      - type: Day 3\n        start: {d2.isoformat()}T08:00\n        duration_minutes: 600",
            f"      - type: Day 4\n        start: {d3.isoformat()}T08:00\n        duration_minutes: 240",
            f"      - type: Podium\n        start: {d3.isoformat()}T15:00\n        duration_minutes: 60",
        ]
    )


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "wrc.yaml"
    lines = [
        "# World Rally Championship — 2026 schedule (collapsed per-day)\n"
        "#\n"
        "series: World Rally Championship\n"
        "slug: wrc\n"
        "calendar_name: WRC 2026\n"
        "description: FIA World Rally Championship 2026 (collapsed per-day; rally-local time)\n"
        "timezone_default: UTC\n"
        "\n"
        "watch_default:\n"
        "  us_broadcast: No US linear TV deal\n"
        "  us_streaming: Rally.tv (FIA official global stream)\n"
        "  confidence: high\n"
        "  notes: Rally.tv is the primary official streaming path for WRC worldwide.\n"
        "\n"
        "rounds:\n",
    ]
    for rnd, name, short, circuit, loc, tz, d0 in ROUNDS:
        lines.append(f"  - round: {rnd}\n")
        lines.append(f"    name: {name}\n")
        lines.append(f"    short_name: {short}\n")
        lines.append(f"    circuit: {circuit}\n")
        lines.append(f"    location: {loc}\n")
        lines.append(f"    tz: {tz}\n")
        lines.append("    sessions:\n")
        lines.append(sessions_for_start(d0))
        lines.append("\n\n")
    out.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
