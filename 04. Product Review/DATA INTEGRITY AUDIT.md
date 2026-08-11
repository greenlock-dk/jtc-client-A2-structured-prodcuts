# Structured Products Data Integrity Audit

Audit date: 2026-08-11
Scope: complete repository, current working tree

## 1. Executive result

**FAIL**

The population and physical image/OCR pairing ledgers close, and both canonical views render 29 records deterministically. The 24 mapped issue-size records have recorded outcomes: 23 numeric values and one `not found`; three of those outcomes were independently re-opened in this audit and the remaining 21 were not visually re-opened. Five products have no mapped image/OCR source, and several dossiers leave product-type material fields absent or only described in narrative evidence. The repository therefore still cannot support a claim that all material consolidated terms are confirmed.

| Metric | Count | Expected/baseline | Result |
| --- | ---: | ---: | --- |
| Canonical products | 29 | 29 | PASS |
| Individual product files | 29 | 29 | PASS |
| Parsed YAML frontmatter | 29 | 29 | PASS |
| Unique valid ISINs | 29 | 29 | PASS |
| Unique display orders | 29 | 29 | PASS |
| Rendered summary rows | 29 | 29 | PASS |
| Rendered detailed rows | 29 | 29 | PASS |
| Mapped images | 71 | 71 | PASS |
| Unmapped image files | 0 | 0 claimed | PASS |
| Mapped OCR files | 71 | 71 | PASS |
| Unmapped OCR files | 0 | 0 claimed | PASS |
| Image/OCR pairs | 71 | 71 | PASS |
| Image/OCR ISIN directories | 24 | 24 | PASS |
| Products with no image/OCR evidence | 5 | 5 | PASS |
| Original-term PDFs | 4 | 4 | PASS |
| Products with original-term evidence | 3 | 3 | PASS |
| Review inventory records | 29 | 29 | PASS |
| Generated views rerendered | 2 | 2 | PASS |
| Generated views deterministic | 2 | 2 | PASS |
| Generated views stale after rerender | 0 | 0 | PASS |
| Mapped issue-size outcomes recorded | 24 | 24 mapped products | PASS |
| Mapped issue-size outcomes independently re-opened in this audit | 3 | 24 | GAP |
| Dossiers with candidate issue-size confirmation pending | 0 | 0 | PASS |
| Dossiers with documentary issue-size confirmation | 1 | not stated | PASS |
| Contradictions requiring action | 0 | 0 unresolved claimed | PASS |
| Provenance/completeness gaps | 29 | 0 claimed | FAIL |
| Unused or unmapped physical artifacts | 0 | 0 | PASS |
| Mapped Bloomberg images not independently re-opened in this audit | 68 | 0 for PASS | FAIL |

The summary and detailed files are generated projections, not independent evidence. `python "90. Scripts/render_products.py" --view summary` and `--view detailed` each completed twice with identical output hashes. The renderer's 29-record invariant and configured columns are in [90. Scripts/render_products.py](../90.%20Scripts/render_products.py#L69-L77) and [05. Canonical Data/views.yaml](../05.%20Canonical%20Data/views.yaml#L1-L45).

The reported position field must not be interpreted as issuer issuance. The controlled classification for all 29 reported position values is recorded in [POSITION SIZE CONTROL.md](POSITION%20SIZE%20CONTROL.md): only `usable invested notional` may enter portfolio-dollar aggregation; shared-line-item, minimum-denomination, issue/outstanding, missing, and unclear values are excluded pending Trust-specific evidence.

## 2. Population and artifact coverage

