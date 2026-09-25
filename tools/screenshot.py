"""Capture screenshot.png (1280x800) with the sheet request mocked.

Volunteer names in the capture are made up. Nothing here reads the
real sheet, so no private data ends up in the image.
Run: python tools/screenshot.py   (needs: pip install playwright; playwright install chromium)
"""
import json, os, random, re
from playwright.sync_api import sync_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
html = open(os.path.join(ROOT, 'index.html'), encoding='utf-8').read()
start = html.index('let TASKS = [') + len('let TASKS = ')
end = html.index('];', start) + 1
tasks_js = html[start:end]

FAKE = ["Alex Rivera", "Sam Carter", "Jordan Lee", "Taylor Brooks", "Morgan Hayes", "Casey Nguyen",
        "Riley Patel", "Jamie Ortiz", "Avery Collins", "Quinn Foster", "Drew Kim", "Reese Morgan"]

errors = []
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={'width': 1280, 'height': 800})
    tasks = page.evaluate('() => ' + tasks_js)
    random.seed(4)
    for t in tasks:
        k = random.randint(0, min(t.get('target') or 3, 3))
        t['owners'] = random.sample(FAKE, k)
        t['status'] = random.choice(['To do', 'To do', 'In progress', 'Done'])
        t['note'] = ''
    body = json.dumps({'ok': True, 'tasks': tasks, 'settings': {'fair_date': '2026-11-07'}})
    page.route(re.compile(r'script\.google\.com'),
               lambda r: r.fulfill(status=200, content_type='application/json', body=body))
    page.on('console', lambda m: errors.append(m.text) if m.type == 'error' else None)
    page.on('pageerror', lambda e: errors.append(str(e)))
    page.goto('file://' + os.path.join(ROOT, 'index.html'))
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1500)
    print('stamp:', page.inner_text('#savestate'))
    page.screenshot(path=os.path.join(ROOT, 'screenshot.png'))
    browser.close()
print('console errors:', errors)
if errors:
    raise SystemExit(1)
