# Issue Size Recovery

> Automated recovery pass over all portfolio ISINs and available Bloomberg OCR.
> `Amt Issued/outstanding` is treated as a candidate issue/outstanding-size field, not confirmed evidence until checked against the source image.

## Results

| ISIN | OCR labels found | Recovered field/context | Status |
| --- | ---: | --- | --- |
| `CH1484588913` | 0 | No issue-size label found in available OCR | Unavailable: document recovery required |
| `XS3234638248` | 0 | No issue-size label found in available OCR | Unavailable: document recovery required |
| `XS0765564827` | 1 | `03. BBG OCR/XS0765564827/XS0765564827 - image-02.txt`: Amt Issued/Outstanding 23) Sustainability PERPETUAL CALLED 0N 09/11/18@100.00 USD 750,000.00 (M) Quick Links Iss Sprd USD (M) 32 ALLQ Pricing Calc Type (1469)FIX-T0-VARIABLE BD; recovered numeric candidate: USD 750,000.00 million | Candidate: visual confirmation required |
| `XS1028242706` | 1 | `03. BBG OCR/XS1028242706/XS1028242706 - image-01.txt` and source image: `Amt Issued/Outstanding` USD 850.00 (M); recovered numeric value: USD 850.00 million | Confirmed by source image |
| `XS1243914071` | 1 | `03. BBG OCR/XS1243914071/XS1243914071 - image-01.txt` and source image: `Amt Issued/Outstanding` USD 1,525.00 (M); recovered numeric value: USD 1,525.00 million | Confirmed by source image |
| `CH0252328973` | 1 | `03. BBG OCR/CH0252328973/CH0252328973 - image-01.txt`: Amt Issued/outstanding 23) Sustainability BULLET USD (M) Quick Links Iss Sprd USD (M) 30 ALLQ Pricing Calc Type (99)*NO CALCULATIONS*; no numeric value parsed | Candidate: visual confirmation required |
| `XS0297701319` | 1 | `03. BBG OCR/XS0297701319/XS0297701319 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability USD 3,000.00 (M) Quick Links Iss Sprd USD (M) 30 ALLQ Pricing Calc Type (198)NO CALC-FLOATERS Min Piece/Increment; recovered numeric candidate: USD 3,000.00 million | Candidate: visual confirmation required |
| `XS0318585791` | 0 | No issue-size label found in available OCR | Unavailable: document recovery required |
| `XS0300388351` | 1 | `03. BBG OCR/XS0300388351/XS0300388351 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability USD 8,370.00 (M) Quick Links Iss Sprd USD (M) 30 ALLQ Pricing Calc Type (521)ACCRUED ONLY FLOAT Qt Recap; recovered numeric candidate: USD 8,370.00 million | Candidate: visual confirmation required |
| `XS0164480286` | 1 | `03. BBG OCR/XS0164480286/XS0164480286 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability CALLED 0N 03/25/08@100.00 USD 19,550.00 (M) Quick Links Iss Sprd USD (M) 32 ALLQ Pricing Calc Type (198)NO CALC-FLOATERS; recovered numeric candidate: USD 19,550.00 million | Candidate: visual confirmation required |
| `XS0165220400` | 1 | `03. BBG OCR/XS0165220400/XS0165220400 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability CALLED 0N 09/24/08@100.00 USD 5,000.00 (M) Quick Links Iss Sprd USD (M) 32 ALLQ Pricing Calc Type (198)NO CALC-FLOATERS; recovered numeric candidate: USD 5,000.00 million | Candidate: visual confirmation required |
| `XS0168875792` | 0 | No issue-size label found in available OCR | Unavailable: document recovery required |
| `XS0169318291` | 1 | `03. BBG OCR/XS0169318291/XS0169318291 - image-01.txt`: Amt Issued/outstanding 23) Sustainability CALLED 0N 06/01/10@100.00 USD 24,070.00 (M) Quick Links Iss Sprd USD (M) 32 ALLQ Pricing Calc Type (198)NO CALC-FL0ATERS; recovered numeric candidate: USD 24,070.00 million | Candidate: visual confirmation required |
| `XS0170303290` | 1 | `03. BBG OCR/XS0170303290/XS0170303290 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability CALLED 0N 12/16/08@100.00 USD 18,000.00 (M) Quick Links Iss Sprd USD (M) 32 ALLQ Pricing Calc Type (198)N0 CALC-FLOATERS; recovered numeric candidate: USD 18,000.00 million | Candidate: visual confirmation required |
| `XS0171914038` | 1 | `03. BBG OCR/XS0171914038/XS0171914038 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability CALLED 0N 04/14/08@100.00 USD 30,850.00 (M) Quick Links Iss Sprd USD (M) 3D ALLQ Pricing Calc Type (198)NO CALC-FLOATERS; recovered numeric candidate: USD 30,850.00 million | Candidate: visual confirmation required |
| `XS0172077769` | 1 | `03. BBG OCR/XS0172077769/XS0172077769 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability CALLED 0N 04/14/08@100.00 USD 6,200.00 (M) Quick Links Iss Sprd USD (M) 3D ALLQ Pricing Calc Type (198)NO CALC-FLOATERS; recovered numeric candidate: USD 6,200.00 million | Candidate: visual confirmation required |
| `XS0241444883` | 1 | `03. BBG OCR/XS0241444883/XS0241444883 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability CALLED 0N 02/10/09@100.00 USD 5,000.00 (M) Quick Links Iss Sprd USD (M) 3D ALLQ Pricing Calc Type (198)NO CALC-FLOATERS; recovered numeric candidate: USD 5,000.00 million | Candidate: visual confirmation required |
| `XS0249805960` | 1 | `03. BBG OCR/XS0249805960/XS0249805960 - image-01.txt`: AmtIssued/outstanding 23) Sustainability USD 17,200.00 (M) Quick Links Iss Sprd USD (M) 3D ALLQ Pricing Calc Type (198)NO CALC-FLOATERS Min Piece/Increment; recovered numeric candidate: USD 17,200.00 million | Candidate: visual confirmation required |
| `XS0277502067` | 1 | `03. BBG OCR/XS0277502067/XS0277502067 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability USD 5,000.00 (M) Quick Links Iss Sprd USD (M) 3D ALLQ Pricing Calc Type (198)NO CALC-FLOATERS Min Piece/Increment; recovered numeric candidate: USD 5,000.00 million | Candidate: visual confirmation required |
| `XS0278550750` | 1 | `03. BBG OCR/XS0278550750/XS0278550750 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability CALLED 0N01/03/09@100.00 USD 10,000.00 (M) Quick Links Iss Sprd USD (M) 3D ALLQ Pricing Calc Type (198)N0 CALC-FLOATERS; recovered numeric candidate: USD 10,000.00 million | Candidate: visual confirmation required |
| `XS0284203071` | 1 | `03. BBG OCR/XS0284203071/XS0284203071 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability USD 10,000.00 (M) Quick Links Iss Sprd USD (M) 32 ALLQ Pricing Calc Type (198)NO CALC-FLOATERS Min Piece/Increment; recovered numeric candidate: USD 10,000.00 million | Candidate: visual confirmation required |
| `XS0294314694` | 1 | `03. BBG OCR/XS0294314694/XS0294314694 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability USD 10,000.00 (M) Quick Links Iss Sprd USD (M) 3D ALLQ Pricing Calc Type (521)ACCRUED ONLY FLOAT Qt Recap; recovered numeric candidate: USD 10,000.00 million | Candidate: visual confirmation required |
| `XS0293931688` | 1 | `03. BBG OCR/XS0293931688/XS0293931688 - image-01.txt`: AmtIssued/outstanding 23) Sustainability CALLED 0N 04/14/09@100.00 USD 3,000.00 (M) Quick Links Iss Sprd USD (M) 32 ALLQ Pricing Calc Type (198)NO CALC-FL0ATERS; recovered numeric candidate: USD 3,000.00 million | Candidate: visual confirmation required |
| `XS0293919121` | 1 | `03. BBG OCR/XS0293919121/XS0293919121 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability USD 2,000.00 (M) Quick Links Iss Sprd USD (M) 32 ALLQ Pricing Calc Type (198)NO CALC-FLOATERS Min Piece/Increment; recovered numeric candidate: USD 2,000.00 million | Candidate: visual confirmation required |
| `XS0297467705` | 1 | `03. BBG OCR/XS0297467705/XS0297467705 - image-01.txt`: AmtIssued/Outstanding 23) Sustainability USD 5,000.00 (M) Quick Links Iss Sprd USD (M) 3D ALLQ Pricing Calc Type (521)ACCRUED ONLY FLOAT Qt Recap; recovered numeric candidate: USD 5,000.00 million | Candidate: visual confirmation required |
| `XS0298465822` | 0 | No issue-size label found in available OCR | Unavailable: document recovery required |
| `XS0304286924` | 1 | `03. BBG OCR/XS0304286924/XS0304286924 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability USD 10,520.00 (M) Quick Links Iss Sprd USD (M) 3D ALLQ Pricing Calc Type (198)NO CALC-FLOATERS MinPiece/Increment; recovered numeric candidate: USD 10,520.00 million | Candidate: visual confirmation required |
| `XS0314283432` | 1 | `03. BBG OCR/XS0314283432/XS0314283432 - image-01.txt`: Amt Issued/Outstanding 23) Sustainability CALLED 0N 02/02/09@100.00 USD 43,400.00 (M) Quick Links Iss Sprd USD (M) 3D ALLQ Pricing Calc Type (521)ACCRUED ONLY FLOAT; recovered numeric candidate: USD 43,400.00 million | Candidate: visual confirmation required |
| `XS0315745447` | 1 | `03. BBG OCR/XS0315745447/XS0315745447 - image-01.txt`: AmtIssued/Outstanding Quick Links Type Fixed Freq Annual EUR 6,050.00 (M) 32 ALLQ Pricing EUR (M); recovered numeric candidate: EUR 6,050.00 million | Candidate: visual confirmation required |

## Totals

- Portfolio instruments scanned: 29
- Instruments with issue-size label candidates: 24
- Instruments with no available issue-size label: 5
- Confirmed original issue sizes: 0

## Interpretation

- The recovery pass does not convert the existing Trust position-size field into issuance size.
- OCR candidates must be visually checked against the linked Bloomberg image and recorded with the displayed currency and amount.
- Instruments without a candidate require final terms, pricing supplements, listing records, or issuer/custodian recovery.
