# Draft Structure: Current-Scope Final Report

**Status:** Draft report architecture  
**Scope:** Current scope - light analytics
**Purpose:** Establish an approximate lifetime economic cost of the structured-product strategy, instrument by instrument, from acquisition or issuance through call, maturity, disposal, or the reporting cut-off.  
**Evidence as of:** 11 August 2026 ([cost-benchmark-research.md](cost-benchmark-research.md) sixth pass; [DATA INTEGRITY AUDIT.md](../04.%20Product%20Review/DATA%20INTEGRITY%20AUDIT.md); [POSITION SIZE CONTROL.md](../04.%20Product%20Review/POSITION%20SIZE%20CONTROL.md)). The current position-size register supersedes older audit wording: 21 ISINs are `usable invested notional`, 2 are `issue/outstanding size`, and 6 are `missing`. Re-validate this date and those controls before publication if any underlying source document is updated later.

This document defines the proposed structure of the final report. It does not establish any fee, payment, recipient, entitlement, disclosure failure, or recoverable amount. The final report must distinguish documented portfolio facts, external benchmark evidence, and scenario assumptions.

## 1. Executive Summary

State the decision-useful result first:

- Estimated lifetime total economic cost by scenario.
- Separate totals for one-off product costs, recurring service costs, contingent exit costs, and potential third-party compensation.
- Number of ISINs and amount of Trust notional included in each result.
- Amount and number of ISINs excluded because the investment basis, acquisition date, disposal record, or benchmark is unresolved.
- Number of ISINs excluded from any structured-product conclusion because primary evidence or structure could not be recovered (see 3.2, path 6).
- Concentration of the estimated cost range by the largest ISINs by notional, so the committee can see which positions drive the result.
- Principal conclusion on whether a portfolio-wide retrocession amount is separately estimable.
- Recommended follow-up records or decisions required from the Trust.

## 2. Mandate, Question, and Scope Boundary

### 2.1 Current-scope question

> What lifetime economic costs are plausible for each structured-product holding, based on its lifecycle and trusted external evidence, and how do those costs aggregate under transparent assumptions?

### 2.2 Included work

- ISIN-by-ISIN lifecycle modelling.
- Product cohort classification and benchmark selection.
- One-off issuance-cost scenarios.
- Recurring annual service-cost scenarios.
- Contingent exit-cost scenarios.
- Potential intermediary compensation shown separately and only where supportable.
- Coverage, sensitivity, source, and exception reporting.

### 2.3 Excluded work

The current scope does not include:

- Recovery or contractual extraction of final terms, KIDs, client agreements, or fee schedules.
- Reconciliation to bank, custody, or payment records.
- Proof of a payment, recipient, disclosure, waiver, entitlement, limitation position, damages, or recoverability.
- A legal opinion, audit opinion, or evidential conclusion.

## 3. Portfolio and Lifecycle Population

Describe all 29 ISINs and show the lifecycle population used in the model. The report must distinguish the 29-record inventory, the 21 ISINs with a usable invested-notional basis, and the 19 ISINs currently cost-assessable under the available scenarios. All 21 usable-basis ISINs remain in the analysis regardless of whether issuer issue-size evidence is available; the other 2 are retained as explicit `unbenchmarked` rows rather than treated as zero cost.

### 3.1 Required ISIN-level fields

| Field | Role in the model |
| --- | --- |
| ISIN | Stable product identifier |
| Product name and structure | Product classification |
| Cohort | Benchmark selection |
| Issuer, guarantor, currency | Comparability and credit context |
| Issue date | Product lifecycle anchor or proxy start date |
| Acquisition date | Trust exposure start; unknown unless supported by Trust records |
| Acquisition notional and price | Cost calculation basis; never substituted with issuer issue size |
| Call, maturity, sale, or reporting-cut-off date | Lifecycle end event |
| Holding-period basis | Actual, documented, or proxy |
| Position-size status | Usability control for dollar aggregation |
| Evidence status | Provenance and confidence flag |

