from __future__ import annotations

from pathlib import Path
from typing import Callable

from diagrams import Diagram


def cluster_style(bgcolor: str, pencolor: str, fontsize: str = "14") -> dict[str, str]:
    return {
        "bgcolor": bgcolor,
        "pencolor": pencolor,
        "fontcolor": "#1F2937",
        "fontsize": fontsize,
        "margin": "18",
    }


def render_bundle_diagram(
    bundle_dir: Path,
    filename: str,
    builder: Callable[[], None],
    *,
    direction: str = "LR",
    node_fontsize: str = "12",
    graph_attr: dict[str, str] | None = None,
) -> None:
    output = bundle_dir / "_diagrams" / filename
    output.parent.mkdir(parents=True, exist_ok=True)
    graph = {
        "label": "",
        "pad": "0.45",
        "nodesep": "0.75",
        "ranksep": "0.95",
        "fontname": "Sans-Serif",
        "fontsize": "16",
        "bgcolor": "white",
    }
    if graph_attr:
        graph.update(graph_attr)

    with Diagram(
        "",
        filename=str(output.with_suffix("")),
        direction=direction,
        curvestyle="ortho",
        outformat="png",
        show=False,
        graph_attr=graph,
        node_attr={"fontsize": node_fontsize},
        edge_attr={"color": "#64748B", "penwidth": "1.6"},
    ):
        builder()
