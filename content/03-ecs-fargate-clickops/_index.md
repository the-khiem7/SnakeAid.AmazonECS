---
title: "ECS Fargate ClickOps"
date: 2026-04-22
weight: 3
chapter: false
---

## Page Objective

This section documents the manual AWS Console workflow for the **ECS Fargate Classic** deployment path used by SnakeAid.

---

## Scope

* Covers manual AWS Console configuration for ECS Fargate Classic
* Follows the current detailed deployment path of this project
* Each child page represents one specific operational task

---

## AWS Deployment Mental Model

Before going step by step in the Console, it helps to keep three views in mind: execution order, runtime shape, and resource dependency.

### Console Workflow Map

This is the operational order we usually follow in AWS Console. It answers the question: "What should be created first so later resources can attach cleanly?"

![AWS Console workflow map](_diagrams/console-workflow.png)

### Runtime Mental Model

This view shifts from setup order to runtime behavior. It shows how traffic reaches the backup stack after the infrastructure has already been created.

![AWS backup runtime mental model diagram](_diagrams/runtime-mental-model.png)

### Resource Dependency

This final view is useful when something breaks. It helps trace which resource depends on which upstream configuration, especially around ALB, target groups, services, and health checks.

![AWS backup resource dependency diagram](_diagrams/resource-dependency.png)

Together, these three diagrams reduce a common source of confusion: the Console flow is not always the same as the runtime flow, and neither is exactly the same as the dependency graph.

---

## Prerequisites

* AWS account with appropriate permissions
* Correct deployment region selected
* Required inputs prepared (service name, port, image, env)

---

## What This Series Covers

The walkthrough is organized around the core Fargate setup path for SnakeAid:

1. Create the ECS cluster
2. Define the application tasks
3. Create the ALB and target groups
4. Create ECS services and attach traffic
5. Validate health checks and failover behavior

Supporting topics such as Amazon MQ connectivity and troubleshooting are added where they become operationally relevant.

---

## Child Pages

{{% children description="true" /%}}

---

## Upcoming Content

Detailed procedures will be added incrementally as child pages under this section.
