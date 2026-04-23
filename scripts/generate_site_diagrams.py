from __future__ import annotations

from pathlib import Path
from typing import Callable

from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import (
    Compute,
    ECS,
    ElasticContainerServiceService,
    ElasticContainerServiceTask,
    Fargate,
)
from diagrams.aws.general import Users
from diagrams.aws.integration import MQ
from diagrams.aws.management import Cloudwatch, CloudwatchLogs, ManagementConsole, ParameterStore
from diagrams.aws.network import ALB, Endpoint, PublicSubnet, VPC
from diagrams.aws.security import IAMRole
from diagrams.generic.blank import Blank
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ
from diagrams.saas.cdn import Cloudflare


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = ROOT / "static" / "images" / "diagrams"
OVERVIEW_ROOT = ROOT / "static" / "images" / "architecture"


def cluster_style(bgcolor: str, pencolor: str, fontsize: str = "14") -> dict[str, str]:
    return {
        "bgcolor": bgcolor,
        "pencolor": pencolor,
        "fontcolor": "#1F2937",
        "fontsize": fontsize,
        "margin": "18",
    }


def render(
    relative_path: str,
    builder: Callable[[], None],
    *,
    direction: str = "LR",
    node_fontsize: str = "12",
    graph_attr: dict[str, str] | None = None,
) -> None:
    output = ROOT / "static" / "images" / f"{relative_path}"
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


def generate_overview_system_diagram() -> None:
    def builder() -> None:
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

    render("architecture/snakeaid-hybrid-architecture-diagram.png", builder, direction="TB")


def generate_overview_failover_diagram() -> None:
    def builder() -> None:
        client = Users("Client")
        cloudflare = Cloudflare("Cloudflare DNS")

        with Cluster(
            "Normal Route",
            graph_attr=cluster_style("#EFF6FF", "#3B82F6"),
        ):
            nginx = Nginx("ZimaOS NGINX")
            api_primary = Docker("Primary API")

        with Cluster(
            "Failover Route",
            graph_attr=cluster_style("#FFF7ED", "#FB923C"),
        ):
            alb = ALB("AWS ALB")
            api_backup = Fargate("Backup API")

        client >> cloudflare
        cloudflare >> Edge(color="#2563EB", penwidth="1.8", label="normal") >> nginx >> api_primary
        cloudflare >> Edge(color="#D97706", style="dashed", penwidth="1.8", label="manual failover") >> alb >> api_backup

    render("diagrams/overview/traffic-failover.png", builder)


def generate_overview_messaging_diagram() -> None:
    def builder() -> None:
        with Cluster(
            "Primary Runtime",
            graph_attr=cluster_style("#EFF6FF", "#3B82F6"),
        ):
            api_primary = Docker("snakeaid-api")
            rabbitmq_local = RabbitMQ("Local RabbitMQ")

        with Cluster(
            "Backup Runtime",
            graph_attr=cluster_style("#FFF7ED", "#FB923C"),
        ):
            api_backup = Fargate("snakeaid-api")

        with Cluster(
            "Managed Messaging",
            graph_attr=cluster_style("#F0FDF4", "#22C55E"),
        ):
            rabbitmq_aws = MQ("Amazon MQ")

        api_primary >> Edge(color="#2563EB", penwidth="1.8", label="priority") >> rabbitmq_local
        api_primary >> Edge(color="#16A34A", style="dashed", penwidth="1.8", label="fallback") >> rabbitmq_aws
        api_backup >> Edge(color="#D97706", penwidth="1.8", label="backup only") >> rabbitmq_aws
        rabbitmq_local - Edge(style="dotted", color="#94A3B8", label="no replication") - rabbitmq_aws

    render("diagrams/overview/messaging-behavior.png", builder)


def generate_overview_failure_sequence_diagram() -> None:
    def builder() -> None:
        normal = Blank("1. Normal state\nCloudflare -> ZimaOS")
        outage = Blank("2. Outage detected\nSelf-host path unavailable")
        switch = Blank("3. Manual failover\nCloudflare -> AWS ALB")
        backup = Blank("4. Backup runtime active\nECS serves traffic")
        queue = Blank("5. Messaging mode\nAmazon MQ becomes active path")

        normal >> outage >> switch >> backup >> queue

    render(
        "diagrams/overview/failure-sequence.png",
        builder,
        graph_attr={"ranksep": "1.15", "nodesep": "0.9"},
        node_fontsize="13",
    )


