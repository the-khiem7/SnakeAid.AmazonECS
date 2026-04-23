from __future__ import annotations

import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    generators = sorted(ROOT.glob("content/**/_tools/generate_diagrams.py"))
    for generator in generators:
        runpy.run_path(str(generator), run_name="__main__")


if __name__ == "__main__":
    main()
