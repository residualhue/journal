#!/usr/bin/env python3
"""Build static journal site with index + individual entry pages."""

import json
from pathlib import Path
from datetime import datetime

entries_dir = Path("entries")
template = Path("template.html").read_text()

# Build individual entry pages
entries = []
for f in sorted(entries_dir.glob("*.json"), reverse=True):
    with open(f) as fp:
        data = json.load(fp)
    
    date = f.stem
    title = data.get("title", f"Entry: {date}")
    
    # Build entry page
    arun_html = f"""
    <div class="section arun-section">
        <div class="section-header arun-header">Arun's Reflection</div>
        <div class="section-body">{data.get('arun', 'No entry yet.')}</div>
    </div>
    """ if data.get('arun') else ""
    
    hermes_html = f"""
    <div class="section hermes-section">
        <div class="section-header hermes-header">Hermes' Reflection</div>
        <div class="section-body">{data.get('hermes', 'No entry yet.')}</div>
    </div>
    """ if data.get('hermes') else ""
    
    topics_html = ""
    if data.get('topics'):
        topic_tags = ''.join([f'<span class="topic">{t}</span>' for t in data['topics']])
        topics_html = f'<div class="topics">{topic_tags}</div>'
    
    entry_content = f"""
    <h1>{title}</h1>
    <p class="subtitle">{date}</p>
    <div class="full-entry">
        {arun_html}
        {hermes_html}
        {topics_html}
    </div>
    """
    
    # Write individual entry page
    entry_html = template.replace("{{TITLE}}", title).replace("{{CONTENT}}", entry_content)
    Path(f"{date}.html").write_text(entry_html)
    
    # Store for index
    entries.append({
        'date': date,
        'title': title,
        'has_arun': bool(data.get('arun')),
        'has_hermes': bool(data.get('hermes')),
        'topics': data.get('topics', [])
    })
    print(f"Built: {date}.html - {title}")

# Build index page
index_items = []
for e in entries:
    arun_badge = '<span class="badge arun-badge">Arun</span>' if e['has_arun'] else ''
    hermes_badge = '<span class="badge hermes-badge">Hermes</span>' if e['has_hermes'] else ''
    
    topics_preview = ', '.join(e['topics'][:3]) if e['topics'] else ''
    
    item = f"""
    <a href="{e['date']}.html" class="entry-item">
        <div class="entry-date">{e['date']}</div>
        <div class="entry-title">{e['title']}</div>
        <div class="entry-meta">
            {arun_badge} {hermes_badge}
            {topics_preview}
        </div>
    </a>
    """
    index_items.append(item)

index_content = f"""
<h1>ResidualHue Journal</h1>
<p class="subtitle">Dual perspectives on building. Daily reflections from Arun and Hermes.</p>

<div class="entry-list">
    {''.join(index_items)}
</div>
"""

index_html = template.replace("{{TITLE}}", "Journal").replace("{{CONTENT}}", index_content)
Path("index.html").write_text(index_html)

print(f"\nBuilt index.html with {len(entries)} entries")
