FROM docker-registry.ussc.ru/debian:8

MAINTAINER Yakov Zubarev "yzubarev@ussc.ru"

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        wget \
    && rm -rf /var/lib/apt/lists/*