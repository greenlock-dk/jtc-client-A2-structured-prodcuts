---
name: data-check
description: "Run an exhaustive, evidence-led audit of the structured-products repository. Use when checking all ISIN records, source coverage, extracted-data usage, contradictions, provenance, and unresolved gaps."
agent: agent
---

# Structured Products Data Integrity Audit

Audit the complete structured-products data set for coverage, consistency, provenance, and faithful use of extracted evidence. Work as a skeptical data auditor: verify claims against evidence, preserve uncertainty, and do not merely summarize existing review conclusions.

## Audit objective

Determine whether:

1. every expected product and source artifact is accounted for;
2. every material value in the product context is supported by a traceable source;
3. all usable extracted data was incorporated or explicitly excluded with a reason;
4. no unresolved contradiction is hidden by normalization, consolidation, or omission; and
5. the repository can support its product descriptions and review conclusions without unsupported inference.

The default scope is the entire repository. Complete all products and artifacts before issuing a final result. Do not sample.

## Repository model

Follow the actual five-phase pipeline:

| Phase | Content | Audit role |
| --- | --- | --- |
| 1-2 | `Trust ISIN information from Bloomberg.xlsx`, `01. Structured Products/ISIN_summary.md`, and `01. Structured Products/ISIN_detailed.md` | Workbook reference data and product index |
| 3 | `02. BBG images/` and `IMAGE INVENTORY.md` | Primary visual evidence extracted from the workbook |
| 4 | `03. BBG OCR/` and `OCR INVENTORY.md` | Machine transcription candidates; never confirmation by themselves |
| 4B | `04. Product Review/`, including per-ISIN reviews and inventories | Derived comparison and review layer |
| 5 | Individual files in `01. Structured Products/` and `PHASE 5 CONSOLIDATION.md` | Consolidated working records; derived output to be tested |

Also inspect `04. Original terms/`, root-level Markdown/data files, `README.md`, and `90. Scripts/` when needed to understand provenance, mappings, transformations, or generated counts.

Generated outputs are not independent corroboration of their inputs. Agreement between a generated file and its source does not count as two-source confirmation.

## Current baseline to verify, not assume

Existing outputs currently claim:

- 29 summary instruments;
- 24 ISIN worksheets with mapped images;
- 71 mapped Bloomberg images;
- 71 mapped OCR files;
- 5 instruments with no image/OCR evidence;
- 3 workbook/OCR disagreements resolved by visual review;
- 0 unresolved workbook/OCR disagreements.

Recalculate these values from the files actually present. Report any difference from the claimed baseline. Inspect `_unmapped` locations and inventory sections directly; do not rely on narrative statements about unmapped counts.

## Evidence hierarchy

Use this hierarchy when assessing a value, while preserving every disagreement:

1. **Original executed/final terms or equivalent contractual source**: strongest evidence for legal and economic terms when clearly matched to the ISIN and applicable version.
2. **Bloomberg/source image**: primary visual evidence for what the source displayed at extraction time.
3. **Workbook cell/reference**: authoritative for what was supplied in the project workbook, but not certification of contractual terms.
4. **OCR text/candidate**: extraction aid only; requires comparison with its exact source image.
5. **Review and consolidated records**: derived interpretations whose inputs and decisions must be traceable.
6. **Summary tables and narrative reports**: indexes and conclusions to validate, not independent evidence.

Source rank alone does not automatically resolve a conflict. Check identity, date/version, context, units, and whether the sources describe different concepts. Record the rationale for every resolution.

## Controlled states

Classify blanks and differences with exactly one of these states:

| State | Meaning |
| --- | --- |
| `confirmed` | Directly supported by inspected evidence |
| `corroborated` | Equivalent values appear in independent evidence sources |
| `derived` | Calculated or interpreted from cited inputs using a stated rule |
| `format-only` | Meaning is identical after safe normalization |
| `not applicable` | Evidence shows the field does not apply |
| `not found` | Searched-for evidence or value could not be located |
| `not extracted` | Available evidence contains a material value absent from extracted context |
| `unclear` | Evidence exists but does not support a reliable interpretation |
| `conflicting` | Applicable sources state incompatible values |
| `uninspected` | Relevant content could not be opened or visually checked |

