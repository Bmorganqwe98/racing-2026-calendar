# NOTES.md — Provenance, Decisions, and Continuity Log

This file is the project's long-term memory. Every change to a `data/<series>.yaml`
schedule should add or update a row in the corresponding section below so future
AI/human sessions know **where the data came from, when, and how confident we are**.

Confidence levels:
- **high** — final calendar published by the official series body.
- **medium** — provisional, official source but flagged "subject to change".
- **low** — rumored, leaked, or extrapolated from an earlier season.

---

## Schema reference (quick)

```yaml
series: <human name>
slug: <lowercase id, used in filenames and UIDs>
calendar_name: <X-WR-CALNAME shown in Google Calendar>
description: <X-WR-CALDESC>
timezone_default: <IANA zone, fallback if a round has no tz>
rounds:
  - round: <int, 1-based>
    name: <full round name>
    short_name: <used in event SUMMARY>
    circuit: <track name>
    location: <City, Country>
    tz: <IANA zone, e.g. Australia/Melbourne>
    sessions:
      - type: <FP1 | Qualifying | Race | Day 1 | ...>
        start: <YYYY-MM-DDTHH:MM naive local>  # or "TBA"
        duration_minutes: <int, optional - see DEFAULT_DURATIONS_MINUTES in generate.py>
```

Stable UIDs follow `{slug}-2026-r{round}-{session-slug}@racing-cal`.
**Do not rename** without bumping subscribers via a CHANGELOG entry below.

---

## F1 — Formula 1 World Championship 2026

**Status:** stub data only — one round (Australian GP) populated for scaffolding.

| Round | Name | Source URL | Retrieved | Confidence | TBA gaps |
|-------|------|-----------|-----------|-----------|----------|
| 1 | Australian Grand Prix | _not yet sourced_ | _pending_ | low | none in stub |
| 2-24 | _not yet populated_ | | | | |

**Editorial decisions:** _none yet._

---

## F2 — FIA Formula 2 Championship 2026

**Status:** stub data only — one round (Sakhir support round) populated.

| Round | Name | Source URL | Retrieved | Confidence | TBA gaps |
|-------|------|-----------|-----------|-----------|----------|
| 1 | Sakhir Round | _not yet sourced_ | _pending_ | low | none in stub |
| 2+ | _not yet populated_ | | | | |

**Editorial decisions:** _none yet._

---

## WEC — FIA World Endurance Championship 2026

**Status:** stub data only — one round (Qatar 1812 km) populated.

| Round | Name | Source URL | Retrieved | Confidence | TBA gaps |
|-------|------|-----------|-----------|-----------|----------|
| 1 | Qatar 1812 km | _not yet sourced_ | _pending_ | low | none in stub |
| 2-8 | _not yet populated_ | | | | |

**Editorial decisions:** _none yet._

---

## IMSA — IMSA WeatherTech SportsCar Championship 2026

**Status:** stub data only — one round (Rolex 24) populated.

| Round | Name | Source URL | Retrieved | Confidence | TBA gaps |
|-------|------|-----------|-----------|-----------|----------|
| 1 | Rolex 24 at Daytona | _not yet sourced_ | _pending_ | low | none in stub |
| 2+ | _not yet populated_ | | | | |

**Editorial decisions:** _none yet._

---

## IndyCar — NTT IndyCar Series 2026

**Status:** stub data only — one round (St Petersburg) populated.

| Round | Name | Source URL | Retrieved | Confidence | TBA gaps |
|-------|------|-----------|-----------|-----------|----------|
| 1 | Firestone Grand Prix of St. Petersburg | _not yet sourced_ | _pending_ | low | none in stub |
| 2+ | _not yet populated_ | | | | |

**Editorial decisions:** _none yet._

---

## WRC — FIA World Rally Championship 2026

**Status:** stub data only — one round (Rallye Monte-Carlo) populated.

| Round | Name | Source URL | Retrieved | Confidence | TBA gaps |
|-------|------|-----------|-----------|-----------|----------|
| 1 | Rallye Monte-Carlo | _not yet sourced_ | _pending_ | low | none in stub |
| 2-14 | _not yet populated_ | | | | |

**Editorial decisions:**

- Per-rally stages are **collapsed** to `Shakedown / Day 1 / Day 2 / Day 3 / Day 4 / Podium`
  rather than per-stage events. Stage-by-stage would produce 20+ events per
  rally × 14 rallies = 280+ entries cluttering subscribers' calendars. Recorded
  in `.cursor/rules/racing-project-context.mdc`.

---

## CHANGELOG (UID-affecting / breaking changes)

UID changes break subscribers' deduplication and effectively re-publish
every event. Record them here with date and reason so we can warn
subscribers if it ever happens.

_None yet._

---

## Data sources to consult during the research phase

| Series | Primary source | Backup |
|--------|----------------|--------|
| F1 | [formula1.com/en/racing/2026.html](https://www.formula1.com/en/racing/2026.html) | Wikipedia: 2026 Formula One World Championship |
| F2 | [fiaformula2.com/Calendar](https://www.fiaformula2.com/Calendar) | Wikipedia: 2026 Formula 2 Championship |
| WEC | [fiawec.com/calendar](https://www.fiawec.com/calendar) | Wikipedia: 2026 FIA World Endurance Championship |
| IMSA | [imsa.com/schedule](https://www.imsa.com/schedule) | Wikipedia: 2026 IMSA SportsCar Championship |
| IndyCar | [indycar.com/Schedule](https://www.indycar.com/Schedule) | Wikipedia: 2026 IndyCar Series |
| WRC | [wrc.com/en/championship/calendar](https://www.wrc.com/en/championship/calendar) | Wikipedia: 2026 World Rally Championship |

When researching, use the project's `wiki-research-tool` MCP for Wikipedia
season pages — it produces structured output that drops cleanly into the
YAML schema.
