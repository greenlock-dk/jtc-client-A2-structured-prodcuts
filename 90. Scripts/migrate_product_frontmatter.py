from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from product_frontmatter import read_product, write_product


ROOT = Path(__file__).resolve().parent.parent
PRODUCT_DIR = ROOT / "01. Structured Products"
CANONICAL_DIR = ROOT / "05. Canonical Data"
SUMMARY_PATH = CANONICAL_DIR / "ISIN_summary.md"
DETAILED_PATH = CANONICAL_DIR / "ISIN_detailed.md"

FIELD_KEYS = {
    "Source / exhibit": "source_exhibit",
    "Trust": "trust",
    "Country of instrument": "country",
    "Custodian / bank held": "bank_held",
    "Issuer": "issuer",
    "Guarantor": "guarantor",
    "Product name": "product_name",
    "Product type / structure": "structure",
    "Currency": "currency",
    "Issue date": "issue_date",
    "Maturity / call date": "maturity",
    "Tenor (years)": "tenor_years",
    "Underlying(s)": "underlying",
    "Coupon / yield": "coupon",
    "Barrier / protection level": "barrier",
    "Observation / payment frequency": "frequency",
    "Annualised rate": "annualised_rate",
    "Other comments": "other_comments",
    "Redemption terms": "redemption_terms",
    "Downside": "downside",
    "Risk notes": "risk",
    "Position size (USD)": "position_size",
    "Denomination (USD)": "denomination_usd",
}

TERM_SHEET_AVAILABLE = {
    "CH1484588913": True,
    "XS0765564827": True,
    "XS3234638248": True,
}


def split_row(line: str) -> list[str]:
    return [cell.strip().replace("\\|", "|") for cell in re.split(r"(?<!\\)\|", line.strip())[1:-1]]


def summary_order() -> dict[str, int]:
    order = {}
    for line in SUMMARY_PATH.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| <a id="):
            continue
        cells = split_row(line)
        if len(cells) >= 3:
            match = re.search(r"record-(\d+)", cells[0])
            if match:
                order[cells[2]] = int(match.group(1))
    return order


def source_sections() -> dict[str, str]:
    sections = {}
    for line in DETAILED_PATH.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| <a id="):
            continue
        cells = split_row(line)
        if len(cells) >= 5:
            sections[cells[4]] = cells[1]
    return sections


def consolidated_values(body: str) -> tuple[dict[str, str], dict[str, str]]:
    values: dict[str, str] = {}
    statuses: dict[str, str] = {}
    in_table = False
    for line in body.splitlines():
        if line == "## Consolidated Product Record":
            in_table = True
            continue
        if in_table and line.startswith("## "):
            break
        if not in_table or not line.startswith("|") or line.startswith("| Field |") or line.startswith("| ---"):
            continue
        cells = split_row(line)
        if len(cells) != 5 or cells[0] not in FIELD_KEYS:
            continue
        key = FIELD_KEYS[cells[0]]
        values[key] = cells[3]
        statuses[key] = cells[4]
    return values, statuses


def issue_size(body: str) -> dict[str, str]:
    marker = "| Original issue / amount issued or outstanding |"
    for line in body.splitlines():
        if line.startswith(marker):
            cells = split_row(line)
            if len(cells) == 4:
                return {"display": cells[1], "status": cells[2], "source": cells[3].strip("`")}
    return {"display": "Not available", "status": "Unavailable: document recovery required", "source": ""}


def migrate(path: Path, display_order: int, source_section: str) -> None:
    existing, body = read_product(path)
    isin_match = re.search(r"\b(?:XS|CH)\d{10}\b", path.name)
    if not isin_match:
        raise ValueError(f"No ISIN in {path}")
    values, statuses = consolidated_values(body)
    data: dict[str, Any] = {
        "schema_version": 1,
        "display_order": display_order,
        "isin": isin_match.group(0),
        "term_sheet_available": TERM_SHEET_AVAILABLE.get(isin_match.group(0), False),
        "source_section": source_section,
        **values,
        "issue_size": issue_size(body),
        "field_statuses": statuses,
    }
    # Preserve future manual additions while making the extracted values authoritative.
    data.update({key: value for key, value in existing.items() if key not in data})
    write_product(path, data, body)


def main() -> None:
    order = summary_order()
    sections = source_sections()
    paths = sorted(PRODUCT_DIR.glob("[XC][HS]* - *.md"))
    if len(paths) != 29:
        raise ValueError(f"Expected 29 product dossiers, found {len(paths)}")
    for path in paths:
        isin = re.search(r"\b(?:XS|CH)\d{10}\b", path.name).group(0)
        migrate(path, order[isin], sections[isin])
    print(f"Migrated canonical frontmatter for {len(paths)} product dossiers")


if __name__ == "__main__":
    main()