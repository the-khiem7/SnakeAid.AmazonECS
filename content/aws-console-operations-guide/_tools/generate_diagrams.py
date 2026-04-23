from __future__ import annotations

import sys
from pathlib import Path

from diagrams import Edge
from diagrams.aws.compute import ECS, ElasticContainerServiceService, ElasticContainerServiceTask, Fargate
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import ALB, Endpoint
from diagrams.onprem.container import Docker


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.diagram_utils import render_bundle_diagram


BUNDLE_DIR = Path(__file__).resolve().parents[1]


def generate_runtime_mental_model_diagram() -> None:
    def builder() -> None:
        cluster = ECS("ECS Cluster\nsnakeaid-backup-cluster")
        service = ElasticContainerServiceService("ECS Service\nsnakeaid-api-service")
        taskdef = ElasticContainerServiceTask("Task Definition\nsnakeaid-api")
        task = Fargate("Running Task")
        alb = ALB("Application Load Balancer")
        target_group = Endpoint("Target Group\nsnakeaid-api-tg")
        container = Docker("Container\n:8080")

        alb >> target_group >> service >> task
        taskdef >> Edge(label="template for") >> service
        cluster >> Edge(label="contains") >> service
        task >> container

    render_bundle_diagram(BUNDLE_DIR, "runtime-mental-model.png", builder)


def generate_console_workflow_diagram() -> None:
    def builder() -> None:
        cluster = ECS("1. Create\nCluster")
        taskdef = ElasticContainerServiceTask("2. Create\nTask Definitions")
        alb = ALB("3. Create\nALB")
        target_group = Endpoint("4. Create\nTarget Group")
        service = ElasticContainerServiceService("5. Create\nECS Service")
        validate = Cloudwatch("6. Validate\nHealth + Routing")
        cluster >> taskdef >> alb >> target_group >> service >> validate

    render_bundle_diagram(BUNDLE_DIR, "console-workflow.png", builder, graph_attr={"nodesep": "0.9"})


def generate_resource_dependency_diagram() -> None:
    def builder() -> None:
        cluster = ECS("Cluster")
        taskdef = ElasticContainerServiceTask("Task Definition")
        service = ElasticContainerServiceService("Service")
        alb = ALB("ALB")
        target_group = Endpoint("Target Group")
        task = Fargate("Task IP")

        cluster >> service
        taskdef >> Edge(label="selected by") >> service
        alb >> target_group
        service >> Edge(label="registers") >> task
        task >> Edge(label="added to") >> target_group

    render_bundle_diagram(BUNDLE_DIR, "resource-dependency.png", builder)


def main() -> None:
    generate_runtime_mental_model_diagram()
    generate_console_workflow_diagram()
    generate_resource_dependency_diagram()


if __name__ == "__main__":
    main()
