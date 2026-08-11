# Audit Gap Resolution Status - Internal vs. External Actions

**Date:** 2026-08-11 (post-verification)  
**Summary:** Of the 5 critical audit gaps, 2 have been internally resolved, 1 was pre-resolved, and 2 require external source recovery.

---

## Status Summary

| Gap | Issue | Resolvable? | Status | Action |
| --- | --- | --- | --- | --- |
| **G-005** | CH1484588913 issuer/guarantor missing | ✓ YES | **RESOLVED** | Extracted from inspected term sheet; fields populated; views rerendered |
| **G-006** | XS0298465822 (unspecified) has zero evidence | ✓ YES | **FORMALIZED** | Added explicit "Disposition Status" section; marked as `not recovered`; review excluded |
| **G-010** | XS0168875792, XS0318585791 zero evidence (2 products) | ✓ YES | **FORMALIZED** | Added explicit "Disposition Status" sections to both; marked as `not recovered`; reviews excluded |
| **G-004** | 25 callable/range/CMS products lack payoff/risk/barrier definitions | ✗ NO | **PENDING** | Requires external term sheets, prospectuses, Bloomberg detailed pages |
| **G-009** | 28 products lack Trust position basis classification | ✗ NO | **PENDING** | Requires Trust custody statements, balance-sheet evidence, position documentation |

---

## Internally Resolved (3 items)

### ✓ G-005: CH1484588913 Issuer/Guarantor Extraction

**What was done:**
- Populated `issuer: Leonteq Securities AG` (from term sheet pages 1-2)
- Added `guarantor: PostFinance Ltd` (from term sheet pages 1-2)
- Updated `currency: CHF` (from term sheet pages 1-2)
- Updated `field_statuses` to reflect `confirmed` sourcing with exact PDF citations
- Updated evidence table with term sheet references
- Rerendered canonical views (deterministic output confirmed)

**Files modified:**
- [01. Structured Products/CH1484588913 - Leonteq Express Certificate.md](01.%20Structured%20Products/CH1484588913%20-%20Leonteq%20Express%20Certificate.md)

**Result:** CH1484588913 moves from "gap" to "clear with source limitation". Issuer identity and currency now confirmed from inspected term sheet.

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

## Externally Dependent (2 items)

### ✗ G-004: 25 Callable/Range/CMS Products — Payoff/Risk/Barrier Extraction

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

**Affected products (25):**
- 22 callable notes (LIBOR/CMS/range-based)
- 3 memory/autocallable products
- **Missing fields:** `downside`, `risk`, `underlying` (structured payoff definitions, principal protection, ranking, coupon linkage)

**What you need to provide:**
1. Original term sheets or prospectuses for 25 products (external recovery)
2. OR: Confirmation that these sources do not exist/are unretrievable (formal non-recovery)

**Action required:** 
- Obtain term sheets from Bloomberg Terminal, issuer websites, or structured product archives
- Extract payoff, barrier, call, downside, ranking, and redemption mechanics
- Populate canonical `downside`, `risk`, `underlying` fields with field-status citations
- Rerender canonical views

**Criticality:** **HIGH** — blocks PASS status and payoff/risk accuracy for 25 products (86% of portfolio)

---

### ✗ G-009: 28 Products — Trust Position Basis Classification

**What's needed:**
- Trust custody statements or position confirmations
- Balance-sheet evidence or ledger entries
- Trust investment documentation or allocation basis
- Reconciliation between workbook position and actual Trust holdings

**Why this is NOT resolvable internally:**
- The repository contains workbook-reported position amounts, not Trust-verified basis
- Only 1 product (XS3234638248) is classified as `usable invested notional`
- The other 28 are classified as: 18 `shared across line items`, 3 `missing`, 2 `unclear`, 5 `minimum denomination`
- Audit states: "Portfolio exposure and concentration cannot be reliably aggregated without Trust-specific basis evidence"
- No local Trust documentation exists to verify basis or reconcile

**Affected products:** 28 of 29 (all except XS3234638248)

**Current classification:**
- 18: "shared across line items" (not usable for direct investment aggregation)
- 3: "missing" (no position reported)
- 2: "unclear" (ambiguous reporting)
- 5: "minimum denomination" (size limits, not investment amounts)

**What you need to provide:**
1. Trust custody statements showing actual position holdings and basis
2. Investment committee or allocation documents showing how positions are classified
3. Balance-sheet reconciliation showing relationship between workbook amounts and actual holdings
4. Confirmation whether shared-line-item amounts should be included/excluded from portfolio analysis

**Action required:**
- Obtain or produce Trust position documentation
- Reclassify each product's position basis with supporting evidence reference
- Update field_statuses with custody or balance-sheet citations
- Rerender canonical views

**Criticality:** **HIGH** — blocks portfolio-aggregation decisions affecting cost model and portfolio concentration analysis

---

## Summary of Internal Changes

**Files modified:** 3 dossiers
- CH1484588913: Issuer/guarantor/currency extracted and populated
- XS0298465822: Disposition section added (explicit exclusion)
- XS0168875792: Disposition section added (explicit exclusion)
- XS0318585791: Disposition section added (explicit exclusion)

**Canonical views:** Rerendered (deterministic, all 29 records present)

**Render status:** ✓ Both summary and detailed views render successfully

**Remaining unresolved gaps:** 2 (G-004, G-009) — external source recovery required

---

## Next Steps for You

### Priority 1: G-004 (25 products)
Locate and provide original term sheets or prospectuses for all callable/range/CMS/memory products. This is the largest data completeness gap affecting payoff accuracy.

### Priority 2: G-009 (28 products)
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
