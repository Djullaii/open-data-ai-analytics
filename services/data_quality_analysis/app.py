import json
import os
import sqlite3
from collections import Counter
from datetime import datetime
from pathlib import Path


DB_PATH = Path(os.getenv("DB_PATH", "/app/db/population.db"))
REPORT_PATH = Path(os.getenv("REPORT_PATH", "/app/reports/quality_report.json"))


def main():
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    rows = conn.execute("select code, attribute, period, value from population").fetchall()
    conn.close()

    missing = {"code": 0, "attribute": 0, "period": 0, "value": 0}
    bad_dates = 0
    bad_values = 0
    records = []

    for row in rows:
        record = dict(row)
        records.append(tuple(record.items()))
        for key in missing:
            if record[key] in ("", None):
                missing[key] += 1
        try:
            datetime.strptime(record["period"], "%Y-%m-%d")
        except ValueError:
            bad_dates += 1
        if record["value"] is None or float(record["value"]) <= 0:
            bad_values += 1

    duplicates = sum(count - 1 for count in Counter(records).values() if count > 1)
    report = {
        "rows_checked": len(rows),
        "missing": missing,
        "duplicates": duplicates,
        "bad_dates": bad_dates,
        "bad_values": bad_values,
        "status": "ok" if duplicates == 0 and bad_dates == 0 and bad_values == 0 and not any(missing.values()) else "check",
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("quality check:", report["status"])


if __name__ == "__main__":
    main()