### 3.2 Lifecycle event treatment

For each ISIN, identify the applicable path:

1. Acquired and held to scheduled maturity.
2. Acquired and redeemed at a documented issuer call.
3. Acquired and sold before maturity.
4. Still held at the reporting cut-off.
5. Lifecycle end or Trust acquisition basis unresolved.
6. No structured-product conclusion is supported because primary evidence or structure could not be recovered.

Where the Trust acquisition date is unavailable, the model may show an explicitly labelled proxy path using issue date. This must remain separate from any evidence-based result. Path 6 is a distinct evidence limitation, not a zero-cost outcome. At the current evidence date it applies to `XS0168875792` and `XS0318585791` (DATA INTEGRITY AUDIT.md G-010) and `XS0298465822` (G-006). Any path-6 ISIN with a usable Trust position remains in the ISIN-level analysis and is labelled according to its available evidence; `XS0298465822` remains in coverage reporting without a dollar aggregation because its Trust position is missing.

## 4. Data Quality and Coverage

Present the controls before presenting dollar totals.

- Reconcile the model to all 29 canonical ISINs, including the 3 path-6 evidence-limited ISINs under 3.2.
- Use the current [POSITION SIZE CONTROL.md](../04.%20Product%20Review/POSITION%20SIZE%20CONTROL.md) classifications: 21 `usable invested notional`, 2 `issue/outstanding size`, and 6 `missing`. Include every usable-basis ISIN in the analysis and do not use issuer issue size, its absence, or its documentary status as an inclusion criterion. The latter 8 ISINs remain outside Trust-exposure aggregation.
- State the position-size resolution status by name and count in every coverage table. The current control register, rather than the superseded one-usable-row wording in older audit material, is the publication authority for those counts.
- Exclude issuer issue size, outstanding size, and minimum denomination from Trust exposure calculations.
- Show usable, excluded, and unresolved notional separately.
- Identify missing acquisition dates, acquisition prices, sale dates, sale proceeds, and balance-through-time information. Although 21 position bases are usable, acquisition/disposal basis is the dominant unresolved lifecycle input for lifetime aggregation; a reported Trust position must not be treated as proof of the Trust's acquisition date, acquisition price, holding-period balance, or disposal proceeds.
- Distinguish a documented product event from a documented Trust transaction.
- State the currency-aggregation method before any cross-currency dollar total is shown: the single reporting currency, the FX source and rate date convention applied to non-reporting-currency ISINs (for example CHF- or EUR-denominated positions), and whether historical or spot rates are used.

No aggregate dollar total should be presented as strategy-wide unless its investment basis is reconciled. Rate-based results may still be shown for rows with unresolved dollar bases.

## 5. Cost Taxonomy and Double-Counting Rules

The model uses mutually exclusive cost buckets.

| Cost component | Timing | Lifetime treatment |
| --- | --- | --- |
| Product manufacturing / structuring margin | Usually one-off | Apply to acquisition notional where comparable evidence supports the measure |
| Distribution compensation | Usually one-off, potentially recurring | Model separately from manufacturing margin unless the source is explicitly all-in |
| Potential retrocession | Sub-allocation of distribution/service compensation | Show only where a source supports the allocation; never add to total cost again |
| Advisory / management fee | Recurring | Apply to the time-weighted invested balance under a service-cost scenario |
| Custody / brokerage / transaction charge | Recurring or transactional | Include only with a comparable schedule or explicit assumption |
| Bid/ask spread or unwind cost | Contingent exit | Apply only to an actual or assumed sale/exit |
| Other explicit product charge | One-off or recurring | Include only if definition and overlap are clear |

Rules:

- Do not add an all-in issuance premium to its component-level manufacturing or distribution assumptions.
- Do not annualise a one-off premium without an explicit holding-period assumption.
- Do not convert annualised reduction in yield into a lifetime amount without a valid holding period and conversion method.
- Do not add potential retrocession to distribution compensation.
- Do not treat an unbenchmarked component as zero.
- Do not multiply a current position by the full historical strategy period without transaction and balance data.

