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
        "static/images/aws-console-operations-guide/ALB/1. create-application-load-balancer/alb-create-1.png",
        "alb-basic-configuration.webp",
        (30, 110, 1045, 1000),
    ),
    (
        "static/images/aws-console-operations-guide/ALB/1. create-application-load-balancer/alb-create-1.png",
        "alb-network-mapping-subnets.webp",
        (30, 1020, 1045, 1840),
    ),
    (
        "static/images/aws-console-operations-guide/ALB/1. create-application-load-balancer/alb-create-2.png",
        "alb-security-listener-routing.webp",
        (30, 100, 1045, 1500),
    ),
    (
        "static/images/aws-console-operations-guide/ALB/1. create-application-load-balancer/alb-create-3.png",
        "alb-advanced-services.webp",
        (25, 120, 1045, 1020),
    ),
    (
        "static/images/aws-console-operations-guide/ALB/1. create-application-load-balancer/alb-create-3.png",
        "alb-review-summary.webp",
        (25, 1040, 1045, 1650),
    ),
]


if __name__ == "__main__":
    build_crops(repo_root=REPO_ROOT, output_dir=OUTPUT_DIR, crops=CROPS)
