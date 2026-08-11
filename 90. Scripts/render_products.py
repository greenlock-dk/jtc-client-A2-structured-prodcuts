from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

import yaml

from product_frontmatter import read_product


ROOT = Path(__file__).resolve().parent.parent
PRODUCT_DIR = ROOT / "01. Structured Products"
VIEWS_PATH = ROOT / "05. Canonical Data" / "views.yaml"

HEADERS = {
    "record_number": "Record #",
    "source_section": "Source section",
    "source_exhibit": "Source / Exhibit",
    "trust": "Trust",
    "isin": "ISIN",
    "product_name": "Name of product",
    "country": "Country of instrument",
    "bank_held": "Bank held",
    "issuer": "Issuer",
    "issue_date": "Issue date",
    "maturity": "Maturity",
    "tenor_years": "Tenor (years)",
    "structure": "Structure",
    "coupon": "Coupon rate",
    "frequency": "Frequency",
    "annualised_rate": "Annualised rate",
    "barrier": "Barrier",
    "underlying": "Underlying",
    "other_comments": "Other comments",
    "downside": "Downside",
    "risk": "Risk",
    "position_size": "Reported Trust position size (USD)",
    "denomination_usd": "Denomination (USD)",
    "detailed_record": "Detailed record",
    "summary_record": "Summary record",
    "issue_size.display": "Issuer issue/outstanding size",
    "issue_size.status": "Issue-size status",
    "term_sheet_available": "Term sheet available",
}


def nested_value(record: dict[str, Any], column: str, report_directory: Path) -> str:
    isin = record["isin"]
    if column == "record_number":
        return f'<a id="{isin.lower()}"></a>{record["display_order"]}'
    if column == "detailed_record":
        target = Path(os.path.relpath(ROOT / "05. Canonical Data/ISIN_detailed.md", report_directory))
        return f"[Detailed]({target.as_posix().replace(' ', '%20')}#{isin.lower()})"
    if column == "summary_record":
        target = Path(os.path.relpath(ROOT / "05. Canonical Data/ISIN_summary.md", report_directory))
        return f"[Summary]({target.as_posix().replace(' ', '%20')}#{isin.lower()})"
    value: Any = record
    for part in column.split("."):
        if not isinstance(value, dict):
            return ""
        value = value.get(part, "")
    if value is None:
        return ""
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def product_records() -> list[dict[str, Any]]:
    records = []
    for path in PRODUCT_DIR.glob("[XC][HS]* - *.md"):
        record, _ = read_product(path)
        if record:
            records.append(record)
    if len(records) != 29:
        raise ValueError(f"Expected 29 canonical product records, found {len(records)}")
    return sorted(records, key=lambda record: (record.get("display_order", 9999), record["isin"]))


def markdown_table(columns: list[str], records: list[dict[str, Any]], report_directory: Path) -> str:
    headers = [HEADERS.get(column, column) for column in columns]
    rows = [
        [nested_value(record, column, report_directory) for column in columns]
        for record in records
    ]
    lines = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in columns) + " |"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render report tables from canonical product frontmatter.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--view", help="Named view in 05. Canonical Data/views.yaml")
    group.add_argument("--columns", help="Comma-separated canonical field names")
    parser.add_argument("--output", help="Output path relative to the repository root")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    views = yaml.safe_load(VIEWS_PATH.read_text(encoding="utf-8"))["views"]
    if args.view:
        if args.view not in views:
            raise ValueError(f"Unknown view: {args.view}")
        view = views[args.view]
        columns = view["columns"]
        output = ROOT / args.output if args.output else ROOT / view["output"]
        title = view["title"]
    else:
        columns = [column.strip() for column in args.columns.split(",") if column.strip()]
        output = ROOT / args.output if args.output else None
        title = "Custom ISIN Report"
    unknown = [column for column in columns if column not in HEADERS]
    if unknown:
        raise ValueError(f"Unknown column(s): {', '.join(unknown)}")
    content = "\n".join([
        f"# {title}",
        "",
        "> Generated from canonical YAML frontmatter in individual product dossiers. Do not edit this table directly.",
        "",
        markdown_table(columns, product_records(), output.parent if output else ROOT / "05. Canonical Data"),
        "",
    ])
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(content, encoding="utf-8")
        print(f"Rendered {len(product_records())} records to {output.relative_to(ROOT)}")
    else:
        print(content, end="")


if __name__ == "__main__":
    main()