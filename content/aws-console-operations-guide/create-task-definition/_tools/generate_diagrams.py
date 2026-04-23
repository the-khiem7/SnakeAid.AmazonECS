from __future__ import annotations

import sys
from pathlib import Path

from diagrams import Cluster, Edge
from diagrams.aws.compute import Compute, ECS, ElasticContainerServiceService, ElasticContainerServiceTask, Fargate
from diagrams.aws.management import CloudwatchLogs
from diagrams.aws.network import Endpoint
from diagrams.aws.security import IAMRole
from diagrams.aws.management import ParameterStore
from diagrams.onprem.container import Docker


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from tools.diagram_utils import cluster_style, render_bundle_diagram


BUNDLE_DIR = Path(__file__).resolve().parents[1]


def generate_task_definition_anatomy_diagram() -> None:
    def builder() -> None:
        taskdef = ElasticContainerServiceTask("Task Definition")
        family = ECS("Family\nsnakeaid-api")
        image = Docker("Image\nDocker Hub")
        sizing = Compute("CPU / Memory")
        port = Endpoint("Port\n8080")
        env = ParameterStore("Environment\nDOPPLER + MQ host")
        logs = CloudwatchLogs("awslogs")
        taskdef >> [family, image, sizing, port, env, logs]

    render_bundle_diagram(BUNDLE_DIR, "task-definition-anatomy.png", builder, direction="TB")


def generate_task_runtime_mapping_diagram() -> None:
    def builder() -> None:
        taskdef = ElasticContainerServiceTask("Task Definition\nblueprint")
        service = ElasticContainerServiceService("ECS Service\ncontroller")
        task = Fargate("Running Task")
        container = Docker("Container")
        taskdef >> Edge(label="used by") >> service >> Edge(label="launches") >> task >> container

    render_bundle_diagram(BUNDLE_DIR, "task-to-runtime.png", builder)


def generate_task_profiles_diagram() -> None:
    def builder() -> None:
        with Cluster("snakeaid-api profile", graph_attr=cluster_style("#EFF6FF", "#3B82F6")):
            api_image = Docker("thekhiem7/snakeaid-api:latest")
            api_cfg = Compute("Port 8080\n0.5 vCPU\n1 GB RAM")
        with Cluster("snakeai profile", graph_attr=cluster_style("#FFF7ED", "#FB923C")):
            ai_image = Docker("thekhiem7/snakeaid-snake-detection-ai:8")
            ai_cfg = Compute("Port 8000\n1 vCPU\n2 GB RAM")
        api_image >> api_cfg
        ai_image >> ai_cfg

    render_bundle_diagram(BUNDLE_DIR, "task-profiles.png", builder)


def generate_iam_roles_diagram() -> None:
    def builder() -> None:
        execution_role = IAMRole("Execution role")
        task_role = IAMRole("Task role")
        task = Fargate("Running Task")
        registry = Docker("Pull image")
        logs = CloudwatchLogs("Write logs")
        runtime = ParameterStore("Runtime AWS access")
        execution_role >> [registry, logs]
        task_role >> runtime
        [execution_role, task_role] >> task

    render_bundle_diagram(BUNDLE_DIR, "iam-roles.png", builder)


def main() -> None:
    generate_task_definition_anatomy_diagram()
    generate_task_runtime_mapping_diagram()
    generate_task_profiles_diagram()
    generate_iam_roles_diagram()


if __name__ == "__main__":
    main()
