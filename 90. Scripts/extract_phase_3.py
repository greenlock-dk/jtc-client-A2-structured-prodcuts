from __future__ import annotations

import hashlib
import os
from io import BytesIO
from pathlib import Path
from zipfile import ZipFile
import posixpath
from xml.etree import ElementTree as ET

from openpyxl import load_workbook
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
WORKBOOK_PATH = ROOT / "Trust ISIN information from Bloomberg.xlsx"
PRODUCT_DIR = ROOT / "01. Structured Products"
EVIDENCE_DIR = ROOT / "02. BBG images"
INVENTORY_PATH = EVIDENCE_DIR / "IMAGE INVENTORY.md"
ISIN_SHEETS = {"Jogger - Tudella 30 June 2009", "ISINs summary", "Bloomberg data >>"}


def image_extension(data: bytes) -> str:
    with Image.open(BytesIO(data)) as image:
        return (image.format or "PNG").lower().replace("jpeg", "jpg")


def markdown_path(path: Path, base: Path = ROOT) -> str:
    return Path(os.path.relpath(path, base)).as_posix().replace(" ", "%20")


def product_document(isin: str) -> Path:
    matches = sorted(PRODUCT_DIR.glob(f"{isin} - *.md"))
    if len(matches) != 1:
        raise FileNotFoundError(f"Expected one product document for {isin}, found {matches}")
    return matches[0]


def replace_evidence_section(path: Path, section: str) -> None:
    marker = "## Evidence Images"
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
    EVIDENCE_DIR.mkdir(exist_ok=True)
    workbook = load_workbook(WORKBOOK_PATH, data_only=True)
    mapped_records = []
    used_hashes = set()

    for worksheet in workbook.worksheets:
        isin = worksheet.title.strip()
        if worksheet.title in ISIN_SHEETS or not isin.startswith(("XS", "CH")):
            continue
        product_dir = EVIDENCE_DIR / isin
        product_dir.mkdir(exist_ok=True)
        links = []
        document_path = product_document(isin)
        for image_number, image in enumerate(worksheet._images, 1):
            data = image._data()
            digest = hashlib.sha256(data).hexdigest()
            used_hashes.add(digest)
            extension = image_extension(data)
            output_path = product_dir / f"{isin} - image-{image_number:02d}.{extension}"
            output_path.write_bytes(data)
            anchor = image.anchor._from
            width = image.width
            height = image.height
            links.append(
                f"| {image_number} | [{output_path.name}]({markdown_path(output_path, document_path.parent)}) | "
                f"{anchor.col + 1} | {anchor.row + 1} | {width} x {height} |"
            )
            mapped_records.append((isin, image_number, output_path, anchor.col + 1, anchor.row + 1, width, height, digest))

        # Two package media files are not attached to a worksheet drawing, but their
        # Bloomberg content identifies XS0765564827. Preserve the content association
        # without fabricating an Excel anchor.
        if isin == "XS0765564827":
            with ZipFile(WORKBOOK_PATH) as archive:
                existing_digests = {record[-1] for record in mapped_records if record[0] == isin}
                for media_name in [
                    "xl/media/image1.png",
                    "xl/media/image2.png",
                ]:
                    data = archive.read(media_name)
                    digest = hashlib.sha256(data).hexdigest()
                    used_hashes.add(digest)
                    if digest in existing_digests:
                        continue
                    image_number = len(links) + 1
                    extension = image_extension(data)
                    output_path = product_dir / f"{isin} - image-{image_number:02d}.{extension}"
                    output_path.write_bytes(data)
                    with Image.open(BytesIO(data)) as extracted:
                        width, height = extracted.size
                    links.append(
                        f"| {image_number} | [{output_path.name}]({markdown_path(output_path, document_path.parent)}) | "
                        f"N/A | N/A | {width} x {height} |"
                    )
                    mapped_records.append((isin, image_number, output_path, "N/A", "N/A", width, height, digest))
                    existing_digests.add(digest)

        evidence_section = [
            "## Evidence Images",
            "",
            f"Images extracted from worksheet `{worksheet.title}`. OCR and interpretation are deferred to Phase 4.",
            "",
            "| Image # | Evidence file | Anchor column | Anchor row | Dimensions |",
            "| --- | --- | ---: | ---: | --- |",
            *links,
            "",
            "Image files are preserved as extracted PNG evidence; filenames identify the ISIN and worksheet image order.",
        ]
        replace_evidence_section(document_path, "\n".join(evidence_section))

    unmapped_records = []
    with ZipFile(WORKBOOK_PATH) as archive:
        package_dir = EVIDENCE_DIR / "_unmapped"
        package_dir.mkdir(exist_ok=True)
        for stale_file in package_dir.glob("*.png"):
            stale_file.unlink()
        for media_name in sorted(name for name in archive.namelist() if name.startswith("xl/media/")):
            data = archive.read(media_name)
            digest = hashlib.sha256(data).hexdigest()
            if digest in used_hashes:
                continue
            extension = image_extension(data)
            output_path = package_dir / f"{Path(media_name).stem}.{extension}"
            output_path.write_bytes(data)
            unmapped_records.append((media_name, output_path, digest))

    inventory_lines = [
        "# BBG Image Inventory",
        "",
        "> Source: `Trust ISIN information from Bloomberg.xlsx`.",
        "> Phase 3 extracts and maps embedded images only. OCR and term-sheet interpretation are deferred to Phase 4.",
        "",
        "## Mapped Worksheet Images",
        "",
        f"- Worksheet-mapped images: {len(mapped_records)}",
        f"- ISIN worksheets with images: {len({record[0] for record in mapped_records})}",
        "",
        "| ISIN | Image # | Evidence file | Anchor column | Anchor row | Dimensions | SHA-256 prefix |",
        "| --- | ---: | --- | ---: | ---: | --- | --- |",
    ]
    inventory_lines.extend(
        f"| `{isin}` | {number} | [{path.name}]({markdown_path(path, INVENTORY_PATH.parent)}) | {column} | {row} | {width} x {height} | `{digest[:12]}` |"
        for isin, number, path, column, row, width, height, digest in mapped_records
    )
    inventory_lines.extend([
        "",
        "## Unmapped Package Media",
        "",
        f"The workbook package contains {len(unmapped_records)} media file(s) without a content or worksheet association. They are preserved without interpretation.",
        "",
        "| Package media | Preserved evidence file | SHA-256 prefix |",
        "| --- | --- | --- |",
    ])
    inventory_lines.extend(
        f"| `{media_name}` | [{path.name}]({markdown_path(path, INVENTORY_PATH.parent)}) | `{digest[:12]}` |"
        for media_name, path, digest in unmapped_records
    )
    INVENTORY_PATH.write_text("\n".join(inventory_lines) + "\n", encoding="utf-8")
    print(f"Extracted {len(mapped_records)} worksheet-mapped images")
    print(f"Preserved {len(unmapped_records)} unmapped package media files")
    print(f"Created {INVENTORY_PATH}")


if __name__ == "__main__":
    main()