def generate_guide_runtime_mental_model_diagram() -> None:
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

    render("diagrams/aws-guide/runtime-mental-model.png", builder)


def generate_guide_console_workflow_diagram() -> None:
    def builder() -> None:
        cluster = ECS("1. Create\nCluster")
        taskdef = ElasticContainerServiceTask("2. Create\nTask Definitions")
        alb = ALB("3. Create\nALB")
        target_group = Endpoint("4. Create\nTarget Group")
        service = ElasticContainerServiceService("5. Create\nECS Service")
        validate = Cloudwatch("6. Validate\nHealth + Routing")

        cluster >> taskdef >> alb >> target_group >> service >> validate

    render("diagrams/aws-guide/console-workflow.png", builder, graph_attr={"nodesep": "0.9"})


def generate_guide_resource_dependency_diagram() -> None:
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

    render("diagrams/aws-guide/resource-dependency.png", builder)


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

    render("diagrams/create-ecs-cluster/cluster-scope.png", builder)


def generate_cluster_in_context_diagram() -> None:
    def builder() -> None:
        alb = ALB("ALB")
        with Cluster(
            "snakeaid-backup-cluster",
            graph_attr=cluster_style("#EFF6FF", "#3B82F6"),
        ):
            service_api = ElasticContainerServiceService("API Service")
            service_ai = ElasticContainerServiceService("AI Service")
        mq = MQ("Amazon MQ")

        alb >> [service_api, service_ai]
        service_api >> mq

    render("diagrams/create-ecs-cluster/cluster-in-context.png", builder)


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

    render("diagrams/create-task-definition/task-definition-anatomy.png", builder, direction="TB")


def generate_task_definition_runtime_mapping_diagram() -> None:
    def builder() -> None:
        taskdef = ElasticContainerServiceTask("Task Definition\nblueprint")
        service = ElasticContainerServiceService("ECS Service\ncontroller")
        task = Fargate("Running Task")
        container = Docker("Container")

        taskdef >> Edge(label="used by") >> service >> Edge(label="launches") >> task >> container

    render("diagrams/create-task-definition/task-to-runtime.png", builder)


def generate_task_definition_profiles_diagram() -> None:
    def builder() -> None:
        with Cluster(
            "snakeaid-api profile",
            graph_attr=cluster_style("#EFF6FF", "#3B82F6"),
        ):
            api_image = Docker("thekhiem7/snakeaid-api:latest")
            api_cfg = Compute("Port 8080\n0.5 vCPU\n1 GB RAM")

        with Cluster(
            "snakeai profile",
            graph_attr=cluster_style("#FFF7ED", "#FB923C"),
        ):
            ai_image = Docker("thekhiem7/snakeaid-snake-detection-ai:8")
            ai_cfg = Compute("Port 8000\n1 vCPU\n2 GB RAM")

        api_image >> api_cfg
        ai_image >> ai_cfg

    render("diagrams/create-task-definition/task-profiles.png", builder)


def generate_task_definition_iam_roles_diagram() -> None:
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

    render("diagrams/create-task-definition/iam-roles.png", builder)


def generate_alb_components_diagram() -> None:
    def builder() -> None:
        client = Users("Client")
        alb = ALB("ALB")
        listener = Endpoint("Listener\nHTTP :80")
        rule = ManagementConsole("Default rule\n/ -> snakeaid-api-tg")
        target_group = Endpoint("Target Group")

        client >> alb >> listener >> rule >> target_group

    render("diagrams/create-application-load-balancer/alb-components.png", builder)


def generate_alb_request_routing_diagram() -> None:
    def builder() -> None:
        client = Users("Client")
        alb = ALB("Public ALB")
        target_group = Endpoint("snakeaid-api-tg")
        task = Fargate("Task IP")
        container = Docker("Container :8080")

        client >> alb >> Edge(label="forward") >> target_group >> task >> container

    render("diagrams/create-application-load-balancer/request-routing.png", builder)


def generate_alb_network_placement_diagram() -> None:
    def builder() -> None:
        with Cluster(
            "Public subnets in two AZs",
            graph_attr=cluster_style("#FFF7ED", "#FB923C"),
        ):
            alb_a = ALB("ALB subnet A")
            alb_b = ALB("ALB subnet B")
        internet = Cloudflare("Public internet path")

        internet >> [alb_a, alb_b]

    render("diagrams/create-application-load-balancer/network-placement.png", builder)


