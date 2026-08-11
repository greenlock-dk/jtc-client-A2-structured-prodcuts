from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
PRODUCT_DIR = ROOT / "01. Structured Products"
WORKBOOK_SOURCE = 'Trust ISIN information from Bloomberg.xlsx, worksheet "ISINs summary"'
ISSUE_ONLY_ISINS = {"XS1028242706", "XS1243914071"}


def format_usd(value: str) -> str:
    return f"USD {int(value.replace(',', '')):,}"


def provenance_block(isin: str, position_size: str) -> str:
    if position_size.strip().strip("'").strip('"'):
        value = format_usd(position_size)
        return (
            f"position_size_status: user-confirmed reported Trust position\n"
            f"position_size_source: {WORKBOOK_SOURCE}\n"
            f"position_size_evidence: Reported Trust position recorded as {value}"
        )
    status = "issue/outstanding size; not Trust-specific" if isin in ISSUE_ONLY_ISINS else "missing"
    evidence = (
        "No Trust-specific position amount recorded; available amount is issuer issue/outstanding size"
        if isin in ISSUE_ONLY_ISINS
        else "No Trust-specific position amount recorded; issuer issue/outstanding size is not substituted"
    )
    return f"position_size_status: {status}\nposition_size_source: {WORKBOOK_SOURCE}\nposition_size_evidence: {evidence}"


def migrate(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "position_size_status:" in text:
        return
    match = re.search(r"^position_size: ?(.*)$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"No position_size field found in {path}")
    isin = re.search(r"\b(?:XS|CH)\d{10}\b", path.name).group(0)
    replacement = f"{match.group(0)}\n{provenance_block(isin, match.group(1))}"
    path.write_text(text[: match.start()] + replacement + text[match.end() :], encoding="utf-8")


def main() -> None:
    paths = sorted(PRODUCT_DIR.glob("[XC][HS]* - *.md"))
    for path in paths:
        migrate(path)
    print(f"Added position-size provenance to {len(paths)} dossiers")


if __name__ == "__main__":
    main()