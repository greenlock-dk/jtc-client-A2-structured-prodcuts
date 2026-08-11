# Public Term-Sheet Search Results

> Research captured 9 August 2026. Five ISINs were searched individually using exact ISIN queries plus issuer, structure, and historical programme terms. No source document below should be treated as evidence of the target instrument unless explicitly marked as an exact match.

## Exact-ISIN Recovery Re-check (11 August 2026)

The three unresolved no-evidence instruments were searched again using the complete ISIN as the primary query, with product-name and historical-issuer terms where available:

| ISIN | Exact public result | Disposition |
| --- | --- | --- |
| `XS0298465822` | No exact instrument page, final terms, pricing supplement, prospectus, or reliable issuer match returned | `not found`; this is not evidence that the document does not exist |
| `XS0168875792` | No exact instrument page, final terms, pricing supplement, prospectus, or reliable issuer match returned; near-matches were different ISINs | `not found`; near-matches are excluded from product evidence |
| `XS0318585791` | No exact instrument page, final terms, pricing supplement, prospectus, or reliable issuer match returned; generic kick-in results were unrelated products | `not found`; generic product-family documents are excluded from product evidence |

This pass does not establish non-existence and does not supply terms for any target. It closes the indexed-public-search step available without issuer, exchange, regulator, or Trust archive access. The three dossiers remain explicitly excluded from structured-product conclusions.

## Scope and conclusion

The search did not recover an exact public term sheet, final terms document, or pricing supplement for four of the five target ISINs. An exact pricing supplement for `XS3234638248` is now available locally and is recorded as original-term evidence in the product dossier. The search also recovered useful product-family examples and archive routes for three of the remaining four products:

- `XS0168875792`: a UBS KeyInvest near-match for a 2003 USD LIBOR range-accrual note.
- `XS0315745447`: a KBC IFIMA base prospectus explaining the relevant final-terms framework.
- `XS0304286924`: historical Dexia final-terms and pricing-supplement examples.

These results are research leads only. They should not replace the missing product documents or be entered as confirmed terms. The locally stored BBVA pricing supplement is an exact match and is treated as primary documentary evidence.

## 1. XS0168875792

**Internal context:** Callable note, Norway, LIBOR-linked; the workbook record has limited product detail and no dedicated worksheet evidence.

**Exact result:** No exact public result for `XS0168875792` was found.

**Relevant near-match:**

