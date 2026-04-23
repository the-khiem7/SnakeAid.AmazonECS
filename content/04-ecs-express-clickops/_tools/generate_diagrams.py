from __future__ import annotations

import sys
from pathlib import Path

from diagrams import Cluster
from diagrams.aws.management import ManagementConsole
from diagrams.aws.network import Endpoint
from diagrams.aws.compute import ElasticContainerServiceService


ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))

from tools.diagram_utils import cluster_style, render_bundle_diagram


BUNDLE_DIR = Path(__file__).resolve().parents[1]


def generate_express_overview_diagram() -> None:
    def builder() -> None:
        with Cluster("ECS Express Mode", graph_attr=cluster_style("#FFF7ED", "#FB923C")):
            entry = ManagementConsole("Faster setup path")
            defaults = Endpoint("More managed defaults")
            service = ElasticContainerServiceService("Opinionated service outcome")
            entry >> defaults >> service

    render_bundle_diagram(BUNDLE_DIR, "express-mode-overview.png", builder)


def main() -> None:
    generate_express_overview_diagram()


if __name__ == "__main__":
    main()
