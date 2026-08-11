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
    lifecycle_end, lifecycle_basis = extract_lifecycle_end(str(record.get("maturity", "")))
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
        lifecycle_basis,
        status,
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
    html_excluded_yaml_fields = {
        "annualised_rate",
        "barrier",
        "coupon",
        "denomination_usd",
        "downside",
        "frequency",
        "other_comments",
        "redemption_terms",
        "risk",
        "schema_version",
    }
    curated_headers = (
        "ISIN",
        "Security",
        "Cohort",
        "Issue date",
        "Lifecycle end",
        "End basis",
        "Position basis",
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
  </style>
</head>
<body>
    <div class="shell">
        <nav class="views" id="views-nav" aria-label="Views">
            <h2>Views</h2>
            <ul class="view-list">
                <li><button class="view-button" type="button" data-view="current">Current</button></li>
                <li><button class="view-button" type="button" data-view="position-size">by Position Size</button></li>
                <li><button class="view-button" type="button" data-view="full dataset">full dataset</button></li>
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
        const usdColumns = headerNames.map((name) => /\(USD\)$/i.test(name));
        [...table.tHead.rows[0].cells].forEach((cell, index) => {{
            cell.classList.toggle('numeric-column', numericColumns[index]);
            cell.classList.toggle('usd-column', usdColumns[index]);
        }});
        const curatedColumnCount = 12;
        const curatedColumnWidths = [120, 340, 180, 130, 150, 150, 170, 170, 190, 190, 190, 190];
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
        }};
        let viewState = JSON.parse(localStorage.getItem('jtc-cost-model-views') || 'null') || defaultViewState;
        if (!viewState['full dataset']) viewState['full dataset'] = createViewState(true);
        let viewOrder = JSON.parse(localStorage.getItem('jtc-cost-model-view-order') || 'null');
        let viewsLoaded = false;
        let activeView = null;
        const tableBody = table.tBodies[0];
        const tableScroll = document.querySelector('#main-table-scroll');
        const widthColumns = document.querySelector('#column-widths');
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
            if (activeView !== 'Definitions' && !viewOrder.includes(activeView)) activeView = viewOrder[0] || names[0];
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
            document.querySelector('#definitions-view').hidden = !definitionsView;
            document.querySelectorAll('.toolbar, .builder-panel').forEach((panel) => panel.hidden = definitionsView);
            document.querySelector('#main-table-scroll').hidden = definitionsView;
            if (definitionsView) return;
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
                viewsLoaded = true;
            }} catch (error) {{
                console.warn('Backend unavailable; using browser-local view state.', error);
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
            list.replaceChildren(...viewItems, definitionsItem);
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
            if (activeView === 'Definitions' && action !== 'new') return;
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