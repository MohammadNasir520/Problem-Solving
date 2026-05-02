#!/usr/bin/env python3
import datetime
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

START_MARKER = "<!-- DAILY-LOG:START -->"
END_MARKER = "<!-- DAILY-LOG:END -->"

DAY_DIR_RE = re.compile(r"^day(\d+)-(\d{2}:\d{2}:\d{4})$")
CF_URL_RE = re.compile(r"codeforces\.com/problemset/problem/(\d+)/([A-Z]\d*)", re.IGNORECASE)


def read_question(day_dir: Path) -> str:
    question_path = day_dir / "question.txt"
    if not question_path.exists():
        return "N/A"
    return question_path.read_text(encoding="utf-8").strip() or "N/A"


def problem_cell(url: str) -> str:
    if url == "N/A":
        return "N/A"
    match = CF_URL_RE.search(url)
    if match:
        name = f"{match.group(1)}{match.group(2)}"
        return f"[{name}]({url})"
    return f"[Problem]({url})"


def as_link(path: str) -> str:
    return f"[{Path(path).name}]({path})" if path != "N/A" else "N/A"


def build_rows() -> list[str]:
    rows = []
    for entry in sorted(ROOT.iterdir()):
        if not entry.is_dir():
            continue
        match = DAY_DIR_RE.match(entry.name)
        if not match:
            continue
        day_num = int(match.group(1))
        date_str = match.group(2)
        url = read_question(entry)
        solutions = sorted(entry.glob("*.cpp"))
        solution = solutions[0].relative_to(ROOT).as_posix() if solutions else "N/A"
        input_file = entry / "input.txt"
        output_file = entry / "output.txt"
        input_path = input_file.relative_to(ROOT).as_posix() if input_file.exists() else "N/A"
        output_path = output_file.relative_to(ROOT).as_posix() if output_file.exists() else "N/A"

        folder_link = f"[Day {day_num}]({entry.name}/)"
        rows.append((
            day_num,
            f"| {folder_link} | {date_str} | {problem_cell(url)} | {as_link(solution)} | {as_link(input_path)} | {as_link(output_path)} |",
        ))

    rows.sort(key=lambda r: r[0])
    return [row for _, row in rows]


def render_log() -> str:
    today = datetime.date.today().strftime("%d %b %Y")
    rows = build_rows()
    total = len(rows)
    if not rows:
        rows = ["| - | - | - | - | - | - |"]

    header = [
        START_MARKER,
        f"**Total problems solved: {total}** &nbsp;|&nbsp; Last updated: {today}",
        "",
        "| Day | Date | Problem | Solution | Input | Output |",
        "| :-: | :--: | ------- | -------- | :---: | :----: |",
    ]
    footer = [END_MARKER]
    return "\n".join(header + rows + footer)


def update_readme() -> None:
    content = README.read_text(encoding="utf-8")
    if START_MARKER not in content or END_MARKER not in content:
        raise SystemExit("Daily log markers not found in README.md")

    pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    new_content = pattern.sub(render_log(), content)
    README.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
