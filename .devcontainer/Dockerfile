FROM mcr.microsoft.com/devcontainers/base:ubuntu

ARG HUGO_VERSION=0.134.3

RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl ca-certificates tar; \
    ARCH="$(dpkg --print-architecture)"; \
    case "${ARCH}" in \
      amd64) HUGO_ARCH='amd64' ;; \
      arm64) HUGO_ARCH='arm64' ;; \
      *) echo "Unsupported architecture: ${ARCH}" >&2; exit 1 ;; \
    esac; \
    curl -fsSL "https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-${HUGO_ARCH}.tar.gz" \
      | tar -xz -C /usr/local/bin hugo; \
    apt-get clean; \
    rm -rf /var/lib/apt/lists/*
