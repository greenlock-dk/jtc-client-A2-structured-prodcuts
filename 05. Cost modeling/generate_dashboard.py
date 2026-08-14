from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
PRODUCT_DIR = ROOT / "01. Structured Products"
POSITION_CONTROL = ROOT / "04. Product Review" / "POSITION SIZE CONTROL.md"
OUTPUT_PATH = ROOT / "07. Visutals" / "index.html"
TOOLTIP_PATH = ROOT / "05. Cost modeling" / "tooltips.yaml"
RESEARCH_REPORT = ROOT / "00. Project scope" / "cost-benchmark-research.md"

sys.path.insert(0, str(ROOT / "90. Scripts"))
from product_frontmatter import read_product  # noqa: E402


DATE_FORMATS = ("%d-%b-%Y", "%d/%m/%Y", "%d-%b-%y")
ESMA_ISSUANCE_LOW = 0.046
ESMA_ISSUANCE_HIGH = 0.055
ESMA_MODERN_ANNUAL = 0.0103
SWISS_EQUITY_LINKED_ANNUAL = 0.017
EMBEDDED_HISTORICAL_BASE = (ESMA_ISSUANCE_LOW + ESMA_ISSUANCE_HIGH) / 2
SWISS_SERVICE_BASE_ANNUAL = 0.0056
EXIT_TRANSACTION_BASE = 0.0096


def read_tooltips() -> dict[str, dict[str, str]]:
    data = yaml.safe_load(TOOLTIP_PATH.read_text(encoding="utf-8")) or {}
    return {
        section: {
            str(key): str(value)
            for key, value in (data.get(section) or {}).items()
            if value is not None
        }
        for section in ("curated", "canonical")
    }


def format_date(value: str) -> str:
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(value, date_format).strftime("%d %b %Y")
        except ValueError:
            continue
    return value


def format_yaml_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return str(value)


def issue_year(value: str) -> int | None:
    for date_format in DATE_FORMATS:
        try:
            return datetime.strptime(value, date_format).year
        except ValueError:
            continue
    return None


def extract_lifecycle_end(maturity: str) -> tuple[str, str]:
    call = re.search(r"Call effective:\s*([^;]+)", maturity, flags=re.IGNORECASE)
    if call:
        return format_date(call.group(1).strip()), "Documented call date"
    maturity_date = re.search(r"Maturity:\s*([^;]+)", maturity, flags=re.IGNORECASE)
    if maturity_date:
        return format_date(maturity_date.group(1).strip()), "Scheduled maturity"
    return format_date(maturity), "Reported maturity"


def read_position_statuses() -> dict[str, str]:
    statuses: dict[str, str] = {}
    for line in POSITION_CONTROL.read_text(encoding="utf-8").splitlines():
        cells = [cell.strip() for cell in line.split("|")]
        if len(cells) < 4 or not re.fullmatch(r"(?:CH|XS)\d{10}", cells[1]):
            continue
        statuses[cells[1]] = cells[3].strip("`")
    if len(statuses) != 29:
        raise ValueError(f"Expected 29 position classifications, found {len(statuses)}")
    return statuses


def product_cohort(record: dict[str, Any]) -> str:
    description = " ".join(
        str(record.get(field, ""))
        for field in ("structure", "product_name", "underlying", "coupon")
    ).lower()
    if any(keyword in description for keyword in ("phoenix", "express", "barrier", "equity-linked", "dual index", "kick in")):
        return "Equity-linked"
    if any(keyword in description for keyword in ("libor", "range accrual", "cms", "callable")):
        return "Modern rate-linked" if issue_year(str(record.get("issue_date", ""))) == 2026 else "Historical rate-linked"
    return "Conventional / specialist debt"


def parse_usd_amount(value: str) -> float | None:
    if not re.fullmatch(r"[\d,]+(?:\.\d+)?", value.strip()):
        return None
    return float(value.replace(",", ""))


def format_calculated_money(value: float) -> str:
    return f"{value:,.0f}"


def is_numeric_display(value: str) -> bool:
    return bool(re.fullmatch(r"-?[\d,]+(?:\.\d+)?%?", value.strip()))


def holding_period_years(record: dict[str, Any]) -> float | None:
    try:
        holding_period = float(str(record.get("holding_period_years", "")))
    except ValueError:
        return None
    return holding_period if holding_period > 0 else None


def usable_position_amount(record: dict[str, Any], status: str) -> float | None:
    position = str(record.get("position_size", "Missing"))
    amount = parse_usd_amount(position)
    if status != "usable invested notional" or amount is None:
        return None
    return amount


def evidence_only_cost(record: dict[str, Any], status: str, cohort: str) -> str:
    amount = usable_position_amount(record, status)
    if amount is None:
        return "Not calculated"
    if cohort == "Historical rate-linked":
        return f"{format_calculated_money(amount * ESMA_ISSUANCE_LOW)} - {format_calculated_money(amount * ESMA_ISSUANCE_HIGH)}"
    if cohort == "Equity-linked":
        holding_period = holding_period_years(record)
        if holding_period is None:
            return "Unbenchmarked"
        return format_calculated_money(amount * ESMA_MODERN_ANNUAL * holding_period)
    return "Unbenchmarked"


def proxy_base_cost(record: dict[str, Any], status: str, cohort: str) -> str:
    amount = usable_position_amount(record, status)
    if amount is None:
        return "Not calculated"
    if cohort == "Historical rate-linked":
        return f"{format_calculated_money(amount * ESMA_ISSUANCE_LOW)} - {format_calculated_money(amount * ESMA_ISSUANCE_HIGH)}"
    if cohort == "Equity-linked":
        holding_period = holding_period_years(record)
        if holding_period is None:
            return "Unbenchmarked"
        return format_calculated_money(amount * SWISS_EQUITY_LINKED_ANNUAL * holding_period)
    return "Unbenchmarked"


def proxy_component_costs(record: dict[str, Any], status: str, cohort: str) -> tuple[str, str, str, str, str]:
    amount = usable_position_amount(record, status)
    if amount is None:
        return "Not calculated", "Not calculated", "Not calculated", "Not calculated", "Not calculated"
    if cohort == "Historical rate-linked":
        embedded_amount = amount * EMBEDDED_HISTORICAL_BASE
    elif cohort == "Equity-linked":
        embedded_amount = amount * SWISS_EQUITY_LINKED_ANNUAL * (holding_period_years(record) or 0)
        if holding_period_years(record) is None:
            return "Unbenchmarked", "Unbenchmarked", "Unbenchmarked", "Unbenchmarked", "Unbenchmarked"
    else:
        return "Unbenchmarked", "Unbenchmarked", "Unbenchmarked", "Unbenchmarked", "Unbenchmarked"
    holding_period = holding_period_years(record)
    if holding_period is None:
        return "Unbenchmarked", "Unbenchmarked", "Unbenchmarked", "Unbenchmarked", "Unbenchmarked"
    recurring_amount = amount * SWISS_SERVICE_BASE_ANNUAL * holding_period
    exit_amount = amount * EXIT_TRANSACTION_BASE
    total = embedded_amount + recurring_amount + exit_amount
    return (
        format_calculated_money(embedded_amount),
        format_calculated_money(recurring_amount),
        format_calculated_money(exit_amount),
        format_calculated_money(total),
        "Calculated: assumed exit; low-confidence service and exit proxies",
    )


def scenario_cost_range(record: dict[str, Any], status: str, cohort: str, scenario: str) -> tuple[str, str]:
    amount = usable_position_amount(record, status)
    if amount is None:
        return "Not calculated", "Not calculated"
    if cohort == "Historical rate-linked":
        return (
            format_calculated_money(amount * ESMA_ISSUANCE_LOW),
            format_calculated_money(amount * ESMA_ISSUANCE_HIGH),
        )
    if cohort == "Equity-linked":
        holding_period = holding_period_years(record)
        if holding_period is None:
            return "Unbenchmarked", "Unbenchmarked"
        annual_rate = ESMA_MODERN_ANNUAL if scenario == "evidence" else SWISS_EQUITY_LINKED_ANNUAL
        cost = format_calculated_money(amount * annual_rate * holding_period)
        return cost, cost
    return "Unbenchmarked", "Unbenchmarked"


def chart_row(record: dict[str, Any], statuses: dict[str, str]) -> dict[str, Any]:
    isin = str(record["isin"])
    status = statuses[isin]
    cohort = product_cohort(record)
    position_amount = usable_position_amount(record, status)
    holding_period = holding_period_years(record)
    evidence_low = evidence_high = proxy_total = None
    embedded_proxy = recurring_proxy = exit_proxy = None
    calculation_status = "Not calculated"

    if position_amount is not None:
        evidence_low_value, evidence_high_value = scenario_cost_range(record, status, cohort, "evidence")
        evidence_low = parse_usd_amount(evidence_low_value)
        evidence_high = parse_usd_amount(evidence_high_value)
        components = proxy_component_costs(record, status, cohort)
        embedded_proxy = parse_usd_amount(components[0])
        recurring_proxy = parse_usd_amount(components[1])
        exit_proxy = parse_usd_amount(components[2])
        proxy_total = parse_usd_amount(components[3])
        calculation_status = components[4]
        if proxy_total is None and evidence_high is not None:
            calculation_status = "Unbenchmarked"

    relative_proxy = None
    relative_evidence = None
    if position_amount is not None and holding_period is not None:
        denominator = position_amount * holding_period
        if proxy_total is not None:
            relative_proxy = proxy_total / denominator
        if evidence_high is not None:
            relative_evidence = evidence_high / denominator

    return {
        "isin": isin,
        "security": str(record.get("product_name") or record.get("structure") or "Not reported"),
        "issuer": str(record.get("issuer") or "Not reported"),
        "cohort": cohort,
        "position": position_amount,
        "holding_period": holding_period,
        "evidence_low": evidence_low,
        "evidence_high": evidence_high,
        "embedded_proxy": embedded_proxy,
        "recurring_proxy": recurring_proxy,
        "exit_proxy": exit_proxy,
        "proxy_total": proxy_total,
        "relative_proxy": relative_proxy,
        "relative_evidence": relative_evidence,
        "status": calculation_status,
    }


