"""Run basic quality checks for the normalized population dataset."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from datetime import datetime
from pathlib import Path

from data_load import PROCESSED_PATH, download_dataset


QUALITY_REPORT_PATH = Path("reports/data_quality_report.json")


def ensure_dataset(path: Path) -> None:
    if not path.exists():
        download_dataset(
            url="https://data.gov.ua/dataset/7b2cffb7-28f9-488b-85c6-fe364a42adde/"
            "resource/7e10f79a-871f-40f0-874e-6f2ff9da56e3/download/"
            "135-chiselnist-naiavnogo-naselennia-na-pochatok-periodu.csv",
            raw_path=Path("data/raw/population_raw.csv"),
            processed_path=path,
        )


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def analyze_quality(rows: list[dict[str, str]]) -> dict[str, object]:
    fields = ["code", "attribute", "period", "value"]
    missing_by_column = {
        field: sum(1 for row in rows if not (row.get(field) or "").strip()) for field in fields
    }

    duplicate_count = sum(count - 1 for count in Counter(tuple(row.items()) for row in rows).values() if count > 1)

    invalid_dates = []
    non_numeric_values = []
    non_positive_values = []

    for index, row in enumerate(rows, start=1):
        try:
            datetime.strptime(row["period"], "%Y-%m-%d")
        except ValueError:
            invalid_dates.append(index)

        try:
            value = float(row["value"])
        except ValueError:
            non_numeric_values.append(index)
            continue

        if value <= 0:
            non_positive_values.append(index)

    return {
        "row_count": len(rows),
        "missing_by_column": missing_by_column,
        "duplicate_rows": duplicate_count,
        "invalid_date_rows": invalid_dates,
        "non_numeric_value_rows": non_numeric_values,
        "non_positive_value_rows": non_positive_values,
        "quality_status": "passed"
        if not any(missing_by_column.values())
        and duplicate_count == 0
        and not invalid_dates
        and not non_numeric_values
        and not non_positive_values
        else "review_required",
    }


def write_report(report: dict[str, object], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze normalized dataset quality.")
    parser.add_argument("--data-path", default=str(PROCESSED_PATH), help="Normalized CSV path.")
    parser.add_argument("--report-path", default=str(QUALITY_REPORT_PATH), help="JSON report path.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    data_path = Path(args.data_path)
    ensure_dataset(data_path)
    report = analyze_quality(load_rows(data_path))
    write_report(report, Path(args.report_path))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

