# jtc-client-A2-structured-prodcuts

## Project Scripts

All project automation scripts are kept in `90. Scripts` so the repository root contains only project inputs, outputs, and documentation.

Run a phase script from the repository root with:

```text
python "90. Scripts/<script-name>.py"
```

Current scripts:

- `generate_phase_1_2.py` - generate initial product records
- `extract_phase_3.py` - extract Bloomberg images
- `ocr_phase_4.py` - transcribe extracted images
- `review_phase_4b.py` - create the OCR review layer
- `consolidate_phase_5.py` - consolidate workbook and OCR evidence
- `recover_issue_size.py` - recover issue/outstanding-size candidates from OCR
- `integrate_issue_size.py` - propagate issue-size findings into portfolio tables and dossiers