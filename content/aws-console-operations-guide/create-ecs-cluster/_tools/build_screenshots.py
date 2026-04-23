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
        "static/images/aws-console-operations-guide/ECS/1. create-cluster/create-ecs-cluster.png",
        "ecs-cluster-form-name-infrastructure.webp",
        (20, 90, 1880, 760),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/1. create-cluster/create-ecs-cluster.png",
        "ecs-cluster-form-monitoring.webp",
        (20, 700, 1880, 1450),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/1. create-cluster/create-ecs-cluster.png",
        "ecs-cluster-form-encryption-tags.webp",
        (20, 1420, 1880, 2210),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/1. create-cluster/ecs-clusters-created.png",
        "ecs-cluster-created-list.webp",
        (20, 115, 1870, 620),
    ),
]


if __name__ == "__main__":
    build_crops(repo_root=REPO_ROOT, output_dir=OUTPUT_DIR, crops=CROPS)
