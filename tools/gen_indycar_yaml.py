"""
Generate data/indycar.yaml from the Wikipedia 2026 IndyCar schedule table.

Broadcast times are listed in US Eastern Time (ET); this script converts each
published start to the circuit's IANA zone as naive local wall-clock times.

Sources:
  https://en.wikipedia.org/wiki/2026_IndyCar_Series (schedule + ET times;
  retrieved 2026-05-03).
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

from dateutil import parser as date_parser
from zoneinfo import ZoneInfo

ET = ZoneInfo("America/New_York")

# (round, date_y-m-d, race_title, short_name, circuit, location, tz, time_et_str or None if TBD)
ROUNDS = [
    (1, "2026-03-01", "Firestone Grand Prix of St. Petersburg", "St. Petersburg GP", "St. Petersburg Street Circuit", "St. Petersburg, Florida, USA", "America/New_York", "12:00 PM"),
    (2, "2026-03-07", "Good Ranchers 250", "Phoenix", "Phoenix Raceway", "Avondale, Arizona, USA", "America/Phoenix", "3:00 PM"),
    (3, "2026-03-15", "Java House Grand Prix of Arlington", "Arlington GP", "Streets of Arlington", "Arlington, Texas, USA", "America/Chicago", "12:30 PM"),
    (4, "2026-03-29", "Children's of Alabama Indy Grand Prix", "Barber GP", "Barber Motorsports Park", "Birmingham, Alabama, USA", "America/Chicago", "1:00 PM"),
    (5, "2026-04-19", "Acura Grand Prix of Long Beach", "Long Beach GP", "Long Beach Street Circuit", "Long Beach, California, USA", "America/Los_Angeles", "5:30 PM"),
    (6, "2026-05-09", "Sonsio Grand Prix", "Indianapolis GP", "Indianapolis Motor Speedway Road Course", "Speedway, Indiana, USA", "America/Indiana/Indianapolis", "4:30 PM"),
    (7, "2026-05-24", "Indianapolis 500", "Indianapolis 500", "Indianapolis Motor Speedway", "Speedway, Indiana, USA", "America/Indiana/Indianapolis", "10:00 AM"),
    (8, "2026-05-31", "Chevrolet Detroit Grand Prix", "Detroit GP", "Detroit Street Circuit", "Detroit, Michigan, USA", "America/New_York", "12:30 PM"),
    (9, "2026-06-07", "Bommarito Automotive Group 500", "Gateway", "World Wide Technology Raceway", "Madison, Illinois, USA", "America/Chicago", "9:00 PM"),
    (10, "2026-06-21", "XPEL Grand Prix at Road America", "Road America GP", "Road America", "Elkhart Lake, Wisconsin, USA", "America/Chicago", "2:00 PM"),
    (11, "2026-07-05", "Honda Indy 200 at Mid-Ohio", "Mid-Ohio GP", "Mid-Ohio Sports Car Course", "Lexington, Ohio, USA", "America/New_York", "12:30 PM"),
    (12, "2026-07-19", "Borchetta Bourbon Music City Grand Prix", "Nashville GP", "Nashville Superspeedway", "Lebanon, Tennessee, USA", "America/Chicago", None),
    (13, "2026-08-09", "BitNile.com Grand Prix of Portland", "Portland GP", "Portland International Raceway", "Portland, Oregon, USA", "America/Los_Angeles", "4:00 PM"),
    (14, "2026-08-16", "Ontario Honda Dealers Indy at Markham", "Markham GP", "Streets of Markham", "Markham, Ontario, Canada", "America/Toronto", "12:00 PM"),
    (15, "2026-08-23", "Freedom 250 Grand Prix of Washington, D.C.", "Washington GP", "Streets of Washington", "Washington, D.C., USA", "America/New_York", None),
    (16, "2026-08-29", "Snap-on Makers and Fixers 250", "Milwaukee Race 1", "Milwaukee Mile", "West Allis, Wisconsin, USA", "America/Chicago", "2:30 PM"),
    (17, "2026-08-30", "Snap-on Milwaukee Mile 250", "Milwaukee Race 2", "Milwaukee Mile", "West Allis, Wisconsin, USA", "America/Chicago", "1:00 PM"),
    (18, "2026-09-06", "IndyCar Grand Prix of Monterey", "Laguna Seca GP", "WeatherTech Raceway Laguna Seca", "Monterey, California, USA", "America/Los_Angeles", "2:30 PM"),
]


def et_to_naive_local(date_iso: str, time_et: str, tz_name: str) -> str:
    venue_tz = ZoneInfo(tz_name)
    dt_et = date_parser.parse(f"{date_iso} {time_et}").replace(tzinfo=ET)
    local = dt_et.astimezone(venue_tz)
    return local.strftime("%Y-%m-%dT%H:%M")


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "indycar.yaml"
    lines = [
        "# IndyCar Series — 2026 schedule\n"
        "#\n"
        "# Race dates and Eastern broadcast times from Wikipedia (see tools/gen_indycar_yaml.py).\n"
        "# Each Race start is stored in the circuit's local zone.\n"
        "# Rounds with no published ET yet use start: TBA (all-day placeholder).\n"
        "#\n"
        "series: IndyCar Series\n"
        "slug: indycar\n"
        "calendar_name: IndyCar 2026\n"
        "description: NTT IndyCar Series 2026 (all sessions in track-local time)\n"
        "timezone_default: America/New_York\n"
        "\n"
        "watch_default:\n"
        "  us_broadcast: FOX / FS1\n"
        "  us_streaming: FOX Sports app / IndyCar Live\n"
        "  confidence: high\n"
        "  notes: FOX holds exclusive US linear rights for IndyCar (multi-year deal incl. 2026).\n"
        "\n"
        "rounds:\n",
    ]
    for row in ROUNDS:
        rnd, d_iso, title, short, circuit, loc, tz, tim = row
        lines.append(f"  - round: {rnd}\n")
        lines.append(f"    name: {title}\n")
        lines.append(f"    short_name: {short}\n")
        lines.append(f"    circuit: {circuit}\n")
        lines.append(f"    location: {loc}\n")
        lines.append(f"    tz: {tz}\n")
        lines.append("    sessions:\n")
        if tim is None:
            lines.append("      - type: Race\n        start: TBA\n        duration_minutes: 120\n")
        else:
            naive = et_to_naive_local(d_iso, tim, tz)
            lines.append(f"      - type: Race\n        start: {naive}\n        duration_minutes: 120\n")
    out.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
