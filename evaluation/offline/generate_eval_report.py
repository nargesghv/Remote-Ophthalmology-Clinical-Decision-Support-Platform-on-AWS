from __future__ import annotations

from pathlib import Path
import json


def write_report(path: str, title: str, content: dict) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(
        "# " + title + "\n\n```json\n" + json.dumps(content, indent=2) + "\n```\n",
        encoding="utf-8",
    )


def main():
    write_report(
        "evaluation/reports/model_reports/demo_report.md",
        "Demo Evaluation Report",
        {"status": "ok", "message": "Replace with real evaluation results."},
    )
    print("Wrote evaluation/reports/model_reports/demo_report.md")


if __name__ == "__main__":
    main()
