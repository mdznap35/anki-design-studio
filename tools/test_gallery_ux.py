#!/usr/bin/env python3
"""Static UX regression checks for the four generated non-protected galleries."""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
DECKS = ("en9", "enlit", "ensci", "fr9")
failures = []

for deck in DECKS:
    path = ROOT / "out" / (deck + ".html")
    if not path.is_file():
        failures.append(f"{deck}: generated page is missing")
        continue
    html = path.read_text(encoding="utf-8")

    checks = {
        "new onboarding styles are present exactly once":
            html.count('id="gallery-ux-polish"') == 1,
        "new illustrated onboarding shell is present":
            'class="ob-shell"' in html,
        "accessible onboarding dialog is present":
            'aria-modal="true" aria-label="الجولة الإرشادية"' in html,
        "onboarding has five guided steps":
            len(re.findall(r"\\{title:'", html[html.find("var ONBOARD_STEPS="):html.find("// WHAT", html.find("var ONBOARD_STEPS="))])) == 5,
        "floating circular-arrow preview button is removed":
            'class="gv-fab gv-flip"' not in html,
        "lower flip-card action remains available":
            'id="gvShowAns"' in html and 'function gvFlip(){' in html,
        "mobile layout rules are present":
            "@media(max-width:760px)" in html and "@media(max-width:380px)" in html,
        "skip and close actions are present":
            "تخطي الجولة" in html and 'aria-label="إغلاق الجولة"' in html,
        "progress indicator is present":
            "ob-progress-track" in html and "تقدّم الجولة" in html,
    }
    bad = [label for label, passed in checks.items() if not passed]
    if bad:
        failures.extend(f"{deck}: {label}" for label in bad)
        print(f"FAIL {deck}: " + "; ".join(bad))
    else:
        print(f"PASS {deck}: onboarding, responsive layout, accessibility, and preview controls")

if failures:
    raise SystemExit("\\n".join(failures))
print("ALL FOUR GALLERY UX REGRESSION CHECKS PASSED")