| Layer | Expected | Found | Mapped | Unmapped / missing | Disposition complete? | Evidence |
| --- | ---: | ---: | ---: | ---: | --- | --- |
| Workbook ISIN population | 29 | 29 ISIN sheets | 29 | 0 | Yes | `Trust ISIN information from Bloomberg.xlsx`; package workbook XML lists 29 ISIN-named sheets plus summary/navigation sheets |
| Canonical dossiers | 29 | 29 | 29 | 0 | Yes | `01. Structured Products/`; parser and renderer both completed |
| Generated summary/detail | 29 each | 29 each | 29 | 0 | Yes | `05. Canonical Data/ISIN_summary.md`, `ISIN_detailed.md`; rerendered twice |
| Bloomberg images | 71 | 71 PNG | 71 | 0 | Yes | [02. BBG images/IMAGE INVENTORY.md](../02.%20BBG%20images/IMAGE%20INVENTORY.md#L6-L17) |
| OCR candidates | 71 | 71 TXT | 71 | 0 | Yes | [03. BBG OCR/OCR INVENTORY.md](../03.%20BBG%20OCR/OCR%20INVENTORY.md#L3-L9) |
| Mapped evidence directories | 24 | 24 ISIN directories | 24 | 0 | Yes | Image and OCR directory listings; `_unmapped` exists but is empty |
| Original terms | 4 PDFs | 4 PDFs | 3 ISINs | 0 | Yes | `04. Original terms/01. Leonteq`, `03. Aquarius`, `04. BBVA` |
| Product Review layer | 29 inventory rows | 29 inventory rows | 29 | 0 | Yes | [04. Product Review/REVIEW INVENTORY.md](REVIEW%20INVENTORY.md#L5-L38) |
| Review/consolidation reports | 4 Markdown artifacts | 4 | n/a | 0 | Yes | `REVIEW INVENTORY.md`, `PHASE 5 CONSOLIDATION.md`, `UNMAPPED REVIEW.md`, `ISSUE SIZE RECOVERY.md` |

Artifact ledger disposition totals:

- `used and traced`: 29 dossier files, 71 images, 71 OCR files, 4 original-term PDFs, 29 review inventory rows, 2 generated views.
- `duplicate/redundant`: 0 physical artifacts identified. Generated views are redundant projections by design, not corroborating evidence.
- `irrelevant`: 0 artifacts identified.
- `unmapped`: 0 image/OCR files; `_unmapped` directories are empty.
- `unreadable/uninspected`: 68 mapped Bloomberg images were not independently re-opened in this audit. This is an inspection limitation, not a claim that the files are unreadable. The three re-opened issue-size images and all 4 PDFs were rendered/inspected at the relevant identity, economic-term, payoff, and lifecycle pages. Searchable PDF text was extracted page-by-page; the 5-page Aquarius publication is image-only but was rendered and visually inspected.
- `missing expected counterpart`: 0 image/OCR filename pairs; no missing counterpart was found.

No duplicate hash prefix reuse was identified from the inventory's listed prefixes during the ledger check. The baseline wording “unmapped package media” is supported by the empty inventory section, not by the existence of the `_unmapped` directories.

## 3. Per-ISIN audit

`Material fields traced` is the number of populated canonical/status entries in the dossier frontmatter (normally 22; BBVA has 23). It is not a confirmation count. `Gaps` include the unconfirmed issue-size state and/or missing product-type material fields.

| Record | ISIN | Product file | Workbook/detail | Images/OCR | Original terms | Material fields traced | Conflicts | Gaps | Result |
| ---: | --- | --- | --- | --- | --- | ---: | ---: | ---: | --- |
| 1 | CH1484588913 | present | present | 0/0 | 1 PDF | 22 | 0 | 2 | gap |
| 2 | XS3234638248 | present | present | 0/0 | 1 PDF | 23 | 0 | 1 | clear with source limitation |
| 3 | XS0765564827 | present | present | 3/3 | 2 PDFs | 22 | 0 | 1 | gap |
| 4 | XS1028242706 | present | present | 1/1 | none | 22 | 0 | 2 | gap |
| 5 | XS1243914071 | present | present | 1/1 | none | 22 | 0 | 2 | gap |
| 6 | CH0252328973 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 7 | XS0297701319 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 8 | XS0318585791 | present | present | 0/0 | none | 22 | 0 | 2 | gap |
| 9 | XS0300388351 | present | present | 5/5 | none | 22 | 0 | 2 | gap |
| 10 | XS0164480286 | present | present | 2/2 | none | 22 | 0 | 2 | gap |
| 11 | XS0165220400 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 12 | XS0168875792 | present | present | 0/0 | none | 22 | 0 | 2 | gap |
| 13 | XS0169318291 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 14 | XS0170303290 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 15 | XS0171914038 | present | present | 6/6 | none | 22 | 0 | 2 | gap |
| 16 | XS0172077769 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 17 | XS0241444883 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 18 | XS0249805960 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 19 | XS0277502067 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 20 | XS0278550750 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 21 | XS0284203071 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 22 | XS0294314694 | present | present | 4/4 | none | 22 | 0 | 2 | gap |
| 23 | XS0293931688 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 24 | XS0293919121 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 25 | XS0297467705 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 26 | XS0298465822 | present | present | 0/0 | none | 22 | 0 | 2 | gap |
| 27 | XS0304286924 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 28 | XS0314283432 | present | present | 3/3 | none | 22 | 0 | 2 | gap |
| 29 | XS0315745447 | present | present | 1/1 | none | 22 | 0 | 2 | gap |

The mapped issue-size outcomes are no longer pending in the canonical dossiers, but 21 of the 24 source images were not independently re-opened in this audit. The substantive recurring gap is missing structured payoff/risk detail: for example, [XS0164480286 - Libor Callable Note.md](../01.%20Structured%20Products/XS0164480286%20-%20Libor%20Callable%20Note.md#L99-L109) preserves an issue-size candidate and does not establish the legal payoff from a term sheet. `XS0298465822` is additionally an unspecified instrument with no mapped evidence. `CH1484588913` has a matched term sheet but no image/OCR; its issuer, guarantor, and currency are now populated from that term sheet. `XS3234638248` is the only dossier whose issue size is documentary-confirmed; its source distinguishes USD 2.4 million nominal from the USD 2 million Trust position.

## 4. Contradiction register

| ID | ISIN | Field | Type | Source A and value | Source B and value | Resolution status | Deciding evidence / required action | Criticality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C-001 | none | issue size | format-only difference | Earlier audit state described mapped candidates as pending | All 24 mapped issue-size records now have visual-review outcomes: 23 `confirmed`, 1 `not found` | Resolved | Canonical dossier frontmatter and linked Bloomberg image paths record each outcome | low |
| C-002 | CH1484588913 | issuer / guarantor | identity conflict | Earlier canonical state was blank/not available | Leonteq term sheet, pages 1-2, identifies issuer `Leonteq Securities AG` and guarantor `PostFinance Ltd` | Resolved and incorporated | Current dossier frontmatter and evidence table contain both values with `confirmed` term-sheet citations | mid |

No other direct incompatible source values were identified in the review inventory or current dossier comparison. This is not equivalent to terms confirmed: 68 mapped images were not independently re-opened in this audit. The dossiers' “No unresolved workbook/OCR field disagreements detected” wording is a status assertion, not a reproducible resolution record by itself.

## 5. Missing, unused, and unsupported data

| ID | ISIN / scope | Field or artifact | State | What is missing, unused, or unsupported | Sources checked | Impact | Required resolution | Criticality |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| G-001 | none | issue_size | confirmed | All 24 mapped issue-size records have recorded canonical outcomes; 23 numeric values are confirmed and CH0252328973 is `not found`. Three source images were independently re-opened in this audit; 21 remain to be re-opened | Canonical YAML, `ISSUE SIZE RECOVERY.md`, and mapped Bloomberg issue-size images | No remaining recorded mapped issue-size gap, but visual reinspection is incomplete | Re-open the remaining 21 issue-size images, preserve exact image citations, and do not substitute position size or denomination | high |
| G-002 | repository | primary visual evidence | uninspected | 68 of 71 mapped Bloomberg images were not independently re-opened in this audit. Three issue-size images were re-opened; all 4 PDFs were rendered and inspected, including the image-only Aquarius publication | `02. BBG images/`; `04. Original terms/`; inventory links; canonical `issue_size.source` entries | Image-to-OCR pairing is verified, but uninspected images leave material OCR-derived values below the audit's strongest confidence level | Re-open all 68 images, compare every material OCR candidate with its image, and retain field-level citations and outcomes | high |
| G-004 | most callable/range/CMS/dual-index products | payoff/risk fields | explicitly limited | Structured `downside`, `risk`, and sometimes `underlying` fields remain unavailable; no unsupported payoff inference is promoted | Dossier frontmatter and narrative evidence tables; configured detailed view includes these fields | Review conclusions remain excluded or limited where loss or trigger mechanics are unavailable | Source recovery and field extraction remain required before a complete product conclusion or PASS; retain explicit unavailable dispositions | high |
| G-006 | XS0298465822 | identity and structure | not found | Exact-ISIN public search re-check returned no reliable match; no image/OCR or original terms are present, and unavailable fields remain explicitly `not found` | [exact-ISIN recovery re-check](../04.%20Original%20terms/search-results.md#exact-isin-recovery-re-check); [XS0298465822 - Unspecified Instrument.md](../01.%20Structured%20Products/XS0298465822%20-%20Unspecified%20Instrument.md#L38-L62) | Product remains in the population but cannot support a structured-product conclusion | Search issuer, regulator, exchange, Bloomberg, or Trust archives if access becomes available; retain exclusion and do not infer terms | high |
| G-007 | all 29 | generated detail completeness | not applicable | The detailed view includes canonical fields but not every evidence-table candidate or provenance rationale | [05. Canonical Data/views.yaml](../05.%20Canonical%20Data/views.yaml#L16-L45) | Generated agreement cannot substitute for source traceability | Keep views as projections and maintain field-level evidence in dossiers/register | low |
| G-008 | repository | source artifact accounting | confirmed | No image/OCR orphan, unmapped file, duplicate filename, or missing counterpart was found | Physical directory scan and inventories | No current artifact-count impact | Retain the closed ledger and rerun after any extraction change | low |
| G-009 | 28 of 29 products | Trust position basis | explicitly limited | Only XS3234638248 is classified as `usable invested notional`; the remaining reported amounts are unclear, shared across line items, minimum denomination, or missing | [POSITION SIZE CONTROL.md](POSITION%20SIZE%20CONTROL.md); dossier position fields | Portfolio exposure and concentration cannot be reliably aggregated without Trust-specific basis evidence | Exclude all non-usable rows from aggregation and recover custody or balance-sheet evidence before using them | high |
| G-010 | XS0168875792; XS0318585791 | primary evidence and structure | not found | Exact-ISIN public search re-check returned no reliable match for either product; both have zero mapped images/OCR, no original terms, and material identity/payoff fields explicitly `not found` | [exact-ISIN recovery re-check](../04.%20Original%20terms/search-results.md#exact-isin-recovery-re-check); [XS0168875792 - Libor Callable Note.md](../01.%20Structured%20Products/XS0168875792%20-%20Libor%20Callable%20Note.md); [XS0318585791 - Kick In Note.md](../01.%20Structured%20Products/XS0318585791%20-%20Kick%20In%20Note.md) | No structured-product or risk conclusion is supported for either instrument | Use issuer, regulator, exchange, Bloomberg, or Trust archives if access becomes available; retain both records excluded from structured conclusions | high |

Expected blanks were not converted to zero. “Not available” and “No issue-size label found in available OCR” were retained as source limitations; they were not treated as contradictions.

## 6. Prior resolutions re-performance

| ISIN | Field | Original disagreement | Visual evidence inspected | Existing resolution reproducible? | Finding |
| --- | --- | --- | --- | --- | --- |
| CH0252328973 | issue size | OCR did not provide a numeric issuance value | Yes: `02. BBG images/CH0252328973/CH0252328973 - image-01.png` | Yes | Confirmed `not found`; no issuance data provided, not zero |
| XS0300388351 | issue size | OCR candidate USD 8,370.00 million | Yes: `02. BBG images/XS0300388351/XS0300388351 - image-01.png` | Yes | Confirmed USD 8,370.00 million |
| XS0765564827 | issue size | OCR candidate USD 750,000.00 million | Yes: `02. BBG images/XS0765564827/XS0765564827 - image-02.png` | Yes | Confirmed USD 750,000.00 million |

The three rows above document the issue-size resolutions independently re-opened in this audit. The canonical dossiers and [ISSUE SIZE RECOVERY.md](ISSUE%20SIZE%20RECOVERY.md) contain recorded outcomes for the remaining 21 mapped products, but those images were not independently re-opened here. Five products remain without mapped image/OCR evidence: CH1484588913, XS0168875792, XS0298465822, XS0318585791, and XS3234638248.

## 7. Inspection limitations

- `rg` was unavailable in the audit environment; equivalent recursive `grep` searches were used.
- The system Python lacked `openpyxl`; workbook sheet population was verified directly from the XLSX package XML. This was sufficient for sheet/artifact enumeration but not for cell-level workbook-value extraction.
- Three of the 71 Bloomberg PNGs were visually re-opened based on the requested confirmations; the remaining 68 were counted, paired, and linked by filename but not visually opened in this audit. OCR text was not treated as confirmation.
- The four original-term PDFs were rendered and inspected. Searchable PDFs were text-extracted page-by-page; the image-only Aquarius publication was visually inspected after rendering. Legal-term conclusions remain limited only where the inspected documents do not cover the relevant ISIN or field.
- The audit did not independently execute spreadsheet image-anchor extraction or OCR generation; it validated the existing inventories and physical pairings.
- The working tree contained pre-existing user modifications and deleted legacy files. No source or product file was reverted. The canonical views were rerendered as requested; their repeated output was deterministic.

G-002 remains open because 68 mapped Bloomberg images were not independently re-opened. The Aquarius prospectus was text-extracted across all 228 pages, with material identity and lifecycle pages visually checked; the Aquarius publication was image-only but all 5 pages were rendered and visually inspected. Remaining FAIL drivers are unsupported or unpopulated structured fields plus the image-inspection limitation.

## 8. Final decision and actions

The repository is **population-consistent and artifact-pairing-consistent**, but it is not yet complete as a provenance-controlled data set: material payoff/risk terms remain unavailable for many products, and XS0298465822 is explicitly retained without a structured conclusion. All physical extracted artifacts are accounted for, but material terms are not adequately evidenced for a PASS.

Highest-priority actions:

1. **G-004:** recover and extract product-type-aware payoff, barrier, trigger, range, call, downside, ranking, and risk terms; do not promote unsupported inference from the current limitations.
2. **G-002:** re-open the remaining 68 mapped Bloomberg images and reperform material OCR-to-image comparisons.
3. **G-006:** recover matched evidence for XS0298465822 before reopening its structured-product review conclusion.
4. Rerender both canonical views after any frontmatter update and verify deterministic output again.
