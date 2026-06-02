"""Download and normalize the selected open-data CSV resource."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
from urllib.request import urlopen


DATASET_URL = (
    "https://data.gov.ua/dataset/7b2cffb7-28f9-488b-85c6-fe364a42adde/"
    "resource/7e10f79a-871f-40f0-874e-6f2ff9da56e3/download/"
    "135-chiselnist-naiavnogo-naselennia-na-pochatok-periodu.csv"
)

RAW_PATH = Path("data/raw/population_raw.csv")
PROCESSED_PATH = Path("data/processed/population.csv")


def decode_response(content: bytes) -> str:
    """Decode the portal CSV, trying UTF-8 first and CP1251 as fallback."""
    for encoding in ("utf-8-sig", "cp1251"):
        try:
            return content.decode(encoding)
        except UnicodeDecodeError:
            continue
    return content.decode("cp1251", errors="replace")


def parse_portal_csv(text: str) -> list[dict[str, str]]:
    """Parse the quoted semicolon rows used by this data.gov.ua resource."""
    rows: list[dict[str, str]] = []

    for raw_line in text.splitlines():
        line = raw_line.strip().strip("\t").strip()
        if not line:
            continue
        if line.startswith('"') and line.endswith('"'):
            line = line[1:-1]

        parts = [part.strip() for part in line.split(";")]
        if len(parts) != 4:
            continue
        if parts[0] in {"code", "коди"}:
            continue

        code, attribute, period, value = parts
        rows.append(
            {
                "code": code,
                "attribute": attribute,
                "period": period,
                "value": value,
            }
        )

    return rows


def write_processed(rows: list[dict[str, str]], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=["code", "attribute", "period", "value"])
        writer.writeheader()
        writer.writerows(rows)


def download_dataset(url: str, raw_path: Path, processed_path: Path) -> int:
    raw_path.parent.mkdir(parents=True, exist_ok=True)
    content = urlopen(url, timeout=30).read()
    raw_path.write_bytes(content)

    rows = parse_portal_csv(decode_response(content))
    write_processed(rows, processed_path)
    return len(rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Download and normalize population data.")
    parser.add_argument("--url", default=DATASET_URL, help="CSV resource URL.")
    parser.add_argument("--raw-path", default=str(RAW_PATH), help="Path for raw downloaded CSV.")
    parser.add_argument(
        "--processed-path",
        default=str(PROCESSED_PATH),
        help="Path for normalized UTF-8 CSV.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    row_count = download_dataset(args.url, Path(args.raw_path), Path(args.processed_path))
    print(f"Saved {row_count} normalized rows to {args.processed_path}")


if __name__ == "__main__":
    main()

