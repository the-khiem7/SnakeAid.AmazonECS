#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SECTION_TOOLS_DIR = SCRIPT_DIR.parents[1] / "_tools"
REPO_ROOT = SCRIPT_DIR.parents[3]
OUTPUT_DIR = SCRIPT_DIR.parent / "_diagrams"

sys.path.insert(0, str(SECTION_TOOLS_DIR))

from screenshot_utils import build_crops  # noqa: E402


CROPS = [
    (
        "static/images/aws-console-operations-guide/ALB/2. create-target-group/target-group-create-1.png",
        "target-group-settings.webp",
        (15, 100, 735, 1380),
    ),
    (
        "static/images/aws-console-operations-guide/ALB/2. create-target-group/target-group-create-2.png",
        "target-group-register-targets-empty.webp",
        (220, 110, 1890, 950),
    ),
    (
        "static/images/aws-console-operations-guide/ALB/2. create-target-group/target-group-create-3.png",
        "target-group-review-health-check.webp",
        (350, 150, 1870, 720),
    ),
    (
        "static/images/aws-console-operations-guide/ALB/2. create-target-group/target-group-create-3.png",
        "target-group-review-zero-targets.webp",
        (350, 730, 1870, 1000),
    ),
]


if __name__ == "__main__":
    build_crops(repo_root=REPO_ROOT, output_dir=OUTPUT_DIR, crops=CROPS)
