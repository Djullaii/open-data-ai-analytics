import html
import json
import os
import sqlite3
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path


DB_PATH = Path(os.getenv("DB_PATH", "/app/db/population.db"))
REPORTS_DIR = Path(os.getenv("REPORTS_DIR", "/app/reports"))
PORT = int(os.getenv("PORT", "8000"))
START_TIME = time.time()
REQUESTS_TOTAL = 0


def read_json(name):
    path = REPORTS_DIR / name
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def read_svg(name):
    path = REPORTS_DIR / "figures" / name
    if not path.exists():
        return "<p>No figure yet</p>"
    return path.read_text(encoding="utf-8")


def rows_from_db():
    if not DB_PATH.exists():
        return []
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("select period, value from population order by period limit 12").fetchall()
    conn.close()
    return rows


def metrics_text(rows_count):
    uptime = time.time() - START_TIME
    return f"""# HELP open_data_web_requests_total Total HTTP requests handled by the web service.
# TYPE open_data_web_requests_total counter
open_data_web_requests_total {REQUESTS_TOTAL}
# HELP open_data_web_uptime_seconds Web service uptime in seconds.
# TYPE open_data_web_uptime_seconds gauge
open_data_web_uptime_seconds {uptime:.0f}
# HELP open_data_population_rows Number of rows available in the population table.
# TYPE open_data_population_rows gauge
open_data_population_rows {rows_count}
"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global REQUESTS_TOTAL
        REQUESTS_TOTAL += 1

        if self.path == "/metrics":
            rows = rows_from_db()
            data = metrics_text(len(rows)).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return

        quality = read_json("quality_report.json")
        research = read_json("research_report.json")
        rows = rows_from_db()
        table_rows = "".join(f"<tr><td>{html.escape(p)}</td><td>{v}</td></tr>" for p, v in rows)

        body = f"""<!doctype html>
<html lang="uk">
<head>
  <meta charset="utf-8">
  <title>Open Data AI Analytics</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; background: #f7f7f7; color: #222; }}
    section {{ background: white; padding: 18px; margin-bottom: 18px; border: 1px solid #ddd; }}
    table {{ border-collapse: collapse; width: 100%; }}
    td, th {{ border: 1px solid #ddd; padding: 8px; }}
    pre {{ background: #f1f1f1; padding: 12px; overflow: auto; }}
  </style>
</head>
<body>
  <h1>Open Data AI Analytics</h1>
  <section>
    <h2>Дані</h2>
    <table><tr><th>Період</th><th>Значення</th></tr>{table_rows}</table>
  </section>
  <section>
    <h2>Перевірка якості</h2>
    <pre>{html.escape(json.dumps(quality, ensure_ascii=False, indent=2))}</pre>
  </section>
  <section>
    <h2>Дослідження</h2>
    <pre>{html.escape(json.dumps(research, ensure_ascii=False, indent=2))}</pre>
  </section>
  <section>
    <h2>Візуалізації</h2>
    {read_svg("population_trend.svg")}
    {read_svg("monthly_change.svg")}
  </section>
</body>
</html>"""
        data = body.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    HTTPServer(("0.0.0.0", PORT), Handler).serve_forever()
