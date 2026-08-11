Greenlock AG | Hinterbergstrasse 49, CH-6312 Steinhausen, Switzerland | greenlock.io

# Tier 1 Cost-Benchmark Research Plan

## Purpose

This plan implements the **Tier 1 - Light Analytics** scope in the [Executive memo: Structured Products](executive-memo-structured-products-retrocession-review.md). It will produce an indicative, portfolio-wide estimate of the economic costs embedded in, or charged alongside, the 29 structured-product positions.

Tier 1 answers the following question:

> What ranges of total economic cost and potential intermediary compensation are plausible for products comparable to the Trust's holdings, based on trusted external evidence and transparent assumptions?

The analysis is intended for board reporting, prioritisation, and negotiation support. It is model-based and does not prove actual fees, payments, recipients, disclosure, entitlement, or recoverability.

## Review of Current Evidence

Four source passes recorded in the [Tier 1 Cost-Benchmark Research](cost-benchmark-research.md) establish a defensible taxonomy and a set of useful, non-interchangeable comparators:

- A historical ESMA all-in issuance-premium observation of approximately `4.6%` of notional, or `5.5%` including issuer credit risk, from a 76-product EU sample (EU-05).
- A modern PRIIPs-era median reduction in yield of `1.03% p.a.`, including `1.01% p.a.` attributed to subscription fees (EU-04).
- Two component-level modern distribution observations: a disclosed distributor fee of up to `1.75%` of nominal on a 2025 EU callable note (EU-06) and a placement fee of up to `3.00%` of issue price on a 2026 Swiss callable range-accrual note (CH-05).
- A modern Swiss all-in comparator of `0.3%-1.7% p.a.` median TER by equity-linked product category from a 20,000-product SIX sample (CH-06), and a `0.16%` average bid/ask spread for German listed discount certificates 2006-2013 (AC-04).
- Official Swiss terminology and disclosure controls at article level (FinSA Art. 26, CH-07) and German equity-linked issuance-premium literature (`2.13%-10.04%` by payoff family, AC-03).

No observation yet identifies a distributor-compensation range or retrocession share for the dominant 2003-2007 rate-linked cohort, and the fourth pass closed the historical rate-linked workstream under the stop rule with an `unbenchmarked` result. The evidence therefore supports model architecture, modern secondary comparators, and sensitivity bands, but not vintage-matched low/base/high assumptions or an estimated retrocession pool.

The next research phase must address six specific weaknesses:

1. **Portfolio mismatch:** no quantitative observation is yet matched to the portfolio's dominant 2003-2007 rate-linked and callable-note population; the closed `unbenchmarked` result may be reopened only against the new vintage-matched source families defined below.
2. **Fee-definition mismatch:** issue-price premia, reduction in yield, issuer margin, distribution compensation, and retrocession are different measures and cannot be substituted for one another.
3. **Missing distribution evidence:** the two disclosed modern placement fees (EU-06, CH-05) are single-product secondary comparators; no market-wide or vintage-matched distributor-compensation range or retrocession share has been adopted.
4. **Missing exit and service-cost evidence:** the AC-04 spread observation is context-only for equity certificates; no suitable rate-linked bid/ask, unwind, advisory, custody, or brokerage benchmarks have been adopted.
5. **Investment-basis uncertainty:** many reported position sizes are described as covering multiple line items, are blank, or appear to be minimum denominations or issue sizes. Research can proceed, but portfolio dollar aggregation must wait for a controlled usability classification.
6. **Proxy-decomposition uncertainty:** the available proxy observations support selected all-in totals and isolated components, but not a reconciled allocation of a proxy total among manufacturing, distribution, service, exit, and potential retrocession buckets. Increasing confidence requires component-level evidence with compatible product, vintage, jurisdiction, channel, timing, and cost definitions, plus an explicit reconciliation to the applicable all-in proxy.

This plan treats the `1-5% of notional` statement in the executive memo as a hypothesis to test, not a target range to validate.

## Scope Boundary

### Included
## Cost Taxonomy

The model will report three non-overlapping cost groups. Each input must state whether it is a one-off rate, an annual rate, or a contingent exit cost. Detailed source categories remain available for research and reconciliation, but they roll up only to the three groups below.

