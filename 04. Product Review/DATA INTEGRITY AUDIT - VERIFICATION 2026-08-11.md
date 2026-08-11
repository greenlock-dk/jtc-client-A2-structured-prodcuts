# Structured Products Data Integrity Audit - Verification & Re-Performance

**Audit date:** 2026-08-11 (verification/re-performance of prior audit from same date)  
**Scope:** Complete repository, current working tree  
**Verification status:** Prior audit FAIL remains confirmed; no improvement; all critical gaps persist

---

## Executive Summary

This verification audit confirms that the prior comprehensive audit conducted on 2026-08-11 accurately assessed the repository state. All population, artifact, and rendering findings remain **valid and unchanged**. The repository continues to have **FAIL** status due to persisting high-criticality gaps in:

1. **Payoff/risk field extraction** (G-004) — most callable/range/CMS products lack structured downside/risk/underlying definitions
2. **Missing source identity** (G-005) — CH1484588913 issuer/guarantor discovered in term sheet but not yet populated  
3. **Unspecified instrument** (G-006) — XS0298465822 has no source evidence; cannot support structured conclusion
4. **Source limitation** (G-010) — XS0168875792 and XS0318585791 have zero primary evidence; marked excluded

**No corrective actions from the prior audit's recommendations have been implemented.** The population, artifact ledger, rendering output, and violation statuses are identical to the prior audit.

---

## 1. Executive Result - Verification Outcomes

| Metric | Count | Expected/baseline | Status | Notes |
| --- | ---: | ---: | --- | --- |
| Canonical products | 29 | 29 | ✓ PASS | All 29 dossiers present with valid YAML frontmatter |
| Individual product files | 29 | 29 | ✓ PASS | Unique ISINs: 29; Unique display_orders: 29 |
| Rendered summary rows | 29 | 29 | ✓ PASS | `05. Canonical Data/ISIN_summary.md` hash: `33aab013ad5a63df1b90f0e334d844b8` (deterministic across 2 renders) |
| Rendered detailed rows | 29 | 29 | ✓ PASS | `05. Canonical Data/ISIN_detailed.md` hash: `5efad3aad0992dd9adc73817fd699fd2` (deterministic across 2 renders) |
| Mapped images | 71 | 71 | ✓ PASS | 24 ISIN directories; all files paired; inventories consistent |
| Mapped OCR files | 71 | 71 | ✓ PASS | 24 ISIN directories; all files paired; inventories consistent |
| Image/OCR pairs | 71 | 71 | ✓ PASS | No orphan files; all 71 paired by ISIN directory |
| Original-term PDFs | 4 | 4 | ✓ PASS | CH1484588913, XS0765564827 (2), XS3234638248 |
| ISINs with image/OCR | 24 | 24 | ✓ PASS | 5 ISINs with zero image/OCR as baseline |
| ISINs with no evidence | 5 | 5 | ✓ PASS | CH1484588913, XS0168875792, XS0298465822, XS0318585791, XS3234638248 |
| Issue-size: confirmed | 24 | 24 mapped | ✓ PASS | 23 numeric values; 1 (CH0252328973) marked `not found` |
| Issue-size: unavailable | 4 | 4 unmapped | ✓ PASS | XS0168875792, XS0298465822, XS0318585791, XS1484588913 |
| Unresolved contradictions | 0 | 0 high unresolved | ✓ PASS | Prior contradictions resolved at source level (C-001, C-002) |
| Provenance/completeness gaps | 5 | 0 claimed | ✗ FAIL | G-004, G-005, G-006, G-009, G-010 remain unresolved |

**Result: FAIL** — Population is consistent and artifacts are accounted for, but material structured fields remain unavailable or unextracted, preventing a complete or reliable consolidated product conclusion.

---

## 2. Population Verification

All baseline counts confirmed:

| Layer | Expected | Found | Disposition | Evidence |
| --- | ---: | ---: | --- | --- |
| Workbook ISIN population | 29 | 29 sheets | 29 mapped to canonical dossiers | `Trust ISIN information from Bloomberg.xlsx` |
| Canonical dossiers | 29 | 29 files | 29 used and traced | `01. Structured Products/`; all 29 parse without YAML errors |
| Generated views | 2 | 2 files | 2 deterministic projections | `05. Canonical Data/ISIN_summary.md`, `ISIN_detailed.md` |
| Bloomberg images | 71 | 71 PNG | 71 used and traced | `02. BBG images/`; 24 ISIN directories; no duplicates |
| Bloomberg OCR | 71 | 71 TXT | 71 used and traced | `03. BBG OCR/`; 24 ISIN directories; all paired |
| Original terms | 4 | 4 PDF | 3 used (CH1484588913, XS0765564827, XS3234638248); 1 (Aquarius) as supplemental evidence | `04. Original terms/` |
| Review inventory | 29 | 29 rows | 29 mapped to canonical ISINs | `04. Product Review/REVIEW INVENTORY.md` |

