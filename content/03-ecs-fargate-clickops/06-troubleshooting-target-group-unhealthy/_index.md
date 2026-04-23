---
title: "Troubleshooting Unhealthy Targets in ECS Target Groups"
date: 2026-04-23
weight: 6
chapter: false
pre: " <b> 6. </b> "
---

# Troubleshooting Unhealthy Targets in ECS Target Groups

In the process of setting up the cloud backup component of SnakeAid's disaster-aware hybrid architecture, we encountered a common issue with AWS ECS and Application Load Balancer (ALB) integration: unhealthy targets in the target group. This post documents the step-by-step troubleshooting process we went through to resolve the issue.

## Initial Problem

After deploying the snakeaid-api service to ECS Fargate, the ALB health checks were failing, marking the targets as unhealthy. This prevented traffic from reaching the application, causing 502 errors.

Navigation: `EC2 > Target groups > snakeaid-api-tg`

![Target group showing stale targets and an unhealthy registration](_diagrams/target-group-stale-targets.webp)

## Step 1: Compare the Target Group with the Live ECS Task

We first confirmed that the problem was not in the application code. The container exposed port `8080`, the ASP.NET Core app listened on `0.0.0.0:8080`, and `/health` was available. The next check was whether the target group was pointing to the current task at all.

Navigation: `ECS > Clusters > snakeaid-backup-cluster > Services > snakeaid-api-service > Tasks > <running-task> > Configuration`

![Running ECS task showing the current private IP](_diagrams/ecs-task-private-ip.webp)

The ECS task had private IP `172.31.46.41`, but the target group still contained older IPs from previous runs. That mismatch made the first failure mode clear: the target group had stale registrations.

## Step 2: Remove Stale Targets and Re-check Health

We deregistered the outdated targets and let the ECS service re-register the live task IP automatically. After that cleanup, the target group no longer showed stale addresses, but the new target still failed health checks.

Navigation: `EC2 > Target groups > snakeaid-api-tg`

![Target group still unhealthy after the stale IPs were removed](_diagrams/target-group-health-check-failed.webp)

This told us the remaining issue was no longer target registration. The next likely causes were task networking and startup timing.

## Step 3: Inspect the Existing Task Security Group

The ECS service was still attached to the default VPC security group. Its inbound rule only allowed traffic from the same security group, which is hard to reason about and easy to misconfigure for ALB-to-task traffic.

Navigation: `EC2 > Security groups > sg-0c14aececd4ae8e46`

![Default security group showing a self-referencing inbound rule](_diagrams/default-security-group-self-reference.webp)

## Step 4: Create a Dedicated ECS Task Security Group

To make the traffic path explicit, we created a dedicated security group for ECS tasks. Its single inbound rule allows TCP `8080` from the ALB security group, while outbound traffic remains open for dependencies such as Supabase, Firebase, Doppler, and RabbitMQ.

Navigation: `EC2 > Security groups > Create security group`

![Dedicated ECS security group allowing port 8080 from the ALB security group](_diagrams/ecs-security-group-from-alb.webp)

## Step 5: Fix the Health Check Grace Period

The service configuration also revealed that the health check grace period was still `0 seconds`. That meant the load balancer started probing `/health` immediately, before the application had time to finish its startup sequence.

Navigation: `ECS > Clusters > snakeaid-backup-cluster > Services > snakeaid-api-service > Configuration and networking`

![Service configuration showing a zero-second health check grace period](_diagrams/service-config-grace-period-zero.webp)

## Step 6: Update the ECS Service and Force a New Deployment

We opened `Update service`, forced a new deployment, increased the grace period to `90 seconds`, and replaced the default task security group with `ecs-snakeaid-sg`.

Navigation: `ECS > Clusters > snakeaid-backup-cluster > Services > snakeaid-api-service > Update service`

![Update service with a 90-second health check grace period](_diagrams/service-update-grace-period-90.webp)

![Update service networking using the dedicated ECS security group](_diagrams/service-update-ecs-security-group.webp)

## Verification

After these changes, the service behavior matched the expected ECS + ALB flow:

- The target group registered the live ECS task IP instead of stale addresses.
- The ALB could reach the task on port `8080`.
- Health checks waited long enough for the application to initialize.
- The target transitioned from `Unhealthy` to `Healthy`.

## Lessons Learned

- Do not manually register targets in an IP-based target group that is managed by an ECS service.
- Use separate security groups for the ALB and for ECS tasks so the traffic contract is explicit.
- Review the health check grace period whenever application startup includes external services or warm-up work.
- When a target is unhealthy, verify the live task IP, the target group registration, the security group path, and the grace period in that order.

This troubleshooting reinforced our understanding of AWS networking in ECS deployments, crucial for maintaining the reliability of SnakeAid's hybrid architecture.