| Cost group | Detailed source categories | Timing | Tier 1 treatment |
| --- | --- | --- | --- |
| Embedded product cost | Product manufacturing / structuring margin, distribution compensation, other explicit product charges, and unexplained embedded residual | One-off | Apply at issuance or acquisition. Reconcile directly evidenced components and any residual to an applicable all-in product-cost proxy; do not allocate a residual without source support. |
| Recurring investment-service cost | Advisory / management fee, custody, recurring account charges, and any directly evidenced recurring distribution payment | Annual / recurring | Report as an annual run-rate. Convert to a holding-period amount only when the invested balance and holding period are valid. Keep outside embedded product cost unless the source expressly includes it. |
| Exit and transaction cost | Brokerage, bid/ask spread, unwind, early-sale charges, and transactional custody or execution charges | Transactional / contingent | Apply only to an actual or stated assumed exit. Exclude from hold-to-maturity and issuance totals. |

Potential retrocession is a memorandum sub-allocation of distribution or service compensation, not a fourth cost group and not an additional investor cost.
- Recovery of final terms, KIDs, client agreements, or other documents.
Run a dedicated workstream to determine whether proxy estimates can be presented confidently across the three cost groups without creating false precision. The objective is not to force every total into a detailed allocation; it is to increase confidence in each group only where compatible evidence and a defensible reconciliation exist.
| Priority | Cost group and research focus | Target evidence | Confidence objective |
- Reconciliation to bank statements or payment records.
| 1 | Embedded product cost: obtain product-level issue price, issuer estimated value, and explicit selling-concession or placement-fee disclosures | Final terms, pricing supplements, KIDs, issuer estimated-value disclosures, and valuation studies with explicit treatment of hedging, credit, production, and distribution costs | Increase confidence in the all-in one-off proxy and, where possible, reconcile directly evidenced embedded items to it while retaining any unexplained residual |
| 2 | Recurring investment-service cost: identify comparable advice, management, custody, and recurring-distribution schedules | Trust-specific agreements and statements where available in Tier 2; otherwise public private-bank mandate tariffs with client segment, asset band, included services, and period | Build separately switchable annual run-rate proxies without importing them into embedded product cost |
| 3 | Exit and transaction cost: identify product- and venue-matched realised execution costs | Transaction datasets, contemporaneous dealer quotes, trade confirmations, exchange studies, and empirical spread studies distinguishing quoted spread from realised one-way execution cost | Build a contingent exit proxy by liquidity, product age, and market condition |
| 4 | Potential retrocession: identify an onward allocation within an evidenced parent payment | Primary intermediary disclosures, distribution agreements, court findings of fact, or regulator datasets identifying the allocation basis and whether it is included within distribution or service compensation | Report only as a nested memorandum allocation; never infer it from a group total or residual |
For each proposed group estimate, create a reconciliation record containing the all-in proxy source where applicable, detailed source categories, cohort, low/base/high values, units, timing, comparability scores, overlap analysis, and residual. Reconcile embedded product cost using:
Recurring investment-service and exit/transaction costs sit outside this embedded-product reconciliation unless the all-in source expressly includes them. Potential retrocession is a memorandum sub-allocation within distribution or service compensation and is never added to the equation.
Do not describe an embedded-product reconciliation as complete when the unexplained residual is material. Do not set manufacturing, distribution, retrocession, or service costs equal to the arithmetic residual merely to make components sum to the all-in proxy. Report group-level confidence and, where shown, detailed-source confidence; group confidence is capped by the weakest material source, unresolved overlap, or residual.
For the embedded product-cost group, adopt detailed-source amounts only when the evidence measures them directly and they can be reconciled to the all-in proxy without concealed overlap. Show any unexplained residual explicitly and retain the undecomposed all-in proxy as the controlling total. Detailed sources do not supersede the all-in proxy unless the group reconciliation reaches at least `Medium` confidence under section 3b. For recurring investment-service and exit/transaction groups, adopt a proxy only when its evidence measures the relevant annual or contingent cost directly.
Calculate and present three non-overlapping cost groups:

