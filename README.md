# Racing 2026 ICS Calendar

A self-updating calendar of every session — practice, qualifying, sprint,
race — for the 2026 seasons of **F1, F2, WEC, IMSA, IndyCar, and WRC**, all
in correct track-local time zones, published to GitHub Pages so your Google
Calendar (or Apple/Outlook) subscribes once and refreshes itself.

> Subscribe to one URL per series; once you've added it, you never have to
> re-import anything. Edit the YAML, push to `main`, and your calendar
> updates on its next refresh.

---

## Subscribe (the only section most people need)

Once this repo is deployed to GitHub Pages, your subscribe URLs will be:

| Calendar | URL |
|----------|-----|
| F1       | `https://Bmorganqwe98.github.io/racing-2026-calendar/f1.ics` |
| F2       | `https://Bmorganqwe98.github.io/racing-2026-calendar/f2.ics` |
| WEC      | `https://Bmorganqwe98.github.io/racing-2026-calendar/wec.ics` |
| IMSA     | `https://Bmorganqwe98.github.io/racing-2026-calendar/imsa.ics` |
| IndyCar  | `https://Bmorganqwe98.github.io/racing-2026-calendar/indycar.ics` |
| WRC      | `https://Bmorganqwe98.github.io/racing-2026-calendar/wrc.ics` |
| All series combined | `https://Bmorganqwe98.github.io/racing-2026-calendar/racing-2026.ics` |

After you push and deploy, the same list with one-click subscribe links is
also rendered at `https://Bmorganqwe98.github.io/racing-2026-calendar/`.

### Google Calendar

1. Copy one of the URLs above.
2. In Google Calendar's left sidebar: **Other calendars → `+` → From URL**.
3. Paste the URL → **Add calendar**.
4. Repeat per series you want. Each appears as its own color-coded calendar
   you can toggle on/off in the sidebar.

Google Calendar refreshes subscribed feeds on its own schedule — typically
every **8 to 24 hours**. There's no setting to make it faster, but you can
force an early refresh with the calendar's three-dot menu → **Refresh**.

### Apple Calendar / Outlook

Both poll subscribed URLs more aggressively than Google does (every 5 min
to a few hours, depending on your settings). Subscribe via **File → New
Calendar Subscription** (Apple) or **Add calendar → Subscribe from web**
(Outlook).

### Why "subscribe" instead of "import"?

Importing copies events once and then they're frozen. Subscribing means
your calendar auto-refreshes whenever the source `.ics` updates — which is
how a 2026 calendar full of "TBA" sessions gradually fills in with real
times throughout the season without you having to do anything.

### Time zones — what you'll actually see

Every session is stored in **track-local** time inside the `.ics` (so the
Australian GP race carries an `Australia/Melbourne` time zone, the Rolex 24
carries `America/New_York`, Le Mans carries `Europe/Paris`, etc.). When you
subscribe, Google Calendar reads that information and **automatically
converts each event to your account's time zone**. You don't have to set
anything.

Worked example for an EST viewer:

| Session | Stored as | Shown in your EST calendar |
|---------|-----------|---------------------------|
| F1 Australian GP — Race  | Sun Mar 8, 15:00 Australia/Melbourne | Sat Mar 7, 11:00 PM EST |
| IMSA Rolex 24 — Race start | Sat Jan 24, 13:40 America/New_York | Sat Jan 24, 1:40 PM EST |
| WEC Le Mans 24h — start (when added) | Sat Jun 13, 16:00 Europe/Paris | Sat Jun 13, 10:00 AM EST |
| WRC Monte-Carlo — Day 2 | Fri Jan 23, 08:00 Europe/Monaco | Fri Jan 23, 2:00 AM EST |

If you ever travel to a different time zone and update Google Calendar's
zone setting, every event re-displays in that new zone automatically.
There's nothing in the `.ics` itself locked to any one zone.

---

## Develop / regenerate locally

You only need this section if you want to edit schedules or run the
generator yourself.

### Setup

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Python 3.11 is recommended (matches CI). 3.10+ should also work.

### Regenerate

```bash
python generate.py
# -> output/f1.ics, f2.ics, wec.ics, imsa.ics, indycar.ics, wrc.ics
# -> output/racing-2026.ics (combined)
# -> output/index.html (landing page)
# -> output/.nojekyll
```

The `output/` folder is gitignored — GitHub Actions regenerates it fresh
on every deploy, so you never need to commit those files.

### Run tests

```bash
pip install pytest
pytest -q
```

### Edit a schedule

1. Open `data/<series>.yaml`.
2. Adjust the offending session's `start` (naive local time, ISO 8601) or
   `duration_minutes`.
3. Run `python generate.py` to preview.
4. Update `NOTES.md` with the source URL and retrieval date for the change.
5. Commit and push. GitHub Actions deploys automatically.

See [`.cursor/rules/racing-project-context.mdc`](.cursor/rules/racing-project-context.mdc)
for the full schema and conventions, and [`NOTES.md`](NOTES.md) for the
provenance log.

---

## How deploys work

```
edit data/<series>.yaml -> git push origin main
                                |
                                v
               .github/workflows/deploy.yml runs:
               1. pip install -r requirements.txt
               2. pytest -q
               3. python generate.py
               4. upload output/ to GitHub Pages
                                |
                                v
        https://Bmorganqwe98.github.io/racing-2026-calendar/<series>.ics
                                |
                                v
        Google Calendar refreshes on its next poll (~8-24h)
```

One-time setup on the GitHub side: **Settings → Pages → Source = GitHub
Actions**. After the first push to `main` the workflow runs, the URL goes
live, and you're done.

---

## Privacy

GitHub Pages is public. The 2026 motorsport schedule isn't sensitive data,
but anything you put into `data/*.yaml` is publicly viewable. Don't paste
private information into the YAML.

## License

[MIT](LICENSE) — do whatever you like with the code or the schedules.