Never convert a blank to zero, `not applicable`, or an inferred value. Preserve explicit terms such as `perpetual`, `matured`, `called`, `actioned`, `unknown`, and `not available` as distinct meanings.

## Audit procedure

### 1. Establish the population

- Enumerate all repository files relevant to product data and classify each as source, extracted evidence, intermediate output, derived record, inventory, script, or unrelated.
- Build the master ISIN set from the workbook/summary, detailed index, individual product files, evidence directories, original terms, and review outputs.
- Validate ISIN syntax and check for duplicate ISINs, duplicate record numbers, duplicate files, orphan records, inconsistent filenames, broken links, and unexpected products.
- Reconcile record numbers across `ISIN_summary.md`, `ISIN_detailed.md`, review inventory, consolidation inventory, and individual records.
- Recalculate file, image, OCR, product, mapped, and unmapped counts. Explain all count differences.

### 2. Close the artifact ledger

Create an internal ledger containing every relevant artifact. Each artifact must end in exactly one disposition:

- `used and traced`;
- `duplicate/redundant` with the matching artifact identified;
- `irrelevant` with a reason;
- `unmapped`;
- `unreadable/uninspected`; or
- `missing expected counterpart`.

For each image, verify that the inventory entry, physical file, ISIN directory, image number, OCR counterpart, and links from the product record agree. Where hashes are listed, check duplicate hash prefixes and suspicious reuse across products.

For each OCR file, verify that its source image exists and is correctly paired. OCR confidence is not evidence accuracy. Visually check material OCR-derived values against the source image whenever the consolidated value depends on OCR or sources disagree.

### 3. Reconcile every ISIN

Build a per-ISIN reconciliation matrix before writing conclusions. At minimum compare:

| Category | Required checks |
| --- | --- |
| Identity | ISIN, issuer, guarantor, product name, product type, source/exhibit |
| Economics | currency, issue/notional size, position size, denomination, issue price |
| Dates/status | issue date, maturity, tenor, call/observation/payment dates, current or historical lifecycle status |
| Return | coupon/rate, spread, reference rate, frequency, day-count or annualisation where stated |
| Structure | underlyings, weights, participation, leverage, caps/floors, barriers, triggers, memory, autocall/callability |
| Redemption/risk | redemption formula, principal protection, downside, settlement, ranking, security, recourse, credit exposure |
| Context | trust, country, custodian, comments, review conclusions, and source provenance |

Apply product-type-aware completeness checks. For example:

- a callable note should identify call mechanics or clearly state that they are unavailable;
- a range accrual/range note should identify range boundaries, observation basis, and coupon linkage where sources provide them;
- an index/basket-linked note should identify all underlyings and the payoff relationship;
- a barrier, kick-in, phoenix, memory, express, or leveraged product should identify the relevant levels, conditions, and loss mechanics;
- a perpetual instrument must not be reported as missing maturity without recognizing its perpetual status.

Compare values semantically, not just as strings. Normalize only for comparison and retain the original representations. Check:

- date equivalence and impossible date order;
- currencies and whether amounts are issuance size, position size, or denomination;
- percent versus decimal and basis-point conversions;
- negative signs, decimal points, OCR character substitutions, and unit scaling;
- nominal versus minimum denomination;
- maturity versus call date;
- issuer versus guarantor/custodian;
- product status as of a stated date versus contractual feature;
- distinct fields accidentally collapsed into one consolidated value.

### 4. Test provenance and data use

For every material consolidated value, identify its immediate source and ultimate evidence. Flag:

- a source fact omitted from the consolidated product record;
- an OCR candidate promoted without visual confirmation;
- a workbook value overwritten without a documented decision;
- a consolidated or review claim with no discoverable source;
- a transformation with no stated rule;
- a review conclusion relying on missing or conflicting terms;
- source evidence attached to the wrong ISIN;
- a material fact present only in narrative text but absent from the structured table;
- a field marked unavailable even though inspected evidence supplies it.

Revisit all prior `resolved by visual review` decisions. Identify the exact field, both candidate values, inspected image, chosen value, reviewer rationale if recorded, and whether the resolution is reproducible. A status label alone is not proof of review.

### 5. Classify contradictions

Assign each difference one type:

- `identity conflict`;
- `economic-term conflict`;
- `date/status conflict`;
- `source-mapping conflict`;
- `extraction/OCR error`;
- `normalization error`;
- `derived-conclusion conflict`;
- `format-only difference`; or
- `unresolved ambiguity`.

