from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run(command: list[str]) -> None:
    print(f"Running: {' '.join(command)}")
    subprocess.run(command, cwd=ROOT, check=True)


def main() -> None:
    python = sys.executable
    run([python, "scripts/generate_data.py"])
    run([python, "scripts/analyze_operations.py"])
    print("Pipeline complete. Start the dashboard with: python3 -m http.server 8000")


if __name__ == "__main__":
    main()

