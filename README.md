# jtc-client-A2-structured-prodcuts

## Project Scripts

All project automation scripts are kept in `90. Scripts` so the repository root contains only project inputs, outputs, and documentation.

Run a phase script from the repository root with:

```text
python "90. Scripts/<script-name>.py"
```

Current scripts:

- `generate_phase_1_2.py` - generate initial product records
- `extract_phase_3.py` - extract Bloomberg images
- `ocr_phase_4.py` - transcribe extracted images
- `review_phase_4b.py` - create the OCR review layer
- `consolidate_phase_5.py` - consolidate workbook and OCR evidence
- `recover_issue_size.py` - recover issue/outstanding-size candidates from OCR
- `integrate_issue_size.py` - propagate issue-size findings into portfolio tables and dossiers
- `migrate_product_frontmatter.py` - initialize canonical YAML frontmatter from existing dossiers
- `render_products.py` - generate named or ad hoc Markdown tables from canonical dossier frontmatter

## Canonical Product Data

Each individual product dossier has YAML frontmatter containing the reviewed canonical data. The Markdown body remains the evidence and review report. The generated summary and detailed views are stored in `05. Canonical Data`; do not edit them directly.

Render the configured preview reports with:

```text
python "90. Scripts/render_products.py" --view summary
python "90. Scripts/render_products.py" --view detailed
```

Render an ad hoc table to standard output or specify `--output` for a Markdown file:

```text
python "90. Scripts/render_products.py" --columns isin,issuer,maturity,coupon
```

## Cost modelling dashboard

Generate the dashboard and start its local backend from the repository root:

```text
python "05. Cost modeling/generate_dashboard.py"
python "90. Scripts/cost_model_server.py"
```

The generated HTML dashboard is written to `07. Visutals/index.html` and served
at `http://127.0.0.1:8000/`. View definitions (selected columns, sorting,
filters, groups) are persisted in the local `05. Cost modeling/.cost-model-views.json`
file through the `/api/views` endpoint.

The fixed `Sources` view presents the verified research register from
`00. Project scope/cost-benchmark-research.md`. It shows each source's market,
payoff relevance, cohort applicability, cost bucket, observed result, Tier 1
use, limitations, and locator. Builder controls are hidden for this view, but
the source register remains exportable as CSV.

The `03c. Cost charts` view shows vertical clustered bars per ISIN, ordered from
highest to lowest total proxy cost. Each ISIN has a total proxy-cost bar and a
maximum evidence-cost bar. The `Absolute` toggle displays USD values; `Relative*`
displays annualised cost as cost USD / usable position size / holding period years.
Rows without a valid denominator are marked `N/A`, not treated as zero.

**Always open the dashboard at `http://127.0.0.1:8000/`, not through VS Code's
Simple Browser / Live Preview extension.** Live Preview serves the file on its
own (often random) port and doesn't implement `/api/views`, so neither the
backend save nor the browser's local fallback storage can persist — every
refresh looks like a fresh browser origin and your view resets. If you open
the dashboard without the backend running, a banner will warn you that
changes are only kept in that browser tab.