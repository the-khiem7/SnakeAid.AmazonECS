from __future__ import annotations

import sys
from pathlib import Path

from diagrams import Cluster
from diagrams.aws.compute import ElasticContainerServiceService, Fargate
from diagrams.aws.management import ManagementConsole
from diagrams.aws.network import ALB, Endpoint


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.diagram_utils import cluster_style, render_bundle_diagram


BUNDLE_DIR = Path(__file__).resolve().parents[1]


def generate_tradeoff_diagram() -> None:
    def builder() -> None:
        with Cluster("Fargate Classic", graph_attr=cluster_style("#EFF6FF", "#3B82F6")):
            cluster = Fargate("More control")
            wiring = Endpoint("ALB + TG + SG")
            service = ElasticContainerServiceService("More setup work")
            cluster >> wiring >> service

        with Cluster("Express Mode", graph_attr=cluster_style("#FFF7ED", "#FB923C")):
            express = ManagementConsole("Faster path")
            defaults = Endpoint("More defaults")
            abstraction = ElasticContainerServiceService("Less low-level control")
            express >> defaults >> abstraction

    render_bundle_diagram(BUNDLE_DIR, "classic-vs-express-tradeoff.png", builder)


def main() -> None:
    generate_tradeoff_diagram()


if __name__ == "__main__":
    main()
