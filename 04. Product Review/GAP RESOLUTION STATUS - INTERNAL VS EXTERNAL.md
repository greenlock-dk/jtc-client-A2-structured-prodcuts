# Audit Gap Resolution Status - Internal vs. External Actions

**Date:** 2026-08-11 (post-verification)  
**Historical summary (superseded by the 2026-08-14 status below):** Of the original 5 critical audit gaps, 2 were internally resolved, 1 was pre-resolved, and 2 required external source recovery.

## 2026-08-14 current status

The 2026-08-11 summary is superseded where it refers to image inspection and position classification. All 71 mapped Bloomberg images were visually reviewed against their paired OCR files on 2026-08-13. The 23 numeric mapped issue-size values are confirmed by their cited source images, CH0252328973 is confirmed `not found`, and CH1484588913 and XS3234638248 now have documentary nominal amounts. The three no-source products remain unavailable without documentary recovery.

Position handling is now a controlled coverage limitation rather than an uncontrolled aggregation risk. [POSITION SIZE CONTROL.md](POSITION%20SIZE%20CONTROL.md) classifies 21 records as `usable invested notional`, 2 as issuer `issue/outstanding size`, and 6 as `missing`. The cost model permits only the 21 usable values in exposure-based calculations; the other 8 records are explicitly returned as `Not calculated` and excluded from totals.

The remaining external-evidence findings are: incomplete payoff/risk terms for the mapped structured products, plus source recovery for the formally excluded records XS0168875792, XS0298465822, and XS0318585791. Neither is resolved by a position proxy or OCR inference.

---

## Status Summary

| Gap | Issue | Resolvable? | Status | Action |
| --- | --- | --- | --- | --- |
| **G-002** | Mapped Bloomberg image/OCR visual review | ✓ YES | **RESOLVED** | All 71 mapped images visually checked against paired OCR; rerun after future evidence changes |
| **G-005** | CH1484588913 issuer/guarantor, currency, and issue size incomplete | ✓ YES | **RESOLVED** | Extracted issuer, guarantor, USD settlement currency, USD 10,000,000 issue size, and documented redemption terms from the inspected term sheet; views rerendered |
| **G-006** | XS0298465822 (unspecified) has zero evidence | ✓ YES | **FORMALIZED** | Added explicit "Disposition Status" section; marked as `not recovered`; review excluded |
| **G-010** | XS0168875792, XS0318585791 zero evidence (2 products) | ✓ YES | **FORMALIZED** | Added explicit "Disposition Status" sections to both; marked as `not recovered`; reviews excluded |
| **G-004** | 23 mapped products retain payoff/risk/redemption gaps | ✗ NO | **PENDING** | Requires external term sheets, prospectuses, or issuer/Bloomberg detailed product terms |
| **G-009** | Trust position basis is limited | PARTIAL | **CONTROLLED LIMITATION** | 21 user-confirmed usable amounts are modeled; 2 issuer-size rows and 6 missing rows are excluded. Trust custody or balance-sheet evidence is still required before expanding aggregation |

---

## Internally resolved or formalized items

### ✓ G-005: CH1484588913 Issuer/Guarantor Extraction

**What was done:**
- Populated `issuer: Leonteq Securities AG` (from term sheet pages 1-2)
- Added `guarantor: PostFinance Ltd` (from term sheet pages 1-2)
- Updated `currency: USD` settlement currency (from term sheet pages 1-2)
- Populated documentary issue size: USD 10,000,000 (term sheet page 1)
- Populated autocall/barrier redemption, downside, and issuer-credit-risk terms (term sheet pages 1-3)
- Updated `field_statuses` to reflect `confirmed` sourcing with exact PDF citations
- Updated evidence table with term sheet references
- Rerendered canonical views (deterministic output confirmed)

**Files modified:**
- [01. Structured Products/CH1484588913 - Leonteq Express Certificate.md](01.%20Structured%20Products/CH1484588913%20-%20Leonteq%20Express%20Certificate.md)

**Result:** CH1484588913 moves from "gap" to "clear with source limitation". Issuer identity, USD settlement currency, issue size, and key redemption/risk terms are now confirmed from the inspected term sheet; no Bloomberg image/OCR evidence is available.

**Impact on repository:** ✓ 1 fewer gap; generated canonical views updated; rendering deterministic

---

### ✓ G-006: XS0298465822 Disposition Formalized

**What was done:**
- Added explicit "Disposition Status" section to dossier markdown
- Declared: `EXPLICIT EXCLUSION` with disposition `not recovered`
- Documented all unavailable material fields
- Stated review conclusions explicitly excluded pending source recovery
- Provided clear recovery action guidance

**Files modified:**
- [01. Structured Products/XS0298465822 - Unspecified Instrument.md](01.%20Structured%20Products/XS0298465822%20-%20Unspecified%20Instrument.md)

**Current state:**
- All material fields marked `not found`
- No images/OCR evidence recovered
- No term sheet or prospectus located
- Record retained for population completeness

**Result:** G-006 disposition is now formal and explicit. The record is clearly marked as excluded pending evidence recovery.

**Impact on repository:** ✓ Explicit exclusion formalized; no ambiguity about conclusion status

---

### ✓ G-010: XS0168875792 and XS0318585791 Dispositions Formalized

**What was done:**
- Added explicit "Disposition Status" sections to both dossier markdowns
- Declared each: `EXPLICIT EXCLUSION` with disposition `not recovered`
- Documented unavailable material fields for each product
- Stated review conclusions explicitly excluded pending source recovery
- Provided product-specific recovery action guidance

