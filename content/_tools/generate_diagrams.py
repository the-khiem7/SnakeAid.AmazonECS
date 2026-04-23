from __future__ import annotations

import sys
from pathlib import Path

from diagrams import Cluster, Edge
from diagrams.aws.compute import Fargate
from diagrams.aws.general import Users
from diagrams.aws.integration import MQ
from diagrams.aws.network import ALB
from diagrams.generic.blank import Blank
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ
from diagrams.saas.cdn import Cloudflare


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from tools.diagram_utils import cluster_style, render_bundle_diagram


BUNDLE_DIR = Path(__file__).resolve().parents[1]


def generate_system_diagram() -> None:
    def builder() -> None:
        with Cluster("Cloudflare DNS", direction="TB", graph_attr=cluster_style("#FFF7ED", "#F59E0B")):
            cloudflare = Cloudflare("api.snakeaid.com")

        with Cluster(
            "Primary System (ZimaOS - Self-hosted)",
            direction="TB",
            graph_attr=cluster_style("#EFF6FF", "#3B82F6"),
        ):
            nginx = Nginx("NGINX\nReverse Proxy")
            with Cluster("Docker Containers", direction="LR", graph_attr=cluster_style("#F8FBFF", "#93C5FD")):
                api_primary = Docker("snakeaid-api")
                ai_primary = Docker("snakeai")
                rabbitmq_local = RabbitMQ("RabbitMQ\n(local)")
            nginx >> [api_primary, ai_primary]
            api_primary >> rabbitmq_local

        with Cluster("AWS Backup System", direction="TB", graph_attr=cluster_style("#FFF7ED", "#FB923C")):
            alb = ALB("Application Load\nBalancer")
            with Cluster("ECS Fargate", direction="LR", graph_attr=cluster_style("#FFFDF7", "#FDBA74")):
                api_backup = Fargate("snakeaid-api")
                ai_backup = Fargate("snakeai")
            alb >> [api_backup, ai_backup]

        with Cluster("Messaging Layer", direction="TB", graph_attr=cluster_style("#F0FDF4", "#22C55E")):
            rabbitmq_aws = MQ("Amazon MQ\n(RabbitMQ managed)")

        cloudflare >> Edge(color="#2563EB", penwidth="1.8") >> nginx
        cloudflare >> Edge(label="failover", style="dashed", color="#D97706", penwidth="1.8") >> alb
        api_primary >> Edge(label="fallback", style="dashed", color="#16A34A", penwidth="1.8") >> rabbitmq_aws
        api_backup >> Edge(color="#2563EB", penwidth="1.8") >> rabbitmq_aws

    render_bundle_diagram(BUNDLE_DIR, "snakeaid-hybrid-architecture-diagram.png", builder, direction="TB")


def generate_failover_diagram() -> None:
    def builder() -> None:
        client = Users("Client")
        cloudflare = Cloudflare("Cloudflare DNS")
        with Cluster("Normal Route", graph_attr=cluster_style("#EFF6FF", "#3B82F6")):
            nginx = Nginx("ZimaOS NGINX")
            api_primary = Docker("Primary API")
        with Cluster("Failover Route", graph_attr=cluster_style("#FFF7ED", "#FB923C")):
            alb = ALB("AWS ALB")
            api_backup = Fargate("Backup API")

        client >> cloudflare
        cloudflare >> Edge(color="#2563EB", penwidth="1.8", label="normal") >> nginx >> api_primary
        cloudflare >> Edge(color="#D97706", style="dashed", penwidth="1.8", label="manual failover") >> alb >> api_backup

    render_bundle_diagram(BUNDLE_DIR, "traffic-failover.png", builder)


def generate_messaging_diagram() -> None:
    def builder() -> None:
        with Cluster("Primary Runtime", graph_attr=cluster_style("#EFF6FF", "#3B82F6")):
            api_primary = Docker("snakeaid-api")
            rabbitmq_local = RabbitMQ("Local RabbitMQ")
        with Cluster("Backup Runtime", graph_attr=cluster_style("#FFF7ED", "#FB923C")):
            api_backup = Fargate("snakeaid-api")
        with Cluster("Managed Messaging", graph_attr=cluster_style("#F0FDF4", "#22C55E")):
            rabbitmq_aws = MQ("Amazon MQ")

        api_primary >> Edge(color="#2563EB", penwidth="1.8", label="priority") >> rabbitmq_local
        api_primary >> Edge(color="#16A34A", style="dashed", penwidth="1.8", label="fallback") >> rabbitmq_aws
        api_backup >> Edge(color="#D97706", penwidth="1.8", label="backup only") >> rabbitmq_aws
        rabbitmq_local - Edge(style="dotted", color="#94A3B8", label="no replication") - rabbitmq_aws

    render_bundle_diagram(BUNDLE_DIR, "messaging-behavior.png", builder)


def generate_failure_sequence_diagram() -> None:
    def builder() -> None:
        normal = Blank("1. Normal state\nCloudflare -> ZimaOS")
        outage = Blank("2. Outage detected\nSelf-host path unavailable")
        switch = Blank("3. Manual failover\nCloudflare -> AWS ALB")
        backup = Blank("4. Backup runtime active\nECS serves traffic")
        queue = Blank("5. Messaging mode\nAmazon MQ becomes active path")
        normal >> outage >> switch >> backup >> queue

    render_bundle_diagram(
        BUNDLE_DIR,
        "failure-sequence.png",
        builder,
        graph_attr={"ranksep": "1.15", "nodesep": "0.9"},
        node_fontsize="13",
    )


def main() -> None:
    generate_system_diagram()
    generate_failover_diagram()
    generate_messaging_diagram()
    generate_failure_sequence_diagram()


if __name__ == "__main__":
    main()
