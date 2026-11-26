#!/usr/bin/env python3
"""Chromium smoke test: 1440/768/390/360, 25 chapter pages, rendered images, errors."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REVIEWED = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
            19, 20, 21, 22, 23, 24, 25, 26, 27, 28]
paths = [ROOT / "docs" / "index.html"] + [ROOT / "docs" / "chapters" / f"{i:02}.html" for i in REVIEWED]
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
            # Force lazy figures to load so the image assertion checks availability, not timing.
            page.evaluate("() => document.querySelectorAll('img[loading=lazy]').forEach(i => { i.loading = 'eager'; })")
            page.evaluate("() => window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_timeout(400)
            page.evaluate("() => window.scrollTo(0, 0)")
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
            defaults = {
                "06.html": ("100", "50"),
                "07.html": ("20%", "87.5%", "50%"),
                "08.html": ("35%", "30%"),
                "09.html": ("1.8 倍", "1 倍", "3 倍"),
                "10.html": ("45", "60", "65"),
                "11.html": ("合并口径营收增长 30%", "可比（有机）增长 5%", "可持续增长率 14%", "PEG 1.67"),
                "12.html": ("经营现金流 560 万元", "净现比 0.56", "自由现金流 260 万元"),
                "13.html": ("净利率 15%", "权益乘数 2 倍", "三因子连乘校验 15%"),
                "14.html": ("参照组中位数 22", "均值 23", "按升序排名第 2"),
                "15.html": ("收入增长 20%", "期末应收增长 80%", "收现比 0.88"),
                "16.html": ("DSRI 1.25", "GMI 1.2", "SGI 2"),
                "17.html": ("货币资金占总资产 30%", "有息负债占总资产 40%", "利息收益率 1%"),
                "18.html": ("控股股东质押比例 80%", "关联方销售占营业收入 50%"),
                "19.html": ("企业价值 18.16", "终值现值占比 73.93%"),
                "20.html": ("PE 20", "PB 2.5", "PEG 1.33"),
                "21.html": ("不良贷款率 1.5%", "拨备覆盖率 160%"),
                "22.html": ("商誉/归母净资产 60%", "商誉/总资产 25%"),
                "23.html": ("同比增长 10%", "CAGR（2 年） 10%", "营业成本占收入（共同比） 60%"),
                "25.html": ("40%", "50%", "相差 10 个百分点"),
                "24.html": ("少数股东损益 1.5", "占归母净利润 17.65%"),
                "26.html": ("相对差异 6.78%"),
                "27.html": ("F-Score 7 / 9", "未满足：F6、F7"),
                "28.html": ("净现比 1.2", "自由现金流 8")
            }
            if path.name in defaults:
                result_node = page.locator("[data-result]").first
                if not result_node.count():
                    fail.append(f"{width}: missing workbench result {path.name}")
                else:
                    default_result = result_node.inner_text()
                    for expected in defaults[path.name]:
                        if expected not in default_result:
                            fail.append(f"{width}: default calculation missing {expected} in {path.name}: {default_result}")
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
                    number = d.locator("input[type=number]").first
                    if number.count():
                        number.fill(str(float(number.input_value()) + 10))
                    else:
                        d.locator("input[type=checkbox]").first.click()
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
print(f"OK: {len(paths)-1} chapter pages + index × 4 widths (1440/768/390/360), images, search, financial calculator, self-check")
