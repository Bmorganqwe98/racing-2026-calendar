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

# Optional: applies to every session in the series unless that session has its
# own `watch:` block. See "Watch info provenance rules" below.
watch_default:
  us_broadcast: <e.g. "ESPN / ESPN2" or "No US linear TV deal">
  us_streaming: <e.g. "ESPN+ / F1 TV Pro">
  confidence: <high | medium | low>
  notes: <free text, e.g. "ESPN holds US F1 rights through 2026">

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
        watch:                                  # optional per-session override
          us_broadcast: <...>
          us_streaming: <...>
          confidence: <...>
          notes: <...>
```

Stable UIDs follow `{slug}-2026-r{round}-{session-slug}@racing-cal`.
**Do not rename** without bumping subscribers via a CHANGELOG entry below.

---

## Watch info provenance rules

Watch info appears inside every event's DESCRIPTION text (alongside Eastern
time). Subscribers rely on it to know which channel/streaming service
covers each session. To keep that signal honest:

### Confidence levels for `watch_default` / `watch.confidence`

- **high** — verified against the broadcaster's *own* current schedule, OR
  the series' official broadcaster announcement for the 2026 season. Cite
  the URL and retrieval date in the per-series table below.
- **medium** — sourced from Wikipedia's "Television" / "Broadcasting"
  section, the series' own boilerplate ("our broadcast partners include
  ..."), or a renewal of a multi-year deal that nominally covers 2026 but
  hasn't been re-verified for this season specifically. This is the
  default starting point for new series.
- **low** — extrapolated from the previous season, rumor, or "the deal
  hasn't been announced yet." The TBD fallback in `generate.py` is
  effectively `low`.

Promote a watch entry to **high** only after writing down where you
confirmed it. If you cannot show a 2026-specific source, do not mark it
high.

### When to update watch info

- Whenever you confirm broadcaster/streaming changes (new TV deals,
  geo-restrictions, app rebrands).
- Whenever a session-specific override is needed (e.g., a race shifts from
  the default streaming partner to broadcast TV for a specific round).
- Whenever any user reports incorrect watch info — even if the source you
  used said otherwise.

### Per-series watch info status

| Series | `watch_default` confidence | Source | Retrieved | Next verification due |
|--------|----------------------------|--------|-----------|-----------------------|
| F1 | medium | _stub from generic ESPN deal coverage_ | _pending_ | before first 2026 round |
| F2 | medium | _F1 TV Pro by elimination (no US linear TV deal)_ | _pending_ | before first 2026 round |
| WEC | medium | _MAX (B/R Sports) per 2024 acquisition coverage_ | _pending_ | before first 2026 round |
| IMSA | medium | _NBC/Peacock multi-year deal_ | _pending_ | before first 2026 round |
| IndyCar | medium | _Fox 2025+ multi-year takeover_ | _pending_ | before first 2026 round |
| WRC | medium | _Rally.tv as canonical FIA stream (no US TV partner)_ | _pending_ | before first 2026 round |

When you confirm a row, update **all four** of its cells in one edit.
Don't bump confidence to `high` without filling in the source URL and
retrieval date.

### Example: what a `high` confidence row looks like

Once you do the schedule-research phase and confirm a series' broadcaster
deal against a 2026-specific source, the row should look like this (and
the matching `watch_default` block in `data/<series>.yaml` can claim
`confidence: high`):

| Series | `watch_default` confidence | Source | Retrieved | Next verification due |
|--------|----------------------------|--------|-----------|-----------------------|
| F1 (example) | high | <https://www.formula1.com/en/latest/article/where-to-watch-f1-2026.12345> + <https://en.wikipedia.org/wiki/2026_Formula_One_World_Championship#Television> | 2026-02-15 | mid-season (after summer break) |

What makes that row promotable to `high`:

1. **At least one URL points to a 2026-specific announcement.** A 2025
   article that "still applies" is medium, not high. The official series
   site or its 2026 season page is the gold standard; Wikipedia's 2026
   season article is acceptable as a cross-check.
2. **A retrieval date in `yyyy-mm-dd` format**, not "recently" or "early
   2026". Future sessions should be able to tell at a glance whether the
   info is two weeks or two years old.
3. **A concrete next-verification trigger** — typically "before first
   round" while the season hasn't started, then "mid-season" once it
   has, since broadcaster shuffles sometimes happen after the summer
   break.

If a session-level `watch:` override is added (e.g., one race shifts from
streaming to network TV for a specific round), add an editorial note to
that series' "Editorial decisions" section above with the round number,
date of confirmation, and source URL — so future sessions know the
override is intentional and confirmed.

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