1. **Embedded product cost**: one-off issuance or acquisition cost, including any unexplained embedded residual.
2. **Recurring investment-service cost**: advisory, management, custody, and other annual account-level costs, shown as an annual run-rate unless a valid holding period and balance basis support a lifetime amount.
3. **Exit and transaction cost**: bid/ask, brokerage, unwind, and other transaction costs under an actual or stated assumed secondary-market exit.
Where an embedded product-cost reconciliation is presented, show the controlling all-in proxy, detailed-source amounts, unexplained residual, and group-confidence level together. Detailed sources marked `Low` or `None` must not be silently included in a reconciled group total.
- Sum only compatible embedded-product estimates across ISINs with usable investment bases.
- Report recurring investment-service amounts as an annual run-rate.
- Report exit and transaction costs as a separate contingent scenario.
- Test benchmark low/base/high cases, inclusion or exclusion of recurring investment-service costs, hold-to-maturity versus exit, and source-supported retrocession allocations.
The portfolio summary will separately show embedded product cost, recurring investment-service annual run-rate, exit and transaction cost, potential retrocession memorandum range where estimable, coverage percentages, group confidence, and sensitivity drivers.
4. **Double-count audit:** Confirm retrocession is nested within distribution or service compensation, all-in fair-value gaps are not stacked with their detailed sources, recurring investment-service charges are not included in embedded product cost, and exit and transaction costs occur only in exit scenarios.
11. **Three-group audit:** Confirm every group input is directly evidenced or explicitly assumed, timing and definitions are compatible, the embedded-product residual is visible, nested retrocession is not added twice, and displayed group confidence follows section 3b.
| Three-group proxy model | Embedded product cost reconciles to the all-in proxy where applicable, recurring and exit costs remain outside it, overlap is controlled, residual is explicit, and group confidence is stated | Retain the undecomposed embedded-product proxy and show detailed-source observations only as separate sensitivities |
6. Run the three-group proxy-confidence workstream, reconcile embedded product cost to each applicable all-in proxy, and record confidence for each group and any detailed-source support.
Group the 29 ISINs by economically comparable payoff and distribution characteristics, using existing canonical product dossiers as the input source:

- Callable, range-accrual, CMS, and other rate-linked notes.
- Equity-linked express, barrier, phoenix, and dual-index products.
- Conventional fixed-rate and EMTN instruments.
- Secured, perpetual, and specialist notes.
- Insufficiently classified exceptions.

For each ISIN, record product segment, issue year or vintage band, tenor where known, currency, issuer and likely distribution jurisdiction, callable or path-dependent features, term-sheet status, position-size quality, and source-confidence flags. The issuer's total issue or outstanding size must not be substituted for the Trust's exposure.

Assign every ISIN to a research cohort before selecting benchmarks:

| Cohort | Portfolio use | Minimum matching dimensions |
| --- | --- | --- |
| Historical rate-linked | Primary cohort for the stated 2003-2007 concentration | Vintage, callable/range/CMS payoff, currency/rate market, investor channel |
| Modern equity-linked | Express, barrier, phoenix, and dual-index products | Payoff family, recommended holding period, jurisdiction, retail/private-bank channel |
| Conventional or specialist debt | Fixed-rate, EMTN, secured, perpetual, and unusual structures | Instrument form, credit/ranking, tenor, liquidity, distribution channel |
| Unclassified exception | Products without enough terms for economic matching | Record as `unbenchmarked` until classification is supportable |

Separately classify each reported `position_size` as `usable invested notional`, `shared across line items`, `minimum denomination`, `issue/outstanding size`, `missing`, or `unclear`. This classification is a calculation control, not document-recovery work. Reconcile the plan's assumed documentation coverage to the repository inventory before using a term-sheet count in any Tier 1 conclusion.

### 2. Use a Source Hierarchy

| Priority | Accepted evidence | Use |
| --- | --- | --- |
| A | Official regulator studies and methodologies; enacted rules; public KIDs, final terms, and comparable product disclosures. | Definitions, disclosure context, and comparable observable costs. |
| B | Empirical academic studies and recognised market datasets that state population, period, product type, and method. | Benchmark calibration. |
| C | Named industry, professional, or consulting surveys with transparent definitions and samples. | Secondary calibration where higher-priority evidence is incomplete. |

Exclude anonymous web commentary, uncited estimates, sales material without methodology, and search-result snippets. A regulator's disclosure rule may explain terminology but cannot prove a payment on a portfolio ISIN.

### 3. Run Targeted Evidence Workstreams

Research in the following order. Each workstream must answer a defined modelling question and produce either an adoptable observation or an explicit evidence gap.