**Artifact ledger complete:** All 206 accounted-for artifacts (29 dossiers + 71 images + 71 OCR + 4 PDFs + 29 review rows + 2 generated views) are dispositioned as `used and traced` with reproducible evidence.

---

## 3. Per-ISIN Verification Summary

All 29 records field-counted and cross-referenced with image/OCR/term availability:

### ISINs with image/OCR evidence (24)

| ISIN | Record | Images | OCR | Material fields | Issue-size | Result |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| CH0252328973 | 6 | 3 | 3 | 22 | not found | gap (no issuer/currency) |
| XS0164480286 | 10 | 2 | 2 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0165220400 | 11 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0169318291 | 13 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0170303290 | 14 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0171914038 | 15 | 6 | 6 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0172077769 | 16 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0241444883 | 17 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0249805960 | 18 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0277502067 | 19 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0278550750 | 20 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0284203071 | 21 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0293919121 | 24 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0293931688 | 23 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0294314694 | 22 | 4 | 4 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0297467705 | 25 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0297701319 | 7 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0300388351 | 9 | 5 | 5 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0304286924 | 27 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0314283432 | 28 | 3 | 3 | 22 | confirmed | gap (payoff/risk unavailable) |
| XS0315745447 | 29 | 1 | 1 | 22 | confirmed | clear (no unmapped structure gaps detected) |
| XS0765564827 | 3 | 3 | 3 | 22 | confirmed | gap (no term sheet payoff definition) |
| XS1028242706 | 4 | 1 | 1 | 22 | confirmed | clear (no unmapped structure gaps detected) |
| XS1243914071 | 5 | 1 | 1 | 22 | confirmed | clear (no unmapped structure gaps detected) |

### ISINs without image/OCR evidence (5)

| ISIN | Record | Images | OCR | Original terms | Material fields | Result |
| --- | ---: | ---: | ---: | --- | ---: | --- |
| CH1484588913 | 1 | 0 | 0 | 1 PDF | 20 | clear with source limitation (term sheet exists but issuer/guarantor not yet extracted) |
| XS0168875792 | 8 | 0 | 0 | none | 16 | gap (zero primary evidence; explicitly excluded from conclusion) |
| XS0298465822 | 26 | 0 | 0 | none | 7 | gap (unspecified instrument; zero evidence) |
| XS0318585791 | 12 | 0 | 0 | none | 13 | gap (zero primary evidence; explicitly excluded from conclusion) |
| XS3234638248 | 2 | 0 | 0 | 1 PDF | 25 | clear with source limitation (documentary issue-size confirmed; position vs. issuance distinguished) |

**Per-ISIN result:** All 29 records accounted for. 5 products have "clear" or "clear with source limitation" status; 24 have "gap" status. Gaps are primarily **missing structured payoff/risk/downside/ranking definitions** (G-004) and **missing document-recovered structural terms** (G-005, G-006, G-010).

---

## 4. Contradiction Register - Verification

The prior audit identified two contradictions, both resolved at source level. Both remain reproducible:

| ID | ISIN | Field | Type | Source A | Source B | Status | Reproducibility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C-001 | CH0252328973 | issue_size | format-only | Canonical `display: Not found` | 02. BBG images/CH0252328973/CH0252328973 - image-01.png visual review | Resolved | ✓ Reproducible: image opened; no issuance data label present |
| C-002 | CH1484588913 | issuer / guarantor | identity conflict | Canonical `issuer: ''` | 04. Original terms/01. Leonteq/CH1484588913_Leonteq_Termsheet.pdf, pages 1-2 | Resolved at source level; canonical field unpopulated | ✓ Reproducible: term sheet inspected; page 1 shows `Leonteq Securities AG` (issuer) and `PostFinance Ltd` (guarantor) |

**Verification result:** No new contradictions detected. No workbook/OCR disagreements detected. Both prior resolutions remain valid and reproducible with exact evidence citations.

---

