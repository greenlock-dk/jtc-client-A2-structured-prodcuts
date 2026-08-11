## 1. Executive Summary

### Decision summary

This current-scope review establishes a controlled starting population for cost analysis. The evidence supports ISIN-level classification, external cost comparators, and transparent sensitivity design. It does not yet support a portfolio-wide historical lifetime-cost total or a separately estimable retrocession amount.

> Indicative scenario estimate - not evidence that a fee or payment was made, received, disclosed, owed, or is recoverable.

The immediate decision is whether the Trust can provide the transaction records most likely to reduce the remaining uncertainty. The priority is Trust transaction evidence, not a further attempt to infer payments from product issue sizes or general market practice.

### Cost-estimation approaches

The report presents two separate, non-additive approaches:

- **Evidence-based:** Apply only an adopted benchmark with a compatible cost definition, unit, timing, and cohort. Where those conditions are not met, report the component as `unbenchmarked` or `not separately estimable`; do not fill the gap with zero.
- **Proxy-based:** Test the closest available secondary comparator under an explicit assumption. The proxy must state its product, vintage, jurisdiction, channel, timing, and cost-definition limitations, and is reported separately from the evidence-based result.

A proxy-based estimate is a sensitivity to a stated assumption, reported separately from the evidence-based result.

### Portfolio coverage at 11 August 2026

| Population | ISINs | Reported position basis | Treatment |
| --- | ---: | ---: | --- |
| Canonical portfolio inventory | 29 | n/a | Maintained in the lifecycle and exception register. |
| Usable invested-notional basis | 21 | USD 71.4 million | All remain in the ISIN-level analysis, regardless of issuer issue-size availability. |
| Currently cost-assessable rows | 19 | USD 70.2 million | Included in the current evidence-based and proxy-based scenario ranges. |
| Currently unbenchmarked rows | 2 | USD 1.0 million | Retained in analysis and coverage, but not assigned a zero cost. |
| Issuer issue-size unavailable | 3 | USD 12.4 million | Remain included because a usable Trust position is available. |
| Position-basis exclusions | 8 | n/a | 2 issuer/outstanding-size values and 6 missing values; excluded from Trust-exposure aggregation. |

The 21-ISIN, USD 71.4 million population includes `CH1484588913`, `XS0168875792`, and `XS0318585791` despite unavailable issuer issue-size evidence. `XS0168875792` and `XS0318585791` remain explicitly evidence-limited, while `XS0298465822` remains in the 29-ISIN coverage register without a dollar aggregation because its Trust position is missing. The two currently unbenchmarked usable-basis rows are `XS0765564827` and `XS0318585791`.

The reported positions are a controlled exposure basis, not evidence of acquisition date, acquisition price, balance through time, sale proceeds, or redemption proceeds. Consequently, they cannot yet support a lifetime aggregation from acquisition through disposal or maturity.

### Cost assessment by scenario

| Scenario | Cost-assessable ISINs | Included reported position basis | Minimum cost (USD) | Maximum cost (USD) | Basis |
| --- | ---: | ---: | ---: | ---: | --- |
| Evidence-based | 19 | USD 70.2 million | 2,900,000 | 3,500,000 | Applicable sourced comparators only, including the historical all-in issuance comparator and modern annualised comparator. |
| Proxy-based | 19 | USD 70.2 million | 3,100,000 | 3,700,000 | Evidence-based comparators plus the stated proxy comparator for the relevant equity-linked rows. |

All calculated monetary outcomes in this summary use `ROUND(X, -5)` and are shown to the nearest USD 100,000. This presentation convention does not alter reported Trust positions, issuer issue/outstanding values, or other source inputs collected from XLS and Bloomberg. The ranges are scenario outputs for non-overlapping cohorts, not a single historical lifetime-cost total. They exclude the two usable-basis `unbenchmarked` rows, account-level service costs, contingent exit costs, and potential retrocession. No issuer issue-size is used as a substitute for a Trust position or as a condition of inclusion.

### Evidence-led cost finding

The available research supports a disciplined separation of one-off product economics, recurring investment-service charges, contingent exit costs, and potential third-party compensation:

- A historical EU all-in issuance-premium comparator reports approximately `4.6%-5.5%` of notional. It is an all-in product-pricing measure and must not be decomposed into manufacturing, distribution, or retrocession components.
- Modern EU and Swiss observations provide annualised and product-specific comparators for distinct product families and regimes. They are secondary comparators or sensitivities, not evidence of costs on the Trust's historical positions.
- The dominant historical rate-linked cohort has no adopted vintage- and payoff-matched manufacturing or distribution benchmark. Its component costs remain `unbenchmarked`.
- No verified source identifies a rate, calculation base, payer, recipient, or payment record that would support a portfolio-wide retrocession amount. Potential retrocession is therefore `not separately estimable`.
- No adopted, comparable benchmarks currently support a historical advisory, custody, brokerage, bid/ask, or unwind-cost total for the portfolio. These components remain separately switchable and unbenchmarked rather than assumed to be zero.

The resulting current-scope output should show evidence-based and proxy-based scenarios separately, with source-labelled rates only where the cost definition, timing, cohort, and investment basis are compatible. It should not present an aggregate dollar amount as actual historical lifetime cost, and it should not stack an all-in comparator with its possible components.

### Main limitations

The principal limitations are not portfolio completeness but transaction and product-evidence completeness:

1. Trust acquisition dates, prices, holdings through time, sale dates, sale proceeds, and redemption proceeds have not been reconciled. These are required to convert annual or contingent rates into a lifetime cost.
2. The dominant 2003-2007 historical rate-linked population lacks an adopted, comparable component-cost benchmark despite targeted research. Existing modern, equity-linked, US, and all-in observations must remain labelled comparators or sensitivities.
3. Three ISINs remain explicit exclusions from a structured-product conclusion. They must remain visible in coverage reporting and must not be coded as zero-cost or ordinary unbenchmarked rows.
4. The data-integrity audit remains a fail for payoff/risk evidence and visual reinspection completeness. Deterministic canonical views and complete artifact pairing do not substitute for final terms or Trust transaction records.

### Recommended decisions and next actions

1. Authorise recovery of Trust acquisition, custody, balance, disposal, call, maturity, and redemption records for the largest position-basis ISINs, beginning with the 19-ISIN, USD 70.2 million cost-assessable population.
2. Recover final terms and pricing supplements for the historical rate-linked cohort before adopting any component-level issuance or distribution assumption.
3. Seek product- and account-level documents that identify the payer, recipient, calculation basis, amount, timing, and disclosure treatment of any third-party compensation. Until then, report retrocession as `not separately estimable`.
4. Maintain evidence-only, proxy-base, and wide-sensitivity views as separate, non-additive results. Require each applied rate to cite its specific source-register ID and comparability rationale.
5. Reassess the three explicit structure exclusions only if primary issuer, exchange, Bloomberg, or Trust evidence is recovered.

### Basis and references

This summary is based on the current [report structure](../tier-1-final-report-structure.md), [cost-benchmark research register](../cost-benchmark-research.md), [position-size control](../../04.%20Product%20Review/POSITION%20SIZE%20CONTROL.md), and [data-integrity audit](../../04.%20Product%20Review/DATA%20INTEGRITY%20AUDIT.md), all as at 11 August 2026.