| Priority | Workstream and question | Target evidence | Tier 1 output |
| --- | --- | --- | --- |
| 1 | **Historical rate-linked issuance economics:** what issue-price premium or issuer-margin distributions were observed for callable, reverse-floater, range-accrual, CMS, or comparable notes around 2000-2010? | Regulator studies, peer-reviewed valuation studies, contemporaneous prospectuses or pricing supplements with issue price and estimated value, recognised datasets | Segment-specific all-in issuance band or `unbenchmarked` |
| 2 | **Distribution compensation:** what selling concessions, placement fees, distributor margins, or third-party payments were disclosed for comparable Swiss and EU private-bank products? | Public final terms, KIDs with cost decomposition, regulator thematic reviews, enforcement records containing market-wide observations, transparent industry datasets | Distribution range by channel/segment; no retrocession inference unless the source identifies it |
| 3 | **Issuer-margin calibration:** what part of the issue-price gap is attributable to manufacturing economics rather than credit, hedging, or distribution? | Full text and tables for AC-01 and AC-02; additional studies with explicit valuation methods and samples | Manufacturing range or all-in-only treatment with a no-decomposition flag |
| 4 | **Modern product comparator:** how do PRIIPs-era entry costs vary by payoff, country, holding period, and risk class? | ESMA 2023 annexes and underlying SRP tables; public KIDs for close comparables | Modern comparator by segment, kept separate from historical estimates |
| 5 | **Exit costs:** what bid/ask spreads or unwind discounts are observed by product type, age, liquidity, and market condition? | Exchange or regulator studies, transaction datasets, issuer quote studies, transparent empirical papers | Contingent exit bands; otherwise `unbenchmarked` |
| 6 | **Account-level service costs:** what advisory, custody, and brokerage schedules are observable for a comparable mandate and client channel? | Public tariff schedules or regulator studies with clear service definitions | Separately switchable annual/transaction scenarios, never embedded-note costs |
| 7 | **Swiss terminology and controls:** what official provisions define third-party compensation and client information duties? | Article-level Fedlex text and relevant official FINMA material | Terminology and disclosure context only; no legal conclusion or numerical rate |

Search historical and modern evidence separately. Prioritise evidence that reports distributions or product-level observations over market-wide averages. A source that only repeats a headline percentage without population, period, measure, and method is discovery material, not benchmark evidence.

For distribution compensation, use a staged search sequence: regulator and exchange publications; prospectus/final-terms language containing `selling concession`, `placement fee`, `distribution fee`, `subscription fee`, `third-party payment`, or equivalent local terminology; academic or recognised dataset evidence; then named industry studies. Record a null result after each stage so the absence of an adopted rate is reproducible.

### 3a. Trusted-Source Expansion for the Next Pass

The fourth pass exhausted generic web discovery for the vintage cohort. The next pass must move from open search to named, high-authority repositories and named literature, in the following order. Each family is mapped to the evidence gap it can close.

| Gap | Trusted source family | What to extract | Why it can succeed where open search failed |
| --- | --- | --- | --- |
| Vintage rate-linked distribution compensation | SEC EDGAR 424B2/424B5 pricing supplements, 2003-2008, for USD callable notes, range-accrual notes, and CMS-spread notes from comparable issuers (Priority A) | The mandatory `agent's discounts and commissions` / selling-concession line, issue price, and estimated-value language, product by product | US-registered vintage notes are payoff- and period-matched to the XS cohort and carry an explicit, dated, per-product fee disclosure that EU/CH documents of that era generally omit |
| Vintage rate-linked final terms in the issuance jurisdiction | Luxembourg Stock Exchange (LuxSE) and Euronext Dublin document archives for the portfolio's own XS ISINs and same-programme siblings (Priority A) | Final terms, pricing supplements, and programme base prospectuses; any `commission`, `concession`, or issue-price-discount clause | The 23 vintage ISINs are Euro-MTN issues most plausibly listed in Luxembourg or Dublin; exchange archives outlive bank retention windows |
| Historical issuance economics, rate-linked | Named academic literature with full-text retrieval via SSRN, RePEc, or journal DOI: Henderson and Pearson (*The Dark Side of Financial Innovation*, JFE 2011), Célérier and Vallée (QJE 2017), Vokata (*Engineering Lemons*, JFE 2021), Jorgensen et al. on retail structured debt overpricing (Priority B) | Sample, period, payoff coverage, measured issue-price premium or embedded-fee distributions, and any decomposition method | These studies measure overpricing and embedded fees at issuance on large samples that include rate-linked and callable retail notes, unlike the German equity-certificate literature already logged |
| Swiss-market historical calibration | Burth, Kraus and Wohlwend (FMPM 2001), Grünbichler and Wohlwend (2005), and other pre-FinSA Swiss primary-market pricing studies (Priority B) | Measured issue-price deviations for SWX/SIX-listed products near the portfolio vintage | Directly Swiss, closer in period than the 2012-2015 SFI study, and complements CH-06 |
| Retrocession share and mechanics | Official Swiss court decisions at full text (ATF 137 III 393; ATF 138 III 755 extending retrocession duties to distribution fees on structured products) via bger.ch, plus FINMA supervisory communications (Priority A) | Any stated calculation parameters, ranges, or `Bestandespflegekommission` mechanics recorded by the court or regulator | Court and regulator texts sometimes record actual market ranges as findings of fact; commentary summaries already logged (CH-02) do not |
| Distribution-channel ranges | National-regulator thematic reviews and enforcement records with market-wide observations: UK FSA/FCA structured-product reviews, BaFin, AMF, Consob, Central Bank of Ireland; ESMA 2023 statistical annexes at table level (Priority A) | Reported distribution-fee or inducement ranges by product class and channel, with population and period | Thematic reviews quantify channel economics that individual final terms cannot |
| AC-01 / AC-02 completion | Publisher full text via DOI, SSRN, or institutional repository (Priority B) | Exact sample, valuation method, and issuer-margin distributions | Converts two logged placeholders into scored, adoptable evidence |