## 6. How Retrocessions Work

Explain retrocessions as a possible allocation of compensation within a distribution or service chain, not as an automatic additional product cost or proof of a payment to the Trust's intermediary. The section should remain descriptive unless primary documents identify the relevant arrangement.

### 6.1 Distribution and service chain

Describe, at a high level, the possible participants and payment paths:

- Product manufacturer, issuer, or arranger that designs and prices the instrument.
- Distributor, placement agent, bank, adviser, or platform that introduces, recommends, or places the product.
- Sub-distributor or other intermediary that may receive part of the distribution or service compensation.
- Client or Trust, which may bear an embedded product margin, an explicit charge, or a recurring service cost depending on the arrangement.

Show that a retrocession is generally a payment or revenue share from one intermediary to another, rather than a separate charge automatically added to the investor's cost. Distinguish the investor-facing cost from the internal allocation of that cost or revenue.

### 6.2 What must be established

For any retrocession conclusion, identify separately:

- The payer and recipient.
- The contractual or commercial basis for the payment.
- The product, service, client account, or transaction to which it relates.
- The rate, amount, calculation base, and payment timing.
- Whether the amount is included within distribution or service compensation, or is an additional client charge.
- Any disclosure, consent, rebate, waiver, or conflict-management treatment.

If these elements cannot be established from reliable evidence, report the amount as `not separately estimable` or as an explicitly labelled scenario allocation. Do not infer a retrocession from the existence of a structured product, an intermediary relationship, a fee range, or a general market practice.

### 6.3 Treatment in the current-scope model

- Present potential retrocession as a nested sub-allocation of distribution or service compensation.
- Do not add it again to one-off product costs, recurring service costs, or any all-in benchmark.
- Apply a rate only where the source defines the payment and its calculation base; otherwise show a rate-based sensitivity without presenting it as a historical payment.
- Keep the payer, recipient, entitlement, disclosure, and recoverability questions outside the current-scope conclusion unless supported by primary records.
- State whether the result is evidence-based, a proxy allocation, or `not separately estimable`.

## 7. Evidence Framework

### 6.1 Source hierarchy

Prioritise:

1. Official regulators, enacted rules, public KIDs, final terms, pricing supplements, and comparable product disclosures.
2. Peer-reviewed academic studies and recognised market datasets with transparent methods.
3. Named industry or professional studies with a defined population and methodology.

### 6.2 Comparability dimensions

Score every quantitative observation from `0` to `2` for:

- Product/payoff.
- Vintage and regulatory regime.
- Jurisdiction and distribution channel.
- Cost definition.
- Unit and timing.
- Method and data quality.

Use high-scoring evidence for adopted bands, partial matches only as labelled secondary comparators or sensitivity inputs, and low-scoring evidence as context only.

### 6.3 Evidence status labels

Every input should be labelled as one of:

- `Adopted benchmark`
- `Secondary comparator`
- `Context only`
- `Assumption-led proxy`
- `Unbenchmarked`
- `Not separately estimable`

Every `Adopted benchmark` or `Secondary comparator` label must also cite the specific source ID from the Verified Source Register in [cost-benchmark-research.md](cost-benchmark-research.md) (for example `CH-05`, `EU-04`, `AC-02`) rather than the evidence-status word alone, so a reader can trace any applied rate back to one named source.

## 8. Cohort Findings

Use the same structure for each cohort:

1. Portfolio population and lifecycle coverage.
2. Available external evidence.
3. Comparability scores and limitations.
4. Adopted benchmark or reason for non-adoption.
5. ISINs included and excluded.
6. Cost components that remain unbenchmarked.

Recommended cohorts:

