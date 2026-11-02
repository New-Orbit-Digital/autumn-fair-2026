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

GitHub Pages from `main` / root, served under the org domain at `/autumn-fair-2026/`. All paths are relative; the only external assets are the Google Fonts stylesheet and the Apps Script data endpoint. The old Netlify site (ews-af26-dashboard.netlify.app) stays up only to serve a redirect here: its deploy is `_redirects` (`/*  https://justbost.com/autumn-fair-2026/:splat  301!`) plus an `index.html`/`404.html` that also redirect. Don't delete that Netlify site.

## Verification

| Date | Check | Result |
|---|---|---|
| 2026-09-25 | Local headless Chromium render of `index.html` with the sheet endpoint mocked | Rendered, "Live from the sheet" stamp shown, no script errors |
| 2026-09-25 | Scan of source for volunteer names and personal emails | Snapshot owners empty; personal first names in task text replaced with roles; only email is the PTC role address |
| 2026-09-25 | Pushed `index.html` (commit f8a3aad) vs. prepared local file | Byte-identical, SHA-1 1050e598555f3138b0f914c9ec9327032b41e0e2 |
| 2026-09-25 | https://justbost.com/autumn-fair-2026/ served by Pages | Loads; title "Autumn Fair 2026 — Volunteer Tracker"; robots meta `noindex,nofollow` present. `screenshot.png` present on `main` (HTTP 200) |
| 2026-09-25 | Live sheet read in a real browser on justbost.com | Confirmed working by Justin |
| 2026-09-25 | https://ews-af26-dashboard.netlify.app/?check=5 | Redirects, Location `https://justbost.com/autumn-fair-2026/?check=5` (query preserved). The fetch tool reported the status as 302; `_redirects` specifies 301 — confirm with `curl -I` |
| 2026-11-02 | Due next changes (past dates folded into "Already passed"; Fair-day tasks show Open/Partial/Filled instead of To do; shifts collapse to one line per job in Due next only) — headless Chrome render, sheet mocked with fake names and live-style "Shift N · time" rows | Only Nov 6–7 above the fold; 12 past dates folded and closed; no "To do" on any Nov 7 line; Blocked survives on a Fair-day task; a shift note surfaces on its group line; fold stays open across a filter re-render and opens itself when filtered to a past date; no script errors (only the blocked Google Fonts request) |
| 2026-11-02 | https://justbost.com/autumn-fair-2026/ after merging PR #1 (ada0956), live sheet, real browser | "Live from the sheet" stamp, no offline banner; Due next shows Nov 5–7 only, 12 past dates folded and closed; Nov 7 has 19 lines, 0 "To do" pills, shifts collapsed per job. Found music sets sorting 1:00 / 1:45 / 11:30 / 12:15 — fixed in PR #2 by keeping sheet order within an activity |
| 2026-11-02 | Live check of PR #2 (8766154) on justbost.com, live sheet | Music sets read 11:30, 12:15, 1:00, 1:45; Nov 7 still 19 lines, 0 "To do"; "Already passed" folded |
| 2026-11-02 | Auto-assign sign-ups: Apps Script project "Autumn Fair signups" (PTC account), Code.gs `doPost` now adds a sign-up to Owners when the task has room (fewer Owners than Target, or no Target), marks the Signups row yes with a note, and emails the volunteer a confirmation; full tasks are held as "no" and the PTC email says it needs a decision. Deployed as Version 8 ("auto-assign signups") on the deployment this page calls | `doPost` run in Node against a mock of the Tasks/Signups layout: 20 of 20 checks (open slot, full, no target, already listed, unknown task, last spot then held, no email, lock busy, no name). Editor content after save and reload matched the tested file (18,609 chars, same checksum); Reminders.gs unchanged. Live test sign-up from this page's origin to "Standby helper" returned `{"ok":true,"assigned":true}`, put the test name on Owners and a "yes" row on Signups; both removed and re-read to confirm. Page messages for all three script answers tested headless |
