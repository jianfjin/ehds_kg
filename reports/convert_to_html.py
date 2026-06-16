#!/usr/bin/env python3
"""
Convert EHDS md reports to self-contained HTML (html-report style).
Pipeline: md text → ViewModel → HTML renderer
"""

import json
import re
import os
from datetime import datetime
from dataclasses import dataclass
from pathlib import Path

REPORTS_DIR = Path("/home/jianfjin/projects/ehds_kg/reports")

# ── CSS (html-report ivory theme) ────────────────────────────────────────────

CSS = r"""
:root {
  --ivory: #FAF7F2;
  --paper: #FFFFFF;
  --slate: #1A1D23;
  --g50: #F7F7F7;
  --g100: #EEEEEE;
  --g200: #E0E0E0;
  --g300: #C0C0C0;
  --g500: #757575;
  --g700: #424242;
  --clay: #8B7355;
  --oat: #D4C5A9;
  --olive: #6B7B4F;
  --serif: 'Georgia', 'Times New Roman', serif;
  --mono: 'SF Mono', 'Cascadia Code', 'Consolas', monospace;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  background: var(--ivory);
  color: var(--slate);
  font-family: var(--serif);
  font-size: 16px;
  line-height: 1.7;
  max-width: 960px;
  margin: 0 auto;
  padding: 40px 24px 80px;
}
h1 { font-size: 32px; font-weight: 500; margin: 0 0 8px; letter-spacing: -0.02em; }
h2 { font-size: 22px; font-weight: 500; margin: 40px 0 16px; color: var(--clay); padding-bottom: 6px; border-bottom: 2px solid var(--oat); }
h3 { font-size: 18px; font-weight: 500; margin: 28px 0 12px; }
p { margin: 0 0 16px; }
a { color: var(--clay); text-decoration: underline; text-underline-offset: 3px; }
a:hover { color: var(--olive); }
.masthead { margin-bottom: 32px; padding-bottom: 20px; border-bottom: 1px solid var(--g200); }
.masthead .meta { font-family: var(--mono); font-size: 12px; color: var(--g500); line-height: 1.8; }
code, pre { font-family: var(--mono); font-size: 13px; background: var(--paper); border: 1px solid var(--g200); border-radius: 6px; }
code { padding: 2px 6px; }
pre { padding: 16px 20px; overflow-x: auto; margin: 16px 0; line-height: 1.5; font-size: 12.5px; }
blockquote {
  margin: 16px 0; padding: 12px 20px;
  border-left: 4px solid var(--oat);
  background: var(--paper);
  border-radius: 0 8px 8px 0;
  font-style: italic;
  color: var(--g700);
}
hr { border: none; border-top: 1px solid var(--g200); margin: 32px 0; }
table { width: 100%; border-collapse: collapse; margin: 16px 0; font-size: 13px; font-family: var(--mono); }
th { background: var(--g100); text-align: left; padding: 8px 12px; font-weight: 600; border-bottom: 2px solid var(--g300); }
td { padding: 8px 12px; border-bottom: 1px solid var(--g200); }
tr:hover td { background: var(--g50); }
ul, ol { margin: 0 0 16px; padding-left: 24px; }
li { margin-bottom: 6px; }
.finding-card {
  border: 1.5px solid var(--g200); border-radius: 10px;
  padding: 20px 24px; margin: 14px 0;
  border-left: 4px solid var(--clay);
  background: var(--paper);
}
.finding-card h3 { font-size: 16px; margin: 0 0 8px; }
.finding-card .source { font-family: var(--mono); font-size: 11px; color: var(--g500); margin-top: 10px; }
.metrics { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 16px; margin: 32px 0; }
.metric-card { background: var(--paper); border: 1.5px solid var(--g200); border-radius: 12px; padding: 20px 24px; }
.metric-value { font-family: var(--serif); font-size: 36px; font-weight: 500; line-height: 1; margin-bottom: 6px; }
.metric-label { font-family: var(--mono); font-size: 11px; text-transform: uppercase; letter-spacing: 0.06em; color: var(--g500); }
.article-list { list-style: none; padding: 0; }
.article-list li { padding: 12px 16px; border-bottom: 1px solid var(--g200); display: flex; gap: 12px; align-items: baseline; }
.article-list li .art-num { font-family: var(--mono); font-size: 12px; color: var(--clay); min-width: 80px; font-weight: 600; }
.sec-head { display: flex; align-items: center; gap: 12px; margin: 40px 0 20px; }
.sec-head .idx { font-family: var(--mono); font-size: 13px; color: var(--g500); background: var(--g100); padding: 2px 10px; border-radius: 20px; }
.sec-head h2 { margin: 0; border: none; padding: 0; }
.footer-note { font-family: var(--mono); font-size: 11px; color: var(--g500); margin-top: 48px; padding-top: 16px; border-top: 1px solid var(--g200); }
.toc { background: var(--paper); border: 1.5px solid var(--g200); border-radius: 12px; padding: 24px 28px; margin: 24px 0; }
.toc h3 { margin: 0 0 12px; font-size: 14px; font-family: var(--mono); text-transform: uppercase; letter-spacing: 0.06em; color: var(--g500); }
.toc ol { margin: 0; padding-left: 20px; }
.toc li { margin-bottom: 8px; font-size: 14px; }
.nav-links { display: flex; gap: 16px; flex-wrap: wrap; margin: 24px 0; }
.nav-link { font-family: var(--mono); font-size: 12px; color: var(--g500); text-decoration: none; padding: 4px 12px; border: 1px solid var(--g200); border-radius: 20px; }
.nav-link:hover { background: var(--g100); border-color: var(--clay); color: var(--clay); }
.tag { display: inline-block; font-family: var(--mono); font-size: 10px; padding: 2px 8px; border-radius: 4px; background: var(--g100); color: var(--g500); margin: 0 4px 4px 0; }
.tag-role { background: #EDF3E8; color: var(--olive); }
.tag-date { background: #F0E8E0; color: var(--clay); }
"""

