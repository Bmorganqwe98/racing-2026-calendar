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

## Privacy checklist (one-time GitHub setup)

You only need to do this once per GitHub account. Each link goes straight
to the relevant settings page — you don't need to remember any paths.

### Account-level (protects every repo, not just this one)

- [ ] **Keep my email addresses private** — [github.com/settings/emails](https://github.com/settings/emails). Tick this checkbox so commits expose only your `…@users.noreply.github.com` address, never your real one.
- [ ] **Block command line pushes that expose my email** — same page, second checkbox. This is the seatbelt: if any future commit ever has your real email on it, GitHub refuses to accept the push instead of letting it leak.
- [ ] **Two-factor authentication enabled** — [github.com/settings/security](https://github.com/settings/security). If your password ever leaks, 2FA is what stops someone else logging in.

### Repository-level (this repo only)

- [ ] **Disable Issues** — [Settings → General](https://github.com/Bmorganqwe98/racing-2026-calendar/settings) → scroll to **Features** → uncheck **Issues**. Personal calendar repos don't need a public bug tracker.
- [ ] **Disable Wikis** — same Features section → uncheck **Wikis**. Unused, just an extra surface to maintain.
- [ ] **Disable Projects** — same Features section → uncheck **Projects**. Unused.
- [ ] **Confirm Pages source is "GitHub Actions"** — [Settings → Pages](https://github.com/Bmorganqwe98/racing-2026-calendar/settings/pages). Should already be set; re-verify if you ever rename the repo.
- [ ] **(Optional)** Disable forking — [Settings → General](https://github.com/Bmorganqwe98/racing-2026-calendar/settings) → uncheck **Allow forking**. Forks aren't a privacy issue (they only copy public content), but turning this off makes the repo slightly less discoverable.

After ticking these, your repo's public face shows only: code, the Pages
site, and the README. No issues page, no wiki, no project boards.

## Pre-push privacy checklist (every time you push)

Two terminal commands; takes about 5 seconds.

```bash
# 1) Confirm git identity for this repo is still anonymized.
git config --local user.email
# expected: 219371880+Bmorganqwe98@users.noreply.github.com

# 2) Confirm the most recent commit's author is anonymized.
git log -1 --format="%an <%ae>"
# expected: Bmorganqwe98 <219371880+Bmorganqwe98@users.noreply.github.com>
```

If either output ever shows your real name, or any email address other
than the `…@users.noreply.github.com` form, **do not push**. Re-set the
local config and amend the commit:

```bash
git config --local user.name  "Bmorganqwe98"
git config --local user.email "219371880+Bmorganqwe98@users.noreply.github.com"
git commit --amend --reset-author --no-edit
```

The "Block command line pushes that expose my email" account setting is
your safety net: even if you forget to check, GitHub will refuse the push
instead of leaking the real email.

## Privacy and use intent

This project is published publicly **only because GitHub Pages requires a
public repo for free `.ics` subscription URLs**, not because the contents
are meant for general distribution. It is a **personal-use calendar**: I
publish it for myself, and anyone who happens to find it is welcome to
subscribe, but the project is not advertised, not maintained on a service
schedule, and not built for resale or any commercial purpose.

What is and is not exposed:

| Visible to anyone on the internet | Not exposed |
|---|---|
| The Python source (`generate.py`), the YAML schedules (`data/*.yaml`), and the published `.ics` files at the GitHub Pages URL | The author's real name and real email — commits use a GitHub no-reply address (see below) |
| The repository name, the commit history, and any text inside committed files | The author's other projects, GitHub private repos, account email, or billing info |
| The published HTML landing page | Anything placed in `.gitignore` (output cache, OneDrive Cursor state, local test caches, etc.) |

If you fork this repo for your own personal calendar:

1. Replace `Bmorganqwe98` and the no-reply email in `generate.py` and any
   subscribe URLs with your own.
2. **Do not paste any personal information** (real name, address, phone,
   email, etc.) into `data/*.yaml`, `NOTES.md`, or any committed file —
   public Pages means anyone can read those.
3. Consider enabling **GitHub → Settings → Emails → "Keep my email
   addresses private"** and **"Block command line pushes that expose my
   email"** before your first push. This is free and prevents accidental
   email leaks.

## License

[MIT](LICENSE) — covers the code only. The published `.ics` schedules are
public information sourced from official series sites and Wikipedia.

The MIT license technically permits commercial reuse of the code; if that
matters to you and you'd prefer a non-commercial-only stance, swap it for
a license like CC BY-NC-4.0 (with caveats: NC licenses are sometimes
incompatible with code-hosting platforms and the definition of "commercial"
is fuzzy). For personal use, MIT is fine and is the project default.
