import csv
import json
import os
import sqlite3
from pathlib import Path


CSV_PATH = Path(os.getenv("CSV_PATH", "/app/data/sample_population.csv"))
DB_PATH = Path(os.getenv("DB_PATH", "/app/db/population.db"))
REPORT_PATH = Path(os.getenv("REPORT_PATH", "/app/reports/load_summary.json"))


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("drop table if exists population")
    cur.execute(
        """
        create table population (
            code text,
            attribute text,
            period text,
            value real
        )
        """
    )

    rows = []
    with CSV_PATH.open("r", encoding="utf-8", newline="") as file:
        for row in csv.DictReader(file):
            item = (
                row["code"].strip(),
                row["attribute"].strip(),
                row["period"].strip(),
                float(row["value"]),
            )
            rows.append(item)

    cur.executemany("insert into population values (?, ?, ?, ?)", rows)
    conn.commit()
    conn.close()

    REPORT_PATH.write_text(
        json.dumps({"rows_loaded": len(rows), "database": str(DB_PATH)}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"loaded {len(rows)} rows")


if __name__ == "__main__":
    main()

