from __future__ import annotations

import sys
from pathlib import Path

from diagrams import Edge
from diagrams.aws.compute import ElasticContainerServiceService, Fargate
from diagrams.aws.management import Cloudwatch, ManagementConsole
from diagrams.aws.network import ALB, Endpoint
from diagrams.onprem.container import Docker


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from tools.diagram_utils import render_bundle_diagram


BUNDLE_DIR = Path(__file__).resolve().parents[1]


def generate_health_check_diagram() -> None:
    def builder() -> None:
        alb = ALB("ALB")
        target_group = Endpoint("Target Group\nHTTP :8080")
        task = Fargate("Task IP")
        health = Cloudwatch("Health check\n/health -> 200 OK")
        alb >> Edge(label="health check") >> target_group >> task >> health

    render_bundle_diagram(BUNDLE_DIR, "health-check.png", builder)


def generate_auto_registration_diagram() -> None:
    def builder() -> None:
        service = ElasticContainerServiceService("ECS Service")
        task = Fargate("New Task IP")
        target_group = Endpoint("Target Group")
        review = ManagementConsole("Register targets screen\ncan stay at 0")
        service >> Edge(label="starts") >> task >> Edge(label="auto-registers") >> target_group
        review >> Edge(style="dotted", label="later replaced by service runtime") >> target_group

    render_bundle_diagram(BUNDLE_DIR, "auto-registration.png", builder)


def generate_port_alignment_diagram() -> None:
    def builder() -> None:
        listener = Endpoint("ALB Listener\n:80")
        target_group = Endpoint("Target Group\n:8080")
        container = Docker("Container\n:8080")
        listener >> target_group >> Edge(label="must match") >> container

    render_bundle_diagram(BUNDLE_DIR, "port-alignment.png", builder)


def main() -> None:
    generate_health_check_diagram()
    generate_auto_registration_diagram()
    generate_port_alignment_diagram()


if __name__ == "__main__":
    main()
