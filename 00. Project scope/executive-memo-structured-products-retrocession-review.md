Greenlock AG | Hinterbergstrasse 49, CH-6312 Steinhausen, Switzerland | greenlock.io

# Executive memo: Structured Products

## Retrocession Review

### Background

The earlier `1-5% of notional` statement is an unverified sensitivity hypothesis, not an adopted market retrocession rate. The controlled model currently contains 21 source-reported USD position amounts totaling **$71.22m**, but only 17 rows totaling **$67.82m** receive a benchmark-based cost calculation after cohort and evidence controls. A mechanical 1-5% sensitivity over the full 21-row basis would be approximately **$0.71m-$3.56m**; that arithmetic is not evidence of a retrocession payment, recipient, or entitlement.

**Time-sensitive:** the 23 vintage ISINs (2003–2007) are at or past typical bank record-retention windows (commonly 10 years). Every quarter of delay reduces the probability of document recovery — and with it, the recoverable value.

### Current Tier 1 cost summary

| Method / component | Cost | Coverage | Treatment |
|---|---:|---:|---|
| **Evidence-based total** | **$2.8m-$3.3m** | **17 ISINs / $67.8m** | Adopted comparators for explicit equity- and rate-linked cohorts |
| **Combined proxy scenario** | **$6.4m** | **17 ISINs / $67.8m** | Sum of proxy components on the same 17-row basis |
| Embedded product proxy | $3.2m | 17 ISINs | One-off product-cost assumption |
| Recurring service proxy | $2.6m | 17 ISINs | Assumed annual rate multiplied by issue-date purchase proxy |
| Exit / transaction proxy | $0.7m | 17 ISINs | Assumed contingent exit cost |

All amounts are rounded to the nearest `$100,000`. The unrounded proxy reconciliation is **$3,209,910 + $2,557,783 + $651,072 = $6,418,765**. The rounded component labels may therefore differ from the rounded total by `$100,000`; the unrounded calculation is the controlling sum. The evidence-based total is supported by adopted comparators, not proof that costs were charged or paid. The proxy rows are assumption-led; potential retrocession remains a nested, non-additive sub-allocation and is not separately estimable.

### Calculation controls

- **Reporting currency and FX:** The model reports in USD. Every included position amount is sourced from the workbook's USD position field or an evidence note explicitly recording USD. No FX conversion is applied. A future non-USD Trust position requires a dated FX source and rate before inclusion. The instrument's denomination currency is shown separately and does not silently change the source position currency. The EUR-denominated instrument has no Trust position and is excluded.
- **Holding period:** Where the Trust purchase date is unavailable, the model explicitly assumes **purchase date = issue date** and uses the reported call or maturity as the end event. This is a lifecycle proxy, not evidence of the Trust's acquisition date, acquisition price, balance through time, or lifetime fee payment.
- **Position provenance:** Historical workbook amounts described as `across different line items` are assumed to represent the total Trust position for this scenario. The `XS0765564827` source amount described as `min 200,000` is likewise treated as a total USD 200,000 Trust position. Both are reversible modelling assumptions pending Trust custody or transaction records.
- **Cohort and benchmark selection:** Explicit equity-linked terms receive the equity-linked comparator; explicit LIBOR, CMS, swap-rate, fixed-to-variable, or rate-linked terms receive the historical rate-linked comparator. `XS0300388351` is therefore rate-linked because its underlying is a USD 30-year swap rate. `XS0297701319` is not benchmarked as rate-linked because its source describes USD/Gold and Nikkei exposure. `XS0168875792` and `XS0318585791` remain evidence-limited because issue dates and primary structure evidence are unavailable. The 17 benchmark-covered rows exclude those four rows and the conventional/specialist `XS0765564827`.

### How retrocessions work

Structured products may embed manufacturing and distribution economics in their issue price, but the research does not establish a universal 1-5% pool or prove that a payment was made on any Trust position. Potential retrocession is treated as a possible sub-allocation of evidenced distribution or service compensation, not as an additional cost layer. Its amount, payer, recipient, timing, disclosure, and entitlement remain unverified. Recovering term sheets and account records is therefore required before any retrocession conclusion; Tier 1 can identify sensitivities and priorities but cannot establish a payment or recipient.

### Proposal

We propose a two-tier engagement to quantify total strategy cost and isolate the retrocession component: Tier 1 (Light Analytics) and Tier 2 (Complete Analytics).

|  | Tier 1 — Light Analytics | Tier 2 — Complete Analytics |
| --- | --- | --- |
| **Coverage** | All 29 ISINs | Subset with recoverable term sheets (6 confirmed; up to 23 vintages, subject to recovery) |
| **Method** | Heuristic/theoretical cost modelling using market data & financial mathematics | Contractual fee extraction from recovered term sheets, reconciled to bank statements |
| **Output** | Evidence-based and proxy cost scenarios, assumptions, coverage, and unresolved retrocession status | Auditable, itemised fee waterfall confirmed against source documents |
| **Confidence** | Indicative — model-based | High — evidence-based |
| **Use case** | Board reporting, initial prioritisation, negotiation leverage | Formal dispute, legal recovery, trustee disclosure |
| **Deliverable** | Excel model + summary tab (ISIN-level costs, sensitivity, assumptions) | Excel model + PDF audit report + source document repository |
| **Timeline** | 2 weeks | 4 weeks (post document recovery) |
| **Fee** | CHF 20,000 | CHF 50,000 |

The Tier 1 fee is CHF 20,000. Because the model reports USD and no dated CHF/USD conversion has been adopted, this memo does not state the fee as a percentage of the USD position basis. The fee should not be compared with a theoretical retrocession amount that has not been evidenced.

## Recommended Path

We suggest starting with Tier 1 across all 29 ISIN records to establish the controlled coverage baseline and identify the highest-exposure positions. Dollar scenarios should remain limited to the 21 USD source-position rows, with benchmark totals limited to the 17 rows that pass cohort and evidence controls. Tier 2 can then prioritise the 6 ISINs with confirmed documentation, followed by vintage ISINs subject to document recovery. In parallel, legal confirmation of retrocession entitlement—whether it rests with the Trust or the bank—should proceed independently, as this determines the recovery strategy regardless of the analytics tier pursued.

We recommend confirming the proof-of-concept ISIN by July 31, 2026, so that any formal document request to distributing banks for the 2003–2007 vintage can be initiated before Q3 2026 quarter-end (September 30, 2026) — minimizing further erosion of an already timesensitive recovery window for these oldest positions.

## Next Step

The Trust has no basis to confirm whether retrocession income on this strategy was received, disclosed, or owed to the Trust — a gap that time will not resolve. Vintage documentation becomes less recoverable each quarter, and entitlement remains an open fiduciary question despite inaction. Commissioning this analysis is the only way to convert that question into a documented, closed matter.