## 5. Missing, Unused, and Unsupported Data - Verification

The five high-priority gaps identified in the prior audit remain unresolved:

| ID | ISIN / scope | Field or artifact | State | Issue | Criticality | Status |
| --- | --- | --- | --- | --- | --- | --- |
| **G-004** | 25 products (callable/range/CMS/dual-index/memory/autocallable) | `downside`, `risk`, `underlying` (structured fields) | explicitly limited | Structured payoff/barrier/trigger/call mechanics remain unavailable in 25 products. No unsupported inference has been promoted, but review conclusions remain limited. | **HIGH** | **UNRESOLVED** — G-004 is the primary blocker for PASS status |
| **G-005** | CH1484588913 | `issuer`, `guarantor` | not extracted | Leonteq term sheet pages 1-2 supply `Leonteq Securities AG` (issuer) and `PostFinance Ltd` (guarantor), but dossier fields remain blank. Blocking: population to canonical and rerender. | **MID** | **UNRESOLVED** — Requires dossier update and view rerender |
| **G-006** | XS0298465822 | identity and structure | explicitly limited | No image/OCR or original terms recovered; all material fields marked `not found`. Product retained for inventory completeness but cannot support economic/risk conclusion. | **HIGH** | **UNRESOLVED** — Requires source recovery before reopening |
| **G-009** | 28 of 29 products | Trust position basis | explicitly limited | Only XS3234638248 classified as `usable invested notional`; 18 are shared-line-item, 3 missing, 2 unclear, 5 minimum-denomination. Portfolio exposure aggregation blocked without Trust evidence. | **HIGH** | **UNRESOLVED** — Excluded from aggregation until basis evidence recovered |
| **G-010** | XS0168875792, XS0318585791 | primary evidence and structure | explicitly limited | Both products have zero mapped images/OCR/original terms; all material identity/payoff fields marked `not found`. Explicitly excluded from structured conclusions. | **HIGH** | **UNRESOLVED** — Requires evidence recovery |

**Verification result:** All five high-criticality gaps from prior audit remain active and unresolved. No material field extraction or source recovery has occurred. **These gaps prevent PASS status.**

---

## 6. Prior Resolutions Re-Performance

Three prior visual confirmations (issue-size) remain reproducible with exact evidence citations:

| ISIN | Field | Original disagreement | Evidence re-inspected | Result |
| --- | --- | --- | --- | --- |
| CH0252328973 | issue_size | OCR provided no numeric value | 02. BBG images/CH0252328973/CH0252328973 - image-01.png (visual inspection) | ✓ Reproducible: No "Amt Issued/Outstanding" numeric value present; marked `not found` |
| XS0300388351 | issue_size | OCR candidate: USD 8,370.00 million | 02. BBG images/XS0300388351/XS0300388351 - image-01.png (visual inspection) | ✓ Reproducible: Confirmed USD 8,370.00 million; marked `confirmed` |
| XS0765564827 | issue_size | OCR candidate: USD 750,000.00 million | 02. BBG images/XS0765564827/XS0765564827 - image-02.png (visual inspection) | ✓ Reproducible: Confirmed USD 750,000.00 million; marked `confirmed` |

**Verification result:** All three prior issue-size resolutions remain reproducible. Exact image citations are preserved in canonical dossier `issue_size.source` fields.

---

## 7. Inspection Limitations

**Current-state limitations:**

- The 68 Bloomberg images not explicitly re-opened in this verification remain unchecked for OCR quality or misalignment, but image-to-OCR pairing is consistent and verified.
- The four original-term PDFs were inspected in the prior audit; no new originals have been discovered or recovered for the five ISINs with source limitations.
- The term-sheet instructions for CH1484588913 (G-005) and the unspecified instrument status for XS0298465822 (G-006) have not been advanced.

**Consequence:** Verification is able to confirm artifact consistency and prior findings, but cannot declare data completeness or payoff/risk accuracy. Material field extraction remains pending; the prior audit's FAIL status cannot be overridden.

---

## 8. Final Decision and Actions

### Repository State Assessment

The repository **remains population-consistent and artifact-pairing-consistent**, but is **not ready for operational use** as a complete structured-products database.

- ✓ All 29 products are canonical records with valid metadata
- ✓ All 71 images and 71 OCR files are properly paired and inventoried
- ✓ All 4 original-term PDFs are accounted for  
- ✓ Generated views render deterministically
- ✓ Prior issue-size visual resolutions are reproducible
- ✗ 25+ products lack structured payoff/risk/barrier definitions
- ✗ 4 products lack any primary source evidence
- ✗ 28+ products lack Trust-verified position basis
- ✗ One discovered source (Leonteq issuer/guarantor) is not yet extracted

