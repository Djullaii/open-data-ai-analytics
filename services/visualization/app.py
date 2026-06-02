import os
import sqlite3
from pathlib import Path


DB_PATH = Path(os.getenv("DB_PATH", "/app/db/population.db"))
FIGURES_DIR = Path(os.getenv("FIGURES_DIR", "/app/reports/figures"))


def scale(value, source_min, source_max, target_min, target_max):
    if source_max == source_min:
        return (target_min + target_max) / 2
    return target_min + (value - source_min) / (source_max - source_min) * (target_max - target_min)


def line_chart(points, title, path):
    width, height = 900, 430
    left, right, top, bottom = 70, 35, 45, 60
    values = [value for _, value in points]
    min_v, max_v = min(values), max(values)
    plot_w, plot_h = width - left - right, height - top - bottom

    coords = []
    for i, (_, value) in enumerate(points):
        x = scale(i, 0, len(points) - 1, left, left + plot_w)
        y = scale(value, min_v, max_v, top + plot_h, top)
        coords.append((x, y))

    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y in coords)
    labels = f"{points[0][0]} - {points[-1][0]}"
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
<rect width="100%" height="100%" fill="white"/>
<text x="{left}" y="28" font-family="Arial" font-size="20" font-weight="700">{title}</text>
<text x="{left}" y="{height - 18}" font-family="Arial" font-size="13">{labels}</text>
<line x1="{left}" y1="{top + plot_h}" x2="{left + plot_w}" y2="{top + plot_h}" stroke="#555"/>
<line x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" stroke="#555"/>
<polyline points="{polyline}" fill="none" stroke="#1769aa" stroke-width="4" stroke-linejoin="round"/>
</svg>"""
    path.write_text(svg, encoding="utf-8")


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute("select period, value from population order by period").fetchall()
    conn.close()

    points = [(period, float(value)) for period, value in rows]
    changes = [(points[i][0], points[i][1] - points[i - 1][1]) for i in range(1, len(points))]

    line_chart(points, "Population value", FIGURES_DIR / "population_trend.svg")
    line_chart(changes, "Monthly change", FIGURES_DIR / "monthly_change.svg")
    print("figures saved")


if __name__ == "__main__":
    main()

