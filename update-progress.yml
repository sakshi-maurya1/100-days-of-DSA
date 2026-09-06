name: Update DSA Progress

on:
  push:
    branches: [main]
    paths:
      - "README.md"

permissions:
  contents: write

jobs:
  update-progress:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Recalculate progress bar
        run: python scripts/update_progress.py

      - name: Commit updated README if changed
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "github-actions[bot]@users.noreply.github.com"
          git add README.md
          git diff --cached --quiet || git commit -m "chore: auto-update DSA progress bar"
          git push
