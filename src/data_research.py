"""Research trends in the normalized population dataset."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path

from data_load import PROCESSED_PATH, download_dataset


RESEARCH_REPORT_PATH = Path("reports/data_research_summary.json")


def ensure_dataset(path: Path) -> None:
    if not path.exists():
        download_dataset(
            url="https://data.gov.ua/dataset/7b2cffb7-28f9-488b-85c6-fe364a42adde/"
            "resource/7e10f79a-871f-40f0-874e-6f2ff9da56e3/download/"
            "135-chiselnist-naiavnogo-naselennia-na-pochatok-periodu.csv",
            raw_path=Path("data/raw/population_raw.csv"),
            processed_path=path,
        )


def load_series(path: Path) -> list[dict[str, object]]:
    with path.open("r", encoding="utf-8", newline="") as file:
        rows = []
        for row in csv.DictReader(file):
            rows.append(
                {
                    "period": datetime.strptime(row["period"], "%Y-%m-%d").date(),
                    "value": float(row["value"]),
                    "attribute": row["attribute"],
                }
            )
    return sorted(rows, key=lambda row: row["period"])


def summarize_series(rows: list[dict[str, object]]) -> dict[str, object]:
    if not rows:
        raise ValueError("Dataset is empty.")

    first = rows[0]
    last = rows[-1]
    values = [float(row["value"]) for row in rows]
    total_change = float(last["value"]) - float(first["value"])
    percent_change = total_change / float(first["value"]) * 100
    monthly_changes = [values[index] - values[index - 1] for index in range(1, len(values))]

    return {
        "attribute": first["attribute"],
        "period_start": str(first["period"]),
        "period_end": str(last["period"]),
        "first_value_thousand": round(float(first["value"]), 2),
        "last_value_thousand": round(float(last["value"]), 2),
        "total_change_thousand": round(total_change, 2),
        "percent_change": round(percent_change, 2),
        "average_monthly_change_thousand": round(sum(monthly_changes) / len(monthly_changes), 2),
        "min_value_thousand": round(min(values), 2),
        "max_value_thousand": round(max(values), 2),
    }


def write_summary(summary: dict[str, object], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize population data trends.")
    parser.add_argument("--data-path", default=str(PROCESSED_PATH), help="Normalized CSV path.")
    parser.add_argument("--report-path", default=str(RESEARCH_REPORT_PATH), help="JSON report path.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    data_path = Path(args.data_path)
    ensure_dataset(data_path)
    summary = summarize_series(load_series(data_path))
    write_summary(summary, Path(args.report_path))
    print(json.dumps(summary, ensure_ascii=True, indent=2))


if __name__ == "__main__":
    main()
