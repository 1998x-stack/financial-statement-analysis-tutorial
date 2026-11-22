#!/usr/bin/env python3
"""Chromium smoke test: 1440/768/390/360, interaction, rendered images, errors."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
paths = [ROOT / "docs" / "index.html"] + [ROOT / "docs" / "chapters" / f"{i:02}.html" for i in range(1,6)]
OUT = ROOT / "reports" / "qa"
OUT.mkdir(parents=True, exist_ok=True)
fail = []
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    for width in (1440, 768, 390, 360):
        context = browser.new_context(viewport={"width":width,"height":900})
        page = context.new_page()
        for path in paths:
            errors = []
            page.on("pageerror", lambda e: errors.append(str(e)))
            page.goto(path.as_uri(),wait_until="load")
            page.wait_for_timeout(120)
            page.screenshot(path=str(OUT / f"{width}-{path.stem}.png"), full_page=True)
            info = page.evaluate("""() => ({
                scroll:document.documentElement.scrollWidth,
                viewport:innerWidth,
                badImages:[...document.querySelectorAll('img')].filter(x=>!x.complete||!x.naturalWidth).map(x=>x.src)
            })""")
            if info["scroll"] > info["viewport"] + 2: fail.append(f"{width}: overflow {path.name}: {info}")
            if info["badImages"]: fail.append(f"{width}: missing images {path.name}: {info['badImages']}")
            if errors: fail.append(f"{width}: script errors {path.name}: {errors}")
            if path.name == "index.html":
                page.locator("#chapter-search").fill("现金流")
                if page.locator(".chapter-card:not([hidden])").count() == 0:
                    fail.append(f"{width}: index search did not match")
            else:
                d = page.locator("[data-calculator]")
                if not d.count(): fail.append(f"{width}: no calculator {path.name}")
                else:
                    result = d.locator("[data-result]")
                    before = result.inner_text()
                    first = d.locator("input[type=number]").first
                    first.fill(str(float(first.input_value()) + 10))
                    if result.inner_text() == before: fail.append(f"{width}: calculator unchanged {path.name}")
                exp = page.locator("details.exercise")
                if not exp.count(): fail.append(f"{width}: no self-check {path.name}")
                else:
                    exp.first.locator("summary").click()
                    if exp.first.get_attribute("open") is None:
                        fail.append(f"{width}: self-check did not expand {path.name}")
        context.close()
    browser.close()
if fail:
    print("\n".join("FAIL: "+x for x in fail))
    raise SystemExit(1)
print("OK: 6 pages × 4 widths (1440/768/390/360), images, search, financial calculator, self-check")
