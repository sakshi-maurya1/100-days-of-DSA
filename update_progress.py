"""
Counts ✅ vs ⬜ in README.md and rewrites the progress bar
between the <!-- PROGRESS-START --> / <!-- PROGRESS-END --> markers.
Run manually with: python scripts/update_progress.py
Also run automatically by .github/workflows/update-progress.yml on every push.
"""

import re
from pathlib import Path

README = Path(__file__).resolve().parent.parent / "README.md"


ROW_RE = re.compile(r"^\|\s*\d+\s*\|.*\|\s*(✅|⬜)\s*\|.*\|\s*$")


def main():
    text = README.read_text(encoding="utf-8")

    start_marker = "<!-- PROGRESS-START -->"
    end_marker = "<!-- PROGRESS-END -->"

    start = text.find(start_marker)
    end = text.find(end_marker)
    if start == -1 or end == -1:
        raise SystemExit("Progress markers not found in README.md")

    before = text[: start + len(start_marker)]
    after = text[end:]

    # Only count actual problem table rows (e.g. "| 1 | Two Sum | Easy | [Link](...) | ✅ | |"),
    # never mentions of the emoji in prose or the bar itself.
    solved = 0
    unsolved = 0
    for line in text.splitlines():
        m = ROW_RE.match(line)
        if m:
            if m.group(1) == "✅":
                solved += 1
            else:
                unsolved += 1
    total = solved + unsolved

    pct = round((solved / total) * 100) if total else 0
    bar_len = 20
    filled = round((pct / 100) * bar_len)
    bar = "🟩" * filled + "⬜" * (bar_len - filled)

    new_block = (
        f"\n**Progress: {solved} / {total} ({pct}%)**\n\n"
        f"{bar}\n"
    )

    new_text = before + new_block + after
    if new_text != text:
        README.write_text(new_text, encoding="utf-8")
        print(f"Updated progress: {solved}/{total} ({pct}%)")
    else:
        print("No change in progress.")


if __name__ == "__main__":
    main()
