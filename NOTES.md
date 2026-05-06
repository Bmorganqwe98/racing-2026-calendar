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
        date_hint: <YYYY-MM-DD, optional; used when start is TBA>
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
| F1 | high | ESPN / Formula One US broadcast partnership + official where-to-watch pages | 2026-05-03 | mid-season |
| F2 | medium | FIA Formula 2 on F1 TV Pro (support championship) | 2026-05-06 | before first round with official weekend listings |
| WEC | high | Warner Bros. Discovery / MAX US motorsport stacks | 2026-05-03 | mid-season |
| IMSA | medium | NBCUniversal IMSA rights announcement / Peacock stacks | 2026-05-06 | before each IMSA race weekend |
| IndyCar | high | Fox Corporation IndyCar US rights (2025–2030 extension press pattern) | 2026-05-03 | mid-season |
| WRC | high | Rally.tv as FIA WRC global streaming provider | 2026-05-03 | mid-season |

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

**Status:** Full **22-round** calendar (Bahrain / Saudi Arabia omitted — not on the official 2026 F1 calendar as published on formula1.com at retrieval time).

| Source | URL | Retrieved |
|--------|-----|-----------|
| Official race calendar (order + weekend dates) | https://www.formula1.com/en/racing/2026 | 2026-05-03 |
| Session start times | Each event page `application/ld+json` SportsEvent → subEvent `startDate` (UTC), converted to circuit zone via `tools/build_f1_yaml_snippet.py` | 2026-05-03 |

**Confidence:** **high** for session times (straight from Formula 1’s published structured data).

**Editorial decisions:**

- Sprint weekends (6 rounds: China, Miami, Canada, UK, Netherlands, Singapore) follow the sprint layout returned by the official JSON-LD for each event.
- Spanish GP round uses the Madrid / **Madring** venue per the official **Spain** event slug on formula1.com (`/spain`), distinct from the **Barcelona-Catalunya** round (`/barcelona-catalunya`).

---

## F2 — FIA Formula 2 Championship 2026

**Status:** Full **14-round** calendar with **accuracy-first placeholders** (`start: TBA` + `date_hint`) for all sessions until official weekend session times are posted.

| Source | URL | Retrieved |
|--------|-----|-----------|
| Calendar table (sprint / feature dates + circuits) | https://en.wikipedia.org/wiki/2026_Formula_2_Championship | 2026-05-03 |
| Official season calendar summary | https://www.fiaformula2.com/Calendar | 2026-05-06 |

**Confidence:** **medium** for exact clock times (dates are sourced; clock times intentionally held as TBA until officially published per event).

**Editorial decisions:**

- **Baku:** sprint scheduled Friday / feature Saturday per calendar note; date hints preserve the Thursday/Friday/Saturday sequence while exact times remain TBA.

---

## WEC — FIA World Endurance Championship 2026

**Status:** Full **8-round** calendar with **race-only** sessions using `start: TBA` + `date_hint` (no FP/Q/Hyperpole breakdown yet).

| Source | URL | Retrieved |
|--------|-----|-----------|
| Calendar + round list | https://en.wikipedia.org/wiki/2026_FIA_World_Endurance_Championship | 2026-05-03 |
| Qatar postponement / Imola season opener | https://www.fiawec.com/en/news/qatar-1812km-postponed-season-to-start-at-imola/11933 | 2026-05-03 |

**Confidence:** **medium** for race green-flag times (race dates are sourced; exact local start times are intentionally TBA until bulletin confirmation).

**Editorial decisions:**

- **Le Mans** remains one long `Race` session with `duration_minutes: 1440`; `date_hint` anchors the all-day placeholder on race weekend without pretending to know a precise start.

---

## IMSA — IMSA WeatherTech SportsCar Championship 2026

**Status:** Full **11-round** WeatherTech calendar with accuracy-first placeholders for race start times.

| Source | URL | Retrieved |
|--------|-----|-----------|
| Official WeatherTech schedule | https://www.imsa.com/weathertech/weathertech-2026-schedule/ | 2026-05-06 |
| Cross-check calendar table | https://en.wikipedia.org/wiki/2026_IMSA_SportsCar_Championship | 2026-05-03 |

**Confidence:** **medium** for exact race/qualifying clock times (IMSA schedule provides event windows/durations; YAML now uses TBA + date_hint to avoid false precision).

**Editorial decisions:**

- Endurance lengths are kept from published event durations (`24h`, `12h`, `6h`, etc.) while exact green flags remain TBA.

---

## IndyCar — NTT IndyCar Series 2026

**Status:** Full **18-round** calendar; **Race-only** sessions (no practice blocks yet).

| Source | URL | Retrieved |
|--------|-----|-----------|
| Official schedule + ET broadcast times | https://www.indycar.com/Schedule | 2026-05-06 |
| Cross-check ET table | https://en.wikipedia.org/wiki/2026_IndyCar_Series | 2026-05-03 |

**Confidence:** **high** for rounds with published ET times on the official schedule (converted to track-local wall time in `tools/gen_indycar_yaml.py`). **TBA** rounds: Nashville (July 19) and Washington DC Freedom 250 now include `date_hint` so all-day placeholders anchor on the correct date.

**Editorial decisions:**

- Times are interpreted as US **Eastern** where the table says “Time (ET)”, then converted to each venue’s IANA zone.

---

## WRC — FIA World Rally Championship 2026

**Status:** Full **14-round** calendar with **collapsed** multi-day sessions and accuracy-first `start: TBA` + `date_hint`.

| Source | URL | Retrieved |
|--------|-----|-----------|
| Calendar (dates + HQ + surfaces) | https://en.wikipedia.org/wiki/2026_World_Rally_Championship | 2026-05-03 |

**Confidence:** **medium** for intraday timing — dates are sourced, but all collapsed sessions intentionally remain TBA pending official stage-by-stage publications.

**Editorial decisions:**

- Per-rally stages remain **collapsed** to `Shakedown / Day 1 / … / Podium` per `.cursor/rules/racing-project-context.mdc`.
- Estonia / Paraguay / Chile / Sardegna / Saudi Arabia stage distances were still **TBA** on Wikipedia at retrieval — calendar dates are still honored via `date_hint`.

---

## CHANGELOG (UID-affecting / breaking changes)

UID changes break subscribers' deduplication and effectively re-publish
every event. Record them here with date and reason so we can warn
subscribers if it ever happens.

### 2026-05-03 — Season-wide YAML expansion

- All six series files were expanded from single-round **scaffolding** to **full published calendars** (see per-series sections above).
- **Net-new sessions** (every round beyond the former single stub round) generate **new UIDs** on first subscribe — expected.
- Where round **1** session types and times still match the old stub (e.g. F1 Australian GP), those **UIDs are unchanged** so existing subscribers update in place for that overlap.

### 2026-05-06 — Accuracy-first TBA placeholder pass

- Added `date_hint` schema support and generator behavior for TBA sessions, so all-day placeholders anchor on the correct race/rally date instead of the Jan 1 fallback.
- Converted uncertain exact times to `start: TBA` + `date_hint` in F2, IMSA, WEC, and WRC data.
- IndyCar retained official published ET-derived starts where available; existing TBA rounds now include `date_hint`.
- UID stability preserved by keeping existing `type` strings unchanged.

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
