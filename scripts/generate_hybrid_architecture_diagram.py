from __future__ import annotations

from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Fargate
from diagrams.aws.integration import MQ
from diagrams.aws.network import ALB
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ
from diagrams.saas.cdn import Cloudflare


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static" / "images" / "architecture" / "snakeaid-hybrid-architecture-diagram"


def cluster_style(bgcolor: str, pencolor: str) -> dict[str, str]:
    return {
        "bgcolor": bgcolor,
        "pencolor": pencolor,
        "fontcolor": "#1F2937",
        "fontsize": "14",
        "margin": "18",
    }


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    graph_attr = {
        "label": "",
        "pad": "0.5",
        "nodesep": "0.8",
        "ranksep": "0.95",
        "fontname": "Sans-Serif",
        "fontsize": "16",
        "bgcolor": "white",
    }
    node_attr = {
        "fontsize": "12",
    }
    edge_attr = {
        "color": "#64748B",
        "penwidth": "1.6",
    }

    with Diagram(
        "",
        filename=str(OUTPUT),
        direction="TB",
        curvestyle="ortho",
        outformat="png",
        show=False,
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
    ):
        with Cluster(
            "Cloudflare DNS",
            direction="TB",
            graph_attr=cluster_style("#FFF7ED", "#F59E0B"),
        ):
            cloudflare = Cloudflare("api.snakeaid.com")

        with Cluster(
            "Primary System (ZimaOS - Self-hosted)",
            direction="TB",
            graph_attr=cluster_style("#EFF6FF", "#3B82F6"),
        ):
            nginx = Nginx("NGINX\nReverse Proxy")

            with Cluster(
                "Docker Containers",
                direction="LR",
                graph_attr=cluster_style("#F8FBFF", "#93C5FD"),
            ):
                api_primary = Docker("snakeaid-api")
                ai_primary = Docker("snakeai")
                rabbitmq_local = RabbitMQ("RabbitMQ\n(local)")

            nginx >> [api_primary, ai_primary]
            api_primary >> rabbitmq_local

        with Cluster(
            "AWS Backup System",
            direction="TB",
            graph_attr=cluster_style("#FFF7ED", "#FB923C"),
        ):
            alb = ALB("Application Load\nBalancer")

            with Cluster(
                "ECS Fargate",
                direction="LR",
                graph_attr=cluster_style("#FFFDF7", "#FDBA74"),
            ):
                api_backup = Fargate("snakeaid-api")
                ai_backup = Fargate("snakeai")

            alb >> [api_backup, ai_backup]

        with Cluster(
            "Messaging Layer",
            direction="TB",
            graph_attr=cluster_style("#F0FDF4", "#22C55E"),
        ):
            rabbitmq_aws = MQ("Amazon MQ\n(RabbitMQ managed)")

        cloudflare >> Edge(color="#2563EB", penwidth="1.8") >> nginx
        cloudflare >> Edge(
            label="failover",
            style="dashed",
            color="#D97706",
            penwidth="1.8",
        ) >> alb

        api_primary >> Edge(
            label="fallback",
            style="dashed",
            color="#16A34A",
            penwidth="1.8",
        ) >> rabbitmq_aws
        api_backup >> Edge(color="#2563EB", penwidth="1.8") >> rabbitmq_aws


if __name__ == "__main__":
    main()