- Historical rate-linked callable, range-accrual, CMS, and related notes.
- Modern equity-linked express, barrier, phoenix, and dual-index products.
- Conventional and specialist debt, including fixed-rate, EMTN, secured, perpetual, and unusual instruments.
- Unclassified exceptions.

These cohort names must match the labels the cost model actually assigns (currently `Historical rate-linked`, `Modern rate-linked`, `Equity-linked`, and `Conventional / specialist debt` in `90. Scripts`/`05. Cost modeling/generate_dashboard.py`). Update either the report's cohort names or the script's cohort function together so the narrative and the generated model never diverge.

The historical rate-linked cohort should receive specific attention because it is the dominant vintage population and the principal unresolved evidence gap.

## 9. Scenario Methodology

### 8.1 Scenario A: Evidence-only

Use only evidence meeting the adoption rules. Leave unsupported components as `unbenchmarked` or `not separately estimable`. This is the most defensible but potentially incomplete result.

### 8.2 Scenario B: Proxy-base

Use the closest available cohort comparator where direct evidence is absent, with explicit adjustments or limitations for payoff, vintage, jurisdiction, channel, and timing. Use documented proxy lifecycle dates only where the Trust transaction date is unavailable.

### 8.3 Scenario C: Wide sensitivity

Test conservative, central, and upper cases for:

- One-off issuance rates.
- Distribution comparators.
- Recurring service rates.
- Holding periods.
- Early-exit versus hold-to-maturity paths.
- Acquisition-date and balance assumptions.
- Inclusion and exclusion of unresolved rows.

A sensitivity is not evidence that the tested amount was paid.

## 10. Lifetime Cost Results

Report results in separate, non-additive views.

### 9.1 One-off product costs

For each ISIN and cohort, show:

- Acquisition or proxy notional.
- Applicable rate or range.
- One-off estimated cost.
- Evidence status, comparability, and the specific source ID applied (for example `EU-05`, `CH-05`, `US-01`).
- Lifecycle event used.

### 9.2 Recurring service costs

Show:

- Annual run-rate.
- Accumulated cost over the modelled holding period.
- Balance and period assumptions.
- Advisory, management, custody, and brokerage components separately, each citing its supporting source ID where a comparator exists (for example `EU-04`, `CH-06`).

### 9.3 Contingent exit costs

Show separately for documented or assumed early exits:

- Exit date and basis.
- Assumed sale notional.
- Bid/ask, unwind, and transaction assumptions.
- Cost range and evidence status.

Do not include exit costs in hold-to-maturity issuance totals.

### 9.4 Potential intermediary compensation

Show only where the evidence identifies the relevant payment definition and basis, citing the specific source ID. Present potential retrocession as a nested sub-allocation of distribution or service compensation. Otherwise state `not separately estimable`.

## 11. Sensitivity and Coverage Presentation

Every aggregate table should include:

- Scenario name.
- Included ISIN count, distinguishing the 21 position-eligible ISINs from the 19 rows currently cost-assessable under a given scenario; show the remaining 2 usable-basis ISINs as `unbenchmarked`, not excluded.
- Included Trust notional.
- Excluded or unresolved ISIN count and notional, with position-basis exclusions (2 `issue/outstanding size`; 6 `missing`) and structure exclusions (3 path-6 ISINs) shown separately.
- One-off, recurring, and exit timing.
- Low/base/high values.
- Evidence confidence.
- Key assumptions driving the result.

Round every calculated monetary outcome displayed in the report, including scenario totals, ranges, and calculated coverage totals, to the nearest USD 100,000 using `ROUND(X, -5)`. Preserve source data exactly as collected: reported Trust positions, issuer issue/outstanding values, minimum denominations, and values sourced from XLS or Bloomberg must not be rounded or overwritten by this presentation convention.

Include a bridge showing how the result changes when:

1. Only usable invested notional is included.
2. Missing and unresolved rows are added under proxy assumptions.
3. Products are assumed acquired at issuance rather than at an unknown later date.
4. Products are held to call/maturity rather than sold early.
5. Annual service costs are excluded, added, or accumulated over alternative periods.