# ── Parse helpers ───────────────────────────────────────────────────────────

def parse_md_metadata(md_text: str) -> dict:
    """Extract title, date, role from md front matter."""
    meta = {}
    lines = md_text.split('\n')
    if lines:
        first = lines[0].strip()
        m = re.match(r'^#\s+(.+)$', first)
        if m:
            meta['title'] = m.group(1)
    for line in lines[:10]:
        m = re.match(r'\*\*日期：\*\*\s*(.*)', line)
        if m:
            meta['date'] = m.group(1).strip()
        m = re.match(r'\*\*轮次：\*\*\s*(.*)', line)
        if m:
            meta['round'] = m.group(1).strip()
        m = re.match(r'\*\*数据来源：\*\*\s*(.*)', line)
        if m:
            meta['source'] = m.group(1).strip()
        # Also try to extract from comprehensive guide
        m = re.match(r'#\s+EHDS\s.*Comprehensive', line)
        if m:
            meta['type'] = 'comprehensive'
    return meta


def md_to_html_body(md_text: str) -> str:
    """Simple md-to-html conversion for the specific format used in these reports."""
    html_parts = []
    in_code_block = False
    code_lines = []
    in_list = False
    list_type = None
    lines = md_text.split('\n')

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Code block
        if stripped.startswith('```'):
            if in_code_block:
                html_parts.append(f'<pre><code>{"".join(code_lines)}</code></pre>\n')
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue
        if in_code_block:
            code_lines.append(line + '\n')
            continue

        # Skip the title line (handled in metadata)
        if i == 0 and stripped.startswith('# ') and not stripped.startswith('## '):
            continue

        # Horizontal rule
        if stripped == '---':
            # Close any open list
            if in_list:
                html_parts.append(f'</{"ol" if list_type == "ordered" else "ul"}>\n')
                in_list = False
                list_type = None
            html_parts.append('<hr>\n')
            continue

        # Empty line
        if not stripped:
            if in_list:
                html_parts.append(f'</{"ol" if list_type == "ordered" else "ul"}>\n')
                in_list = False
                list_type = None
            continue

        # Headers
        m = re.match(r'^(#{1,4})\s+(.+)$', stripped)
        if m:
            level = len(m.group(1))
            text = m.group(2)
            # Skip metadata lines that look like headers but start with bold
            if level == 2 and text.startswith('**') and '：' in text:
                html_parts.append(f'<h3>{escape_html(text)}</h3>\n')
            else:
                tag = f'h{level+1}' if level == 1 else f'h{level}'  # shift h1→h2 if not title
                html_parts.append(f'<{tag}>{escape_html(text)}</{tag}>\n')
            continue

        # Article refs like "**Art. X — Title**"
        m = re.match(r'^\*\*(Art(?:icle)?\.?\s*[\d]+.*?)\*\*\s*(.*)$', stripped)
        if m:
            art_title = m.group(1)
            art_desc = m.group(2).strip()
            rendered = f'<strong>{escape_html(art_title)}</strong>'
            if art_desc:
                rendered += f' {escape_html(art_desc)}'
            html_parts.append(f'<p>{rendered}</p>\n')
            continue

        # Metadata lines like "**日期：** 2026-06-06"
        m = re.match(r'^\*\*(.+?)：\*\*\s*(.*)', stripped)
        if m:
            label = m.group(1)
            value = m.group(2).strip()
            value = re.sub(r'`([^`]+)`', r'<code>\1</code>', value)
            html_parts.append(f'<p><strong>{escape_html(label)}：</strong> {value}</p>\n')
            continue

        # Lists
        m = re.match(r'^(\d+)\.\s+(.+)$', stripped)
        if m:
            if not in_list:
                html_parts.append('<ol>\n')
                in_list = True
                list_type = 'ordered'
            html_parts.append(f'<li>{escape_html(m.group(2))}</li>\n')
            continue

        m = re.match(r'^[-*]\s+(.+)$', stripped)
        if m:
            if not in_list:
                html_parts.append('<ul>\n')
                in_list = True
                list_type = 'unordered'
            html_parts.append(f'<li>{escape_html(m.group(1))}</li>\n')
            continue

        # Blockquote (lines starting with >)
        m = re.match(r'^>\s*(.+)$', stripped)
        if m:
            html_parts.append(f'<blockquote>{escape_html(m.group(1))}</blockquote>\n')
            continue

        # Regular paragraph
        # Inline formatting
        text = stripped
        text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
        text = re.sub(r'\*(.+?)\*', r'<em>\1</em>', text)
        text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
        # Links
        text = re.sub(r'\[\[(.+?)\]\]', r'<span class="tag">\1</span>', text)
        html_parts.append(f'<p>{text}</p>\n')

    if in_code_block:
        html_parts.append(f'<pre><code>{"".join(code_lines)}</code></pre>\n')

    return ''.join(html_parts)


