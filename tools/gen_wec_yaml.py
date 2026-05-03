"""
Generate data/wec.yaml — 2026 FIA WEC calendar (race anchors).

Round dates from Wikipedia; green-flag times are provisional midday / typical WEC
anchors on that calendar date (medium confidence — expand to full FP/Q/Hyperpole/Race
once official bulletins are wired in).

Source: https://en.wikipedia.org/wiki/2026_FIA_World_Endurance_Championship (retrieved 2026-05-03).
Official calendar moves (e.g. Qatar postponement) cross-checked to FIA WEC news:
https://www.fiawec.com/en/news/qatar-1812km-postponed-season-to-start-at-imola/11933
"""

from __future__ import annotations

from pathlib import Path

ROUNDS = [
    (
        1,
        "6 Hours of Imola",
        "Imola 6h",
        "Imola Circuit",
        "Imola, Italy",
        "Europe/Rome",
        "2026-04-19T12:45",
        360,
    ),
    (
        2,
        "6 Hours of Spa-Francorchamps",
        "Spa 6h",
        "Circuit de Spa-Francorchamps",
        "Stavelot, Belgium",
        "Europe/Brussels",
        "2026-05-09T12:45",
        360,
    ),
    (
        3,
        "24 Hours of Le Mans",
        "Le Mans 24h",
        "Circuit de la Sarthe",
        "Le Mans, France",
        "Europe/Paris",
        "2026-06-13T16:00",
        1440,
    ),
    (
        4,
        "6 Hours of São Paulo",
        "São Paulo 6h",
        "Interlagos Circuit",
        "São Paulo, Brazil",
        "America/Sao_Paulo",
        "2026-07-12T11:30",
        360,
    ),
    (
        5,
        "Lone Star Le Mans",
        "COTA 6h",
        "Circuit of The Americas",
        "Austin, Texas, USA",
        "America/Chicago",
        "2026-09-06T13:00",
        360,
    ),
    (
        6,
        "6 Hours of Fuji",
        "Fuji 6h",
        "Fuji Speedway",
        "Oyama, Shizuoka, Japan",
        "Asia/Tokyo",
        "2026-09-27T11:00",
        360,
    ),
    (
        7,
        "Qatar 1812 km",
        "Qatar 1812 km",
        "Lusail International Circuit",
        "Lusail, Qatar",
        "Asia/Qatar",
        "2026-10-24T14:00",
        720,
    ),
    (
        8,
        "8 Hours of Bahrain",
        "Bahrain 8h",
        "Bahrain International Circuit",
        "Sakhir, Bahrain",
        "Asia/Bahrain",
        "2026-11-07T14:00",
        480,
    ),
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    out = root / "data" / "wec.yaml"
    lines = [
        "# FIA World Endurance Championship — 2026 schedule\n"
        "# Race anchors from Wikipedia + FIA WEC calendar news (see file header in tools/gen_wec_yaml.py).\n"
        "#\n"
        "series: World Endurance Championship\n"
        "slug: wec\n"
        "calendar_name: WEC 2026\n"
        "description: FIA World Endurance Championship 2026 (track-local time)\n"
        "timezone_default: UTC\n"
        "\n"
        "watch_default:\n"
        "  us_broadcast: MAX (B/R Sports tier)\n"
        "  us_streaming: MAX / FIA WEC App\n"
        "  confidence: high\n"
        "  notes: Warner Bros. Discovery / MAX carries WEC in the US; verify race listings on MAX.\n"
        "\n"
        "rounds:\n",
    ]
    for rnd, name, short, circuit, loc, tz, start, dur in ROUNDS:
        lines.append(f"  - round: {rnd}\n")
        lines.append(f"    name: {name}\n")
        lines.append(f"    short_name: {short}\n")
        lines.append(f"    circuit: {circuit}\n")
        lines.append(f"    location: {loc}\n")
        lines.append(f"    tz: {tz}\n")
        lines.append("    sessions:\n")
        lines.append(
            f"      - type: Race\n        start: {start}\n        duration_minutes: {dur}\n\n"
        )
    out.write_text("".join(lines), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
