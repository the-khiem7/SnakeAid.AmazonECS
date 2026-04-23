from __future__ import annotations

import sys
from pathlib import Path

import diagrams
from diagrams import Cluster, Edge
from diagrams.aws.compute import Compute, ECS, ElasticContainerServiceService, ElasticContainerServiceTask, Fargate
from diagrams.aws.management import CloudwatchLogs
from diagrams.aws.network import Endpoint
from diagrams.aws.security import IAMRole
from diagrams.aws.management import ParameterStore
from graphviz import Digraph
from diagrams.onprem.container import Docker


ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT))

from tools.diagram_utils import cluster_style, render_bundle_diagram


BUNDLE_DIR = Path(__file__).resolve().parents[1]


def _diagrams_root() -> Path:
    return Path(diagrams.__file__).resolve().parent.parent


def _icon_path(node_cls: type) -> str:
    return str(_diagrams_root() / node_cls._icon_dir / node_cls._icon)


def generate_task_definition_anatomy_diagram() -> None:
    output = BUNDLE_DIR / "_diagrams" / "task-definition-anatomy"
    dot = Digraph(format="png")
    dot.attr(rankdir="TB", bgcolor="white", pad="0.35", nodesep="0.55", ranksep="0.85", splines="line")
    dot.attr(
        "node",
        shape="box",
        style="rounded",
        fixedsize="true",
        imagescale="true",
        labelloc="b",
        fontname="Sans-Serif",
        fontsize="13",
        fontcolor="#2D3436",
        width="1.4",
        height="1.4",
    )
    dot.attr("edge", color="#64748B", penwidth="1.6", arrowsize="0.8")

    dot.node("taskdef", "\nTask Definition", image=_icon_path(ElasticContainerServiceTask), shape="none", height="2.2")
    dot.node("family", "\nFamily\nsnakeaid-api", image=_icon_path(ECS), shape="none", height="2.2")
    dot.node("image", "\nImage\nDocker Hub", image=_icon_path(Docker), shape="none", height="2.2")
    dot.node("size", "\nCPU / Memory", image=_icon_path(Compute), shape="none", height="2.2")
    dot.node("port", "\nPort\n8080", image=_icon_path(Endpoint), shape="none", height="2.2")
    dot.node("env", "\nEnvironment\nDOPPLER + MQ host", image=_icon_path(ParameterStore), shape="none", height="2.25")
    dot.node("logs", "\nawslogs", image=_icon_path(CloudwatchLogs), shape="none", height="2.2")

    with dot.subgraph() as s:
        s.attr(rank="same")
        s.node("family")
        s.node("image")
        s.node("size")
        s.node("port")
        s.node("env")
        s.node("logs")

    dot.edge("taskdef", "family")
    dot.edge("taskdef", "image")
    dot.edge("taskdef", "size")
    dot.edge("taskdef", "port")
    dot.edge("taskdef", "env")
    dot.edge("taskdef", "logs")

    output.parent.mkdir(parents=True, exist_ok=True)
    dot.render(str(output), cleanup=True)


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


def generate_compose_to_task_definition_diagram() -> None:
    def builder() -> None:
        compose = Docker("docker-compose\nsingle service")
        taskdef = ElasticContainerServiceTask("ECS Task Definition")
        service = ElasticContainerServiceService("Later used by\nECS Service")
        compose >> Edge(label="mental model") >> taskdef >> Edge(label="becomes input for") >> service

    render_bundle_diagram(BUNDLE_DIR, "compose-to-task-definition.png", builder)


def generate_minimum_fields_diagram() -> None:
    output = BUNDLE_DIR / "_diagrams" / "minimum-fields-to-create-task"
    dot = Digraph(format="png")
    dot.attr(rankdir="LR", bgcolor="white", pad="0.35", nodesep="0.45", ranksep="0.65", splines="ortho")
    dot.attr(
        "node",
        shape="box",
        style="rounded",
        fixedsize="true",
        imagescale="true",
        labelloc="b",
        fontname="Sans-Serif",
        fontsize="13",
        fontcolor="#2D3436",
        width="1.4",
        height="1.4",
    )
    dot.attr("edge", color="#64748B", penwidth="1.6")

    dot.node("family", "Name / Family", image=_icon_path(ECS), shape="none", height="1.9")
    dot.node("image", "Image", image=_icon_path(Docker), shape="none", height="1.9")
    dot.node("port", "Port", image=_icon_path(Endpoint), shape="none", height="1.9")
    dot.node("env", "Environment", image=_icon_path(ParameterStore), shape="none", height="1.9")
    dot.node("size", "CPU / RAM", image=_icon_path(Compute), shape="none", height="1.9")
    dot.node(
        "taskdef",
        "Create Task Definition",
        image=_icon_path(ElasticContainerServiceTask),
        shape="none",
        height="1.9",
        width="1.9",
    )

    dot.edge("family", "image")
    dot.edge("image", "port")
    dot.edge("port", "env")
    dot.edge("env", "size")
    dot.edge("size", "taskdef")

    output.parent.mkdir(parents=True, exist_ok=True)
    dot.render(str(output), cleanup=True)


def main() -> None:
    generate_task_definition_anatomy_diagram()
    generate_task_runtime_mapping_diagram()
    generate_task_profiles_diagram()
    generate_iam_roles_diagram()
    generate_compose_to_task_definition_diagram()
    generate_minimum_fields_diagram()


if __name__ == "__main__":
    main()
