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
        "static/images/aws-console-operations-guide/ECS/1. create-cluster/ecs-clusters-created.png",
        "task-definition-cluster-created-list.webp",
        (20, 115, 1870, 620),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/2. create-task-definition/task-definition.png",
        "task-definition-list-create-button.webp",
        (360, 95, 1880, 600),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/2. create-task-definition/task-definition-create.png",
        "task-definition-create-top-config.webp",
        (20, 90, 1880, 1550),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/2. create-task-definition/task-definition-create.png",
        "task-definition-create-container-port.webp",
        (20, 1500, 1880, 3050),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/2. create-task-definition/task-definition-create.png",
        "task-definition-create-env-logging.webp",
        (20, 2900, 1880, 4300),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/3. task-definition-results/task-snakeaid-api-rev1.png",
        "task-definition-api-created.webp",
        (20, 110, 1870, 1710),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/3. task-definition-results/task-snakeai.png",
        "task-definition-ai-created.webp",
        (20, 120, 1880, 1750),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/2. create-task-definition/ecs-services.png",
        "task-definition-next-step-services.webp",
        (20, 120, 1880, 980),
    ),
]


if __name__ == "__main__":
    build_crops(repo_root=REPO_ROOT, output_dir=OUTPUT_DIR, crops=CROPS)