Apply these retrieval tactics across all families:

- Search in the market's languages, not only English: `Platzierungsprovision`, `Vertriebsvergütung`, `Vertriebsentschädigung`, `Bestandespflegekommission`, `Ausgabeaufschlag`, `rétrocession`, `commission de placement`, `commission de distribution`.
- Query issuer document hubs and programme archives directly (e.g. issuer EMTN programme pages) for same-programme sibling notes when the portfolio ISIN's own final terms are not indexed.
- Use official web archives only to retrieve a document whose original publisher and identity are verifiable; an archived copy inherits the original's priority level, never a higher one.
- For every EDGAR or exchange-archive observation, capture accession number or document ID, filing date, issuer, payoff type, tenor, and the exact fee clause, so the observation can be comparability-scored like any other source.
- US observations are channel and regime mismatched for Swiss private-bank distribution: cap their comparability score on the jurisdiction/channel dimension at `1` and use them to bound, not set, the vintage distribution band.
- Continue to record a null result per family; reopening the closed rate-linked workstream requires at least one Priority A/B observation from these families, not a repeat of exhausted open-search queries.

### 3b. Proxy-Decomposition Confidence Workstream

Run a dedicated workstream to determine whether an all-in proxy total can be split into mutually exclusive sub-components without creating false precision. The objective is not to force every total into a complete allocation; it is to increase confidence only where compatible component evidence and a defensible reconciliation exist.

Prioritise the following research directions:

| Priority | Component | Target evidence | Confidence objective |
| --- | --- | --- | --- |
| 1 | Manufacturing / structuring margin | Product-level issue price and independently estimated fair value, or issuer-disclosed estimated value, with explicit treatment of hedging, credit, production, and distribution costs | Isolate issuer economics from the all-in issue-price gap for a matched payoff and vintage |
| 2 | Distribution compensation | Final terms, pricing supplements, KIDs, or placement agreements stating selling concession, agent commission, placement fee, issue-price discount, recipient class, and payment timing | Establish a cohort-specific one-off or recurring distribution band rather than extrapolating from a single product |
| 3 | Potential retrocession | Primary intermediary disclosures, distribution agreements, court findings of fact, or regulator datasets identifying the allocation basis and whether it is included within distribution or service compensation | Estimate only a nested share of an evidenced parent component; never infer it as the residual of an all-in cost |
| 4 | Advisory / management and custody | Trust-specific agreements and statements where available in Tier 2; otherwise public private-bank mandate tariffs with client segment, asset band, included services, and period | Build separately switchable recurring proxy bands and keep them outside embedded product cost |
| 5 | Brokerage, bid/ask, and unwind | Product- and venue-matched transaction datasets, contemporaneous dealer quotes, trade confirmations, or empirical spread studies distinguishing quoted spread from realised one-way execution cost | Build a contingent exit scenario by liquidity, product age, and market condition |
| 6 | Other explicit product charges | Product documents identifying a charge, basis, timing, and overlap with disclosed total costs | Include only document-defined residual buckets that do not duplicate another component |

