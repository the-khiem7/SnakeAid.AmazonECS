from __future__ import annotations

import sys
from pathlib import Path

from diagrams.aws.general import Users
from diagrams.aws.management import ManagementConsole
from diagrams.aws.network import ALB, Endpoint
from diagrams.onprem.container import Docker
from diagrams.aws.compute import Fargate
from diagrams import Cluster, Edge


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from tools.diagram_utils import cluster_style, render_bundle_diagram


BUNDLE_DIR = Path(__file__).resolve().parents[1]


def generate_alb_components_diagram() -> None:
    def builder() -> None:
        client = Users("Client")
        alb = ALB("ALB")
        listener = Endpoint("Listener\nHTTP :80")
        rule = ManagementConsole("Default rule\n/ -> snakeaid-api-tg")
        target_group = Endpoint("Target Group")
        client >> alb >> listener >> rule >> target_group

    render_bundle_diagram(BUNDLE_DIR, "alb-components.png", builder)


def generate_request_routing_diagram() -> None:
    def builder() -> None:
        client = Users("Client")
        alb = ALB("Public ALB")
        target_group = Endpoint("snakeaid-api-tg")
        task = Fargate("Task IP")
        container = Docker("Container :8080")
        client >> alb >> Edge(label="forward") >> target_group >> task >> container

    render_bundle_diagram(BUNDLE_DIR, "request-routing.png", builder)


def generate_network_placement_diagram() -> None:
    def builder() -> None:
        with Cluster("Public subnets in two AZs", graph_attr=cluster_style("#FFF7ED", "#FB923C")):
            alb_a = ALB("ALB subnet A")
            alb_b = ALB("ALB subnet B")
        internet = Users("Public clients")
        internet >> [alb_a, alb_b]

    render_bundle_diagram(BUNDLE_DIR, "network-placement.png", builder)


def generate_empty_target_group_diagram() -> None:
    def builder() -> None:
        alb = ALB("ALB created")
        target_group = Endpoint("Target Group\nTargets = 0")
        service = Fargate("ECS Service\nattach later")
        alb >> Edge(label="cannot forward yet") >> target_group
        service >> Edge(label="registers tasks later") >> target_group

    render_bundle_diagram(BUNDLE_DIR, "empty-target-group-state.png", builder)


def main() -> None:
    generate_alb_components_diagram()
    generate_request_routing_diagram()
    generate_network_placement_diagram()
    generate_empty_target_group_diagram()


if __name__ == "__main__":
    main()
