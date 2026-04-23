# SnakeAid Disaster-Aware Hybrid Architecture

SnakeAid.AmazonECS documents a practical **self-host + cloud backup** architecture for SnakeAid.

The core idea is simple:

- keep the primary runtime on self-hosted infrastructure
- keep AWS as a backup execution path when the primary system is unavailable
- stay lean enough for real operation without jumping straight into a heavy platform

## Architecture Goal

This repository exists to explore a **disaster-aware hybrid architecture** that balances:

- **availability**
  when self-hosted infrastructure fails, traffic can be redirected to AWS
- **cost and control**
  the system does not run cloud-first by default
- **operational simplicity**
  the design stays focused on ECS, ALB, and a small number of moving parts

In practice, that means:

- **Primary path**
  ZimaOS + NGINX + local services + local RabbitMQ
- **Backup path**
  AWS ALB + ECS + Amazon MQ

![SnakeAid hybrid architecture diagram](content/_diagrams/snakeaid-hybrid-architecture-diagram.png)

## The Main Architectural Idea

SnakeAid is not designed as a cloud-first system.

The intended operating model is:

- run normally on self-hosted infrastructure
- keep the AWS path ready as a backup runtime
- fail over only when the primary system is unavailable or unstable

This leads to a few deliberate choices:

- **active-passive topology**
  AWS is the backup path, not the default home of the workload
- **separate messaging paths**
  local RabbitMQ serves the primary path, while Amazon MQ serves the backup path
- **manual-first failover**
  the system favors clarity and control first, with automation added later

This is why the repo talks so much about ALB, target groups, ECS services, health checks, and RabbitMQ behavior: those pieces define whether the backup path is actually usable during failure.

![SnakeAid traffic failover diagram](content/_diagrams/traffic-failover.png)

## Current Runtime Model

At the moment, the architecture can be summarized like this:

- **Edge**
  Cloudflare DNS in front of both primary and backup paths
- **Primary runtime**
  ZimaOS + NGINX + `snakeaid-api` + `snakeai` + local RabbitMQ
- **Backup runtime**
  AWS ALB + ECS + Amazon MQ
- **Failover style**
  active-passive, with room to evolve from cold standby toward warmer and more automated recovery

This is intentionally not presented as full high availability yet.

Current limitations include:

- no multi-region setup
- no automatic message replication between local RabbitMQ and Amazon MQ
- no fully automated failover as the default operating mode

![SnakeAid messaging behavior diagram](content/_diagrams/messaging-behavior.png)

## Why ECS Is the Focus

The AWS side of the architecture is centered on ECS because it gives a useful middle ground:

- more operational structure than raw containers on EC2
- less platform overhead than Kubernetes
- enough control to reason clearly about networking, health checks, and service registration

Within ECS, this repo compares two deployment styles:

- **ECS Fargate Classic**
  more explicit setup, more control, easier low-level reasoning
- **ECS Express Mode**
  faster and more opinionated, but more abstracted

That comparison matters because SnakeAid is not choosing a deployment mode only for speed. It is choosing for reliability, debuggability, and realistic failover behavior.

## What This Repo Contains

This repo is both:

- a working Hugo documentation site
- a written engineering log for the AWS backup path of SnakeAid

The documentation focuses on:

- architectural reasoning
- trade-offs between **ECS Fargate Classic** and **ECS Express Mode**
- step-by-step ClickOps walkthroughs
- troubleshooting notes from real setup issues

The repository should still make architectural sense on its own, but the main reading experience is the published documentation site.

## Start From the Website

The best entry point is the published site:

`https://the-khiem7.github.io/SnakeAid.AmazonECS/`

Suggested reading order on the site:

1. Architecture overview
2. Fargate Classic vs Express Mode
3. ECS Fargate ClickOps
4. ECS Express ClickOps

## Documentation Tracks

The documentation is organized into three main tracks:

- **Fargate vs Express**
  why the two deployment models feel different in control, speed, and debugging
- **ECS Fargate ClickOps**
  the main step-by-step manual AWS Console workflow
- **ECS Express ClickOps**
  the faster, more opinionated path being documented in parallel

![SnakeAid failure transition diagram](content/_diagrams/failure-sequence.png)

## Why This Is Useful

This repo is aimed at the gap between:

- toy cloud tutorials
- and full enterprise platform engineering

It is meant to be useful if you want to understand:

- how to keep a self-hosted system as primary
- how to add AWS as a backup path
- how ECS, ALB, target groups, health checks, and messaging fit together
- how real troubleshooting affects the final design

## Local Development

Run the docs locally:

```bash
hugo server -D
```

Build the production output:

```bash
hugo
```

## Published Site

`https://the-khiem7.github.io/SnakeAid.AmazonECS/`
