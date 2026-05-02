#!/usr/bin/env python3
import datetime
import os
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

START_MARKER = "<!-- DAILY-LOG:START -->"
END_MARKER = "<!-- DAILY-LOG:END -->"
SUMMARY_START = "<!-- SUMMARY:START -->"
SUMMARY_END = "<!-- SUMMARY:END -->"

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
    if not url.startswith("http"):
        return url
    match = CF_URL_RE.search(url)
    if match:
        name = f"{match.group(1)}{match.group(2)}"
        return f"[{name}]({url})"
    return f"[Problem]({url})"


def as_link(path: str) -> str:
    return f"[{Path(path).name}]({path})" if path != "N/A" else "N/A"


def build_entries() -> list[dict]:
    entries = []
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
        entries.append({
            "day_num": day_num,
            "date_str": date_str,
            "url": url,
            "solution": solution,
            "input_path": input_path,
            "output_path": output_path,
            "folder": entry.name,
        })
    entries.sort(key=lambda e: e["day_num"])
    return entries


def build_rows() -> list[str]:
    rows = []
    for e in build_entries():
        folder_link = f"[Day {e['day_num']}]({e['folder']}/)"
        rows.append(
            f"| {folder_link} | {e['date_str']} | {problem_cell(e['url'])} "
            f"| {as_link(e['solution'])} | {as_link(e['input_path'])} | {as_link(e['output_path'])} |"
        )
    return rows


def render_summary() -> str:
    entries = build_entries()
    total = len(entries)
    days_active = len({e["date_str"] for e in entries})
    cf_count = sum(1 for e in entries if CF_URL_RE.search(e["url"]))
    lines = [
        SUMMARY_START,
        f"| Total Problems Solved | Days Active | Codeforces Problems |",
        f"| :-------------------: | :---------: | :-----------------: |",
        f"| {total} | {days_active} | {cf_count} |",
        SUMMARY_END,
    ]
    return "\n".join(lines)


def render_log() -> str:
    today = datetime.date.today().strftime("%d %b %Y")
    rows = build_rows()
    total = len(rows)
    if not rows:
        rows = ["| - | - | - | - | - | - |"]

    header = [
        START_MARKER,
        f"Last updated: {today}",
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

    log_pattern = re.compile(
        re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
        re.DOTALL,
    )
    new_content = log_pattern.sub(render_log(), content)

    if SUMMARY_START in new_content and SUMMARY_END in new_content:
        summary_pattern = re.compile(
            re.escape(SUMMARY_START) + r".*?" + re.escape(SUMMARY_END),
            re.DOTALL,
        )
        new_content = summary_pattern.sub(render_summary(), new_content)

    README.write_text(new_content, encoding="utf-8")


if __name__ == "__main__":
    update_readme()
