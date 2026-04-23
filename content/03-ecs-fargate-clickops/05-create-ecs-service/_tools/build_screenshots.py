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
        "static/images/aws-console-operations-guide/ECS/2. create-task-definition/ecs-services.png",
        "ecs-service-entry-create-button.webp",
        (20, 120, 1880, 980),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/4. create-service/ecs-services-creation.png",
        "ecs-service-details.webp",
        (20, 90, 1880, 1120),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/4. create-service/ecs-services-creation.png",
        "ecs-service-deployment-configuration.webp",
        (20, 1080, 1880, 2800),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/4. create-service/ecs-services-creation.png",
        "ecs-service-networking.webp",
        (20, 2750, 1880, 4050),
    ),
    (
        "static/images/aws-console-operations-guide/ECS/4. create-service/ecs-services-creation.png",
        "ecs-service-load-balancing.webp",
        (20, 3950, 1880, 6100),
    ),
]


if __name__ == "__main__":
    build_crops(repo_root=REPO_ROOT, output_dir=OUTPUT_DIR, crops=CROPS)
