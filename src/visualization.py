"""Create an SVG line chart for the population time series."""

from __future__ import annotations

import argparse
from pathlib import Path

from data_load import PROCESSED_PATH
from data_research import ensure_dataset, load_series


FIGURE_PATH = Path("reports/figures/population_trend.svg")


def scale(value: float, source_min: float, source_max: float, target_min: float, target_max: float) -> float:
    if source_max == source_min:
        return (target_min + target_max) / 2
    ratio = (value - source_min) / (source_max - source_min)
    return target_min + ratio * (target_max - target_min)


def build_svg(points: list[tuple[str, float]], output_path: Path) -> None:
    width = 960
    height = 540
    margin_left = 80
    margin_right = 40
    margin_top = 40
    margin_bottom = 80

    values = [value for _, value in points]
    min_value = min(values)
    max_value = max(values)
    plot_width = width - margin_left - margin_right
    plot_height = height - margin_top - margin_bottom

    coordinates = []
    for index, (_, value) in enumerate(points):
        x = scale(index, 0, len(points) - 1, margin_left, margin_left + plot_width)
        y = scale(value, min_value, max_value, margin_top + plot_height, margin_top)
        coordinates.append((x, y))

    polyline = " ".join(f"{x:.1f},{y:.1f}" for x, y in coordinates)
    first_period, first_value = points[0]
    last_period, last_value = points[-1]

    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="100%" height="100%" fill="#ffffff"/>
  <text x="{margin_left}" y="28" font-family="Arial" font-size="22" font-weight="700">Population trend from Data.gov.ua</text>
  <line x1="{margin_left}" y1="{margin_top + plot_height}" x2="{margin_left + plot_width}" y2="{margin_top + plot_height}" stroke="#444" stroke-width="1"/>
  <line x1="{margin_left}" y1="{margin_top}" x2="{margin_left}" y2="{margin_top + plot_height}" stroke="#444" stroke-width="1"/>
  <text x="20" y="{margin_top + 12}" font-family="Arial" font-size="13" fill="#333">{max_value:.1f}k</text>
  <text x="20" y="{margin_top + plot_height}" font-family="Arial" font-size="13" fill="#333">{min_value:.1f}k</text>
  <text x="{margin_left}" y="{height - 35}" font-family="Arial" font-size="13" fill="#333">{first_period}</text>
  <text x="{margin_left + plot_width - 70}" y="{height - 35}" font-family="Arial" font-size="13" fill="#333">{last_period}</text>
  <polyline points="{polyline}" fill="none" stroke="#1769aa" stroke-width="4" stroke-linejoin="round" stroke-linecap="round"/>
  <circle cx="{coordinates[0][0]:.1f}" cy="{coordinates[0][1]:.1f}" r="5" fill="#1769aa"/>
  <circle cx="{coordinates[-1][0]:.1f}" cy="{coordinates[-1][1]:.1f}" r="5" fill="#1769aa"/>
  <text x="{margin_left + 10}" y="{margin_top + 35}" font-family="Arial" font-size="14" fill="#1769aa">Start: {first_value:.1f}k</text>
  <text x="{margin_left + plot_width - 150}" y="{margin_top + plot_height - 20}" font-family="Arial" font-size="14" fill="#1769aa">End: {last_value:.1f}k</text>
</svg>
"""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(svg, encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Create a population trend SVG chart.")
    parser.add_argument("--data-path", default=str(PROCESSED_PATH), help="Normalized CSV path.")
    parser.add_argument("--figure-path", default=str(FIGURE_PATH), help="SVG output path.")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    data_path = Path(args.data_path)
    ensure_dataset(data_path)
    rows = load_series(data_path)
    points = [(str(row["period"]), float(row["value"])) for row in rows]
    build_svg(points, Path(args.figure_path))
    print(f"Saved SVG chart to {args.figure_path}")


if __name__ == "__main__":
    main()

