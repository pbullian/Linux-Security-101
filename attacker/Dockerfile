FROM debian:12
ARG DEBIAN_FRONTEND=noninteractive
RUN apt-get -o APT::Update::Error-Mode=any update \
    && apt-get install -y --no-install-recommends \
       openssh-client iproute2 iputils-ping curl netcat-openbsd nmap sshpass \
       ca-certificates procps \
    && rm -rf /var/lib/apt/lists/*
CMD ["sleep", "infinity"]
