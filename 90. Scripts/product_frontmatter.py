from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


FRONTMATTER_DELIMITER = "---"


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    if not text.startswith(f"{FRONTMATTER_DELIMITER}\n"):
        return {}, text
    _, raw_frontmatter, body = text.split(FRONTMATTER_DELIMITER, 2)
    data = yaml.safe_load(raw_frontmatter) or {}
    if not isinstance(data, dict):
        raise ValueError("Product frontmatter must be a mapping")
    return data, body.lstrip("\n")


def with_frontmatter(data: dict[str, Any], body: str) -> str:
    frontmatter = yaml.safe_dump(
        data,
        allow_unicode=False,
        default_flow_style=False,
        sort_keys=False,
    ).rstrip()
    return f"{FRONTMATTER_DELIMITER}\n{frontmatter}\n{FRONTMATTER_DELIMITER}\n\n{body.lstrip()}"


def read_product(path: Path) -> tuple[dict[str, Any], str]:
    return split_frontmatter(path.read_text(encoding="utf-8"))


def write_product(path: Path, data: dict[str, Any], body: str) -> None:
    path.write_text(with_frontmatter(data, body), encoding="utf-8")