**Files modified:**
- [01. Structured Products/XS0168875792 - Libor Callable Note.md](01.%20Structured%20Products/XS0168875792%20-%20Libor%20Callable%20Note.md)
- [01. Structured Products/XS0318585791 - Kick In Note.md](01.%20Structured%20Products/XS0318585791%20-%20Kick%20In%20Note.md)

**Current state:**
- Both products: zero images/OCR evidence
- No original term sheets or prospectuses located
- All critical fields marked `not found`
- Both records retained for population completeness

**Result:** G-010 disposition is now formal and explicit. Both records are clearly marked as excluded pending evidence recovery.

**Impact on repository:** ✓ Explicit exclusions formalized for both products; no ambiguity about conclusion status

---

## Remaining external dependency and controlled limitation

### ✗ G-004: 23 Mapped Products — Payoff/Risk/Redemption Extraction

**What's needed:**
- Original executed term sheets or prospectuses
- Bloomberg Terminal detailed worksheets (not images/screenshots)
- Structured product research databases or issuer documentation

**Why this is NOT resolvable internally:**
- The 24 mapped Bloomberg images are worksheet excerpts only (data tables), not legal term documents
- OCR text from worksheet images is worksheets (prices, amounts) — not contract language
- Audit rule: "Do not treat OCR alone as confirmation"
- Audit rule: "Do not promote unsupported payoff inference"
- No local repository contains contract language, payoff definitions, barrier mechanics, or trigger documentation

**Affected products (23):**
- Mapped historical callable, range, CMS, dual-index, fixed-rate, and related notes with at least one remaining unconfirmed payoff, risk, or redemption field
- **Remaining gaps:** `downside`, `risk`, `redemption_terms`, and in some records `underlying` or `barrier` (legal payoff definitions, principal protection, ranking, coupon linkage)

**What you need to provide:**
1. Original term sheets or prospectuses for the 23 affected products (external recovery)
2. OR: Confirmation that these sources do not exist/are unretrievable (formal non-recovery)

**Action required:** 
- Obtain term sheets from Bloomberg Terminal, issuer websites, or structured product archives
- Extract payoff, barrier, call, downside, ranking, risk, and redemption mechanics
- Populate canonical `redemption_terms`, `downside`, `risk`, and `underlying` fields with field-status citations
- Rerender canonical views

**Criticality:** **HIGH** — blocks PASS status and payoff/risk accuracy for 23 products (79% of portfolio)

---

### ⚠ G-009: Trust Position Basis — Controlled Limitation

**What's needed:**
- Trust custody statements or position confirmations
- Balance-sheet evidence or ledger entries
- Trust investment documentation or allocation basis
- Reconciliation between workbook position and actual Trust holdings

**Why full documentary resolution still requires external evidence:**
- The repository contains workbook-reported position amounts, not Trust-verified basis
- 21 products are classified as `usable invested notional`
- 2 products are classified as issuer `issue/outstanding size` and 6 are `missing`
- The cost model calculates only the 21 usable values and returns `Not calculated` for the 8 excluded rows
- No local Trust documentation exists to verify basis or reconcile

**Affected products:** 8 of 29 are excluded from aggregation pending Trust-specific evidence

**Current classification:**
- 21: `usable invested notional`
- 2: `issue/outstanding size` (issuer amount, not Trust exposure)
- 6: `missing` (no reported Trust position amount)

**What you need to provide:**
1. Trust custody statements showing actual position holdings and basis
2. Investment committee or allocation documents showing how positions are classified
3. Balance-sheet reconciliation showing relationship between workbook amounts and actual holdings
4. Confirmation whether shared-line-item amounts should be included/excluded from portfolio analysis

**Action required:**
- Retain the current 8-row exclusion rule in the cost model
- Obtain Trust position documentation before reclassifying any excluded row
- Update field statuses with custody or balance-sheet citations if evidence is recovered
- Rerender canonical views after any frontmatter update

**Criticality:** **HIGH** — blocks portfolio-aggregation decisions affecting cost model and portfolio concentration analysis

---

## Summary of Internal Changes

**Files modified:** 6 dossiers
- CH1484588913: Issuer/guarantor, USD settlement currency, issue size, and documented payoff terms extracted and populated
- CH0252328973: Bullet/single-repayment term promoted from the workbook structure
- XS0765564827: Documentary early-redemption and lifecycle terms promoted from original terms
- XS0298465822: Disposition section added (explicit exclusion)
- XS0168875792: Disposition section added (explicit exclusion)
- XS0318585791: Disposition section added (explicit exclusion)

**Canonical views:** Rerendered (deterministic, all 29 records present)

**Render status:** ✓ Both summary and detailed views render successfully

**Remaining unresolved gaps:** 2 (G-004, G-009) — external source recovery required

---

## Next Steps for You

### Priority 1: G-004 (23 products)
Locate and provide original term sheets or prospectuses for the 23 mapped products with remaining payoff, risk, or redemption gaps. This is the largest data completeness gap affecting payoff accuracy.

### Priority 2: G-009 (8 excluded products)
Provide Trust position basis documentation. This is required before portfolio-aggregation or cost-model decisions can be made reliably.

### Priority 3: Monitor G-006, G-010
These are now formally excluded from conclusions. If you later locate sources for XS0298465822, XS0168875792, or XS0318585791, the dossiers can be updated and re-rendered.

---

## Verification

All internally resolved changes have been tested:
- ✓ CH1484588913 issuer now shows in generated views
- ✓ Canonical views render deterministically
- ✓ All 29 products present in summary and detailed views
- ✓ Disposition sections formalize exclusion status for G-006, G-010
- ✓ No new contradictions introduced

**Ready for your review and external source recovery actions.**