[UBS 15-year USD range accrual note, ISIN XS0177608824](https://keyinvest-ch.ubs.com/produkt/detail/index/isin/XS0177608824/termsheet)

This is a different ISIN, but it is a closely related historical product-family example. The search result describes:

- 15-year USD callable daily range-accrual notes.
- Interest linked to 6-month USD LIBOR.
- Issuer call after six months and semi-annually thereafter.
- Coupon based on the number of days LIBOR remains within a stated range.
- Issue date 3 October 2003 and maturity date 3 October 2018.
- 100% optional redemption amount.
- UBS AG, London Branch as calculation agent.
- Euroclear/Clearstream settlement.

**Assessment:** Useful for identifying terminology, likely programme documentation, and historical archive search patterns. It is not evidence of the terms of `XS0168875792`.

**Priority:** Medium. Search the UBS KeyInvest archive and issuer EMTN records using the target ISIN and variations of “callable daily range accrual”, “6 month USD LIBOR”, and the internal issue/maturity details if available.

## 2. `XS0298465822`

**Internal context:** Unspecified instrument. The workbook record contains no product name, issuer, issue date, maturity, structure, coupon, or underlying.

**Exact result:** No exact public result or reliable product identification was found.

**Relevant archive route:**

[BaFin securities prospectus database guidance](https://www.bafin.de/EN/die-bafin/publikationen-daten/datenbanken-uebersichten/prospektdatenbanken/wertpapiere/wertpapiere_node_en.html)

The BaFin page states that securities prospectuses and securities information sheets can be searched by issuer, German securities identifier, or ISIN. It also points to the ESMA Prospectus Register, where prospectuses, supplements, and final terms can be searched by ISIN and issuer.

**Assessment:** No product facts were recovered. This is an identification-recovery case and should not be analysed as a structured product until the issuer or instrument type is established.

**Priority:** High for identification, low for immediate term extraction. Search the BaFin and ESMA registers directly by the complete ISIN, then test likely listing venues and issuer names once any identifier is returned.

## 3. XS0318585791

**Internal context:** “Kick in” note; no dedicated worksheet or OCR evidence is available in the current product-review layer.

**Exact result:** No exact public term sheet or final terms document was found.

**False-positive search results:** Searches returned unrelated 2007 structured-product documents, including:

- JPMorgan reverse exchangeable notes filed with the SEC.
- ABN AMRO knock-in securities filed with the SEC.

These documents are not associated with `XS0318585791` and must not be used as product evidence.

**Assessment:** The phrase “kick-in” is too broad and produces many unrelated results. The target needs an issuer, exchange, currency, denomination, or underlying before a meaningful public-document search can be narrowed.

**Priority:** Medium to high for identification. Obtain issuer/currency or a visual reading of the original Bloomberg evidence before further web searching.

## 4. XS0315745447

**Internal context:** KBC IFIMA NV note, issued 3 August 2007, maturing 20 August 2012, with a 10.50% annual coupon in the workbook. No detailed structure is recorded.

**Exact result:** No exact final terms document for `XS0315745447` was found.

**Relevant KBC programme document:**

[KBC IFIMA base prospectus](https://img.iex.nl/iexprofs/GEP_Documents/Prospectus/XS0363151647.pdf)

This is not the final terms for the target ISIN and its URL contains a different ISIN. It is nevertheless relevant to the issuer and programme. The document states that:

- KBC Internationale Financieringsmaatschappij N.V. was incorporated in the Netherlands as a financing subsidiary.
- KBC Bank NV provided an unconditional and irrevocable guarantee for the programme.
- The programme covered senior guaranteed and dated subordinated guaranteed notes.
- Fixed-rate, floating-rate, zero-coupon, index-linked, currency-linked, equity-linked, and other structured notes could be issued.
- Tranche-specific terms were set out in separate Final Terms documents.
- Notes could be distributed privately or publicly, on a syndicated or non-syndicated basis.

**Assessment:** The internal KBC issuer identification is plausible and the programme document provides a credible document trail. It does not verify the target note’s currency, guarantee status, denomination, issue price, or redemption mechanics. The best next target is the KBC IFIMA Final Terms or pricing supplement for the August 2007 tranche.

**Priority:** High. Search KBC IFIMA, KBC Bank, CSSF/Luxembourg, Euronext, and archive copies for Final Terms around 3 August 2007.

## 5. XS0304286924

**Internal context:** Matured callable note attributed in the workbook to Dexia Banque International LUX SA, issued 30 May 2007 and maturing 27 June 2022, with a LIBOR range-linked description.

**Exact result:** No exact public result for `XS0304286924` was found.

**Relevant Dexia document examples:**

[Dexia Banque Internationale à Luxembourg final terms, December 2007](https://www.globenewswire.com/news-release/2007/12/07/75115/0/da/files/177413/0/al%20dollar%20-%20final%20terms.pdf)

This unrelated Dexia document demonstrates the fields expected in a final-terms document, including issuer, programme, series/tranche, currency, nominal amount, issue price, denomination, issue and maturity dates, interest basis, redemption basis, listing, clearing, ISIN, calculation agent, and risk disclosures.

[Dexia historical pricing supplement, July 2002](https://dl.bourse.lu/dl?v=aEzdGoviK%2F1GO4X6hu8pDL2h8j9b08nIc19pTyRwT%2ByP0GAW6sqvUmeIRLHbbbOK8fC639lByA%2FKgZ5kgjyOuo4LVJRxMyegXd%2FPHsyneenBJQhdxjUOIRfG0LMMjg7s14%2Bk9Rts9qfZFnynzEqJoVj7%2Bvym5SuKvvITcfXIJog1DW%2B5ftKONvqOD3n9vzT)

This unrelated 2002 document is a Dexia pricing supplement for equity-basket-linked notes under a Dexia EMTN programme. It confirms that historical Dexia programme documents may be available through Luxembourg exchange archives.

**Assessment:** The documents do not prove the target note’s terms. They do provide a credible recovery route and a template for the fields to seek. Search Luxembourg exchange archives and Dexia EMTN programme records for the 30 May 2007 issue date and the target ISIN.

**Priority:** High. The issuer and approximate issue date are known, making this a stronger archive-recovery candidate than the unidentified instruments.

## 6. Exact source subsequently added: XS3234638248

An exact pricing supplement was added after the public-search pass:

[BBVA Global Markets, B.V. Series 40076 Pricing Supplement](04.%20BBVA/XS3234638248_BBVA_Global_Markets_Pricing_Supplement_2026-01-27.pdf)

The document identifies `XS3234638248` on page 12 and confirms on pages 1-3 and 7-11:

- Issuer: BBVA Global Markets, B.V.; guarantor: Banco Bilbao Vizcaya Argentaria, S.A.
- Series 40076; USD 2,400,000 nominal amount; USD 1,000 denomination; 100% issue price.
- Issue date: 27 January 2026; maturity date: 22 July 2027.
- Worst-of basket: Amazon, Microsoft, and NVIDIA shares.
- Memory coupon: 2.75% when the worst value is at least the 68% coupon barrier; otherwise zero.
- Automatic early redemption from July 2026 through April 2027 with triggers stepping down from 100% to 94%.
- Final redemption at 100% when the worst value is at least 68%; otherwise physical delivery of the worst-performing share, subject to the stated entitlement and residual-amount mechanics.

The termsheet confirms the workbook’s core structure, coupon, barrier, dates, underlyings, and denomination. It also identifies a material amount distinction: the workbook records a USD 2,000,000 position size, while the pricing supplement states a USD 2,400,000 nominal amount. These values describe different concepts and are both retained.

## Research limitations

- Search-result availability does not establish that a document is authentic, complete, or applicable to the target ISIN.
- Several historical term sheets are not indexed by search engines, may have been removed, or may be available only through exchange, issuer, regulator, or paid data archives.
- Near-match documents are retained here to guide further recovery, not as substitutes for the missing original terms.

## Remaining 24 products

The following products were included in the continuation search. The grouped public searches returned no verified exact-ISIN term sheet, final terms document, pricing supplement, or official listing record for these targets. Search results that belonged to other ISINs or unrelated issuers were excluded from the product context.

| ISIN | Internal anchor | Public search result | Recommended next route |
| --- | --- | --- | --- |
| `CH0252328973` | Credit Suisse Nassau senior unsecured Euro MTN; 2015 issue; 55% barrier linked to SPX/SMI | No exact public hit | Credit Suisse/UBS archive; SIX/Swiss exchange records; local Bloomberg images are the stronger evidence source |
| `CH1484588913` | Leonteq Express Certificate on S&P 500/SMI; 2026 issue | No exact public hit in grouped search; a local six-page term sheet exists under `04. Original terms/01. Leonteq/` | Use the local term sheet as primary evidence; search Leonteq product archive by ISIN |
| `XS0765564827` | Aquarius perpetual limited-recourse secured notes backed by Swiss Re; 2012 issue | No exact public hit in grouped search; local Aquarius prospectus/publication documents exist | Use local prospectus/publication as primary evidence; search Aquarius/Swiss Re and listing archives for supplements |
| `XS1028242706` | Morgan Stanley EMTN; 2014 issue; apparent zero-coupon bullet | No exact public hit | Morgan Stanley EMTN archive; Euroclear/Clearstream and listing-venue records |
| `XS1243914071` | Nomura Bank International senior unsecured Euro Dollar; 2015 issue; apparent zero-coupon bullet | No exact public hit | Nomura EMTN archive; Luxembourg exchange and regulator records |
| `XS3234638248` | BBVA Phoenix Memory note linked to Amazon/Microsoft/Nvidia; 2026 issue | Exact local pricing supplement subsequently added; no exact public hit in the original grouped search | Local BBVA pricing supplement is now the primary source; retain issuer archive as a supplementary route |
| `XS0164480286` | Lloyds TSB callable Euro MTN; 2003 issue; USD 6-month LIBOR range | No exact public hit | Lloyds/UBS/Deutsche historical EMTN archives; search by issue date and LIBOR range-accrual language |
| `XS0165220400` | Banque Caisse Epargne callable note; 2003 issue; USD 6-month LIBOR range | No exact public hit | Issuer successor archives, Luxembourg records, and arranging-bank archives |
| `XS0169318291` | Lloyds TSB callable note; 2003 issue; USD 6-month LIBOR range | No exact public hit | Lloyds historical EMTN archive; search exact issue/maturity dates and range-accrual terms |
| `XS0170303290` | Banque Caisse Epargne callable note; 2003 issue; USD 6-month LIBOR range | No exact public hit | Issuer successor archives and Luxembourg listing records |
| `XS0171914038` | Lloyds TSB callable note; 2003 issue; USD 6-month LIBOR range | No exact public hit | Lloyds/Deutsche historical EMTN archives; use denomination and maturity as additional filters |
| `XS0172077769` | Lloyds TSB callable note; 2003 issue; USD LIBOR range | No exact public hit | Lloyds/Deutsche/Pictet archives and Luxembourg records |
| `XS0241444883` | Banque International Lux callable note; 2006 issue; USD 6-month LIBOR range | No exact public hit | Luxembourg exchange archive; issuer successor and arranging-bank records |
| `XS0249805960` | Banque International Lux callable note; 2006 issue; long-dated USD 6-month LIBOR range | No exact public hit | Luxembourg exchange archive and historical EMTN programme supplements |
| `XS0277502067` | Commonwealth Bank Australia callable note; 2006 issue; USD LIBOR range | No exact public hit | Commonwealth Bank structured-products archive; Australian and Luxembourg listing records |
| `XS0278550750` | Dexia Banque International LUX callable/actioned note; 2006 issue; USD 3-month LIBOR range | No exact public hit | Dexia/Luxembourg exchange archives; use the related issuer-document examples in the earlier section |
| `XS0284203071` | Commonwealth Bank Australia callable CMS spread note; 2007 issue | No exact public hit | Commonwealth Bank archive; Luxembourg exchange and dealer records; search CMS spread terminology |
| `XS0293919121` | Commonwealth Bank Australia callable note; 2007 issue; USD 6-month LIBOR range | No exact public hit | Commonwealth Bank and arranging-bank archives; Luxembourg listing records |
| `XS0293931688` | Commonwealth Bank Australia callable/actioned CMS spread note; 2007 issue | No exact public hit | Commonwealth Bank archive; search CMS spread, callable, and 2007 EMTN programme terms |
| `XS0294314694` | Bank of Scotland callable note; 2007 issue; USD 3-month LIBOR range | No exact public hit | Lloyds Banking Group/Bank of Scotland legacy EMTN archive; UK and Luxembourg records |
| `XS0297467705` | Commonwealth Bank Australia matured note; 2007 issue; USD 6-month LIBOR range | No exact public hit | Commonwealth Bank archive and listing records; confirm whether the instrument was listed or privately placed |
| `XS0300388351` | Commonwealth Bank Australia callable dual-indexed leveraged note; 2007 issue | No exact public hit | Commonwealth Bank archive; search USD swap-rate and dual-indexed note terminology |
| `XS0314283432` | Commonwealth Bank Australia callable/actioned note; 2007 issue | No exact public hit | Commonwealth Bank and dealer archives; issue-date and maturity-date searches |
| `XS0297701319` | Commonwealth Bank Australia callable range note; 2007 issue; USD/Gold Spot and Nikkei 225 | No exact public hit | Commonwealth Bank structured-products archive; search the dual-underlying range/coupon description |

### Cross-search observations

- The historical exact-ISIN searches did not surface target-specific documents through indexed public web pages.
- Search results did surface many contemporary SEC term sheets for unrelated US issuers, including Merrill Lynch, JPMorgan, Morgan Stanley, Bear Stearns, and Citigroup. These establish comparable disclosure formats but are not evidence for the listed ISINs.
- The [BaFin securities prospectus database](https://www.bafin.de/EN/die-bafin/publikationen-daten/datenbanken-uebersichten/prospektdatenbanken/wertpapiere/wertpapiere_node_en.html) and the ESMA Prospectus Register remain the most systematic public routes for exact-ISIN searches.
- For the 2003-2007 instruments, issuer, arranger, listing venue, and denomination are more useful search keys than generic product names. Several internal names are normalized descriptions rather than original security titles.
- The two locally held original-document sets, Leonteq and Aquarius, remain materially stronger than the public-search results for their respective products.

## Issuer-Led Follow-Up Pass

> Follow-up research performed 9 August 2026. This pass used each target ISIN with the known issuer, issue date, maturity date, and product mechanics, rather than generic product labels. The results below supersede neither the earlier exact-search findings nor the source-evidence hierarchy.

### Exact public endpoint recovered: `CH1484588913`

[SIX Structured Products record for CH1484588913](https://www.six-structured-products.com/en/zertifikat/-CH1484588913)

The SIX endpoint resolves for the exact target ISIN. Its current publicly crawlable content identifies the security as expired, but does not expose the product name, symbol, issuer, underlying, coupon, barrier, terms document, or historic trading data. It is nevertheless a verified listing-record lead for the target product.

The direct Leonteq product URL was also tested:

[Leonteq product URL for CH1484588913](https://structuredproducts-ch.leonteq.com/isin/CH1484588913)

The page timed out in the public crawler, so it did not yield extractable terms in this pass. This is not evidence that the issuer page does not exist. The locally held Leonteq PDF remains the primary documentary source for this ISIN.

### Historical issuer-specific searches with no exact document recovered

| ISIN | Search formulation | Result |
| --- | --- | --- |
| `XS0164480286` | Lloyds TSB; 28 February 2003 issue; 25 March 2018 maturity; callable USD 6-month LIBOR range accrual | No exact public document or listing record found |
| `XS0165220400` | Banque Caisse d'Epargne; 11 March 2003 issue; 24 September 2008 maturity; callable USD 6-month LIBOR range accrual | No exact public document or listing record found |
| `XS0169318291` | Lloyds TSB; 19 May 2003 issue; 1 June 2010 maturity; callable USD 6-month LIBOR range accrual | No exact public document or listing record found |
| `XS0277502067` | Commonwealth Bank of Australia; 24 November 2006 issue; 14 December 2021 maturity; callable USD 3-month LIBOR range accrual | No exact public document or listing record found |
| `XS0284203071` | Commonwealth Bank of Australia; 18 January 2007 issue; 14 February 2022 maturity; callable CMS spread note | No exact public document or listing record found |
| `XS0300388351` | Commonwealth Bank of Australia; 30 May 2007 issue; 30 May 2017 maturity; callable dual-indexed note linked to USD semiannual 30-year swap rate | No exact public document or listing record found |
| `XS3234638248` | BBVA; 27 January 2026 issue; 22 July 2027 maturity; Phoenix Memory structure linked to Amazon, Microsoft, and Nvidia | No exact public document or listing record was recovered in the web pass; an exact local pricing supplement is now available and supersedes this negative result |
| `CH0252328973` | Credit Suisse Nassau; 28 May 2015 issue; 28 May 2020 maturity; S&P 500/SMI 55% barrier note | No exact public document or listing record found |

### Result quality and next action

- The exact SIX endpoint for `CH1484588913` is a verified target-specific discovery, though it currently has insufficient publicly exposed content to corroborate individual terms.
- The eight issuer-led negative searches are stronger than generic negative searches because each used the available issuer, lifecycle, and payoff information. They do not establish that the instruments were unlisted or that no document exists.
- The historical notes may have been privately placed, delisted, held in archives not indexed by web search, or published as pricing supplements under programme names without the ISIN in indexed text.
- For the 2003-2007 notes, the next recovery method should be directed document requests to the issuer or successor, lead distributor/custodian, Luxembourg Stock Exchange archive, and Euroclear/Clearstream documentation channels. Include ISIN, issue date, maturity date, denomination, issuer, and the internal range-accrual or CMS description in each request.
- For `CH0252328973`, query the issuer's current structured-products desk or investor-document portal with the exact ISIN rather than relying on historical web indexing. `XS3234638248` now has an exact local BBVA pricing supplement; no further recovery action is required for its core terms.

## Brave and Exa Direct-ISIN Recovery Pass (11 August 2026)

This follow-up pass searched each of the 29 portfolio ISINs individually through Brave Search and Exa. Queries used the exact ISIN plus, where known, issuer, issue date, maturity, coupon/reference-rate mechanics, and the document terms “final terms”, “pricing supplement”, “term sheet”, or “prospectus”. Each result page was screened for the target ISIN before being treated as a discovery.

**Result:** No additional exact original terms, final terms, pricing supplement, official target-specific listing, or product page was recovered. This is a public-indexing/discovery null result, not evidence that the documents do not exist, that the notes were unlisted, or that they were not issued under the identified programmes.

### Coverage

The direct pass covered:

- `CH1484588913`, `XS3234638248`, `XS0765564827`, `XS1028242706`, `XS1243914071`, and `CH0252328973`.
- `XS0297701319`, `XS0318585791`, `XS0300388351`, `XS0164480286`, `XS0165220400`, `XS0168875792`, `XS0169318291`, `XS0170303290`, `XS0171914038`, and `XS0172077769`.
- `XS0241444883`, `XS0249805960`, `XS0277502067`, `XS0278550750`, `XS0284203071`, `XS0294314694`, `XS0293931688`, `XS0293919121`, `XS0297467705`, `XS0298465822`, `XS0304286924`, `XS0314283432`, and `XS0315745447`.

### New verified recovery routes

- [Commonwealth Bank EMTN programme](https://www.commbank.com.au/about-us/investors/emtn-programme.html): the issuer endpoint explicitly publishes programme materials and final terms. The current public index does not expose the 2007 target notes, but it is the strongest issuer-led retrieval route for `XS0277502067`, `XS0284203071`, `XS0293931688`, `XS0293919121`, `XS0297467705`, `XS0297701319`, `XS0300388351`, and `XS0314283432`.
- [Morgan Stanley B.V. programme supplement](https://sp.morganstanley.com/download/prospectus/57fb1850-2b79-478c-aa77-8c400d271307/): confirms a contemporaneous Morgan Stanley B.V. medium-term-note programme and the requirement for instrument-level Final Terms. It does not name `XS1028242706`, so it is a programme-recovery lead only.
- [Banque Internationale a Luxembourg final-terms example](https://www.bil.com/Documents/EMTN/FT_XS2219003915-en.pdf): confirms an accessible BIL EMTN final-terms repository and expected documentary format. This document is for `XS2219003915`, not `XS0241444883` or `XS0249805960`.

### Excluded near-matches

The searches again returned several documents for different ISINs that have similar callable LIBOR range-accrual or CMS-spread mechanics. They include the already-recorded UBS KeyInvest examples, unrelated Bank of America SEC filings, and other Commonwealth Bank and Credit Suisse structured-product sheets. None names a target ISIN and none is evidence of the target product’s terms.

For `XS0298465822`, the direct search did not identify an issuer or instrument type. The [BaFin securities prospectus database](https://www.bafin.de/EN/die-bafin/publikationen-daten/datenbanken-uebersichten/prospektdatenbanken/wertpapiere/wertpapiere_node_en.html) remains the appropriate next public retrieval interface because it supports ISIN searches and points to the ESMA register for final terms.

### Next recovery step

Continue with the exchange archive interfaces and same-programme issuer-document retrieval. Requests should include the exact ISIN, issuer, issue date, maturity date, denomination, and the available rate-linked or equity-linked description. Do not substitute any of the near-matches above for the missing original terms.