def generate_target_group_health_check_diagram() -> None:
    def builder() -> None:
        alb = ALB("ALB")
        target_group = Endpoint("Target Group\nHTTP :8080")
        task = Fargate("Task IP")
        health = Cloudwatch("Health check\n/health -> 200 OK")

        alb >> Edge(label="health check") >> target_group >> task >> health

    render("diagrams/create-target-group/health-check.png", builder)


def generate_target_group_auto_registration_diagram() -> None:
    def builder() -> None:
        service = ElasticContainerServiceService("ECS Service")
        task = Fargate("New Task IP")
        target_group = Endpoint("Target Group")
        review = ManagementConsole("Register targets screen\ncan stay at 0")

        service >> Edge(label="starts") >> task >> Edge(label="auto-registers") >> target_group
        review >> Edge(style="dotted", label="later replaced by service runtime") >> target_group

    render("diagrams/create-target-group/auto-registration.png", builder)


def generate_target_group_port_alignment_diagram() -> None:
    def builder() -> None:
        listener = Endpoint("ALB Listener\n:80")
        target_group = Endpoint("Target Group\n:8080")
        container = Docker("Container\n:8080")

        listener >> target_group >> Edge(label="must match") >> container

    render("diagrams/create-target-group/port-alignment.png", builder)


def generate_service_orchestration_diagram() -> None:
    def builder() -> None:
        service = ElasticContainerServiceService("ECS Service\nDesired tasks = 1")
        task_running = Fargate("Healthy task")
        task_replace = Fargate("Replacement task")

        service >> task_running
        service >> Edge(style="dashed", label="if unhealthy") >> task_replace

    render("diagrams/create-ecs-service/service-orchestration.png", builder)


def generate_service_alb_binding_diagram() -> None:
    def builder() -> None:
        alb = ALB("ALB :80")
        target_group = Endpoint("snakeaid-api-tg")
        service = ElasticContainerServiceService("snakeaid-api-service")
        task = Fargate("Task")
        container = Docker("snakeaid-api :8080")

        alb >> target_group >> service >> task >> container

    render("diagrams/create-ecs-service/alb-binding.png", builder)


def generate_service_rolling_update_diagram() -> None:
    def builder() -> None:
        old_task = Fargate("Old task\nrev N")
        new_task = Fargate("New task\nrev N+1")
        health = Cloudwatch("Health check passes")
        drain = ElasticContainerServiceTask("Old task drained")

        old_task >> Edge(label="deploy") >> new_task >> health >> drain

    render("diagrams/create-ecs-service/rolling-update.png", builder)


def generate_service_network_placement_diagram() -> None:
    def builder() -> None:
        vpc = VPC("VPC")
        with Cluster(
            "Service placement",
            graph_attr=cluster_style("#F8FAFC", "#94A3B8"),
        ):
            with Cluster(
                "Subnet A",
                graph_attr=cluster_style("#EFF6FF", "#3B82F6"),
            ):
                subnet_a = PublicSubnet("Subnet A")
                task_a = Fargate("Task A")
            with Cluster(
                "Subnet B",
                graph_attr=cluster_style("#FFF7ED", "#FB923C"),
            ):
                subnet_b = PublicSubnet("Subnet B")
                task_b = Fargate("Task B")
        alb = ALB("Public ALB")

        vpc >> [subnet_a, subnet_b]
        subnet_a >> task_a
        subnet_b >> task_b
        alb >> [task_a, task_b]

    render("diagrams/create-ecs-service/network-placement.png", builder)


def generate_all_diagrams() -> None:
    generate_overview_system_diagram()
    generate_overview_failover_diagram()
    generate_overview_messaging_diagram()
    generate_overview_failure_sequence_diagram()
    generate_guide_runtime_mental_model_diagram()
    generate_guide_console_workflow_diagram()
    generate_guide_resource_dependency_diagram()
    generate_cluster_scope_diagram()
    generate_cluster_in_context_diagram()
    generate_task_definition_anatomy_diagram()
    generate_task_definition_runtime_mapping_diagram()
    generate_task_definition_profiles_diagram()
    generate_task_definition_iam_roles_diagram()
    generate_alb_components_diagram()
    generate_alb_request_routing_diagram()
    generate_alb_network_placement_diagram()
    generate_target_group_health_check_diagram()
    generate_target_group_auto_registration_diagram()
    generate_target_group_port_alignment_diagram()
    generate_service_orchestration_diagram()
    generate_service_alb_binding_diagram()
    generate_service_rolling_update_diagram()
    generate_service_network_placement_diagram()


if __name__ == "__main__":
    generate_all_diagrams()
