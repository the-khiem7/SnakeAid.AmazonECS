from __future__ import annotations

import sys
from pathlib import Path

from diagrams import Cluster, Edge
from diagrams.aws.compute import ElasticContainerServiceService, ElasticContainerServiceTask, Fargate
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import ALB, Endpoint, PublicSubnet, VPC
from diagrams.onprem.container import Docker


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from tools.diagram_utils import cluster_style, render_bundle_diagram


BUNDLE_DIR = Path(__file__).resolve().parents[1]


def generate_service_orchestration_diagram() -> None:
    def builder() -> None:
        service = ElasticContainerServiceService("ECS Service\nDesired tasks = 1")
        task_running = Fargate("Healthy task")
        task_replace = Fargate("Replacement task")
        service >> task_running
        service >> Edge(style="dashed", label="if unhealthy") >> task_replace

    render_bundle_diagram(BUNDLE_DIR, "service-orchestration.png", builder)


def generate_alb_binding_diagram() -> None:
    def builder() -> None:
        alb = ALB("ALB :80")
        target_group = Endpoint("snakeaid-api-tg")
        service = ElasticContainerServiceService("snakeaid-api-service")
        task = Fargate("Task")
        container = Docker("snakeaid-api :8080")
        alb >> target_group >> service >> task >> container

    render_bundle_diagram(BUNDLE_DIR, "alb-binding.png", builder)


def generate_rolling_update_diagram() -> None:
    def builder() -> None:
        old_task = Fargate("Old task\nrev N")
        new_task = Fargate("New task\nrev N+1")
        health = Cloudwatch("Health check passes")
        drain = ElasticContainerServiceTask("Old task drained")
        old_task >> Edge(label="deploy") >> new_task >> health >> drain

    render_bundle_diagram(BUNDLE_DIR, "rolling-update.png", builder)


def generate_network_placement_diagram() -> None:
    def builder() -> None:
        vpc = VPC("VPC")
        with Cluster("Service placement", graph_attr=cluster_style("#F8FAFC", "#94A3B8")):
            with Cluster("Subnet A", graph_attr=cluster_style("#EFF6FF", "#3B82F6")):
                subnet_a = PublicSubnet("Subnet A")
                task_a = Fargate("Task A")
            with Cluster("Subnet B", graph_attr=cluster_style("#FFF7ED", "#FB923C")):
                subnet_b = PublicSubnet("Subnet B")
                task_b = Fargate("Task B")
        alb = ALB("Public ALB")
        vpc >> [subnet_a, subnet_b]
        subnet_a >> task_a
        subnet_b >> task_b
        alb >> [task_a, task_b]

    render_bundle_diagram(BUNDLE_DIR, "network-placement.png", builder)


def generate_service_runtime_stack_diagram() -> None:
    def builder() -> None:
        alb = ALB("snakeaid-alb\n:80")
        target_group = Endpoint("snakeaid-api-tg")
        service = ElasticContainerServiceService("snakeaid-api-service")
        task = Fargate("Fargate task")
        container = Docker("Container\n:8080")
        alb >> target_group >> service >> task >> container

    render_bundle_diagram(BUNDLE_DIR, "service-runtime-stack.png", builder)


def main() -> None:
    generate_service_orchestration_diagram()
    generate_alb_binding_diagram()
    generate_rolling_update_diagram()
    generate_network_placement_diagram()
    generate_service_runtime_stack_diagram()


if __name__ == "__main__":
    main()
