# Autumn Fair 2026 — Volunteer Tracker

A single-page volunteer tracker for the Emerson Waldorf School Autumn Fair (Nov 7, 2026), run by the Parent Teacher Collaborative. It lists every Fair task with its deadline, headcount target and sign-ups, shows what still needs people, and lets parents raise a hand for a task.

Live: https://justbost.com/autumn-fair-2026/ (unlisted — `noindex,nofollow`)

## How it works

- `index.html` is the whole app: vanilla JS and inline CSS, no build step. Fonts (Fraunces, Montserrat) load from Google Fonts.
- Data is read at page load from a Google Sheet (the PTC-owned `autumn-fair-tracker-sheet`) through an Apps Script web app (`DATA_ENDPOINT`). The same web app receives "I can help" sign-ups by POST; if that fails, the page falls back to a pre-written email to the PTC address.
- To change tasks, owners, targets or statuses, **edit the sheet**, not this file.
- If the sheet can't be reached, the page shows a built-in snapshot under an amber banner. **In this repo that snapshot has had all volunteer and personal names removed**, so the offline view shows every task as unfilled. Names only ever come from the live sheet at runtime.

## Privacy

This repo is public. Do not commit volunteer names, emails, or a refreshed snapshot that contains either. `screenshot.png` uses made-up placeholder names: `tools/screenshot.py` mocks the sheet request, and the `Screenshot` workflow re-captures and commits it whenever `index.html` changes.

## Hosting

GitHub Pages from `main` / root, served under the org domain at `/autumn-fair-2026/`. All paths are relative; the only external assets are the Google Fonts stylesheet and the Apps Script data endpoint. The old Netlify site stays up only to serve a 301 redirect here.

## Verification

| Date | Check | Result |
|---|---|---|
| 2026-09-25 | Local headless Chromium render of `index.html` with the sheet endpoint mocked | Rendered, "Live from the sheet" stamp shown, 0 console errors |
| 2026-09-25 | Scan of source for volunteer names and personal emails | Snapshot owners empty; personal first names in task text replaced with roles; only email is the PTC role address |
| pending | https://justbost.com/autumn-fair-2026/ loads, live sheet read works | — |
| pending | `curl -I` on old Netlify URL returns 301 → justbost.com/autumn-fair-2026/ | — |
