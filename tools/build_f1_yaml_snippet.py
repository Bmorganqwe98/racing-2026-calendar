"""Emit full data/f1.yaml rounds section by querying formula1.com JSON-LD."""
from __future__ import annotations

import json
import re
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo

# slug, IANA tz, round display name, short_name, circuit, location
ROUNDS = [
    (1, "australia", "Australia/Melbourne", "Australian Grand Prix", "Australian GP", "Albert Park Circuit", "Melbourne, Australia"),
    (2, "china", "Asia/Shanghai", "Chinese Grand Prix", "Chinese GP", "Shanghai International Circuit", "Shanghai, China"),
    (3, "japan", "Asia/Tokyo", "Japanese Grand Prix", "Japanese GP", "Suzuka International Racing Course", "Suzuka, Japan"),
    (4, "miami", "America/New_York", "Miami Grand Prix", "Miami GP", "Miami International Autodrome", "Miami Gardens, Florida, USA"),
    (5, "canada", "America/Toronto", "Canadian Grand Prix", "Canadian GP", "Circuit Gilles Villeneuve", "Montreal, Canada"),
    (6, "monaco", "Europe/Monaco", "Monaco Grand Prix", "Monaco GP", "Circuit de Monaco", "Monte Carlo, Monaco"),
    (7, "barcelona-catalunya", "Europe/Madrid", "Barcelona-Catalunya Grand Prix", "Barcelona-Catalunya GP", "Circuit de Barcelona-Catalunya", "Montmeló, Spain"),
    (8, "austria", "Europe/Vienna", "Austrian Grand Prix", "Austrian GP", "Red Bull Ring", "Spielberg, Austria"),
    (9, "great-britain", "Europe/London", "British Grand Prix", "British GP", "Silverstone Circuit", "Silverstone, UK"),
    (10, "belgium", "Europe/Brussels", "Belgian Grand Prix", "Belgian GP", "Circuit de Spa-Francorchamps", "Stavelot, Belgium"),
    (11, "hungary", "Europe/Budapest", "Hungarian Grand Prix", "Hungarian GP", "Hungaroring", "Mogyoród, Hungary"),
    (12, "netherlands", "Europe/Amsterdam", "Dutch Grand Prix", "Dutch GP", "Circuit Zandvoort", "Zandvoort, Netherlands"),
    (13, "italy", "Europe/Rome", "Italian Grand Prix", "Italian GP", "Monza Circuit", "Monza, Italy"),
    (14, "spain", "Europe/Madrid", "Spanish Grand Prix", "Spanish GP", "Madring / Madrid street circuit", "Madrid, Spain"),
    (15, "azerbaijan", "Asia/Baku", "Azerbaijan Grand Prix", "Azerbaijan GP", "Baku City Circuit", "Baku, Azerbaijan"),
    (16, "singapore", "Asia/Singapore", "Singapore Grand Prix", "Singapore GP", "Marina Bay Street Circuit", "Singapore"),
    (17, "united-states", "America/Chicago", "United States Grand Prix", "United States GP", "Circuit of The Americas", "Austin, Texas, USA"),
    (18, "mexico", "America/Mexico_City", "Mexico City Grand Prix", "Mexico City GP", "Autódromo Hermanos Rodríguez", "Mexico City, Mexico"),
    (19, "brazil", "America/Sao_Paulo", "São Paulo Grand Prix", "São Paulo GP", "Interlagos Circuit", "São Paulo, Brazil"),
    (20, "las-vegas", "America/Los_Angeles", "Las Vegas Grand Prix", "Las Vegas GP", "Las Vegas Strip Circuit", "Las Vegas, Nevada, USA"),
    (21, "qatar", "Asia/Qatar", "Qatar Grand Prix", "Qatar GP", "Lusail International Circuit", "Lusail, Qatar"),
    (22, "united-arab-emirates", "Asia/Dubai", "Abu Dhabi Grand Prix", "Abu Dhabi GP", "Yas Marina Circuit", "Abu Dhabi, UAE"),
]


def fetch_html(slug: str) -> str:
    url = f"https://www.formula1.com/en/racing/2026/{slug}"
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; racing-ics-calendar/1.0)"},
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        return resp.read().decode("utf-8", errors="replace")


def iter_session_events(html: str):
    blocks = re.findall(
        r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    for raw in blocks:
        raw = raw.strip()
        if not raw:
            continue
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(data, dict) or data.get("@type") != "SportsEvent":
            continue
        for sub in data.get("subEvent") or []:
            if isinstance(sub, dict) and sub.get("startDate"):
                yield sub


def session_label(name: str) -> str:
    n = name.lower()
    if "practice 1" in n:
        return "FP1"
    if "practice 2" in n:
        return "FP2"
    if "practice 3" in n:
        return "FP3"
    if "sprint qualifying" in n:
        return "Sprint Qualifying"
    if "sprint" in n and "qualifying" not in n:
        return "Sprint"
    if "qualifying" in n and "sprint" not in n:
        return "Qualifying"
    if "race" in n and "sprint" not in n:
        return "Race"
    return "Session"


def sessions_yaml(slug: str, tz_name: str) -> str:
    tz = ZoneInfo(tz_name)
    html = fetch_html(slug)
    events = sorted(iter_session_events(html), key=lambda e: e.get("startDate", ""))
    lines = []
    for ev in events:
        start_s = ev.get("startDate")
        if not start_s:
            continue
        label = session_label(str(ev.get("name", "")))
        start = datetime.fromisoformat(start_s.replace("Z", "+00:00"))
        local = start.astimezone(tz)
        lines.append(
            f"      - type: {label}\n"
            f"        start: {local.strftime('%Y-%m-%dT%H:%M')}"
        )
    return "\n".join(lines)


def main() -> None:
    print("# Generated by tools/build_f1_yaml_snippet.py — paste into data/f1.yaml")
    for num, slug, tz, full_name, short_name, circuit, loc in ROUNDS:
        print(f"  - round: {num}")
        print(f"    name: {full_name}")
        print(f"    short_name: {short_name}")
        print(f"    circuit: {circuit}")
        print(f"    location: {loc}")
        print(f"    tz: {tz}")
        print(f"    sessions:")
        try:
            body = sessions_yaml(slug, tz)
            print(body)
        except Exception as e:
            print(f"      # ERROR {slug}: {e}")
        print()


if __name__ == "__main__":
    main()
