#!/usr/bin/env python3
"""Minimal static site generator for journal."""

import json
from pathlib import Path
from datetime import datetime

# Read all entries
entries = []
entries_dir = Path("entries")
if entries_dir.exists():
    for f in sorted(entries_dir.glob("*.json"), reverse=True):
        with open(f) as fp:
            data = json.load(fp)
            date = f.stem
            
            arun_html = f"<div class='entry arun'><div class='date'>{date}</div><strong>Arun:</strong><br>{data.get('arun','')}</div>" if data.get('arun') else ""
            hermes_html = f"<div class='entry hermes'><div class='date'>{date}</div><strong>Hermes:</strong><br>{data.get('hermes','')}</div>" if data.get('hermes') else ""
            
            entries.append(arun_html + hermes_html)

# Build index
template = open("template.html").read()
html = template.replace("{{ENTRIES}}", "\n".join(entries))

# Write
Path("index.html").write_text(html)
print(f"Built index.html with {len(entries)} entries")