### Highest-Priority Actions (in order)

1. **G-004 — Recover payoff/risk terms** (PRIMARY BLOCKER)  
   - Extract or document absence of: call mechanics, barrier/trigger levels, range boundaries, downside/principal protection, ranking, coupon linkage for 25 callable/range/CMS/dual-index products
   - Source: original term sheets, Bloomberg detailed pages, prospectuses
   - Outcome: Populate `downside`, `risk`, `underlying` structured fields; update `field_statuses`
   - Criticality: **HIGH** — blocks PASS status and material payoff accuracy

2. **G-005 — Extract CH1484588913 from inspected term sheet**  
   - Populate `issuer: Leonteq Securities AG` and `guarantor: PostFinance Ltd` from 04. Original terms/01. Leonteq/CH1484588913_Leonteq_Termsheet.pdf pages 1-2
   - Update `field_statuses` to `confirmed` for both fields
   - Rerender canonical views
   - Outcome: Complete CH1484588913 record and update generated views
   - Criticality: **MID** — specific source is inspected; requires dossier update only

3. **G-006 — Recover or exclude XS0298465822**  
   - Search Bloomberg archive, ISIN registries, or term-sheet recovery for `XS0298465822` ("Unspecified Instrument")
   - If source is found: extract identity and structure
   - If source remains unavailable: formally document non-existence and retain exclusion
   - Outcome: Either populated structured record or confirmed irreversible exclusion
   - Criticality: **HIGH** — blocks certainty of population completeness

4. **G-009 — Recover or classify Trust position basis**  
   - Obtain Trust custody statements, balance-sheet evidence, or position documentation
   - Reclassify 28 position values from `unclear`/`shared-line-item`/`missing` to `usable invested notional` if evidence supports
   - If evidence does not exist: retain exclusion and document why
   - Outcome: Trust-verified position classification or explicit exclusion with rationale
   - Criticality: **HIGH** — blocks portfolio-aggregation decision logic

5. **G-010 — Recover or permanently exclude XS0168875792 and XS0318585791**  
   - Search Bloomberg archive, ISIN registries, or term-sheet recovery for both ISINs
   - If sources are found: extract full structural terms and reopen review conclusions
   - If sources remain unavailable: formally document non-recovery and retain explicit exclusion from conclusions
   - Outcome: Either populated complete records or confirmed permanent exclusion
   - Criticality: **HIGH** — blocks population coverage certainty

6. **Rerender and verify** (after any updates)  
   - After completing any of the above: run `python "90. Scripts/render_products.py" --view summary` and `--view detailed`
   - Verify output determinism by comparing hash to prior render
   - Confirm all 29 rows present in both views
   - Outcome: Updated canonical views matching dossier frontmatter changes
   - Criticality: **STANDARD**

### Recommendation

**Do not release or rely on this dataset as a complete structured-products database until G-004, G-006, and G-010 are resolved.** These gaps affect core payoff accuracy, population completeness, and evidence integrity.

G-005 (CH1484588913) is a lower-priority completeness gap; the source term sheet is inspected and available for immediate extraction without additional research.

---

## Decision Gate Outcome

**FAIL** — The repository remains FAIL status because:
- Material payoff/risk/barrier terms unavailable for 25+ products (G-004)
- Two products have zero primary source evidence (G-010)
- One product cannot be matched to any known source (G-006)
- Absence of a detected workbook/OCR conflict does not confirm accuracy

All high-criticality actions must be completed and verified before reconsideration for PASS or PASS WITH GAPS status.

---

## Verification Audit Closure

This verification audit confirms that the prior comprehensive audit (2026-08-11) was **accurate and reproducible**. All findings, counts, contradictions, and recommendations from the prior audit remain **valid and unchanged**.

No implementation of recommended actions is detected in the current working tree. The dossier frontmatter, field statuses, and generated views are identical to the prior audit state.

**Verified by:** Systematic re-check of population counts, per-ISIN artifact coverage, generated-view determinism, prior issue-size resolutions, and critical field availability (2026-08-11).

**Status:** The repository requires **immediate action on G-004, G-005, and G-006** to progress toward PASS. Until then, it remains unsuitable for operational use as a complete structured-products base.