Do not call a conflict resolved unless the deciding evidence was inspected and cited. Do not report `No detected inconsistency` as equivalent to `terms confirmed`.

## Criticality rubric

Use only lowercase `low`, `mid`, or `high`:

- `high`: wrong/missing identity; wrong product mapping; conflicting or unsupported legal/economic term; payoff, principal, currency, amount, maturity, barrier, leverage, redemption, or lifecycle issue; material source is uninspected; or the issue can change a review conclusion.
- `mid`: meaningful descriptive, operational, or provenance issue that weakens reliability but does not currently change the core economic interpretation.
- `low`: cosmetic/formatting metadata issue with no substantive impact, or a documented limitation with a reliable workaround.

When uncertain between levels, use the higher level and explain why.

## Evidence and citation rules

- Cite repository-relative file paths for every contradiction, gap, count, and resolution.
- Include the field/table/section or image number needed to locate the evidence.
- Quote short conflicting values exactly. Do not reproduce long source passages.
- Separate observation from interpretation.
- State what was searched when marking something `not found`.
- State why an artifact was not inspectable and the consequence for confidence.
- Do not modify source or product files during this audit unless explicitly asked. The deliverable is the report.

## Required final report

Return one Markdown report with the following sections in this exact order.

### 1. Executive result

Use one status: `PASS`, `PASS WITH GAPS`, or `FAIL`.

| Metric | Count | Expected/baseline | Result |
| --- | ---: | ---: | --- |

Include products, individual product files, mapped/unmapped images, OCR files, original-term artifacts, review records, contradictions, provenance gaps, unused artifacts, and uninspected items.

### 2. Population and artifact coverage

| Layer | Expected | Found | Mapped | Unmapped / missing | Disposition complete? | Evidence |
| --- | ---: | ---: | ---: | ---: | --- | --- |

After the table, list every orphan, duplicate, unmapped, unreadable, or missing-counterpart artifact. The disposition totals must reconcile to the number of artifacts found.

### 3. Per-ISIN audit

Include all ISINs, including those with no secondary evidence.

| Record | ISIN | Product file | Workbook/detail | Images/OCR | Original terms | Material fields traced | Conflicts | Gaps | Result |
| ---: | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |

Allowed per-ISIN results: `clear`, `clear with source limitation`, `gap`, or `conflict`.

### 4. Contradiction register

| ID | ISIN | Field | Type | Source A and value | Source B and value | Resolution status | Deciding evidence / required action | Criticality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Use `None identified` only after every ISIN and artifact has been checked.

### 5. Missing, unused, and unsupported data

| ID | ISIN / scope | Field or artifact | State | What is missing, unused, or unsupported | Sources checked | Impact | Required resolution | Criticality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |

Include source gaps, unaccounted extracted facts, fields incorrectly marked unavailable, unsupported review conclusions, and all inspection limitations. An extracted item is accounted for only if it is used, explicitly redundant, irrelevant with rationale, or reported here.

### 6. Prior resolutions re-performance

| ISIN | Field | Original disagreement | Visual evidence inspected | Existing resolution reproducible? | Finding |
| --- | --- | --- | --- | --- | --- |

Cover all existing `resolved by visual review` cases.

### 7. Inspection limitations

List inaccessible or unsupported content and quantify the affected products/artifacts. Explain which conclusions cannot be made because of each limitation.

### 8. Final decision and actions

State whether the repository is internally consistent, whether all usable extracted data is incorporated or accounted for, and whether material terms are adequately evidenced. List the highest-priority actions by finding ID.

## Decision gates

- `PASS`: all products and artifacts are dispositioned; no unresolved high/mid finding; no material uninspected evidence; all material consolidated values are traced; all prior visual resolutions are reproducible.
- `PASS WITH GAPS`: no known unresolved contradiction affecting core terms, but one or more low/mid completeness, provenance, source-coverage, or inspection gaps remain.
- `FAIL`: any unresolved high finding; any wrong/missing product mapping; any material contradiction; a material conclusion unsupported by evidence; artifact accounting does not close; or relevant content was skipped while claiming completeness.

Absence of a detected conflict is not proof of correctness. If primary evidence is missing or uninspected, state the source limitation and lower the result accordingly.
