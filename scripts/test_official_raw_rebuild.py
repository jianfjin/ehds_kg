#!/usr/bin/env python3
"""Regression tests for rebuilding EHDS Index from official raw OJ HTML."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "32025R0327_oj_en.html"
SRC_PATH = PROJECT_ROOT / "src" / "ehds_raw_import.py"
INDEX_ROOT = PROJECT_ROOT / "ehds_index"

EXPECTED_TITLES = {
    33: "Obligations of distributors",
    50: "Applicability to health data holders",
    51: "Minimum categories of electronic health data for secondary use",
    53: "Purposes for which electronic health data can be processed for secondary use",
    60: "Duties of health data holders",
    61: "Duties of health data users",
    68: "Data permit",
    73: "Secure processing environment",
}


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def load_importer():
    spec = importlib.util.spec_from_file_location("ehds_raw_import", SRC_PATH)
    check(spec is not None and spec.loader is not None, "src/ehds_raw_import.py must exist")
    module = importlib.util.module_from_spec(spec)
    sys.modules["ehds_raw_import"] = module
    spec.loader.exec_module(module)  # type: ignore[union-attr]
    return module


def parse_frontmatter_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = re.search(r'^title:\s*"([^"]+)"', text, re.MULTILINE)
    if match:
        return match.group(1)
    match = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
    return match.group(1).strip().strip('"') if match else ""


def main() -> int:
    check(RAW_PATH.exists(), f"official raw HTML missing: {RAW_PATH}")
    check(RAW_PATH.stat().st_size > 500_000, "raw HTML looks too small to be official OJ source")

    importer = load_importer()
    articles = importer.parse_oj_html(RAW_PATH)
    check(len(articles) == 105, f"expected 105 articles from raw HTML, got {len(articles)}")
    by_num = {article.article: article for article in articles}
    for number, expected_title in EXPECTED_TITLES.items():
        check(number in by_num, f"raw parser missing Article {number}")
        actual_title = by_num[number].title
        check(actual_title == expected_title, f"raw Art.{number} title mismatch: {actual_title!r}")
        check(len(by_num[number].text) > 500, f"raw Art.{number} text is suspiciously short")

    for number, expected_title in EXPECTED_TITLES.items():
        path = INDEX_ROOT / f"EHDS-2025-327_Art-{number:03d}.md"
        check(path.exists(), f"rebuilt index missing zero-padded file {path.name}")
        actual_title = parse_frontmatter_title(path)
        check(actual_title == expected_title, f"index Art.{number} title mismatch: {actual_title!r}")
        text = path.read_text(encoding="utf-8", errors="replace")
        check(f'EHDS-2025-327-A{number:03d}' in text, f"index Art.{number} missing zero-padded stable_id")
        check("source_path: \"data/raw/32025R0327_oj_en.html\"" in text, f"index Art.{number} missing local raw source provenance")

    print("official raw rebuild tests passed")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