For each proposed split, create a decomposition record containing the all-in proxy source, component sources, cohort, low/base/high values, units, timing, comparability scores, overlap analysis, and residual. Reconcile components using:

`all-in proxy = manufacturing + distribution + other embedded product costs + unexplained residual`

Advisory, custody, brokerage, and contingent exit costs sit outside this embedded-product reconciliation unless the all-in source expressly includes them. Potential retrocession is a memorandum sub-allocation within distribution or service compensation and is never added to the equation.

Assign a confidence level to each split:

| Confidence | Minimum evidence standard | Permitted presentation |
| --- | --- | --- |
| High | Direct product or tightly matched cohort decomposition; compatible definitions and timing; independent corroboration; all material components and residual reconcile to the all-in total | Component low/base/high amounts and reconciled total |
| Medium | At least one high-quality component observation plus independent support, with documented but bounded cohort mismatch and a transparent residual | Labelled proxy component ranges and residual; no claim of actual allocation |
| Low | Single-product, mismatched, or context-only component observations; incomplete reconciliation or material unexplained residual | Sensitivity only, shown separately from the proxy total |
| None | No quantitative component evidence, incompatible definitions, or double-counting cannot be ruled out | `Unbenchmarked` or `not separately estimable` |

Do not describe a proxy split as complete when the unexplained residual is material. Do not set manufacturing, distribution, retrocession, or service costs equal to the arithmetic residual merely to make components sum to the all-in proxy. Report both component-level confidence and overall split confidence, with overall confidence capped by the weakest material component or unresolved overlap.

### 4. Capture a Benchmark Evidence Register

Record each external observation before using it in the model. The register will contain:

- Source ID, publisher, title, publication date, URL or repository location, and access date.
- Page, table, or section locator.
- Jurisdiction, observation period, product population, and distribution channel.
- Cost bucket, quoted statistic or range, unit, timing, and currency.
- Methodology, sample size where reported, limitations, and analyst confidence.
- Decision on applicability to each portfolio segment.

Also record whether the observation is `all-in` or `component-level`, whether credit and hedging effects are included, and whether the statistic is a mean, median, percentile, range, or single-product value. Preserve quoted source units before making any conversion.

Research Swiss and EU/EEA evidence separately. Distinguish historical evidence relevant to the 2003-2007 vintage concentration from modern MiFID II or PRIIPs-era evidence; do not apply modern disclosure figures retrospectively without a documented comparability adjustment.

### 5. Score Comparability Before Adoption

Score each quantitative observation against the intended portfolio cohort. Use `2` for a direct match, `1` for a partial match with a documented limitation, and `0` for a material mismatch.

| Dimension | Adoption question |
| --- | --- |
| Product/payoff | Is the observation for the same economic payoff family? |
| Vintage/regime | Is the observation contemporaneous, or is an explicit vintage adjustment supportable? |
| Jurisdiction/channel | Does it reflect a comparable Swiss or EU/EEA retail/private-bank distribution setting? |
| Cost definition | Does the source measure the exact model bucket without overlap? |
| Unit/timing | Is it expressed on a compatible notional, fair-value, one-off, annualised, or holding-period basis? |
| Method/data quality | Are sample, method, locator, and statistic reproducible? |

An observation scoring `10-12` may support a benchmark band. A score of `7-9` may be used only as a labelled secondary comparator or to widen a band supported by stronger evidence. A score below `7` is context or sensitivity evidence only. Regardless of score, an all-in observation cannot calibrate a component-level distribution or retrocession assumption.

### 6. Construct Benchmark Bands

Create low, base, and high assumptions for each applicable portfolio segment using compatible evidence. Prefer reported percentiles; otherwise use a documented central statistic and observed bounds. Triangulation requires either one high-comparability quantitative source corroborated by a second independent source, or two independent quantitative sources with no material definition conflict. Do not average evidence with incompatible products, eras, fee definitions, or units.

For every adopted band, write a short decision record containing the cohort, cost bucket, low/base/high values, unit and timing, source IDs, comparability scores, conversion formula if any, overlap treatment, and reason for adoption. Where only an all-in issuance comparator exists, model it as a separate all-in scenario and do not decompose it into manufacturing, distribution, or retrocession components.

