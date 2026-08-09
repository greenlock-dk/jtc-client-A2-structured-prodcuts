from __future__ import annotations

import os
from pathlib import Path

from rapidocr_onnxruntime import RapidOCR

ROOT = Path(__file__).resolve().parent.parent
EVIDENCE_DIR = ROOT / "02. BBG images"
OCR_DIR = ROOT / "03. BBG OCR"
PRODUCT_DIR = ROOT / "01. Structured Products"


def relative_link(path: Path, base: Path) -> str:
    return Path(os.path.relpath(path, base)).as_posix().replace(" ", "%20")


def dossier_for(isin: str) -> Path:
    matches = sorted(PRODUCT_DIR.glob(f"{isin} - *.md"))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected one dossier for {isin}, found {matches}")
    return matches[0]


def ocr_image(ocr: RapidOCR, image_path: Path) -> tuple[str, int, float]:
    result, _ = ocr(str(image_path))
    if not result:
        return "", 0, 0.0
    lines = []
    confidences = []
    for item in result:
        text = str(item[1]).strip()
        if text:
            lines.append(text)
            confidences.append(float(item[2]))
    average = sum(confidences) / len(confidences) if confidences else 0.0
    return "\n".join(lines), len(lines), average


def replace_ocr_section(path: Path, section: str) -> None:
    marker = "## OCR Transcription"
    text = path.read_text(encoding="utf-8")
    if marker in text:
        before, after = text.split(marker, 1)
        next_section = after.find("\n## ")
        tail = after[next_section + 1:] if next_section >= 0 else ""
        text = before.rstrip() + "\n\n" + section.rstrip() + "\n"
        if tail:
            text += "\n" + tail.lstrip()
        path.write_text(text, encoding="utf-8")
        return
    path.write_text(text.rstrip() + "\n\n" + section.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    OCR_DIR.mkdir(exist_ok=True)
    for stale_file in (OCR_DIR / "_unmapped").glob("*.txt") if (OCR_DIR / "_unmapped").exists() else []:
        stale_file.unlink()
    ocr = RapidOCR()
    mapped_by_isin: dict[str, list[tuple[Path, Path, int, float, str]]] = {}
    unmapped_records = []
    images = sorted(EVIDENCE_DIR.glob("*/**/*.png"))
    for image_path in images:
        if image_path.parent.name == "_unmapped":
            continue
        isin = image_path.parent.name
        output_dir = OCR_DIR / isin
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{image_path.stem}.txt"
        text, line_count, average_confidence = ocr_image(ocr, image_path)
        output_path.write_text(text + "\n", encoding="utf-8")
        mapped_by_isin.setdefault(isin, []).append((image_path, output_path, line_count, average_confidence, text))

    for image_path in sorted((EVIDENCE_DIR / "_unmapped").glob("*.png")):
        output_dir = OCR_DIR / "_unmapped"
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / f"{image_path.stem}.txt"
        text, line_count, average_confidence = ocr_image(ocr, image_path)
        output_path.write_text(text + "\n", encoding="utf-8")
        unmapped_records.append((image_path, output_path, line_count, average_confidence, text))

    for isin, records in mapped_by_isin.items():
        dossier = dossier_for(isin)
        rows = []
        for number, (image_path, output_path, line_count, confidence, text) in enumerate(records, 1):
            status = "Review required" if confidence < 0.85 else "OCR captured; review required"
            rows.append(
                f"| {number} | [{image_path.name}]({relative_link(image_path, dossier.parent)}) | "
                f"[{output_path.name}]({relative_link(output_path, dossier.parent)}) | {line_count} | {confidence:.1%} | {status} |"
            )
        section = [
            "## OCR Transcription",
            "",
            "Raw OCR is preserved separately from normalized product information. All OCR-derived values require visual review against the source image.",
            "",
            "| Image # | Source image | Raw OCR | Detected lines | Average confidence | Status |",
            "| ---: | --- | --- | ---: | ---: | --- |",
            *rows,
        ]
        replace_ocr_section(dossier, "\n".join(section))

    inventory_path = OCR_DIR / "OCR INVENTORY.md"
    inventory = [
        "# BBG OCR Inventory",
        "",
        "> Phase 4 raw OCR output generated with RapidOCR. OCR is transcription support, not confirmed product evidence.",
        "",
        "## ISIN-Mapped OCR",
        "",
        "| ISIN | Image | Source image | Raw OCR | Detected lines | Average confidence | Status |",
        "| --- | ---: | --- | --- | ---: | ---: | --- |",
    ]
    for isin, records in mapped_by_isin.items():
        for number, (image_path, output_path, line_count, confidence, _) in enumerate(records, 1):
            status = "Review required" if confidence < 0.85 else "OCR captured; review required"
            inventory.append(
                f"| `{isin}` | {number} | [{image_path.name}]({relative_link(image_path, inventory_path.parent)}) | "
                f"[{output_path.name}]({relative_link(output_path, inventory_path.parent)}) | {line_count} | {confidence:.1%} | {status} |"
            )
    inventory.extend([
        "",
        "## Unmapped OCR",
        "",
        "These images remain unassigned to an ISIN. OCR may provide identification clues, but no automatic reassignment is made.",
        "",
        "| Source image | Raw OCR | Detected lines | Average confidence | Status |",
        "| --- | --- | ---: | ---: | --- |",
    ])
    for image_path, output_path, line_count, confidence, _ in unmapped_records:
        inventory.append(
            f"| [{image_path.name}]({relative_link(image_path, inventory_path.parent)}) | "
            f"[{output_path.name}]({relative_link(output_path, inventory_path.parent)}) | {line_count} | {confidence:.1%} | Unmapped; review required |"
        )
    inventory_path.write_text("\n".join(inventory) + "\n", encoding="utf-8")
    print(f"OCR processed {sum(len(records) for records in mapped_by_isin.values())} mapped images")
    print(f"OCR processed {len(unmapped_records)} unmapped images")
    print(f"Created {OCR_DIR}")


if __name__ == "__main__":
    main()