def escape_html(text: str) -> str:
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def extract_role_name(filename: str) -> str:
    """Extract readable role name from filename."""
    basename = filename.replace('.md', '')
    parts = basename.split('-')
    # Find role part after 'perspective' or after date
    role_start = 0
    for i, p in enumerate(parts):
        if p == 'perspective':
            role_start = i + 2  # skip date
            break
    if role_start and role_start < len(parts):
        role = '-'.join(parts[role_start:])
    else:
        role = basename

    role_names = {
        'healthcare_provider': 'Healthcare Provider Network',
        'hospital_clinic': 'Hospital / Clinic',
        'principal_investigator': 'Principal Investigator (Research)',
        'general_physician': 'General Physician (GP)',
        'specialist': 'Medical Specialist',
        'data_analyst': 'Data Analyst',
        'service_provider': 'Service Provider (IT/Tech)',
        'secondary_use_org': 'Secondary Use Organization',
        'insurer': 'Health Insurer',
        'contractor': 'Contractor (CRO)',
        'pharma': 'Pharmaceutical Company',
        'third_country_pharma': 'Third Country — Pharma',
        'third_country_hospital': 'Third Country — Hospital',
        'third_country_research_org': 'Third Country — Research Org',
        'comprehensive-guide': 'Comprehensive Article-by-Article Guide',
    }
    return role_names.get(role, role.replace('_', ' ').title())


