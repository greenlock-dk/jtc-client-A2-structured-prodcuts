# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

The primary user is an investment committee reviewing a portfolio of legacy and current structured products, the evidence supporting each record, and the cost assumptions that may be used for decision-making.

## Product Purpose

This product makes it possible to inspect, compare, and challenge structured-product records and lifetime-cost assumptions in one evidence-led workspace. Success means that committee members can move from a portfolio-level table to the underlying dossier and source evidence while preserving uncertainty, exclusions, and modelling basis.

## Positioning

The repository is more than a document archive or generic spreadsheet: it joins 29 products by immutable ISIN across canonical dossiers, Bloomberg images and OCR, original-terms recovery, product-review controls, and generated table views. Each conclusion is expected to retain field-level provenance and an explicit evidence status.

## Operating Context

The workspace supports investment-committee review, analyst preparation, source recovery, data-integrity auditing, and cost-benchmark research. Users work primarily with Markdown dossiers, generated Markdown tables, and a generated HTML table view with saved slices of the dataset. The canonical data is rendered from individual product dossiers; generated views are outputs and must not be edited directly.

## Capabilities and Constraints

- The core experience is table-first, with different slices and views over the same dataset.
- The current table-view interaction supports visible columns, filters, grouping, sorting, saved views, and portfolio cohorts.
- The dataset covers 29 ISIN records and includes product terms, lifecycle dates, position and issue-size bases, risk information, cost scenarios, and provenance metadata.
- Evidence-only cost and proxy-base cost must remain distinct; unsupported or unreconciled values remain explicitly uncalculated or unbenchmarked.
- ISIN is the immutable cross-layer join key. Canonical YAML frontmatter in individual dossiers is the source for generated views.
- The product should remain a document-first web workspace. It should use a light, easy-to-scan interface with modern typography and rounded corners, while avoiding charts, graphics, and decorative visualizations.
- The repository currently uses Python scripts and generated static HTML rather than a frontend application framework. Future stack decisions are open.

## Evidence on Hand

- [README.md](README.md) documents the processing scripts and canonical-data workflow.
- [01. Structured Products/](01.%20Structured%20Products/) contains 29 individual product dossiers with canonical YAML frontmatter and evidence-led review text.
- [02. BBG images/](02.%20BBG%20images/) and [03. BBG OCR/](03.%20BBG%20OCR/) contain extracted Bloomberg evidence and OCR review material.
- [04. Original terms/](04.%20Original%20terms/) contains original-terms recovery material.
- [04. Product Review/](04.%20Product%20Review/) contains data-integrity, position-size, and issue-size controls.
- [05. Canonical Data/](05.%20Canonical%20Data/) contains generated summary and detailed views.
- [05. Cost modeling/](05.%20Cost%20modeling/) contains the generated table-first cost-model view.
- [00. Project scope/](00.%20Project%20scope/) contains the cost-benchmark research plan, research record, and executive memo.
- The repository does not establish approved branding, a product name beyond the repository name, deployment claims, or a final frontend framework.

## Product Principles

- Preserve traceability from every displayed value to its source and status.
- Make comparison and challenge fast for committee review.
- Separate confirmed evidence, proxy assumptions, and unresolved gaps.
- Keep generated outputs reproducible from canonical source records.
- Prefer clear tables and useful controls over decorative presentation.
