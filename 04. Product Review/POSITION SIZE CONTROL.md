# Position Size Control

Audit date: 2026-08-11

This register separates the reported Trust position from issuer-level issue/outstanding size. `position_size` is not changed by this control. Issue/outstanding values remain documentary context only and must not be used as a fallback for Trust exposure. A user-reported value is not treated as usable invested notional where the source evidence identifies the same amount as issuer-level issue/outstanding size.

## Classification rules

| Status | Treatment in portfolio aggregation |
| --- | --- |
| `usable invested notional` | May be aggregated, subject to the source and date limitations recorded in the dossier. |
| `shared across line items` | Exclude until the line-item scope and aggregation basis are reconciled to Trust records. |
| `minimum denomination` | Exclude; this is a trading/unit constraint, not a holding amount. |
| `issue/outstanding size` | Exclude from Trust exposure calculations. |
| `missing` | Exclude; do not substitute issue/outstanding size. |
| `unclear` | Exclude until Trust-specific evidence resolves the basis. |

## ISIN classifications

| ISIN | Reported position value | Position-size status | Scope / interpretation | Issue/outstanding comparison | Required action |
| --- | --- | --- | --- | --- | --- |
| CH1484588913 | USD 10,000,000 | `usable invested notional` | User-confirmed reported Trust position | Not available | Retain user confirmation with model output |
| XS3234638248 | USD 2,000,000 | `usable invested notional` | Trust position explicitly distinguished from documentary nominal amount | USD 2.4 million | Retain as the model example; preserve documentary source |
| XS0765564827 | USD 200,000 | `usable invested notional` | User-confirmed reported Trust position | USD 750 million | Retain user confirmation with model output |
| XS1028242706 | USD 850,000,000 | `issue/outstanding size` | Bloomberg image explicitly labels USD 850.00 million as `Amt Issued/Outstanding`; no separate Trust-specific holding evidence | USD 850 million | Exclude from Trust exposure; recover a Trust holding record before using as position |
| XS1243914071 | USD 1,525,000,000 | `issue/outstanding size` | Bloomberg image explicitly labels USD 1,525.00 million as `Amt Issued/Outstanding`; no separate Trust-specific holding evidence | USD 1,525 million | Exclude from Trust exposure; recover a Trust holding record before using as position |
| CH0252328973 | Missing | `missing` | No reported position amount | Not found | Recover Trust-specific position evidence |
| XS0297701319 | USD 800,000 | `usable invested notional` | User-confirmed reported Trust position | USD 3,000 million | Retain user confirmation with model output |
| XS0318585791 | USD 800,000 | `usable invested notional` | User-confirmed reported Trust position | Not available | Retain user confirmation with model output |
| XS0300388351 | USD 600,000 | `usable invested notional` | User-confirmed reported Trust position | USD 8,370 million | Retain user confirmation with model output |
| XS0164480286 | USD 5,900,000 | `usable invested notional` | User-confirmed reported Trust position | USD 19,550 million | Retain user confirmation with model output |
| XS0165220400 | USD 5,000,000 | `usable invested notional` | User-confirmed reported Trust position | USD 5,000 million | Retain user confirmation with model output |
| XS0168875792 | USD 1,600,000 | `usable invested notional` | User-confirmed reported Trust position | Not available | Retain user confirmation with model output |
| XS0169318291 | USD 9,650,000 | `usable invested notional` | User-confirmed reported Trust position | USD 24,070 million | Retain user confirmation with model output |
| XS0170303290 | USD 6,250,000 | `usable invested notional` | User-confirmed reported Trust position | USD 18,000 million | Retain user confirmation with model output |
| XS0171914038 | USD 10,700,000 | `usable invested notional` | User-confirmed reported Trust position | USD 30,850 million | Retain user confirmation with model output |
| XS0172077769 | USD 1,400,000 | `usable invested notional` | User-confirmed reported Trust position | USD 6,200 million | Retain user confirmation with model output |
| XS0241444883 | USD 1,380,000 | `usable invested notional` | User-confirmed reported Trust position | USD 5,000 million | Retain user confirmation with model output |
| XS0249805960 | USD 5,600,000 | `usable invested notional` | User-confirmed reported Trust position | USD 17,200 million | Retain user confirmation with model output |
| XS0277502067 | USD 1,000,000 | `usable invested notional` | User-confirmed reported Trust position | USD 5,000 million | Retain user confirmation with model output |
| XS0278550750 | USD 1,000,000 | `usable invested notional` | User-confirmed reported Trust position | USD 10,000 million | Retain user confirmation with model output |
| XS0284203071 | USD 3,190,000 | `usable invested notional` | User-confirmed reported Trust position | USD 10,000 million | Retain user confirmation with model output |
| XS0294314694 | USD 2,200,000 | `usable invested notional` | User-confirmed reported Trust position | USD 10,000 million | Retain user confirmation with model output |
| XS0293931688 | USD 500,000 | `usable invested notional` | User-confirmed reported Trust position | USD 3,000 million | Retain user confirmation with model output |
| XS0293919121 | USD 1,450,000 | `usable invested notional` | User-confirmed reported Trust position | USD 2,000 million | Retain user confirmation with model output |
| XS0297467705 | Missing | `missing` | No reported position amount | USD 5,000 million | Recover Trust-specific position evidence |
| XS0298465822 | Missing | `missing` | No reported position amount | Not available | Recover Trust-specific position evidence |
| XS0304286924 | Missing | `missing` | No reported position amount | USD 10,520 million | Recover Trust-specific position evidence |
| XS0314283432 | Missing | `missing` | No reported position amount | USD 43,400 million | Recover Trust-specific position evidence |
| XS0315745447 | Missing | `missing` | No reported position amount | EUR 6,050 million | Recover Trust-specific position evidence |

## Aggregation rule

Only rows classified as `usable invested notional` may enter a portfolio-dollar aggregation. `unclear`, `shared across line items`, `minimum denomination`, `issue/outstanding size`, and `missing` rows must be excluded or shown separately as coverage gaps. The issue/outstanding field must never populate a missing position field.