For proxy decompositions, adopt a component band only when its evidence measures that component directly and the combined component ranges can be reconciled to the all-in proxy without concealed overlap. Show any unexplained residual explicitly and retain the undecomposed all-in proxy as the controlling total. A more detailed split does not supersede the all-in proxy unless the decomposition reaches at least `Medium` confidence under section 3b.

The executive memo's current 1-5% range is an unverified working hypothesis. Retain it only as a sensitivity comparator until external research either supports, narrows, or replaces it. Where the evidence is insufficient, report `unbenchmarked` rather than imposing a portfolio-wide percentage.

### 7. Apply Research Stop Rules

A workstream is complete when one of the following is true:

- The adoption rule is met and the observation has a reproducible page, table, section, or product-document locator.
- The available evidence supports only an all-in comparator, and further decomposition would require Tier 2 documents or unsupported assumptions.
- The source hierarchy has been exhausted and the evidence gap is recorded with searches performed, sources rejected, and the reason no benchmark was adopted.

Do not delay the Tier 1 workbook solely to force a retrocession rate. A rigorous `not separately estimable` result is a valid Tier 1 finding.

## Model Design

### Investment Basis

Use the reported `position_size` as the basis for a product calculation only where it plausibly represents the Trust's invested notional. Flag and exclude from aggregate dollar totals where the value is missing, is a minimum denomination, is stated as covering multiple line items, or otherwise cannot be used reliably.

### Per-ISIN Views

Calculate and present three non-overlapping views:

1. **Issuance view**: one-off structuring and distribution cost ranges.
2. **Recurring annual view**: advisory, management, and custody ranges shown per annum without inventing a holding period.
3. **Exit view**: bid/ask, brokerage, and unwind ranges under an assumed secondary-market sale.

Potential retrocession is a possible sub-allocation of distribution compensation. If no source supports the allocation, mark it `not separately estimable` rather than asserting a percentage or recipient.

Where a proxy decomposition is presented, show the controlling all-in proxy, component estimates, unexplained residual, and split-confidence level together. Components marked `Low` or `None` must not be silently included in a reconciled component total.

### Aggregation and Sensitivities

- Sum only compatible one-off estimates across ISINs with usable investment bases.
- Report recurring amounts as an annual run-rate.
- Report exit costs as a separate contingent scenario.
- Display modeled notional, excluded or ambiguous notional, modeled ISIN count, excluded ISIN count, and confidence by segment beside every aggregate result.
- Do not multiply current or reported position sizes across the 23-year strategy period, or model lifetime fees, without trade dates, balances, disposals, and turnover data.
- Test benchmark low/base/high cases, inclusion or exclusion of external advisory and custody charges, hold-to-maturity versus exit, and source-supported retrocession allocations.

If usable invested notional cannot be separated from shared or ambiguous line-item values, publish rate-based ISIN and cohort results plus a coverage table. Do not produce a portfolio dollar total from ambiguous bases. Where a source reports annualised reduction in yield, retain that measure unless the source provides the recommended holding period and a valid conversion method; do not compare or add it directly to a one-off percentage of notional.

## Deliverables

### Excel Workbook

The Tier 1 workbook will include these sheets:

1. `Read Me & Limitations`
2. `Portfolio Summary`
3. `ISIN Model`
4. `Benchmark Assumptions`
5. `Source Register`
6. `Coverage & Exceptions`

The portfolio summary will separately show one-off estimated total cost, annual recurring run-rate, contingent exit cost, potential retrocession range where estimable, coverage percentages, and sensitivity drivers.

### Methodology Note

Publish a concise methodology note covering the taxonomy, source standards, vintage matching, scenario construction, calculation rules, double-counting controls, and data limitations. It documents an indicative model and is not a Tier 2 audit report or legal memorandum.

### Executive Memo Update

Only after model validation, update the [Executive memo: Structured Products](executive-memo-structured-products-retrocession-review.md) so any headline ranges reconcile to the workbook and clearly describe **estimated potential compensation**, not money actually received.

## Quality Controls

