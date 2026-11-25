#!/usr/bin/env python3
"""Static regression checks: no third-party deps."""
import html.parser
import json
import pathlib
import re
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, unquote

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
# Chapters that have been technically reviewed and must meet the full content bar
# (figures, semantic sections, fictional-data disclaimer, primary-source section).
REVIEWED = {*range(1, 17), 18, 19, 20, 21, 22, 24, 26, 27, 28}
errors = []

def err(message):
    errors.append(message)

class Document(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.h1 = 0
        self.title = 0
        self.figures = 0
        self.captions = 0
        self.images = []
        self.ids = set()
    def handle_starttag(self, tag, pairs):
        a = dict(pairs)
        if tag == "h1": self.h1 += 1
        if tag == "title": self.title += 1
        if tag == "figure": self.figures += 1
        if tag == "figcaption": self.captions += 1
        if "id" in a: self.ids.add(a["id"])
        if tag == "a": self.links.append(a.get("href", ""))
        if tag == "link" and a.get("rel") == "stylesheet": self.links.append(a.get("href", ""))
        if tag == "script" and "src" in a: self.links.append(a["src"])
        if tag == "img":
            self.images.append(a)
            self.links.append(a.get("src", ""))

manifest = json.loads((DOCS / "courses.json").read_text(encoding="utf-8"))
chapters = manifest["chapters"]
if len(chapters) != 28 or [i["num"] for i in chapters] != [f"{i:02}" for i in range(1, 29)]:
    err("courses.json must contain ordered 01..28")
pages = [DOCS / "index.html"] + [DOCS / "chapters" / f"{i:02}.html" for i in range(1,29)]
for path in pages:
    if not path.is_file():
        err(f"missing page {path.relative_to(ROOT)}")
        continue
    source = path.read_text(encoding="utf-8")
    d = Document()
    d.feed(source)
    reviewed = path.stem.isdigit() and int(path.stem) in REVIEWED
    if d.title != 1: err(f"{path.name}: expected one title")
    if d.h1 != 1 and (path.name == "index.html" and path.parent == DOCS or reviewed):
        err(f"{path}: expected one H1")
    if d.figures > d.captions: err(f"{path}: each figure needs caption")
    for link in d.links:
        if not link or link.startswith(("http:", "https:", "mailto:", "tel:", "data:", "javascript:")):
            continue
        target = urlparse(link)
        local = (path.parent / unquote(target.path)).resolve() if target.path else path
        if not local.is_relative_to(ROOT) or not local.exists():
            err(f"{path.relative_to(ROOT)}: missing link {link}")
        if target.fragment and local.is_file() and local.suffix == ".html" and local == path and target.fragment not in d.ids:
            err(f"{path.relative_to(ROOT)}: broken anchor #{target.fragment}")
    for img in d.images:
        if not img.get("alt"): err(f"{path.relative_to(ROOT)}: image missing alt")
    if reviewed:
        if d.figures < 2: err(f"{path.name}: expected at least 2 teaching figures")
        if source.count("<section ") < 5: err(f"{path.name}: article too short or no semantic sections")
        if "教学虚构" not in source: err(f"{path.name}: missing fictional-data disclaimer")
        if 'class="sources"' not in source: err(f"{path.name}: no primary-source section")

for svg in sorted((DOCS / "assets" / "figures").glob("*.svg")):
    try:
        x = ET.parse(svg).getroot()
        if not x.tag.endswith("svg") or "viewBox" not in x.attrib:
            err(f"{svg.name}: invalid SVG root")
        ns = "{http://www.w3.org/2000/svg}"
        if x.find(ns+"title") is None or x.find(ns+"desc") is None:
            err(f"{svg.name}: requires title & desc")
    except ET.ParseError as e:
        err(f"{svg.name}: XML parse error {e}")

for i in range(1,29):
    if not (ROOT/f"{i:02}.html").exists(): err(f"legacy redirect {i:02}.html absent")
if errors:
    print("\n".join("ERROR: "+m for m in errors))
    sys.exit(1)
print(f"OK: {len(pages)} pages, {len(list((DOCS/'assets'/'figures').glob('*.svg')))} SVG files, 28 redirects, all local links")
