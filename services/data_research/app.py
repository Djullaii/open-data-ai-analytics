import json
import os
import sqlite3
from pathlib import Path


DB_PATH = Path(os.getenv("DB_PATH", "/app/db/population.db"))
REPORT_PATH = Path(os.getenv("REPORT_PATH", "/app/reports/research_report.json"))


def main():
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("select period, value from population order by period").fetchall()
    conn.close()

    values = [float(row[1]) for row in rows]
    first_period, first_value = rows[0][0], values[0]
    last_period, last_value = rows[-1][0], values[-1]
    changes = [values[i] - values[i - 1] for i in range(1, len(values))]

    report = {
        "period_start": first_period,
        "period_end": last_period,
        "first_value": round(first_value, 2),
        "last_value": round(last_value, 2),
        "min_value": round(min(values), 2),
        "max_value": round(max(values), 2),
        "total_change": round(last_value - first_value, 2),
        "average_monthly_change": round(sum(changes) / len(changes), 2),
    }
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print("research report saved")


if __name__ == "__main__":
    main()