## 12. Conclusions and Decisions

The conclusion should answer:

- What lifetime cost range is supported by evidence alone?
- What additional range appears under proxy assumptions?
- Which components dominate the result?
- How much of the portfolio is covered by usable investment bases?
- Which results are rate-based only rather than dollar estimates?
- Is a potential retrocession amount separately estimable?
- Which unresolved issues materially affect the result?
- Which records would most reduce uncertainty within the current scope?

The final conclusion must not describe the proxy-base or wide-sensitivity result as an actual historical fee total.

## 13. Recommended Next Actions

Prioritise actions by expected reduction in uncertainty and recovery value:

1. Reconcile Trust acquisition notional and dates for the highest-value ISINs.
2. Recover disposal, call, maturity, and redemption proceeds where available.
3. Retrieve final terms and pricing supplements for the historical rate-linked cohort.
4. Test distribution and compensation clauses against the relevant product documents.
5. Obtain account-level advisory, custody, brokerage, and transaction records if those components are required.
6. Update the model only when each new input has a source, definition, timing, and non-overlap decision.

## 14. Appendices

- Appendix A: 29-ISIN lifecycle matrix.
- Appendix B: Position-size usability and coverage register.
- Appendix C: Benchmark evidence register.
- Appendix D: Benchmark comparability scores and adoption decisions.
- Appendix E: Scenario assumptions and formulas.
- Appendix F: ISIN-level lifetime cost outputs.
- Appendix G: Negative-evidence and search log.
- Appendix H: Limitations, glossary, and scope boundary.

## Proposed Final Report Deliverables

1. PDF or Markdown methodology and findings report.
2. Workbook or generated model with ISIN-level calculations, assumptions, source register, and coverage controls.
3. Executive summary table suitable for board reporting.
4. Prioritisation list linked to unresolved cost and lifecycle inputs.

## Sign-Off Controls

Before publication:

- All 29 ISINs have exactly one lifecycle row.
- Coverage tables reconcile to the current position-size register: 21 `usable invested notional`, 2 `issue/outstanding size`, and 6 `missing`.
- `XS0168875792`, `XS0318585791`, and `XS0298465822` are visible as explicit evidence-limited rows. Any with a usable Trust position remains in the analysis; none is assigned a zero cost.
- Every cost input resolves to a source or an explicitly labelled assumption.
- Low, base, and high values are ordered correctly.
- One-off, annual, and exit costs are not mixed.
- All-in measures are not stacked with their components.
- Potential retrocession is nested, not additive.
- Issuer issue size and minimum denomination are excluded from Trust exposure.
- Aggregate dollar results reconcile to included usable notional.
- Every calculated monetary outcome displayed in the report uses `ROUND(X, -5)`; source values collected from XLS and Bloomberg remain unchanged.
- Cross-currency aggregate results state the reporting currency, FX source, and rate-date convention used.
- Every applied rate cites a specific Verified Source Register ID; no cost result relies on an evidence-status label alone.
- Path-6 ISINs (DATA INTEGRITY AUDIT.md G-006 and G-010) are shown as explicit evidence limitations. A usable Trust position keeps an ISIN in the analysis regardless of issuer issue-size availability; a missing Trust position prevents only dollar aggregation, not coverage reporting.
- The position-size resolution status stated in the report matches the current POSITION SIZE CONTROL.md register; older audit wording that predates the 21 usable-basis classifications is not used for publication.
- Every headline result states timing, coverage, scenario, confidence, and limitations.
- The executive memo, if updated, reconciles exactly to the validated model outputs.

## 15. Limitation and Disclaimer

Place one dedicated limitation and disclaimer statement in the Executive Summary. It applies to all scenario results, including evidence-based and proxy-based estimates, and is not repeated elsewhere in the final report. Tables and charts should instead identify their scenario, evidence status, timing, coverage, and key assumptions.
