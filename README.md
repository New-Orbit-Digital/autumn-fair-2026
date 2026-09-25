# Autumn Fair 2026 — Volunteer Tracker

A single-page volunteer tracker for the Emerson Waldorf School Autumn Fair (Nov 7, 2026), run by the Parent Teacher Collaborative. It lists every Fair task with its deadline, headcount target and sign-ups, shows what still needs people, and lets parents raise a hand for a task.

Live: https://justbost.com/autumn-fair-2026/ (unlisted — `noindex,nofollow`)

## How it works

- `index.html` is the whole app: vanilla JS and inline CSS, no build step. Fonts (Fraunces, Montserrat) load from Google Fonts.
- Data is read at page load from a Google Sheet (the PTC-owned `autumn-fair-tracker-sheet`) through an Apps Script web app (`DATA_ENDPOINT`). The same web app receives "I can help" sign-ups by POST; if that fails, the page falls back to a pre-written email to the PTC address.
- To change tasks, owners, targets or statuses, **edit the sheet**, not this file.
- If the sheet can't be reached, the page shows a built-in snapshot under an amber banner. **In this repo that snapshot has had all volunteer and personal names removed**, so the offline view shows every task as unfilled. Names only ever come from the live sheet at runtime.

## Privacy

This repo is public. Do not commit volunteer names, emails, or a refreshed snapshot that contains either. `screenshot.png` uses made-up placeholder names: `tools/screenshot.py` captures it with the sheet request mocked (`pip install playwright && playwright install chromium`, then `python tools/screenshot.py`).

## Hosting

GitHub Pages from `main` / root, served under the org domain at `/autumn-fair-2026/`. All paths are relative; the only external assets are the Google Fonts stylesheet and the Apps Script data endpoint. The old Netlify site (ews-af26-dashboard.netlify.app) stays up only to serve a 301 redirect here.

## Verification

| Date | Check | Result |
|---|---|---|
| 2026-09-25 | Local headless Chromium render of `index.html` with the sheet endpoint mocked | Rendered, "Live from the sheet" stamp shown, no script errors |
| 2026-09-25 | Scan of source for volunteer names and personal emails | Snapshot owners empty; personal first names in task text replaced with roles; only email is the PTC role address |
| 2026-09-25 | Pushed `index.html` (commit f8a3aad) vs. prepared local file | Byte-identical, SHA-1 1050e598555f3138b0f914c9ec9327032b41e0e2 |
| 2026-09-25 | https://justbost.com/autumn-fair-2026/ served by Pages | Loads; title "Autumn Fair 2026 — Volunteer Tracker"; robots meta `noindex,nofollow` present. `screenshot.png` present on `main` (HTTP 200) |
| pending | Live sheet read in a real browser on justbost.com ("Live from the sheet" stamp, no amber banner) | — (fetch tool used does not run JS) |
| pending | `curl -I` on https://ews-af26-dashboard.netlify.app/ returns 301 → justbost.com/autumn-fair-2026/ | — |
