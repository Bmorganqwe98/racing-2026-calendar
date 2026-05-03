"""
Generate data/imsa.yaml from the Wikipedia 2026 IMSA WeatherTech schedule.

Session times for sprint rounds use typical afternoon green-flag anchors on the
listed calendar date (medium confidence — confirm on imsa.com before treating as final).

Endurance rounds include a single Race session spanning the published duration.

Source: https://en.wikipedia.org/wiki/2026_IMSA_SportsCar_Championship (retrieved 2026-05-03).
"""

from __future__ import annotations

from pathlib import Path

ROUNDS = [
    # rnd, name, short, circuit, location, tz, sessions_yaml_lines
    (
        1,
        "Rolex 24 at Daytona",
        "Rolex 24",
        "Daytona International Speedway",
        "Daytona Beach, Florida, USA",
        "America/New_York",
        """      - type: Qualifying
        start: 2026-01-23T15:30
        duration_minutes: 60
      - type: Race
        start: 2026-01-24T13:40
        duration_minutes: 1440""",
    ),
    (
        2,
        "Mobil 1 Twelve Hours of Sebring",
        "Sebring 12h",
        "Sebring International Raceway",
        "Sebring, Florida, USA",
        "America/New_York",
        """      - type: Race
        start: 2026-03-21T10:10
        duration_minutes: 720""",
    ),
    (
        3,
        "Acura Grand Prix of Long Beach",
        "Long Beach GP",
        "Long Beach Street Circuit",
        "Long Beach, California, USA",
        "America/Los_Angeles",
        """      - type: Race
        start: 2026-04-18T14:10
        duration_minutes: 100""",
    ),
    (
        4,
        "StubHub Monterey SportsCar Championship",
        "Laguna Seca GP",
        "WeatherTech Raceway Laguna Seca",
        "Monterey, California, USA",
        "America/Los_Angeles",
        """      - type: Race
        start: 2026-05-03T14:10
        duration_minutes: 160""",
    ),
    (
        5,
        "Chevrolet Detroit Sports Car Classic",
        "Detroit GP",
        "Detroit Street Circuit",
        "Detroit, Michigan, USA",
        "America/New_York",
        """      - type: Race
        start: 2026-05-30T14:10
        duration_minutes: 100""",
    ),
    (
        6,
        "Sahlen's Six Hours of The Glen",
        "Watkins Glen 6h",
        "Watkins Glen International",
        "Watkins Glen, New York, USA",
        "America/New_York",
        """      - type: Race
        start: 2026-06-28T10:10
        duration_minutes: 360""",
    ),
    (
        7,
        "Chevrolet Grand Prix",
        "CTMP GP",
        "Canadian Tire Motorsport Park",
        "Bowmanville, Ontario, Canada",
        "America/Toronto",
        """      - type: Race
        start: 2026-07-12T14:10
        duration_minutes: 160""",
    ),
    (
        8,
        "Motul SportsCar Endurance Grand Prix",
        "Road America 6h",
        "Road America",
        "Elkhart Lake, Wisconsin, USA",
        "America/Chicago",
        """      - type: Race
        start: 2026-08-02T10:10
        duration_minutes: 360""",
    ),
    (
        9,
        "Michelin GT Challenge at VIR",
        "VIR GT Challenge",
        "Virginia International Raceway",
        "Alton, Virginia, USA",
        "America/New_York",
        """      - type: Race
        start: 2026-08-23T14:10
        duration_minutes: 160""",
    ),
    (
        10,
        "Tirerack.com Battle on the Bricks",
        "Indianapolis GP",
        "Indianapolis Motor Speedway",
        "Speedway, Indiana, USA",
        "America/Indiana/Indianapolis",
        """      - type: Race
        start: 2026-09-20T14:10
        duration_minutes: 160""",
    ),
    (
        11,
        "Motul Petit Le Mans",
        "Petit Le Mans",
        "Michelin Raceway Road Atlanta",
        "Braselton, Georgia, USA",
        "America/New_York",
        """      - type: Race
        start: 2026-10-03T11:10
        duration_minutes: 600""",
    ),
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "imsa.yaml"
    parts = [
        "# IMSA WeatherTech SportsCar Championship — 2026 schedule\n"
        "# See tools/gen_imsa_yaml.py for how race anchors were chosen.\n"
        "#\n"
        "series: IMSA SportsCar Championship\n"
        "slug: imsa\n"
        "calendar_name: IMSA 2026\n"
        "description: IMSA WeatherTech SportsCar Championship 2026 (all sessions in track-local time)\n"
        "timezone_default: America/New_York\n"
        "\n"
        "watch_default:\n"
        "  us_broadcast: NBC / USA Network\n"
        "  us_streaming: Peacock / IMSA.tv (free for practice and qualifying)\n"
        "  confidence: high\n"
        "  notes: NBCUniversal holds US IMSA rights; confirm race vs USA Network per weekend.\n"
        "\n"
        "rounds:\n"
    ]
    for rnd, name, short, circuit, loc, tz, sess in ROUNDS:
        parts.append(
            f"  - round: {rnd}\n"
            f"    name: {name}\n"
            f"    short_name: {short}\n"
            f"    circuit: {circuit}\n"
            f"    location: {loc}\n"
            f"    tz: {tz}\n"
            f"    sessions:\n{sess}\n\n"
        )
    out.write_text("".join(parts), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