def research_source_rows() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    in_register = False
    for line in RESEARCH_REPORT.read_text(encoding="utf-8").splitlines():
        if line.strip() == "## Verified Source Register":
            in_register = True
            continue
        if in_register and line.startswith("## "):
            break
        if not in_register or not line.startswith("|") or line.startswith("| ---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) != 5 or cells[0] == "ID":
            continue
        source_id, source, evidence, tier_use, limitations = cells
        locator_match = re.search(r"\((https?://[^)]+)\)", source)
        locator = locator_match.group(1) if locator_match else ""
        source_name = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", source).strip()
        searchable = " ".join((source_name, evidence, tier_use, limitations)).lower()
        if source_id.startswith("EU-"):
            jurisdiction = "European Union"
        elif source_id.startswith(("CH-", "WM-")):
            jurisdiction = "Switzerland"
        elif source_id.startswith("US-"):
            jurisdiction = "United States"
        elif source_id.startswith("AC-"):
            jurisdiction = "Academic / source-specific"
        elif source_id.startswith("EXIT-"):
            jurisdiction = "United States / Europe"
        else:
            jurisdiction = "Industry / source-specific"
        if any(term in searchable for term in ("libor", "range-accrual", "range accrual", "cms-spread", "rate-linked")):
            payoff = "Rate-linked / callable / range-accrual"
            applies_to = "Historical rate-linked cohort; no direct ISIN mapping"
        elif any(term in searchable for term in ("equity-linked", "discount certificate", "bonus certificate", "barrier reverse", "dax")):
            payoff = "Equity-linked certificates"
            applies_to = "Modern equity-linked cohort; no direct ISIN mapping"
        elif "structured product" in searchable or "structured note" in searchable:
            payoff = "Structured products / notes"
            applies_to = "Structured-product cohorts; no direct ISIN mapping"
        else:
            payoff = "General investment products"
            applies_to = "No direct ISIN mapping; context only"
        if any(term in searchable for term in ("distribution", "commission", "placement", "selling", "retrocession", "inducement")):
            cost_bucket = "Distribution / third-party compensation"
        elif any(term in searchable for term in ("service", "advisory", "custody", "brokerage")):
            cost_bucket = "Investment-service cost"
        elif any(term in searchable for term in ("exit", "spread", "unwind", "liquidity")):
            cost_bucket = "Exit / transaction cost"
        elif any(term in searchable for term in ("margin", "premium", "overpricing", "hedging", "issuer")):
            cost_bucket = "Product manufacturing / embedded cost"
        else:
            cost_bucket = "Methodology / controls"
        rows.append({
            "Source ID": source_id,
            "Source": source_name,
            "Jurisdiction / Market": jurisdiction,
            "Product / Payoff Type": payoff,
            "Applies To": applies_to,
            "Cost Bucket": cost_bucket,
            "Observed Result": evidence,
            "Tier 1 Use": tier_use,
            "Limitations": limitations,
            "Locator / Link": locator,
        })
    if not rows:
        raise ValueError("Verified Source Register is empty")
    return rows


SOURCE_HEADERS = (
    "Source ID",
    "Source",
    "Jurisdiction / Market",
    "Product / Payoff Type",
    "Applies To",
    "Cost Bucket",
    "Observed Result",
    "Tier 1 Use",
    "Limitations",
    "Locator / Link",
)


def source_table_rows(source_rows: list[dict[str, str]]) -> str:
    return "\n".join(
        "<tr>" + "".join(f"<td>{html.escape(row[header])}</td>" for header in SOURCE_HEADERS) + "</tr>"
        for row in source_rows
    )


def scenario_totals(records: list[dict[str, Any]], statuses: dict[str, str]) -> dict[str, float | int]:
    totals: dict[str, float | int] = {
        "populated_positions": 0,
        "covered_positions": 0,
        "covered_notional": 0.0,
        "evidence_low": 0.0,
        "evidence_high": 0.0,
        "proxy_low": 0.0,
        "proxy_high": 0.0,
    }
    for record in records:
        amount = usable_position_amount(record, statuses[record["isin"]])
        if amount is None:
            continue
        totals["populated_positions"] += 1
        cohort = product_cohort(record)
        if cohort == "Historical rate-linked":
            totals["covered_positions"] += 1
            totals["covered_notional"] += amount
            totals["evidence_low"] += amount * ESMA_ISSUANCE_LOW
            totals["evidence_high"] += amount * ESMA_ISSUANCE_HIGH
            totals["proxy_low"] += amount * ESMA_ISSUANCE_LOW
            totals["proxy_high"] += amount * ESMA_ISSUANCE_HIGH
        elif cohort == "Equity-linked" and (holding_period := holding_period_years(record)) is not None:
            totals["covered_positions"] += 1
            totals["covered_notional"] += amount
            totals["evidence_low"] += amount * ESMA_MODERN_ANNUAL * holding_period
            totals["evidence_high"] += amount * ESMA_MODERN_ANNUAL * holding_period
            totals["proxy_low"] += amount * SWISS_EQUITY_LINKED_ANNUAL * holding_period
            totals["proxy_high"] += amount * SWISS_EQUITY_LINKED_ANNUAL * holding_period
    return totals


def product_records() -> list[dict[str, Any]]:
    records = []
    for path in PRODUCT_DIR.glob("[XC][HS]* - *.md"):
        record, _ = read_product(path)
        if record:
            records.append(record)
    if len(records) != 29:
        raise ValueError(f"Expected 29 canonical product records, found {len(records)}")
    return sorted(records, key=lambda record: (record.get("display_order", 9999), record["isin"]))


def table_row(record: dict[str, Any], statuses: dict[str, str], yaml_fields: list[str]) -> str:
    isin = str(record["isin"])
    lifecycle_end, _ = extract_lifecycle_end(str(record.get("maturity", "")))
    status = statuses[isin]
    position = str(record.get("position_size", "Missing"))
    cohort = product_cohort(record)
    evidence_min, evidence_max = scenario_cost_range(record, status, cohort, "evidence")
    embedded_proxy, recurring_proxy, exit_proxy, proxy_total, proxy_status = proxy_component_costs(
        record, status, cohort
    )
    cells = (
        isin,
        str(record.get("product_name") or record.get("structure") or "Not reported"),
        cohort,
        format_date(str(record.get("issue_date", ""))),
        lifecycle_end,
        position,
        evidence_min,
        evidence_max,
        embedded_proxy,
        recurring_proxy,
        exit_proxy,
        proxy_total,
        proxy_status,
    ) + tuple(format_yaml_value(record.get(field)) for field in yaml_fields)
    return "<tr>" + "".join(
        f'<td class="numeric-cell" data-column-index="{index}">{html.escape(cell)}</td>'
        if is_numeric_display(cell)
        else f'<td data-column-index="{index}">{html.escape(cell)}</td>'
        for index, cell in enumerate(cells)
    ) + "</tr>"


def dashboard_html(records: list[dict[str, Any]], statuses: dict[str, str]) -> str:
    tooltips = read_tooltips()
    source_rows = research_source_rows()
    html_excluded_yaml_fields = {
        "annualised_rate",
        "barrier",
        "coupon",
        "denomination_usd",
        "downside",
        "frequency",
        "field_statuses",
        "guarantor",
        "other_comments",
        "position_size_evidence",
        "position_size_source",
        "position_size_status",
        "redemption_terms",
        "risk",
        "schema_version",
        "source_exhibit",
        "source_section",
        "tenor_years",
        "underlying",
        "end_basis",
    }
    curated_headers = (
        "ISIN",
        "Security",
        "Cohort",
        "Issue date",
        "Lifecycle end",
        "Reported position (USD)",
        "Evidence-only min (USD)",
        "Evidence-only max (USD)",
        "Proxy Cost_ Embedded product proxy (USD)",
        "Proxy Cost_ Recurring service proxy (USD, holding period)",
        "Proxy Cost_ Exit / transaction proxy (USD)",
        "Proxy total (USD)",
        "Proxy calculation status",
    )
    yaml_fields = sorted(
        {
            key
            for record in records
            for key in record
            if key not in {
                "position_size",
                "product_name",
                "isin",
                "issue_date",
                *html_excluded_yaml_fields,
            }
        }
    )
    headers = curated_headers + tuple(field.replace("_", " ").title() for field in yaml_fields)
    header_tooltips = tuple(
        tooltips["curated"].get(header, f"Dashboard column: {header}.")
        for header in curated_headers
    ) + tuple(
        tooltips["canonical"].get(field, f"Canonical YAML field: {field}.")
        for field in yaml_fields
    )
    definition_rows = "".join(
        f'<tr title="{html.escape(tooltip)}" data-tooltip="{html.escape(tooltip)}"><td class="definition-name">{html.escape(header)}</td><td>{html.escape(tooltip)}</td></tr>'
        for header, tooltip in zip(headers, header_tooltips)
    )
    header_html = "".join(
        f'<th scope="col" data-column-index="{index}" data-tooltip="{html.escape(tooltip)}" title="{html.escape(tooltip)}"><button type="button" aria-label="{html.escape(header)}. {html.escape(tooltip)}"><span class="header-label">{html.escape(header)}</span><span class="sort-icon" aria-hidden="true"></span></button><span class="column-resizer" data-resize-column="{index}" role="separator" aria-label="Resize {html.escape(header)} column"></span></th>'
        for index, (header, tooltip) in enumerate(zip(headers, header_tooltips))
    )
    rows = "\n".join(table_row(record, statuses, yaml_fields) for record in records)
    source_header_html = "".join(f'<th scope="col">{html.escape(header)}</th>' for header in SOURCE_HEADERS)
    source_rows_html = source_table_rows(source_rows)
    chart_rows = [chart_row(record, statuses) for record in records]
    chart_data = json.dumps(chart_rows, ensure_ascii=True).replace("</", "<\\/")
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Cost modelling</title>
  <style>
        :root {{
            color-scheme: light;
            font-family: Inter, Aptos, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            color: #18201d;
            background: #edf1ec;
            --ink: #18201d;
            --muted: #63706a;
            --line: #d6ded8;
            --line-strong: #b9c8be;
            --paper: #ffffff;
            --wash: #f4f7f3;
            --rail: #e3ebe4;
            --accent: #176b52;
            --accent-dark: #0f4d3b;
            --accent-soft: #dceee5;
            --radius: 10px;
        }}
        * {{ box-sizing: border-box; }}
        body {{ min-height: 100vh; margin: 0; padding: 28px; background: radial-gradient(circle at 8% 0%, #f8fbf7 0, #edf1ec 42%, #e6ece7 100%); }}
        button, input, select {{ font: inherit; }}
        button, select, input {{ border-radius: 8px; }}
        button {{ transition: border-color 160ms ease, background 160ms ease, color 160ms ease, box-shadow 160ms ease; }}
        button:focus-visible, input:focus-visible, select:focus-visible {{ outline: 3px solid rgba(23, 107, 82, 0.28); outline-offset: 2px; }}
        .shell {{ display: grid; grid-template-columns: 232px minmax(0, 1fr); gap: 18px; max-width: 1920px; margin: 0 auto; align-items: start; }}
        .views {{ position: sticky; top: 28px; padding: 20px 12px 14px; border: 1px solid var(--line); border-radius: var(--radius); background: var(--rail); box-shadow: 0 12px 28px rgba(31, 61, 48, 0.06); }}
        .views h2 {{ margin: 0 10px 16px; color: var(--accent-dark); font-size: 11px; font-weight: 800; letter-spacing: 0.14em; text-transform: uppercase; }}
        .view-list {{ display: grid; gap: 5px; margin: 0; padding: 0; list-style: none; }}
        .view-list li {{ position: relative; }}
        .view-list li.is-view-dragging {{ opacity: 0.45; }}
        .view-list li.is-view-drop-target {{ outline: 2px solid #9acbb6; outline-offset: 2px; border-radius: 8px; }}
        .view-button {{ width: 100%; padding: 11px 12px; border: 1px solid transparent; background: transparent; color: #29453a; font-size: 13px; font-weight: 650; text-align: left; cursor: pointer; }}
        .view-list li {{ cursor: grab; }}
        body.is-view-dragging .view-list li {{ cursor: grabbing; }}
        .view-button:hover {{ border-color: var(--line-strong); background: rgba(255, 255, 255, 0.62); }}
        .view-button[aria-current="page"] {{ border-color: #9acbb6; background: var(--paper); color: var(--accent-dark); box-shadow: 0 4px 12px rgba(23, 107, 82, 0.08); }}
        .view-actions {{ position: relative; margin: 20px -12px -14px; padding: 12px 12px 14px; border-top: 1px solid rgba(198, 212, 202, 0.72); }}
        .view-action-toggle {{ display: flex; width: 100%; align-items: center; justify-content: space-between; padding: 6px 2px; border: 0; background: transparent; color: #6a7d72; font-size: 11px; font-weight: 750; letter-spacing: 0.04em; text-align: left; text-transform: uppercase; cursor: pointer; }}
        .view-action-toggle::after {{ width: 7px; height: 7px; border-right: 1.5px solid currentColor; border-bottom: 1.5px solid currentColor; content: ""; transform: rotate(45deg) translateY(-2px); transition: transform 160ms ease; }}
        .view-action-toggle:hover, .view-action-toggle[aria-expanded="true"] {{ color: var(--accent-dark); }}
        .view-action-toggle[aria-expanded="true"]::after {{ transform: rotate(225deg) translate(-1px, -1px); }}
        .view-action-menu {{ position: absolute; right: 12px; bottom: calc(100% - 2px); left: 12px; z-index: 20; display: grid; gap: 2px; padding: 6px; border: 1px solid rgba(157, 181, 166, 0.78); border-radius: 9px; background: #f7faf7; box-shadow: 0 12px 28px rgba(31, 61, 48, 0.14); }}
        .view-action-menu[hidden] {{ display: none; }}
        .view-menu-item {{ padding: 9px 10px; border: 0; background: transparent; color: #38564a; font-size: 12px; font-weight: 650; text-align: left; cursor: pointer; }}
        .view-menu-item:hover, .view-menu-item:focus-visible {{ background: var(--accent-soft); color: var(--accent-dark); }}
        .view-menu-item.is-primary {{ color: var(--accent-dark); font-weight: 800; }}
        .view-menu-item.is-danger {{ margin-top: 4px; border-top: 1px solid var(--line); color: #9b4b46; }}
        .view-menu-item.is-danger:hover, .view-menu-item.is-danger:focus-visible {{ background: #fff0ee; color: #8a322d; }}
        main {{ min-width: 0; overflow: hidden; border: 1px solid var(--line); border-radius: var(--radius); background: var(--paper); box-shadow: 0 16px 36px rgba(31, 61, 48, 0.08); }}
        .toolbar {{ display: flex; flex-wrap: wrap; gap: 8px; padding: 16px 20px; border-bottom: 1px solid var(--line); background: var(--paper); }}
        .tool-button {{ padding: 9px 13px; border: 1px solid var(--line-strong); background: var(--wash); color: #29453a; font-size: 13px; font-weight: 700; cursor: pointer; }}
        #export-csv {{ margin-left: auto; }}
        .tool-button:hover, .tool-button[aria-expanded="true"] {{ border-color: #78b59d; background: var(--accent-soft); color: var(--accent-dark); }}
        .builder-panel {{ display: none; padding: 18px 20px; border-bottom: 1px solid var(--line); background: var(--wash); }}
        .builder-panel.is-open {{ display: block; }}
        .builder-panel h2 {{ margin: 0 0 13px; color: var(--accent-dark); font-size: 14px; letter-spacing: -0.01em; }}
        .builder-grid {{ display: grid; grid-template-columns: minmax(150px, 220px) minmax(120px, 180px) minmax(180px, 1fr) auto; gap: 10px; align-items: end; }}
        .builder-grid label {{ text-transform: none; letter-spacing: 0; }}
        .builder-grid select, .builder-grid input {{ width: 100%; min-width: 0; padding: 9px 11px; border: 1px solid var(--line-strong); background: var(--paper); color: var(--ink); }}
        #columns-panel {{ padding: 14px 20px 18px; background: #eef5f0; }}
        #columns-panel h2 {{ margin: 0 0 10px; font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase; }}
        .column-list, .rule-list {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 0; padding: 0; list-style: none; }}
        .column-list {{ display: grid; grid-template-columns: repeat(2, minmax(180px, 1fr)); max-width: 720px; padding: 8px; border: 1px solid var(--line); border-radius: 10px; background: rgba(255, 255, 255, 0.76); box-shadow: 0 8px 20px rgba(31, 61, 48, 0.06); overflow: visible; }}
        .column-choice {{ position: relative; display: flex; gap: 10px; align-items: center; min-height: 40px; padding: 8px 10px; border: 1px solid transparent; border-radius: 8px; background: transparent; color: #40564c; font-size: 13px; cursor: pointer; }}
        .column-choice:hover {{ border-color: var(--line); background: var(--paper); }}
        .column-choice[data-tooltip]::after {{ position: absolute; top: calc(100% + 7px); left: 10px; z-index: 30; width: max-content; max-width: 230px; padding: 8px 10px; border: 1px solid #b9d2c3; border-radius: 8px; background: #173d31; color: #f4fbf7; content: attr(data-tooltip); font-size: 12px; font-weight: 550; letter-spacing: 0; line-height: 1.35; opacity: 0; pointer-events: none; text-transform: none; transform: translateY(-3px); transition: opacity 140ms ease, transform 140ms ease; white-space: normal; box-shadow: 0 8px 18px rgba(15, 77, 59, 0.18); }}
        .column-choice[data-tooltip]:hover::after, .column-choice[data-tooltip]:focus-within::after {{ opacity: 1; transform: translateY(0); }}
        .column-choice input {{ appearance: none; position: relative; flex: 0 0 auto; width: 34px; height: 20px; margin: 0; border: 1px solid #aebfb4; border-radius: 999px; background: #d9e2dc; cursor: pointer; transition: background 160ms ease, border-color 160ms ease; }}
        .column-choice input::after {{ position: absolute; top: 3px; left: 3px; width: 12px; height: 12px; border-radius: 50%; background: white; box-shadow: 0 1px 3px rgba(24, 32, 29, 0.2); content: ""; transition: transform 160ms ease; }}
        .column-choice input:checked {{ border-color: var(--accent); background: var(--accent); }}
        .column-choice input:checked::after {{ transform: translateX(14px); }}
        .column-choice:has(input:checked) {{ color: var(--accent-dark); font-weight: 700; }}
        .rule-list {{ display: grid; gap: 6px; margin-top: 12px; }}
        .rule {{ display: flex; flex-wrap: wrap; gap: 8px; align-items: center; padding: 8px 10px; border: 1px solid var(--line); border-radius: 8px; background: var(--paper); color: #50625a; font-size: 13px; }}
        .rule strong {{ color: var(--accent-dark); }}
        .rule button {{ padding: 4px 8px; border: 1px solid var(--line-strong); background: transparent; color: var(--accent-dark); font-size: 12px; cursor: pointer; }}
        .rule button:hover {{ background: var(--accent-soft); }}
        .empty-state {{ color: var(--muted); font-size: 13px; }}
        .definitions-view {{ padding: 20px; }}
        .definitions-view[hidden] {{ display: none; }}
        .definitions-view h2 {{ margin: 0 0 6px; color: var(--accent-dark); font-size: 18px; letter-spacing: -0.01em; }}
        .definitions-intro {{ max-width: 72ch; margin: 0 0 18px; color: var(--muted); font-size: 13px; line-height: 1.5; }}
        .definitions-table {{ width: 100%; min-width: 0; table-layout: fixed; }}
        .definitions-table th {{ position: static; padding: 12px 16px; background: #edf4ef; color: #315044; font-size: 11px; font-weight: 850; letter-spacing: 0.06em; text-transform: uppercase; }}
        .definitions-table td {{ white-space: normal; overflow-wrap: anywhere; }}
        .definitions-table .definition-name {{ width: 30%; color: var(--accent-dark); font-weight: 800; }}
        .definitions-table tbody tr:hover {{ background: #f0f8f3; }}
        .group-row td {{ padding: 10px 16px; border-top: 1px solid var(--line-strong); background: var(--accent-soft); color: var(--accent-dark); font-size: 11px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; }}
        .group-row .group-indent {{ display: inline-block; width: var(--group-indent); }}
        .filters {{ display: flex; flex-wrap: wrap; gap: 14px 24px; align-items: end; padding: 17px 20px; border-bottom: 1px solid var(--line); background: var(--wash); }}
        label {{ display: grid; gap: 6px; color: #52675c; font-size: 11px; font-weight: 800; letter-spacing: 0.08em; text-transform: uppercase; }}
        select {{ min-width: 210px; padding: 10px 30px 10px 11px; border: 1px solid var(--line-strong); background: var(--paper); color: var(--ink); cursor: pointer; }}
        select:hover, input:hover {{ border-color: #78b59d; }}
        .table-scroll {{ width: 100%; max-width: 100%; overflow-x: auto; overflow-y: visible; overscroll-behavior-x: contain; }}
        table {{ width: max-content; min-width: 100%; table-layout: fixed; border-collapse: separate; border-spacing: 0; font-size: 13px; line-height: 1.45; }}
        thead {{ background: #edf4ef; }}
        th {{ position: relative; position: sticky; top: 0; z-index: 1; overflow: hidden; text-align: left; border-bottom: 1px solid var(--line-strong); white-space: normal; }}
        th button {{ display: flex; width: 100%; min-width: 0; min-height: 52px; gap: 7px; align-items: center; justify-content: space-between; padding: 13px 20px 13px 16px; border: 0; border-radius: 0; background: transparent; color: #315044; font-size: 11px; font-weight: 850; letter-spacing: 0.06em; line-height: 1.25; text-align: left; text-transform: uppercase; cursor: pointer; white-space: normal; overflow: visible; overflow-wrap: break-word; text-overflow: clip; }}
        .header-label {{ min-width: 0; }}
        .sort-icon {{ position: relative; flex: 0 0 9px; width: 9px; height: 14px; opacity: 0.5; }}
        .sort-icon::before, .sort-icon::after {{ position: absolute; left: 0; width: 0; height: 0; content: ""; border-right: 4.5px solid transparent; border-left: 4.5px solid transparent; }}
        .sort-icon::before {{ top: 1px; border-bottom: 5px solid currentColor; }}
        .sort-icon::after {{ bottom: 1px; border-top: 5px solid currentColor; }}
        th[aria-sort="ascending"] .sort-icon, th[aria-sort="descending"] .sort-icon {{ opacity: 1; }}
        th[aria-sort="ascending"] .sort-icon::after, th[aria-sort="descending"] .sort-icon::before {{ opacity: 0.2; }}
        body.is-column-dragging th button {{ cursor: grabbing; }}
        th button:hover {{ background: #dcebe1; color: var(--accent-dark); }}
        th[data-tooltip]::after {{ position: absolute; top: calc(100% + 8px); left: 12px; z-index: 20; width: max-content; max-width: 230px; padding: 8px 10px; border: 1px solid #b9d2c3; border-radius: 8px; background: #173d31; color: #f4fbf7; content: attr(data-tooltip); font-size: 12px; font-weight: 550; letter-spacing: 0; line-height: 1.35; opacity: 0; pointer-events: none; text-transform: none; transform: translateY(-3px); transition: opacity 140ms ease, transform 140ms ease; white-space: normal; box-shadow: 0 8px 18px rgba(15, 77, 59, 0.18); }}
        th[data-tooltip]:hover::after, th[data-tooltip]:focus-within::after {{ opacity: 1; transform: translateY(0); }}
        .column-resizer {{ position: absolute; top: 0; right: 0; bottom: 0; z-index: 2; width: 10px; cursor: col-resize; touch-action: none; }}
        .column-resizer:hover, body.is-resizing .column-resizer {{ background: rgba(23, 107, 82, 0.22); }}
        body.is-resizing, body.is-resizing * {{ cursor: col-resize !important; user-select: none !important; }}
        td {{ overflow: hidden; padding: 12px 16px; border-bottom: 1px solid #e7ede8; vertical-align: top; white-space: nowrap; text-overflow: ellipsis; }}
        tbody tr:nth-child(even) {{ background: #fbfdfb; }}
        tbody tr:hover {{ background: #f0f8f3; }}
        td:first-child {{ color: var(--accent); font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 12px; font-weight: 800; letter-spacing: 0.02em; }}
        td.numeric-cell {{ font-variant-numeric: tabular-nums; text-align: center; white-space: nowrap; }}
        td.usd-column, th.usd-column, th.usd-column button {{ text-align: center; }}
        th.numeric-column, th.numeric-column button {{ text-align: center; }}
        @media (max-width: 760px) {{
            body {{ padding: 12px; }}
            .shell {{ grid-template-columns: 1fr; gap: 12px; }}
            .views {{ position: static; padding: 14px 10px 10px; }}
            .views h2 {{ margin-bottom: 10px; }}
            .view-list {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }}
            .view-actions {{ grid-template-columns: repeat(2, minmax(0, 1fr)); margin-top: 12px; padding-top: 10px; }}
            .builder-grid {{ grid-template-columns: 1fr; }}
            .column-list {{ grid-template-columns: 1fr; }}
            .filters {{ align-items: stretch; }}
            .filters label, .filters select {{ width: 100%; }}
            .toolbar, .builder-panel, .filters {{ padding-left: 14px; padding-right: 14px; }}
            .definitions-view {{ padding: 14px; }}
            .definitions-table .definition-name {{ width: 40%; }}
        }}
        @media (prefers-reduced-motion: reduce) {{
            *, *::before, *::after {{ scroll-behavior: auto !important; transition-duration: 0.01ms !important; }}
        }}
        .backend-banner {{ display: flex; gap: 12px; align-items: center; justify-content: space-between; max-width: 1920px; margin: 0 auto 14px; padding: 12px 16px; border: 1px solid #e6c66b; border-radius: var(--radius); background: #fdf6e0; color: #6b5410; font-size: 13px; }}
        .backend-banner[hidden] {{ display: none; }}
        .backend-banner button {{ flex: 0 0 auto; padding: 6px 10px; border: 1px solid #d9b957; background: transparent; color: #6b5410; font-size: 12px; font-weight: 700; cursor: pointer; }}
          .cost-charts {{ position: relative; padding: 20px 20px 58px; overflow-x: auto; background: var(--paper); }}
          .cost-charts[hidden] {{ display: none; }}
          .chart-header {{ display: flex; flex-wrap: wrap; gap: 14px 20px; align-items: end; justify-content: space-between; margin-bottom: 16px; }}
          .chart-header h2 {{ margin: 0; color: var(--accent-dark); font-size: 18px; letter-spacing: -0.01em; }}
          .chart-intro {{ max-width: 72ch; margin: 5px 0 0; color: var(--muted); font-size: 13px; line-height: 1.45; }}
          .chart-actions {{ display: inline-flex; flex-wrap: wrap; gap: 8px; align-items: center; }}
          .chart-toggle {{ display: inline-flex; gap: 2px; padding: 3px; border: 1px solid var(--line-strong); border-radius: 9px; background: var(--wash); }}
          .chart-toggle button {{ padding: 8px 12px; border: 0; border-radius: 6px; background: transparent; color: #52675c; font-size: 12px; font-weight: 800; cursor: pointer; }}
          .chart-toggle button[aria-pressed="true"] {{ background: var(--accent); color: white; box-shadow: 0 2px 6px rgba(23, 107, 82, 0.18); }}
          .chart-legend {{ display: flex; flex-wrap: wrap; gap: 16px; align-items: center; justify-content: center; margin: 12px auto 0; color: #52675c; font-size: 12px; font-weight: 700; }}
          .chart-legend span::before {{ display: inline-block; width: 10px; height: 10px; margin-right: 6px; border-radius: 2px; content: ""; vertical-align: -1px; }}
          .chart-legend .proxy-embedded-key::before {{ background: #176b52; }}
          .chart-legend .proxy-recurring-key::before {{ background: #2f8b6c; }}
          .chart-legend .proxy-exit-key::before {{ background: #79b89d; }}
          .chart-legend .evidence-min-key::before {{ background: #62676b; }}
          .chart-legend .evidence-delta-key::before {{ background: #c5c9cc; }}
          .chart-stage {{ min-width: 900px; border-top: 1px solid var(--line); }}
          .chart-svg {{ display: block; width: 100%; min-width: 900px; height: 540px; overflow: visible; }}
          .chart-gridline {{ stroke: #dfe8e1; stroke-width: 1; }}
          .chart-axis {{ stroke: #9eb3a5; stroke-width: 1; }}
          .chart-tick, .chart-label {{ fill: #63706a; font-size: 11px; }}
          .chart-label {{ fill: #29453a; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 10px; font-weight: 800; }}
        .chart-bar {{ cursor: help; transition: opacity 140ms ease; }}
          .chart-bar:hover, .chart-bar:focus {{ opacity: 0.78; outline: none; }}
          .chart-bar.proxy {{ fill: #176b52; }}
          .chart-bar.proxy-embedded {{ fill: #176b52; }}
          .chart-bar.proxy-recurring {{ fill: #2f8b6c; }}
          .chart-bar.proxy-exit {{ fill: #79b89d; }}
          .chart-bar.evidence {{ fill: #62676b; }}
          .chart-bar.evidence-delta {{ fill: #c5c9cc; }}
          .chart-note {{ position: absolute; bottom: 20px; left: 20px; max-width: calc(100% - 72px); margin: 0; color: var(--muted); font-size: 12px; }}
          .chart-footer {{ position: absolute; right: 20px; bottom: 14px; display: flex; align-items: center; justify-content: flex-end; margin: 0; }}
          .chart-export-icon {{ display: inline-grid; width: 32px; height: 32px; place-items: center; padding: 0; border: 1px solid transparent; border-radius: 8px; background: transparent; color: #6d8177; cursor: pointer; }}
          .chart-export-icon:hover, .chart-export-icon:focus-visible {{ border-color: var(--line-strong); background: var(--wash); color: var(--accent-dark); }}
          .chart-export-icon svg {{ width: 17px; height: 17px; fill: none; stroke: currentColor; stroke-linecap: round; stroke-linejoin: round; stroke-width: 1.8; }}
        .chart-tooltip {{ position: fixed; z-index: 40; width: min(300px, calc(100vw - 24px)); padding: 12px 14px; border: 1px solid #9fc3b0; border-radius: 10px; background: #173d31; color: #f4fbf7; box-shadow: 0 12px 28px rgba(15, 77, 59, 0.22); font-size: 12px; line-height: 1.45; pointer-events: none; }}
        .chart-tooltip[hidden] {{ display: none; }}
        .chart-tooltip strong {{ display: block; margin-bottom: 5px; color: white; font-size: 13px; }}
        .chart-tooltip span {{ display: block; color: #d7ebe0; }}
        .chart-tooltip .tooltip-row {{ display: flex; gap: 10px; justify-content: space-between; padding: 2px 0; }}
        .chart-tooltip .tooltip-label {{ color: #b9d7c8; }}
        .chart-tooltip .tooltip-value {{ color: #f4fbf7; font-variant-numeric: tabular-nums; text-align: right; }}
                .sources-view {{ padding: 20px; background: var(--paper); }}
                .sources-view[hidden] {{ display: none; }}
                .sources-view h2 {{ margin: 0 0 6px; color: var(--accent-dark); font-size: 18px; }}
                .sources-intro {{ max-width: 80ch; margin: 0 0 18px; color: var(--muted); font-size: 13px; line-height: 1.5; }}
                .sources-table {{ width: max-content; min-width: 100%; table-layout: fixed; }}
                .sources-table th {{ position: static; min-width: 150px; padding: 12px 14px; background: #edf4ef; color: #315044; font-size: 11px; font-weight: 850; letter-spacing: 0.05em; text-align: left; text-transform: uppercase; white-space: normal; }}
                .sources-table th:nth-child(1) {{ min-width: 90px; }}
                .sources-table th:nth-child(2) {{ min-width: 280px; }}
                .sources-table th:nth-child(7), .sources-table th:nth-child(8), .sources-table th:nth-child(9) {{ min-width: 340px; }}
                .sources-table th:nth-child(10) {{ min-width: 280px; }}
                .sources-table td {{ max-width: 440px; padding: 12px 14px; white-space: normal; overflow-wrap: anywhere; vertical-align: top; }}
                .sources-table tbody tr:hover {{ background: #f0f8f3; }}
                @media (max-width: 720px) {{
                        .sources-view {{ padding: 14px; }}
                        .sources-table td {{ max-width: 300px; }}
                }}
  </style>
</head>
<body>
    <div class="backend-banner" id="backend-banner" role="status" hidden>
        <span>View changes are only saved in this browser tab. Run <code>python "90. Scripts/cost_model_server.py"</code> and open <code>http://127.0.0.1:8000/</code> to keep columns, sorting and filters across refreshes and devices.</span>
        <button type="button" id="backend-banner-dismiss">Dismiss</button>
    </div>
    <div class="shell">
        <nav class="views" id="views-nav" aria-label="Views">
            <h2>Views</h2>
            <ul class="view-list">
                <li><button class="view-button" type="button" data-view="current">Current</button></li>
                <li><button class="view-button" type="button" data-view="position-size">by Position Size</button></li>
                <li><button class="view-button" type="button" data-view="full dataset">full dataset</button></li>
                <li><button class="view-button" type="button" data-view="Sources">Sources</button></li>
                <li><button class="view-button" type="button" data-view="Definitions">Definitions</button></li>
            </ul>
            <div class="view-actions">
                <button class="view-action-toggle" id="view-actions-toggle" type="button" aria-expanded="false" aria-haspopup="menu">View actions</button>
                <div class="view-action-menu" id="view-action-menu" role="menu" hidden>
                    <button class="view-menu-item is-primary" type="button" role="menuitem" data-view-action="new">Create new view</button>
                    <button class="view-menu-item" type="button" role="menuitem" data-view-action="duplicate">Duplicate current view</button>
                    <button class="view-menu-item" type="button" role="menuitem" data-view-action="rename">Rename current view</button>
                    <button class="view-menu-item is-danger" type="button" role="menuitem" data-view-action="delete">Delete current view</button>
                </div>
            </div>
        </nav>
        <main>
            <div class="toolbar" aria-label="View builder">
                <button class="tool-button" type="button" data-panel="columns-panel" aria-expanded="false">Columns</button>
                <button class="tool-button" type="button" data-panel="filters-panel" aria-expanded="false">Filters</button>
                <button class="tool-button" type="button" data-panel="groups-panel" aria-expanded="false">Group by</button>
                <button class="tool-button" type="button" data-panel="sorts-panel" aria-expanded="false">Sort</button>
                <button class="tool-button" id="export-csv" type="button">Export CSV</button>
            </div>
            <section class="builder-panel" id="columns-panel" aria-label="Choose columns">
                <h2>Visible columns</h2>
                <ul class="column-list" id="column-list" aria-label="Toggle visible columns"></ul>
            </section>
            <section class="builder-panel" id="filters-panel" aria-label="Choose filters">
                <h2>Filter rows</h2>
                <div class="builder-grid">
                    <label>Column<select id="filter-column"></select></label>
                    <label>Condition<select id="filter-operator"><option value="contains">contains</option><option value="equals">is exactly</option><option value="not-empty">is not empty</option></select></label>
                    <label>Value<input id="filter-value" type="text" placeholder="Filter value"></label>
                    <button class="tool-button" id="add-filter" type="button">Add filter</button>
                </div>
                <ul class="rule-list" id="filter-list"></ul>
            </section>
            <section class="builder-panel" id="groups-panel" aria-label="Choose groups">
                <h2>Nested groups</h2>
                <div class="builder-grid">
                    <label>Group rows by<select id="group-column"></select></label>
                    <span></span><span></span>
                    <button class="tool-button" id="add-group" type="button">Add group</button>
                </div>
                <ul class="rule-list" id="group-list"></ul>
            </section>
            <section class="builder-panel" id="sorts-panel" aria-label="Choose sorting">
                <h2>Sort rows</h2>
                <div class="builder-grid">
                    <label>Column<select id="sort-column"></select></label>
                    <label>Direction<select id="sort-direction"><option value="asc">A to Z</option><option value="desc">Z to A</option></select></label>
                    <span></span>
                    <button class="tool-button" id="add-sort" type="button">Add sort</button>
                </div>
                <ul class="rule-list" id="sort-list"></ul>
            </section>
            <section class="definitions-view" id="definitions-view" aria-labelledby="definitions-heading" hidden>
                <h2 id="definitions-heading">Definitions</h2>
                <p class="definitions-intro">One definition for every column and canonical field shown in the dashboard. Hover a row to see its definition as a tooltip.</p>
                <div class="table-scroll">
                    <table class="definitions-table">
                        <thead><tr><th scope="col">Column / field</th><th scope="col">Definition</th></tr></thead>
                        <tbody>{definition_rows}</tbody>
                    </table>
                </div>
            </section>
            <section class="sources-view" id="sources-view" aria-labelledby="sources-heading" hidden>
                <h2 id="sources-heading">Research sources</h2>
                <p class="sources-intro">Verified research findings, their intended Tier 1 use, and the cohorts they may inform. Applicability is cohort-level unless a direct ISIN mapping is documented.</p>
                <div class="table-scroll">
                    <table class="sources-table" id="sources-table">
                        <thead><tr>{source_header_html}</tr></thead>
                        <tbody>{source_rows_html}</tbody>
                    </table>
                </div>
            </section>
            <section class="cost-charts" id="cost-charts" aria-labelledby="cost-charts-heading" hidden>
                <div class="chart-header">
                    <div>
                        <h2 id="cost-charts-heading">Cost by ISIN</h2>
                        <p class="chart-intro" id="chart-intro">Total proxy cost compared with the maximum evidence-based cost estimate.</p>
                    </div>
                    <div class="chart-actions">
                        <div class="chart-toggle" role="group" aria-label="Chart units">
                            <button type="button" data-chart-mode="absolute" aria-pressed="true">Absolute</button>
                            <button type="button" data-chart-mode="relative" aria-pressed="false">Relative*</button>
                        </div>
                        <div class="chart-toggle" role="group" aria-label="Chart detail">
                            <button type="button" data-chart-detail="summary" aria-pressed="true">Summary</button>
                            <button type="button" data-chart-detail="detailed" aria-pressed="false">Detailed</button>
                        </div>
                    </div>
                </div>
                <div class="chart-stage" id="chart-stage"></div>
                <div class="chart-legend" id="chart-legend" aria-label="Chart legend"></div>
                <div class="chart-tooltip" id="chart-tooltip" role="tooltip" hidden></div>
                <p class="chart-note">* Relative values are annualized as cost USD / usable position size / holding period years.</p>
                <div class="chart-footer">
                    <button class="chart-export-icon" id="export-chart-svg" type="button" aria-label="Export chart as SVG" title="Export chart as SVG">
                        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3v11"></path><path d="m8 10 4 4 4-4"></path><path d="M5 18v2h14v-2"></path></svg>
                    </button>
                </div>
            </section>
        <div class="table-scroll" id="main-table-scroll">
        <table id="cost-model">
            <colgroup id="column-widths"></colgroup>
      <thead><tr>{header_html}</tr></thead>
      <tbody>
{rows}
      </tbody>
    </table>
        </div>
    </main>
  </div>
  <script>
    const viewsNav = document.querySelector('#views-nav');
        const panelButtons = [...document.querySelectorAll('[data-panel]')];
        const panels = [...document.querySelectorAll('.builder-panel')];
        const table = document.querySelector('#cost-model');
        const headerNames = [...table.tHead.rows[0].cells].map((cell) => cell.textContent.trim());
        const columnTooltips = {json.dumps(header_tooltips)};
        const originalRows = [...table.tBodies[0].rows];
        const numericColumns = headerNames.map((_, index) => originalRows.some((row) => row.cells[index]?.classList.contains('numeric-cell')));
        const usdColumns = headerNames.map((name) => /\\(USD\\)$/i.test(name));
        [...table.tHead.rows[0].cells].forEach((cell, index) => {{
            cell.classList.toggle('numeric-column', numericColumns[index]);
            cell.classList.toggle('usd-column', usdColumns[index]);
        }});
        const curatedColumnCount = 13;
        const curatedColumnWidths = [120, 340, 180, 130, 150, 170, 190, 190, 190, 190, 190, 190, 190];
        const defaultColumnWidths = headerNames.map((_, index) => curatedColumnWidths[index] || 180);
        function createViewState(allColumns = false) {{
            const visible = allColumns ? headerNames.map((_, index) => index) : headerNames.map((_, index) => index).filter((index) => index < curatedColumnCount);
            return {{ visible, filters: [], groups: [], sorts: [], widths: [...defaultColumnWidths], order: headerNames.map((_, index) => index) }};
        }}
        const positionSizeVisible = headerNames.map((name, index) => /position basis|reported position|position-size/i.test(name) ? index : -1).filter((index) => index >= 0);
        const defaultViewState = {{
            current: createViewState(),
            'position-size': {{ ...createViewState(), visible: [...new Set([...createViewState().visible, ...positionSizeVisible])] }},
            'full dataset': createViewState(true),
            '03c. Cost charts': {{ mode: 'absolute', detail: 'summary' }},
        }};
        const sourceViewName = 'Sources';
        const chartViewName = '03c. Cost charts';
        const chartData = {chart_data};
        let viewState = JSON.parse(localStorage.getItem('jtc-cost-model-views') || 'null') || defaultViewState;
        if (!viewState['full dataset']) viewState['full dataset'] = createViewState(true);
        if (!viewState[chartViewName]) viewState[chartViewName] = {{ mode: 'absolute', detail: 'summary' }};
        viewState[chartViewName].mode = viewState[chartViewName].mode === 'relative' ? 'relative' : 'absolute';
        viewState[chartViewName].detail = viewState[chartViewName].detail === 'detailed' ? 'detailed' : 'summary';
        let viewOrder = JSON.parse(localStorage.getItem('jtc-cost-model-view-order') || 'null');
        let viewsLoaded = false;
        let activeView = null;
        const tableBody = table.tBodies[0];
        const tableScroll = document.querySelector('#main-table-scroll');
        const widthColumns = document.querySelector('#column-widths');
        const chartView = document.querySelector('#cost-charts');
        const chartStage = document.querySelector('#chart-stage');
        const chartModeButtons = [...document.querySelectorAll('[data-chart-mode]')];
        const chartDetailButtons = [...document.querySelectorAll('[data-chart-detail]')];
        headerNames.forEach((_, index) => {{
            const column = document.createElement('col');
            column.dataset.columnIndex = index;
            widthColumns.append(column);
        }});
        const columnLists = [document.querySelector('#filter-column'), document.querySelector('#group-column'), document.querySelector('#sort-column')];
        columnLists.forEach((select) => headerNames.forEach((name, index) => select.add(new Option(name, index))));
        const columnList = document.querySelector('#column-list');
        headerNames.map((name, index) => ({{ name, index }})).sort((left, right) => left.name.localeCompare(right.name, undefined, {{ sensitivity: 'base' }})).forEach(({{ name, index }}) => {{
            const item = document.createElement('li');
            item.innerHTML = `<label class="column-choice" data-tooltip="${{columnTooltips[index]}}" title="${{columnTooltips[index]}}"><input type="checkbox" data-column="${{index}}" checked> ${{name}}</label>`;
            columnList.append(item);
        }});

        function activeState() {{
            const state = viewState[activeView];
            state.widths = headerNames.map((_, index) => Number.isFinite(state.widths?.[index]) ? state.widths[index] : defaultColumnWidths[index]);
            const savedOrder = Array.isArray(state.order) ? state.order.filter((index) => Number.isInteger(index) && index >= 0 && index < headerNames.length) : [];
            state.order = [...new Set(savedOrder)].concat(headerNames.map((_, index) => index).filter((index) => !savedOrder.includes(index)));
            return state;
        }}
        function normalizeViewOrder() {{
            const names = Object.keys(viewState);
            const saved = Array.isArray(viewOrder) ? viewOrder.filter((name) => typeof name === 'string' && names.includes(name)) : [];
            viewOrder = [...new Set(saved)].concat(names.filter((name) => !saved.includes(name)));
            if (activeView !== 'Definitions' && activeView !== sourceViewName && !viewOrder.includes(activeView)) activeView = viewOrder[0] || names[0];
        }}
        function saveViewOrder() {{
            localStorage.setItem('jtc-cost-model-view-order', JSON.stringify(viewOrder));
        }}
        function valueFor(row, index) {{ return row.querySelector(`[data-column-index="${{index}}"]`).textContent.trim(); }}
        function numericValue(value) {{
            if (!/^-?[\\d,]+(?:\\.\\d+)?%?$/.test(value)) return null;
            return Number(value.replace(/[,%]/g, ""));
        }}
        function matchesFilter(row, filter) {{
            const value = valueFor(row, filter.column).toLowerCase();
            const target = filter.value.toLowerCase();
            if (filter.operator === 'not-empty') return value !== '';
            if (filter.operator === 'equals') return value === target;
            return value.includes(target);
        }}
        function compareRows(left, right, sorts) {{
            for (const sort of sorts) {{
                const leftValue = valueFor(left, sort.column);
                const rightValue = valueFor(right, sort.column);
                const leftNumber = numericColumns[sort.column] ? numericValue(leftValue) : null;
                const rightNumber = numericColumns[sort.column] ? numericValue(rightValue) : null;
                let result;
                if (leftNumber !== null && rightNumber !== null) result = leftNumber - rightNumber;
                else if (leftNumber !== null) return -1;
                else if (rightNumber !== null) return 1;
                else result = leftValue.localeCompare(rightValue, undefined, {{ numeric: true, sensitivity: 'base' }});
                if (result !== 0) return sort.direction === 'desc' ? -result : result;
            }}
            return 0;
        }}
        function escapeHtml(value) {{
            return String(value).replace(/[&<>"']/g, (character) => ({{ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }})[character]);
        }}
        function formatChartValue(value, mode) {{
            if (value === null || !Number.isFinite(value)) return 'N/A';
            if (mode === 'relative') return `${{(value * 100).toFixed(2)}}%`;
            return `$${{Math.round(value).toLocaleString('en-US')}}`;
        }}
        function renderCostChart() {{
            const state = viewState[chartViewName] || (viewState[chartViewName] = {{ mode: 'absolute', detail: 'summary' }});
            const mode = state.mode === 'relative' ? 'relative' : 'absolute';
            const detail = state.detail === 'detailed' ? 'detailed' : 'summary';
            const valueKey = mode === 'relative' ? 'relative_proxy' : 'proxy_total';
            const evidenceKey = mode === 'relative' ? 'relative_evidence' : 'evidence_high';
            const chartValue = (row, key) => {{
                const value = row[key];
                if (mode === 'absolute' || key.startsWith('relative_') || value === null || !Number.isFinite(value)) return value;
                const denominator = row.position * row.holding_period;
                return Number.isFinite(denominator) && denominator > 0 ? value / denominator : null;
            }};
            const detailLegend = detail === 'detailed'
                ? [['proxy-embedded-key', 'Embedded product proxy'], ['proxy-recurring-key', 'Recurring service proxy'], ['proxy-exit-key', 'Exit / transaction proxy'], ['evidence-min-key', 'Evidence minimum'], ['evidence-delta-key', 'Evidence range to maximum']]
                : [['proxy-embedded-key', 'Total proxy cost'], ['evidence-min-key', 'Evidence cost (max)']];
            document.querySelector('#chart-legend').innerHTML = detailLegend.map(([className, label]) => `<span class="${{className}}">${{label}}</span>`).join('');
            const rows = [...chartData].filter((row) => Number.isFinite(row[valueKey]) || Number.isFinite(row[evidenceKey])).sort((left, right) => {{
                const leftValue = left[valueKey];
                const rightValue = right[valueKey];
                if (leftValue === null && rightValue === null) return left.isin.localeCompare(right.isin);
                if (leftValue === null) return 1;
                if (rightValue === null) return -1;
                return rightValue - leftValue || left.isin.localeCompare(right.isin);
            }});
            const width = Math.max(900, rows.length * 92 + 112);
            const height = 540;
            const margin = {{ top: 28, right: 24, bottom: 72, left: 88 }};
            const plotWidth = width - margin.left - margin.right;
            const plotHeight = height - margin.top - margin.bottom;
            const values = rows.flatMap((row) => [chartValue(row, valueKey), chartValue(row, evidenceKey)]).filter((value) => value !== null && Number.isFinite(value));
            const dataMax = Math.max(...values, 0);
            let maxValue = Math.max(dataMax, 1);
            let tickCount = 4;
            if (mode === 'relative') {{
                const percentMax = dataMax * 100;
                const targetStep = percentMax / 4 || 1;
                const magnitude = 10 ** Math.floor(Math.log10(targetStep));
                const normalizedStep = targetStep / magnitude;
                const niceStep = ([1, 2, 2.5, 5, 10].find((step) => normalizedStep <= step) || 10) * magnitude;
                const axisMaxPercent = Math.max(niceStep, Math.ceil(percentMax / niceStep) * niceStep);
                maxValue = axisMaxPercent / 100;
                tickCount = Math.round(axisMaxPercent / niceStep);
            }}
            const barWidth = Math.min(25, Math.max(12, plotWidth / rows.length / 3.6));
            const groupWidth = plotWidth / Math.max(rows.length, 1);
            const y = (value) => margin.top + plotHeight - (value / maxValue) * plotHeight;
            const tickLabel = (value) => mode === 'relative' ? `${{(value * 100).toFixed(1)}}%` : `$${{(Math.round(value / 10000) * 10000).toLocaleString('en-US')}}`;
            let markup = `<svg class="chart-svg" role="img" aria-labelledby="cost-chart-title cost-chart-desc" viewBox="0 0 ${{width}} ${{height}}"><title id="cost-chart-title">Cost comparison by ISIN</title><desc id="cost-chart-desc">Vertical clustered bars sorted from highest to lowest total proxy cost. Each ISIN has a proxy cost bar and an evidence maximum bar.</desc>`;
            for (let tick = 0; tick <= tickCount; tick += 1) {{
                const value = maxValue * tick / tickCount;
                const yPosition = y(value);
                markup += `<line class="chart-gridline" x1="${{margin.left}}" x2="${{width - margin.right}}" y1="${{yPosition}}" y2="${{yPosition}}"></line><text class="chart-tick" x="${{margin.left - 10}}" y="${{yPosition + 4}}" text-anchor="end">${{escapeHtml(tickLabel(value))}}</text>`;
            }}
            markup += `<line class="chart-axis" x1="${{margin.left}}" x2="${{width - margin.right}}" y1="${{margin.top + plotHeight}}" y2="${{margin.top + plotHeight}}"></line>`;
            rows.forEach((row, index) => {{
                const center = margin.left + groupWidth * (index + 0.5);
                const proxyX = center - barWidth - 2;
                const evidenceX = center + 2;
                const evidenceLow = chartValue(row, 'evidence_low');
                const evidenceHigh = chartValue(row, 'evidence_high');
                const evidenceDelta = Number.isFinite(evidenceLow) && Number.isFinite(evidenceHigh) ? Math.max(0, evidenceHigh - evidenceLow) : null;
                const bars = detail === 'detailed'
                    ? [[chartValue(row, 'embedded_proxy'), proxyX, 'proxy-embedded', 'Embedded product proxy'], [chartValue(row, 'recurring_proxy'), proxyX, 'proxy-recurring', 'Recurring service proxy'], [chartValue(row, 'exit_proxy'), proxyX, 'proxy-exit', 'Exit / transaction proxy'], [evidenceLow, evidenceX, 'evidence', 'Evidence minimum'], [evidenceDelta, evidenceX, 'evidence-delta', 'Evidence range to maximum']]
                    : [[chartValue(row, valueKey), proxyX, 'proxy', 'Total proxy cost'], [chartValue(row, evidenceKey), evidenceX, 'evidence', 'Evidence cost (max)']];
                const evidenceRange = `${{formatChartValue(evidenceLow, mode)}} - ${{formatChartValue(evidenceHigh, mode)}}`;
                const position = row.position === null ? 'N/A' : `$${{Math.round(row.position).toLocaleString('en-US')}}`;
                const holdingPeriod = row.holding_period === null ? 'N/A' : `${{row.holding_period.toFixed(2)}} years`;
                const embeddedProxy = formatChartValue(chartValue(row, 'embedded_proxy'), mode);
                const recurringProxy = formatChartValue(chartValue(row, 'recurring_proxy'), mode);
                const exitProxy = formatChartValue(chartValue(row, 'exit_proxy'), mode);
                let proxyStack = 0;
                let evidenceStack = 0;
                bars.forEach(([value, x, series, label]) => {{
                    if (value === null || !Number.isFinite(value) || value <= 0) return;
                    const isEvidence = x === evidenceX;
                    const stack = isEvidence ? evidenceStack : proxyStack;
                    const barY = y(stack + value);
                    const barHeight = y(stack) - barY;
                    if (isEvidence) evidenceStack += value;
                    else proxyStack += value;
                    const detailText = `${{row.isin}} | ${{row.security}} | Issuer: ${{row.issuer}} | ${{label}}: ${{formatChartValue(value, mode)}} | ${{series.startsWith('proxy') && detail === 'summary' ? `Embedded product proxy: ${{embeddedProxy}} | Recurring service proxy: ${{recurringProxy}} | Exit / transaction proxy: ${{exitProxy}}` : `Evidence range: ${{evidenceRange}}`}} | Position: ${{position}} | Holding period: ${{holdingPeriod}} | Status: ${{row.status}}`;
                    markup += `<rect class="chart-bar ${{series}}" tabindex="0" data-isin="${{escapeHtml(row.isin)}}" data-security="${{escapeHtml(row.security)}}" data-issuer="${{escapeHtml(row.issuer)}}" data-series="${{escapeHtml(series)}}" data-label="${{escapeHtml(label)}}" data-value="${{escapeHtml(formatChartValue(value, mode))}}" data-range="${{escapeHtml(evidenceRange)}}" data-embedded-proxy="${{escapeHtml(embeddedProxy)}}" data-recurring-proxy="${{escapeHtml(recurringProxy)}}" data-exit-proxy="${{escapeHtml(exitProxy)}}" data-position="${{escapeHtml(position)}}" data-holding-period="${{escapeHtml(holdingPeriod)}}" data-status="${{escapeHtml(row.status)}}" x="${{x}}" y="${{barY}}" width="${{barWidth}}" height="${{Math.max(barHeight, 1)}}" role="img" aria-label="${{escapeHtml(detailText)}}"><title>${{escapeHtml(detailText)}}</title></rect>`;
                }});
                const labelY = margin.top + plotHeight + 22;
                markup += `<text class="chart-label" x="${{center}}" y="${{labelY}}" text-anchor="middle">${{escapeHtml(row.isin)}}</text>`;
            }});
            markup += '</svg>';
            chartStage.innerHTML = markup;
            const tooltip = document.querySelector('#chart-tooltip');
            const hideTooltip = () => {{ tooltip.hidden = true; }};
            const showTooltip = (event) => {{
                const bar = event.currentTarget;
                const rows = [
                    ['Security', bar.dataset.security],
                    ['Issuer', bar.dataset.issuer],
                    ['Measure', `${{bar.dataset.label}}: ${{bar.dataset.value}}`],
                    ...(bar.dataset.series === 'proxy' ? [
                        ['Embedded product proxy', bar.dataset.embeddedProxy],
                        ['Recurring service proxy', bar.dataset.recurringProxy],
                        ['Exit / transaction proxy', bar.dataset.exitProxy],
                    ] : [['Evidence range', bar.dataset.range]]),
                    ['Position', bar.dataset.position],
                    ['Holding period', bar.dataset.holdingPeriod],
                    ['Status', bar.dataset.status],
                ];
                tooltip.innerHTML = `<strong>${{escapeHtml(bar.dataset.isin)}}</strong>${{rows.map(([label, value]) => `<span class="tooltip-row"><span class="tooltip-label">${{escapeHtml(label)}}</span><span class="tooltip-value">${{escapeHtml(value)}}</span></span>`).join('')}}`;
                tooltip.hidden = false;
                const rect = bar.getBoundingClientRect();
                const x = event.clientX || rect.left + rect.width / 2;
                const yPosition = event.clientY || rect.top;
                tooltip.style.left = `${{Math.min(Math.max(12, x + 14), window.innerWidth - tooltip.offsetWidth - 12)}}px`;
                tooltip.style.top = `${{Math.min(Math.max(12, yPosition - tooltip.offsetHeight - 12), window.innerHeight - tooltip.offsetHeight - 12)}}px`;
            }};
            chartStage.querySelectorAll('.chart-bar').forEach((bar) => {{
                bar.addEventListener('pointerenter', showTooltip);
                bar.addEventListener('pointermove', showTooltip);
                bar.addEventListener('pointerleave', hideTooltip);
                bar.addEventListener('focus', showTooltip);
                bar.addEventListener('blur', hideTooltip);
            }});
            chartModeButtons.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.chartMode === mode)));
            chartDetailButtons.forEach((button) => button.setAttribute('aria-pressed', String(button.dataset.chartDetail === detail)));
            document.querySelector('#chart-intro').textContent = detail === 'detailed'
                ? (mode === 'relative' ? 'Annualized proxy components and evidence range as percentages of usable position size.' : 'Proxy cost components and the evidence range from minimum to maximum.')
                : (mode === 'relative' ? 'Annualized cost as a percentage of usable position size, compared with the maximum evidence-based estimate.' : 'Total proxy cost compared with the maximum evidence-based cost estimate.');
        }}
        function exportChartSvg() {{
            const source = chartStage.querySelector('svg');
            if (!source) return;
            const svg = source.cloneNode(true);
            const sourceElements = source.querySelectorAll('*');
            const clonedElements = svg.querySelectorAll('*');
            const presentationProperties = ['fill', 'stroke', 'stroke-width', 'stroke-linecap', 'stroke-linejoin', 'font-family', 'font-size', 'font-weight', 'text-anchor', 'opacity'];
            sourceElements.forEach((sourceElement, index) => {{
                const clonedElement = clonedElements[index];
                if (!clonedElement) return;
                const computedStyle = getComputedStyle(sourceElement);
                presentationProperties.forEach((property) => {{
                    const value = computedStyle.getPropertyValue(property);
                    if (value) clonedElement.setAttribute(property, value);
                }});
            }});
            const viewBox = svg.viewBox.baseVal;
            const legendHeight = 34;
            const originalHeight = viewBox.height;
            const chartContent = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            [...svg.children].forEach((child) => {{
                if (child.tagName !== 'title' && child.tagName !== 'desc') chartContent.append(child);
            }});
            chartContent.setAttribute('transform', 'translate(0 0)');
            svg.append(chartContent);
            svg.setAttribute('viewBox', `0 0 ${{viewBox.width}} ${{originalHeight + legendHeight}}`);
            svg.setAttribute('height', String(originalHeight + legendHeight));
            svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
            const style = document.createElementNS('http://www.w3.org/2000/svg', 'style');
            style.textContent = '.chart-gridline{{stroke:#dfe8e1;stroke-width:1}}.chart-axis{{stroke:#9eb3a5;stroke-width:1}}.chart-tick,.chart-label{{fill:#63706a;font-size:11px}}.chart-label{{fill:#29453a;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:10px;font-weight:800}}.chart-bar.proxy,.chart-bar.proxy-embedded{{fill:#176b52}}.chart-bar.proxy-recurring{{fill:#2f8b6c}}.chart-bar.proxy-exit{{fill:#79b89d}}.chart-bar.evidence{{fill:#62676b}}.chart-bar.evidence-delta{{fill:#c5c9cc}}';
            svg.insertBefore(style, svg.firstChild);
            const legend = document.createElementNS('http://www.w3.org/2000/svg', 'g');
            legend.setAttribute('aria-label', 'Chart legend');
            const detail = viewState[chartViewName]?.detail === 'detailed' ? 'detailed' : 'summary';
            const legendItems = detail === 'detailed'
                ? [['#176b52', 'Embedded product proxy'], ['#2f8b6c', 'Recurring service proxy'], ['#79b89d', 'Exit / transaction proxy'], ['#62676b', 'Evidence minimum'], ['#c5c9cc', 'Evidence range to maximum']]
                : [['#176b52', 'Total proxy cost'], ['#62676b', 'Evidence cost (max)']];
            const legendGap = 16;
            const legendWidths = legendItems.map(([, label]) => 26 + label.length * 7);
            const legendWidth = legendWidths.reduce((total, itemWidth) => total + itemWidth, 0) + legendGap * Math.max(legendItems.length - 1, 0);
            let legendX = (viewBox.width - legendWidth) / 2;
            legend.setAttribute('transform', `translate(0 ${{originalHeight + 8}})`);
            legendItems.forEach(([color, label], index) => {{
                const swatch = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
                swatch.setAttribute('x', String(legendX));
                swatch.setAttribute('y', '0');
                swatch.setAttribute('width', '10');
                swatch.setAttribute('height', '10');
                swatch.setAttribute('rx', '2');
                swatch.setAttribute('fill', color);
                const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
                text.setAttribute('x', String(legendX + 16));
                text.setAttribute('y', '9');
                text.setAttribute('fill', '#52675c');
                text.setAttribute('font-family', 'ui-sans-serif,system-ui,sans-serif');
                text.setAttribute('font-size', '12');
                text.setAttribute('font-weight', '700');
                text.textContent = label;
                legend.append(swatch, text);
                legendX += legendWidths[index] + legendGap;
            }});
            svg.append(legend);
            const serialized = new XMLSerializer().serializeToString(svg);
            const mode = viewState[chartViewName]?.mode === 'relative' ? 'relative' : 'absolute';
            const filename = `03c-cost-charts-${{mode}}-${{detail}}.svg`;
            const link = document.createElement('a');
            link.href = URL.createObjectURL(new Blob([serialized], {{ type: 'image/svg+xml;charset=utf-8' }}));
            link.download = filename;
            link.click();
            URL.revokeObjectURL(link.href);
        }}
        function csvCell(value) {{
            return `"${{String(value).replace(/"/g, '""')}}"`;
        }}
        function exportCsv() {{
            if (activeView === sourceViewName) {{
                const sourceTable = document.querySelector('#sources-table');
                const sourceCsv = [...sourceTable.querySelectorAll('tr')].map((row) => [...row.cells].map((cell) => csvCell(cell.textContent.trim())).join(',')).join('\\r\\n');
                const sourceLink = document.createElement('a');
                sourceLink.href = URL.createObjectURL(new Blob([`\\ufeff${{sourceCsv}}`], {{ type: 'text/csv;charset=utf-8' }}));
                sourceLink.download = 'sources.csv';
                sourceLink.click();
                URL.revokeObjectURL(sourceLink.href);
                return;
            }}
            const state = activeState();
            const visible = new Set(state.visible);
            const columns = state.order.filter((index) => visible.has(index));
            const rows = originalRows
                .filter((row) => state.filters.every((filter) => matchesFilter(row, filter)))
                .sort((left, right) => compareRows(left, right, state.sorts));
            const csv = [
                columns.map((index) => csvCell(headerNames[index])).join(','),
                ...rows.map((row) => columns.map((index) => csvCell(valueFor(row, index))).join(',')),
            ].join('\\r\\n');
            const filename = `${{(activeView || 'view').replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '').toLowerCase() || 'view'}}.csv`;
            const link = document.createElement('a');
            link.href = URL.createObjectURL(new Blob([`\\ufeff${{csv}}`], {{ type: 'text/csv;charset=utf-8' }}));
            link.download = filename;
            link.click();
            URL.revokeObjectURL(link.href);
        }}
        function groupedRows(rows, groups, level = 0) {{
            if (level >= groups.length) return rows;
            const grouped = new Map();
            rows.forEach((row) => {{
                const value = valueFor(row, groups[level]);
                if (!grouped.has(value)) grouped.set(value, []);
                grouped.get(value).push(row);
            }});
            return [...grouped.entries()].flatMap(([value, groupRows]) => {{
                const groupRow = document.createElement('tr');
                groupRow.className = 'group-row';
                const cell = document.createElement('td');
                cell.colSpan = headerNames.length;
                cell.innerHTML = `<span class="group-indent" style="--group-indent: ${{level * 18}}px"></span>${{headerNames[groups[level]]}}: ${{value || '(blank)'}}`;
                groupRow.append(cell);
                return [groupRow, ...groupedRows(groupRows, groups, level + 1)];
            }});
        }}
        function renderRules() {{
            const state = activeState();
            document.querySelector('#filter-list').innerHTML = state.filters.length ? state.filters.map((filter, index) => `<li class="rule"><strong>${{headerNames[filter.column]}}</strong> ${{filter.operator}} ${{filter.value}} <button type="button" data-remove-filter="${{index}}">Remove</button></li>`).join('') : '<li class="empty-state">No filters added.</li>';
            document.querySelector('#group-list').innerHTML = state.groups.length ? state.groups.map((column, index) => `<li class="rule"><strong>${{index + 1}}.</strong> ${{headerNames[column]}} <button type="button" data-move-group="${{index}}" data-direction="up">Up</button><button type="button" data-move-group="${{index}}" data-direction="down">Down</button><button type="button" data-remove-group="${{index}}">Remove</button></li>`).join('') : '<li class="empty-state">No groups added.</li>';
            document.querySelector('#sort-list').innerHTML = state.sorts.length ? state.sorts.map((sort, index) => `<li class="rule"><strong>${{index + 1}}.</strong> ${{headerNames[sort.column]}} (${{sort.direction === 'asc' ? 'A to Z' : 'Z to A'}}) <button type="button" data-move-sort="${{index}}" data-direction="up">Up</button><button type="button" data-move-sort="${{index}}" data-direction="down">Down</button><button type="button" data-remove-sort="${{index}}">Remove</button></li>`).join('') : '<li class="empty-state">No sorting added.</li>';
        }}
        function applyColumnWidths() {{
            const state = activeState();
            const visible = new Set(state.visible);
            let visibleWidth = 0;
            state.widths.forEach((width, index) => {{
                const column = widthColumns.querySelector(`[data-column-index="${{index}}"]`);
                column.style.width = `${{width}}px`;
                column.style.display = visible.has(index) ? '' : 'none';
                if (visible.has(index)) visibleWidth += width;
            }});
            table.style.width = `${{Math.max(tableScroll.clientWidth, visibleWidth)}}px`;
        }}
        function applyColumnOrder() {{
            const state = activeState();
            const headerRow = table.tHead.rows[0];
            state.order.forEach((index) => {{
                const header = headerRow.querySelector(`[data-column-index="${{index}}"]`);
                const column = widthColumns.querySelector(`[data-column-index="${{index}}"]`);
                headerRow.append(header);
                widthColumns.append(column);
            }});
            [...tableBody.rows].forEach((row) => {{
                if (row.classList.contains('group-row')) return;
                state.order.forEach((index) => row.append(row.querySelector(`[data-column-index="${{index}}"]`)));
            }});
        }}
        function reorderColumn(sourceIndex, targetIndex) {{
            const state = activeState();
            const sourcePosition = state.order.indexOf(sourceIndex);
            const targetPosition = state.order.indexOf(targetIndex);
            if (sourcePosition === -1 || targetPosition === -1 || sourcePosition === targetPosition) return;
            state.order.splice(sourcePosition, 1);
            state.order.splice(targetPosition, 0, sourceIndex);
            renderTable();
        }}
        let resizeSession = null;
        function finishColumnResize() {{
            if (!resizeSession) return;
            resizeSession = null;
            document.body.classList.remove('is-resizing');
            saveViews();
        }}
        table.tHead.addEventListener('pointerdown', (event) => {{
            const handle = event.target.closest('[data-resize-column]');
            if (!handle) return;
            const index = Number(handle.dataset.resizeColumn);
            resizeSession = {{ index, startX: event.clientX, startWidth: activeState().widths[index] }};
            document.body.classList.add('is-resizing');
            event.preventDefault();
        }});
        document.addEventListener('pointermove', (event) => {{
            if (!resizeSession) return;
            const state = activeState();
            state.widths[resizeSession.index] = Math.max(96, Math.round(resizeSession.startWidth + event.clientX - resizeSession.startX));
            applyColumnWidths();
        }});
        document.addEventListener('pointerup', finishColumnResize);
        document.addEventListener('pointercancel', finishColumnResize);
        let dragSession = null;
        let suppressHeaderSort = false;
        table.tHead.addEventListener('pointerdown', (event) => {{
            if (event.target.closest('.column-resizer')) return;
            const header = event.target.closest('[data-column-index]');
            if (!header) return;
            dragSession = {{ index: Number(header.dataset.columnIndex), startX: event.clientX, moved: false }};
        }});
        document.addEventListener('pointermove', (event) => {{
            if (!dragSession) return;
            if (Math.abs(event.clientX - dragSession.startX) < 6) return;
            dragSession.moved = true;
            const target = document.elementFromPoint(event.clientX, event.clientY)?.closest('[data-column-index]');
            if (target && target.closest('thead')) reorderColumn(dragSession.index, Number(target.dataset.columnIndex));
            document.body.classList.add('is-column-dragging');
        }});
        document.addEventListener('pointerup', () => {{
            if (!dragSession) return;
            suppressHeaderSort = dragSession.moved;
            dragSession = null;
            document.body.classList.remove('is-column-dragging');
            if (suppressHeaderSort) setTimeout(() => {{ suppressHeaderSort = false; }}, 0);
            saveViews();
        }});
        document.addEventListener('pointercancel', () => {{
            dragSession = null;
            document.body.classList.remove('is-column-dragging');
        }});
        table.tHead.addEventListener('click', (event) => {{
            const button = event.target.closest('th button');
            if (!button || suppressHeaderSort) return;
            const column = Number(button.closest('[data-column-index]').dataset.columnIndex);
            const state = activeState();
            const currentSort = state.sorts[0];
            const direction = currentSort?.column === column && currentSort.direction === 'asc' ? 'desc' : 'asc';
            state.sorts = [{{ column, direction }}];
            renderTable();
        }});
        function renderTable() {{
            const definitionsView = activeView === 'Definitions';
            const isSourcesView = activeView === sourceViewName;
            const isChartView = activeView === chartViewName;
            document.querySelector('#definitions-view').hidden = !definitionsView;
            document.querySelector('#sources-view').hidden = !isSourcesView;
            document.querySelectorAll('.toolbar').forEach((panel) => panel.hidden = definitionsView || isSourcesView);
            document.querySelectorAll('.builder-panel').forEach((panel) => panel.hidden = definitionsView || isSourcesView || isChartView);
            document.querySelectorAll('[data-panel]').forEach((button) => button.hidden = definitionsView || isSourcesView || isChartView);
            if (isChartView) {{
                panels.forEach((panel) => panel.classList.remove('is-open'));
                panelButtons.forEach((button) => button.setAttribute('aria-expanded', 'false'));
            }}
            chartView.hidden = !isChartView;
            document.querySelector('#main-table-scroll').hidden = definitionsView || isSourcesView || isChartView;
            if (definitionsView || isSourcesView || isChartView) {{
                if (isChartView) renderCostChart();
                return;
            }}
            const state = activeState();
            const visible = new Set(state.visible);
            applyColumnOrder();
            applyColumnWidths();
            [...columnList.querySelectorAll('[data-column]')].forEach((checkbox) => {{
                checkbox.checked = visible.has(Number(checkbox.dataset.column));
            }});
            [...table.tHead.rows[0].cells].forEach((cell) => {{
                const column = Number(cell.dataset.columnIndex);
                cell.hidden = !visible.has(column);
                const sort = state.sorts[0];
                cell.setAttribute('aria-sort', sort?.column === column ? (sort.direction === 'asc' ? 'ascending' : 'descending') : 'none');
            }});
            let rows = originalRows.filter((row) => state.filters.every((filter) => matchesFilter(row, filter)));
            rows.sort((left, right) => compareRows(left, right, state.sorts));
            tableBody.replaceChildren(...groupedRows(rows, state.groups));
            [...tableBody.rows].forEach((row) => {{
                if (!row.classList.contains('group-row')) {{
                    applyColumnOrder();
                    [...row.cells].forEach((cell) => {{
                        const index = Number(cell.dataset.columnIndex);
                        cell.classList.toggle('numeric-cell', numericColumns[index]);
                        cell.classList.toggle('usd-column', usdColumns[index]);
                        cell.hidden = !visible.has(index);
                    }});
                }}
            }});
            renderRules();
            saveViews();
        }}
        panelButtons.forEach((button) => button.addEventListener('click', () => {{
            const panel = document.querySelector(`#${{button.dataset.panel}}`);
            const open = panel.classList.toggle('is-open');
            button.setAttribute('aria-expanded', String(open));
            panels.filter((candidate) => candidate !== panel).forEach((candidate) => candidate.classList.remove('is-open'));
            panelButtons.filter((candidate) => candidate !== button).forEach((candidate) => candidate.setAttribute('aria-expanded', 'false'));
        }}));
        document.querySelector('#export-csv').addEventListener('click', exportCsv);
        document.querySelector('#export-chart-svg').addEventListener('click', exportChartSvg);
        chartModeButtons.forEach((button) => button.addEventListener('click', () => {{
            viewState[chartViewName].mode = button.dataset.chartMode;
            renderCostChart();
            saveViews();
        }}));
        chartDetailButtons.forEach((button) => button.addEventListener('click', () => {{
            viewState[chartViewName].detail = button.dataset.chartDetail;
            renderCostChart();
            saveViews();
        }}));
        function saveViews() {{
            normalizeViewOrder();
            localStorage.setItem('jtc-cost-model-views', JSON.stringify(viewState));
            saveViewOrder();
            if (!viewsLoaded) return;
            fetch('/api/views', {{
                method: 'PUT',
                headers: {{ 'Content-Type': 'application/json' }},
                body: JSON.stringify(viewState),
            }}).catch(() => {{
                console.warn('View changes could not be saved to the backend.');
            }});
        }}
        async function loadViews() {{
            try {{
                const response = await fetch('/api/views');
                if (!response.ok) throw new Error(`HTTP ${{response.status}}`);
                const savedViews = await response.json();
                if (savedViews && typeof savedViews === 'object' && Object.keys(savedViews).length) viewState = savedViews;
                if (!viewState[chartViewName]) viewState[chartViewName] = {{ mode: 'absolute' }};
                viewsLoaded = true;
            }} catch (error) {{
                console.warn('Backend unavailable; using browser-local view state.', error);
                const banner = document.querySelector('#backend-banner');
                if (sessionStorage.getItem('jtc-cost-model-banner-dismissed') !== '1') banner.hidden = false;
            }}
            normalizeViewOrder();
            renderViewList();
            renderTable();
        }}
        function renderViewList() {{
            const list = viewsNav.querySelector('.view-list');
            normalizeViewOrder();
            const viewItems = viewOrder.map((viewName) => {{
                const item = document.createElement('li');
                const button = document.createElement('button');
                button.className = 'view-button';
                button.type = 'button';
                button.dataset.view = viewName;
                button.textContent = viewName;
                if (viewName === activeView) button.setAttribute('aria-current', 'page');
                item.append(button);
                item.draggable = false;
                return item;
            }});
            const definitionsItem = document.createElement('li');
            const definitionsButton = document.createElement('button');
            definitionsButton.className = 'view-button';
            definitionsButton.type = 'button';
            definitionsButton.dataset.view = 'Definitions';
            definitionsButton.textContent = 'Definitions';
            if (activeView === 'Definitions') definitionsButton.setAttribute('aria-current', 'page');
            definitionsItem.append(definitionsButton);
            const sourcesItem = document.createElement('li');
            const sourcesButton = document.createElement('button');
            sourcesButton.className = 'view-button';
            sourcesButton.type = 'button';
            sourcesButton.dataset.view = sourceViewName;
            sourcesButton.textContent = sourceViewName;
            if (activeView === sourceViewName) sourcesButton.setAttribute('aria-current', 'page');
            sourcesItem.append(sourcesButton);
            list.replaceChildren(...viewItems, sourcesItem, definitionsItem);
        }}
        function moveView(viewName, targetName) {{
            normalizeViewOrder();
            const sourcePosition = viewOrder.indexOf(viewName);
            const targetPosition = viewOrder.indexOf(targetName);
            if (sourcePosition === -1 || targetPosition === -1 || sourcePosition === targetPosition) return;
            viewOrder.splice(sourcePosition, 1);
            viewOrder.splice(targetPosition, 0, viewName);
            renderViewList();
            saveViewOrder();
        }}
        let viewDragSession = null;
        let suppressViewClick = false;
        viewsNav.addEventListener('pointerdown', (event) => {{
            const item = event.target.closest('.view-list li');
            if (!item) return;
            const button = item.querySelector('.view-button');
            if (!button) return;
            viewDragSession = {{ name: button.dataset.view, startX: event.clientX, startY: event.clientY, moved: false }};
        }});
        document.addEventListener('pointermove', (event) => {{
            if (!viewDragSession) return;
            const distance = Math.hypot(event.clientX - viewDragSession.startX, event.clientY - viewDragSession.startY);
            if (distance < 6) return;
            viewDragSession.moved = true;
            document.body.classList.add('is-view-dragging');
            const target = document.elementFromPoint(event.clientX, event.clientY)?.closest('.view-list li');
            [...viewsNav.querySelectorAll('.view-list li')].forEach((candidate) => candidate.classList.toggle('is-view-drop-target', candidate === target && candidate.querySelector('.view-button')?.dataset.view !== viewDragSession.name));
            if (target) {{
                const targetName = target.querySelector('.view-button')?.dataset.view;
                if (targetName && targetName !== viewDragSession.name) moveView(viewDragSession.name, targetName);
            }}
        }});
        function finishViewDrag() {{
            if (!viewDragSession) return;
            suppressViewClick = viewDragSession.moved;
            viewDragSession = null;
            document.body.classList.remove('is-view-dragging');
            viewsNav.querySelectorAll('.is-view-drop-target').forEach((item) => item.classList.remove('is-view-drop-target'));
            if (suppressViewClick) setTimeout(() => {{ suppressViewClick = false; }}, 0);
        }}
        document.addEventListener('pointerup', finishViewDrag);
        document.addEventListener('pointercancel', finishViewDrag);
        viewsNav.addEventListener('click', (event) => {{
            if (suppressViewClick) return;
            const button = event.target.closest('.view-button');
            if (!button) return;
            activeView = button.dataset.view;
            document.querySelector('#filter-value').value = '';
            renderViewList();
            renderTable();
        }});
        const viewActionsToggle = document.querySelector('#view-actions-toggle');
        const viewActionMenu = document.querySelector('#view-action-menu');
        function closeViewActionMenu() {{
            viewActionMenu.hidden = true;
            viewActionsToggle.setAttribute('aria-expanded', 'false');
        }}
        viewActionsToggle.addEventListener('click', () => {{
            const open = viewActionMenu.hidden;
            viewActionMenu.hidden = !open;
            viewActionsToggle.setAttribute('aria-expanded', String(open));
            if (open) viewActionMenu.querySelector('[data-view-action]').focus();
        }});
        viewActionMenu.addEventListener('click', (event) => {{
            const action = event.target.closest('[data-view-action]')?.dataset.viewAction;
            if (!action) return;
            closeViewActionMenu();
            if (activeView === 'Definitions' || activeView === sourceViewName) return;
            if (action === 'new') {{
                const name = prompt('Name this view');
                if (!name || viewState[name.trim()]) return;
                viewState[name.trim()] = createViewState();
                viewOrder.push(name.trim());
                activeView = name.trim();
            }} else if (action === 'duplicate') {{
                const name = prompt('Name the duplicate view', `${{activeView}} copy`);
                if (!name || viewState[name.trim()]) return;
                viewState[name.trim()] = JSON.parse(JSON.stringify(activeState()));
                viewOrder.push(name.trim());
                activeView = name.trim();
            }} else if (action === 'rename') {{
                const name = prompt('Rename this view', activeView);
                if (!name || name.trim() === activeView || viewState[name.trim()]) return;
                viewState[name.trim()] = viewState[activeView];
                viewOrder[viewOrder.indexOf(activeView)] = name.trim();
                delete viewState[activeView];
                activeView = name.trim();
            }} else if (action === 'delete') {{
                if (Object.keys(viewState).length === 1 || !confirm(`Delete the view "${{activeView}}"?`)) return;
                delete viewState[activeView];
                viewOrder = viewOrder.filter((name) => name !== activeView);
                activeView = viewOrder[0] || Object.keys(viewState)[0];
            }}
            saveViews();
            renderViewList();
            renderTable();
        }});
        document.addEventListener('click', (event) => {{
            if (!event.target.closest('.view-actions')) closeViewActionMenu();
        }});
        document.addEventListener('keydown', (event) => {{
            if (event.key === 'Escape' && !viewActionMenu.hidden) {{
                closeViewActionMenu();
                viewActionsToggle.focus();
            }}
        }});
        columnList.addEventListener('change', (event) => {{
            if (!event.target.matches('[data-column]')) return;
            const column = Number(event.target.dataset.column);
            const state = activeState();
            state.visible = event.target.checked ? [...new Set([...state.visible, column])] : state.visible.filter((index) => index !== column);
            renderTable();
        }});
        document.querySelector('#add-filter').addEventListener('click', () => {{
            const value = document.querySelector('#filter-value').value.trim();
            const operator = document.querySelector('#filter-operator').value;
            if (operator !== 'not-empty' && !value) return;
            activeState().filters.push({{ column: Number(document.querySelector('#filter-column').value), operator, value }});
            document.querySelector('#filter-value').value = '';
            renderTable();
        }});
        document.querySelector('#add-group').addEventListener('click', () => {{
            const column = Number(document.querySelector('#group-column').value);
            if (!activeState().groups.includes(column)) activeState().groups.push(column);
            renderTable();
        }});
        document.querySelector('#add-sort').addEventListener('click', () => {{
            activeState().sorts.push({{ column: Number(document.querySelector('#sort-column').value), direction: document.querySelector('#sort-direction').value }});
            renderTable();
        }});
        document.querySelector('#filter-list').addEventListener('click', (event) => {{
            if (event.target.dataset.removeFilter) activeState().filters.splice(Number(event.target.dataset.removeFilter), 1);
            renderTable();
        }});
        function reorderRule(list, index, direction) {{
            const next = direction === 'up' ? index - 1 : index + 1;
            if (next < 0 || next >= list.length) return;
            [list[index], list[next]] = [list[next], list[index]];
        }}
        document.querySelector('#group-list').addEventListener('click', (event) => {{
            const index = Number(event.target.dataset.moveGroup ?? event.target.dataset.removeGroup);
            if (event.target.dataset.removeGroup) activeState().groups.splice(index, 1);
            else if (event.target.dataset.moveGroup) reorderRule(activeState().groups, index, event.target.dataset.direction);
            renderTable();
        }});
        document.querySelector('#sort-list').addEventListener('click', (event) => {{
            const index = Number(event.target.dataset.moveSort ?? event.target.dataset.removeSort);
            if (event.target.dataset.removeSort) activeState().sorts.splice(index, 1);
            else if (event.target.dataset.moveSort) reorderRule(activeState().sorts, index, event.target.dataset.direction);
            renderTable();
        }});
        document.querySelector('#backend-banner-dismiss').addEventListener('click', () => {{
            sessionStorage.setItem('jtc-cost-model-banner-dismissed', '1');
            document.querySelector('#backend-banner').hidden = true;
        }});
        loadViews();
  </script>
</body>
</html>
"""


def generate_dashboard() -> None:
    statuses = read_position_statuses()
    records = product_records()
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(dashboard_html(records, statuses), encoding="utf-8")
    print(f"Rendered {len(records)} securities to {OUTPUT_PATH.relative_to(ROOT)}")


def main() -> None:
    generate_dashboard()


if __name__ == "__main__":
    main()