1. **Source audit:** Every model input resolves to an evidence-register source with matching fee definition, unit, vintage, product segment, and page/table locator.
2. **Coverage audit:** All 29 ISINs map to one segment or a documented exception; modeled and excluded investment bases reconcile to portfolio source data.
3. **Formula audit:** Independently reproduce at least one rate-linked and one equity-linked calculation. Confirm low <= base <= high and correct percentage/basis-point and currency treatment.
4. **Double-count audit:** Confirm retrocession is nested within distribution compensation, all-in fair-value gaps are not stacked with their components, annual charges are not included in upfront totals, and exit costs occur only in exit scenarios.
5. **Sensitivity audit:** Confirm a visible assumption change updates ISIN and portfolio outputs consistently.
6. **Board-readout audit:** Every headline figure identifies timing, covered and excluded notional, scenario, confidence, and the label `Indicative estimate - not evidence of payment`.
7. **Memo reconciliation:** Validate that every range inserted into the executive memo equals the final workbook output and carries the same limitations.
8. **Comparability audit:** Reperform every adopted source score and confirm that observations below the adoption threshold remain comparators or sensitivities only.
9. **Negative-evidence audit:** Confirm every `unbenchmarked` bucket has a reproducible search record and is not silently represented as zero.
10. **Basis audit:** Confirm each dollar calculation uses only `usable invested notional`; shared line-item amounts, minimum denominations, and issue/outstanding sizes remain excluded.
11. **Proxy-decomposition audit:** Confirm every component is directly evidenced or explicitly assumed, component timing and definitions are compatible, the residual is visible, nested retrocession is not added twice, and the displayed split confidence follows section 3b.

## Decision Gates

| Gate | Pass condition | Failure treatment |
| --- | --- | --- |
| Portfolio mapping | All 29 ISINs assigned to a cohort or documented exception | Keep unmatched ISINs out of segment assumptions |
| Investment basis | Each position-size value classified and usable bases reconciled | Publish rates and coverage without an unsupported portfolio dollar total |
| Benchmark adoption | Every input meets source, locator, definition, and comparability rules | Retain as comparator/sensitivity or mark `unbenchmarked` |
| Distribution/retrocession | Component-level evidence identifies the payment definition and basis | Report `not separately estimable`; do not infer a share from all-in costs |
| Proxy decomposition | Components reconcile to the all-in proxy, overlap is controlled, the residual is explicit, and the split reaches at least `Medium` confidence | Retain the undecomposed proxy total and show component observations only as separate sensitivities |
| Double counting | All-in and component scenarios are mutually exclusive | Block workbook sign-off until corrected |
| Board output | Headline values state timing, coverage, confidence, and evidence limitation | Do not update the executive memo |

## Work Sequence

1. Freeze the cost definitions, units, overlap rules, and controlled `unbenchmarked` state.
2. Build the 29-ISIN cohort matrix and classify every reported investment basis.
3. Extract AC-01, AC-02, the ESMA 2023 annexes, and the ESMA historical study into the evidence register with exact locators and comparability scores.
4. Run the historical rate-linked and distribution-compensation workstreams first because they control the largest stated vintage cohort and the memo's central hypothesis, using the trusted-source expansion in section 3a (EDGAR vintage pricing supplements, LuxSE/Euronext Dublin archives, and the named academic and court sources) before declaring any renewed stop-rule result.
5. Run modern equity-linked, exit-cost, and account-service workstreams; record negative results under the stop rules.
6. Run the proxy-decomposition confidence workstream, reconcile candidate components to each applicable all-in proxy, and record component and overall split confidence.
7. Hold a benchmark adoption review and create decision records for each segment and cost bucket.
8. Build the workbook first with rates, evidence status, coverage, residuals, and split-confidence fields; enable dollar aggregation only for usable invested-notional rows.
9. Reperform one historical rate-linked and one modern equity-linked calculation and complete all quality-control gates.
10. Produce the methodology note and prioritisation list, distinguishing research gaps addressable in Tier 1 from documents requiring Tier 2 recovery.
11. Update the executive memo only if validated headline ranges reconcile to the workbook; otherwise replace unsupported claims with the evidenced comparator and limitation language.

## Repository Inputs and Outputs

| Location | Role in Tier 1 |
| --- | --- |
| `01. Structured Products/` | Read-only source for product classification, position size, vintage, and existing provenance. |
| `05. Canonical Data/` | Generated views used to cross-check portfolio completeness; do not manually amend. |
| `04. Product Review/` | Recommended location for the Tier 1 evidence register, methodology note, model inputs, and generated analytical outputs. |
| `90. Scripts/render_products.py` | May be reused to export canonical inputs; Tier 1 modeled values should remain outside product dossier frontmatter. |