def build_index_html(reports: list[dict]) -> str:
    """Build index page linking to all reports."""
    date_groups = {}
    for r in reports:
        d = r.get('date', 'unknown')
        date_groups.setdefault(d, []).append(r)

    sorted_dates = sorted(date_groups.keys(), reverse=True)

    report_cards = ''
    for date in sorted_dates:
        report_cards += f'<h2>{escape_html(date)}</h2>\n'
        for r in date_groups[date]:
            report_cards += f'''
<div class="finding-card">
  <h3><a href="{escape_html(r['html_file'])}">{escape_html(r['role'])}</a></h3>
  <div class="source">
    <span class="tag tag-role">{escape_html(r.get('round', '—'))}</span>
    <span class="tag tag-date">{r.get('size', '?')} KB</span>
    <span class="tag">{escape_html(r.get('source', 'EHDS KG'))}</span>
  </div>
</div>
'''

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EHDS 报告索引</title><style>{CSS}</style></head>
<body>
<div class="masthead">
  <h1>EHDS 监管合规报告</h1>
  <p style="color:var(--g700);margin-top:8px;">European Health Data Space（Reg. (EU) 2025/327）— 多角色视角解读</p>
  <div class="meta">
    <div>数据来源：EHDS Knowledge Graph (105 条款 / 20 Wiki / 2 规则)</div>
    <div>更新：{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</div>
    <div>共 {len(reports)} 份报告</div>
  </div>
</div>

<div class="metrics">
  <div class="metric-card">
    <div class="metric-value">{len([r for r in reports if 'comprehensive' not in r['filename']])}</div>
    <div class="metric-label">角色视角报告</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">{len(date_groups)}</div>
    <div class="metric-label">涵盖天数</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">105</div>
    <div class="metric-label">条款数</div>
  </div>
  <div class="metric-card">
    <div class="metric-value">2025/327</div>
    <div class="metric-label">法规编号</div>
  </div>
</div>

{report_cards}

<div class="footer-note">
  Generated by Hermes Agent (Fei-Fei Li profile) · EHDS KG Service
</div>
</body></html>'''
    return html


def build_report_html(md_text: str, filename: str) -> str:
    """Convert single md report to HTML."""
    meta = parse_md_metadata(md_text)
    role = extract_role_name(filename)
    body = md_to_html_body(md_text)

    title = meta.get('title', role)
    date_str = meta.get('date', filename[-12:-3])

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{escape_html(title)}</title><style>{CSS}</style></head>
<body>

<div class="nav-links">
  <a class="nav-link" href="index.html">← 返回索引</a>
  <span class="nav-link">EHDS 报告</span>
</div>

<div class="masthead">
  <h1>{escape_html(role)}</h1>
  <div class="meta">
    <div>📅 {escape_html(date_str)}</div>
    <div>📄 {escape_html(meta.get('round', ''))}</div>
    <div>📡 {escape_html(meta.get('source', 'EHDS KG'))}</div>
  </div>
</div>

{body}

<div class="footer-note">
  Reg. (EU) 2025/327 · EHDS Knowledge Graph · Generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
  <br><a href="index.html">← 返回报告索引</a>
</div>
</body></html>'''
    return html


def build_comprehensive_html(md_text: str) -> str:
    """Convert comprehensive guide to special HTML."""
    meta = parse_md_metadata(md_text)
    body = md_to_html_body(md_text)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EHDS Comprehensive Guide</title><style>{CSS}</style></head>
<body>

<div class="nav-links">
  <a class="nav-link" href="index.html">← 返回索引</a>
  <span class="nav-link">📖 全条款指南</span>
</div>

<div class="masthead">
  <h1>EHDS — European Health Data Space</h1>
  <p style="font-size:18px;color:var(--clay);margin-top:4px;">Comprehensive Article-by-Article Guide</p>
  <div class="meta">
    <div>Regulation (EU) 2025/327</div>
    <div>生效：2025年3月 · 全面适用：2027年3月</div>
    <div>105 条款 · 双支柱架构</div>
  </div>
</div>

<div class="toc">
  <h3>目录</h3>
  <ol>
    <li>Chapter I &amp; II — General Provisions &amp; Natural Persons' Rights</li>
    <li>Chapter III-IV — Governance, MyHealth@EU &amp; EHR Systems</li>
    <li>Chapter V — Secondary Use of Electronic Health Data</li>
    <li>Chapter VI-VIII — Governance, Delegated Acts &amp; Final Provisions</li>
  </ol>
</div>

{body}

<div class="footer-note">
  Reg. (EU) 2025/327 · EHDS Knowledge Graph · Generated {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}
  <br><a href="index.html">← 返回报告索引</a>
</div>
</body></html>'''
    return html


# ── Main ────────────────────────────────────────────────────────────────────

def main():
    report_files = sorted(REPORTS_DIR.glob("ehds-*.md"))

    # First pass: collect metadata
    reports = []
    for fp in report_files:
        md_text = fp.read_text(encoding='utf-8')
        meta = parse_md_metadata(md_text)
        role = extract_role_name(fp.name)
        size_kb = round(fp.stat().st_size / 1024, 1)
        html_name = fp.stem + '.html'
        reports.append({
            'filename': fp.name,
            'html_file': html_name,
            'role': role,
            'date': meta.get('date', ''),
            'round': meta.get('round', ''),
            'source': meta.get('source', 'EHDS KG'),
            'size': size_kb,
            'is_comprehensive': 'comprehensive' in fp.name or 'comprehensive' in fp.stem,
        })

    # Second pass: render HTML
    for fp in report_files:
        md_text = fp.read_text(encoding='utf-8')
        is_comp = 'comprehensive' in fp.name or 'comprehensive' in fp.stem

        if is_comp:
            html = build_comprehensive_html(md_text)
        else:
            html = build_report_html(md_text, fp.name)

        html_path = fp.with_suffix('.html')
        html_path.write_text(html, encoding='utf-8')
        print(f"  ✓ {html_path.name} ({round(html_path.stat().st_size / 1024, 1)} KB)")

    # Build index
    index_html = build_index_html(reports)
    index_path = REPORTS_DIR / 'index.html'
    index_path.write_text(index_html, encoding='utf-8')
    print(f"\n  ✓ index.html ({round(index_path.stat().st_size / 1024, 1)} KB)")

    print(f"\nDone. {len(reports)} reports converted.")


if __name__ == '__main__':
    main()
