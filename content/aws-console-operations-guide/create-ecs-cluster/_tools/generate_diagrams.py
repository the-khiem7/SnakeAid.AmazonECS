from __future__ import annotations

import sys
from pathlib import Path

from diagrams import Cluster
from diagrams.aws.compute import ElasticContainerServiceService, Fargate
from diagrams.aws.integration import MQ
from diagrams.aws.network import ALB


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from tools.diagram_utils import cluster_style, render_bundle_diagram


BUNDLE_DIR = Path(__file__).resolve().parents[1]


def generate_cluster_scope_diagram() -> None:
    def builder() -> None:
        with Cluster(
            "ECS Cluster = logical container for runtime resources",
            graph_attr=cluster_style("#EFF6FF", "#3B82F6"),
        ):
            service_api = ElasticContainerServiceService("Service\nsnakeaid-api-service")
            service_ai = ElasticContainerServiceService("Service\nsnakeai-service")
            task_api = Fargate("Task")
            task_ai = Fargate("Task")
            service_api >> task_api
            service_ai >> task_ai

    render_bundle_diagram(BUNDLE_DIR, "cluster-scope.png", builder)


def generate_cluster_in_context_diagram() -> None:
    def builder() -> None:
        alb = ALB("ALB")
        with Cluster("snakeaid-backup-cluster", graph_attr=cluster_style("#EFF6FF", "#3B82F6")):
            service_api = ElasticContainerServiceService("API Service")
            service_ai = ElasticContainerServiceService("AI Service")
        mq = MQ("Amazon MQ")
        alb >> [service_api, service_ai]
        service_api >> mq

    render_bundle_diagram(BUNDLE_DIR, "cluster-in-context.png", builder)


def main() -> None:
    generate_cluster_scope_diagram()
    generate_cluster_in_context_diagram()


if __name__ == "__main__":
    main()
