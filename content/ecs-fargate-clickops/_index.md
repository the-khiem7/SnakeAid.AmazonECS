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

### Console Workflow Map

![AWS Console workflow map](_diagrams/console-workflow.png)

### Runtime Mental Model

![AWS backup runtime mental model diagram](_diagrams/runtime-mental-model.png)

### Resource Dependency

![AWS backup resource dependency diagram](_diagrams/resource-dependency.png)

---

## Prerequisites

* AWS account with appropriate permissions
* Correct deployment region selected
* Required inputs prepared (service name, port, image, env)

---

## Child Page Template

Each child page should follow this structure:

1. **Purpose**
2. **Required inputs**
3. **Console steps**
4. **Expected result**
5. **Notes / common issues**
6. **Rollback (if applicable)**

---

## Planned Child Topics

1. Create ECS Cluster (Fargate)
2. Create Task Definition for `snakeaid-api`
3. Create Task Definition for `snakeai`
4. Create ALB and Target Groups
5. Create ECS Services and attach ALB
6. Configure Amazon MQ connectivity
7. Validate health checks and failover

---

## Child Pages

{{% children description="true" /%}}

---

## Authoring Notes

* Include Console navigation paths for each step
* Keep naming conventions consistent across resources
* Keep raw console captures in `raw/` and treat them as immutable source material
* Publish focused screenshot crops from each page bundle under `_diagrams/`, preferably as `webp`
* Reference screenshot assets with page-relative paths so English and Vietnamese pages can reuse the same crop

---

## Upcoming Content

Detailed procedures will be added incrementally as child pages under this section.
