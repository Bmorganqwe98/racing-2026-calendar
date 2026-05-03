"""
Fetch formula1.com race-weekend session times from JSON-LD (SportsEvent / subEvent).

startDate values are real UTC; we convert to the circuit IANA zone for YAML.

Usage:
    python tools/fetch_f1_sessions.py miami America/New_York
"""

from __future__ import annotations

import json
import re
import sys
import urllib.request
from datetime import datetime
from zoneinfo import ZoneInfo


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
        if not isinstance(data, dict):
            continue
        if data.get("@type") != "SportsEvent":
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
    if "grand prix" in n or (n.endswith("gp") or " race" in n):
        return "Race"
    if "race" in n and "sprint" not in n:
        return "Race"
    return name[:80]


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python tools/fetch_f1_sessions.py <slug> <IANA_tz>", file=sys.stderr)
        sys.exit(2)
    slug, tz_name = sys.argv[1], sys.argv[2]
    tz = ZoneInfo(tz_name)
    html = fetch_html(slug)
    events = list(iter_session_events(html))
    print(f"# slug={slug} tz={tz_name} sessions={len(events)}")
    for ev in sorted(events, key=lambda e: e.get("startDate", "")):
        start_s = ev.get("startDate")
        name = ev.get("name", "")
        if not start_s:
            continue
        start = datetime.fromisoformat(start_s.replace("Z", "+00:00"))
        local = start.astimezone(tz)
        label = session_label(str(name))
        print(
            f"      - type: {label}\n"
            f"        start: {local.strftime('%Y-%m-%dT%H:%M')}"
        )


if __name__ == "__main__":
    main()
