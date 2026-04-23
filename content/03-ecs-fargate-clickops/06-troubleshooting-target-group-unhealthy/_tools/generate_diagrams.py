from __future__ import annotations

import sys
from pathlib import Path

from diagrams import Edge
from diagrams.aws.compute import Fargate
from diagrams.aws.network import ALB, Endpoint


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from tools.diagram_utils import render_bundle_diagram


BUNDLE_DIR = Path(__file__).resolve().parents[1]


def generate_troubleshooting_order_diagram() -> None:
    def builder() -> None:
        target_group = Endpoint("Target Group\ncheck live IP")
        registration = Endpoint("Registration\nremove stale targets")
        security = Endpoint("Security group\npath")
        grace = ALB("Grace period\nstartup timing")
        task = Fargate("Healthy task")

        target_group >> Edge(label="then") >> registration >> Edge(label="then") >> security >> Edge(label="then") >> grace >> Edge(
            label="result"
        ) >> task

    render_bundle_diagram(BUNDLE_DIR, "troubleshooting-order.png", builder)


def main() -> None:
    generate_troubleshooting_order_diagram()


if __name__ == "__main__":
    main()
