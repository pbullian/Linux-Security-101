FROM ubuntu:24.04
ARG DEBIAN_FRONTEND=noninteractive

# Dependencies are installed before any firewall exercise.
RUN apt-get -o APT::Update::Error-Mode=any update \
    && apt-get install -y --no-install-recommends \
       openssh-server openssh-client sudo vim nftables rsyslog \
       iproute2 iputils-ping procps libpam-modules libpam-modules-bin passwd \
       fail2ban acl libcap2-bin python3 curl wget ca-certificates \
       busybox-static aide unattended-upgrades apt-listchanges needrestart \
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /run/sshd /artifacts /var/spool/rsyslog \
    && useradd -m -s /bin/bash student \
    && echo 'student:student' | chpasswd \
    && usermod -aG sudo student \
    && rm -f /etc/ssh/ssh_host_* \
    && printf '%s\n' 'PermitRootLogin no' 'PasswordAuthentication yes' \
       'KbdInteractiveAuthentication no' 'LogLevel VERBOSE' \
       > /etc/ssh/sshd_config.d/10-lab-defaults.conf \
    && printf '%s\n' '[sshd]' 'enabled = false' 'backend = polling' \
       > /etc/fail2ban/jail.d/99-lab-defaults.local

# Deliberate vulnerabilities for the permissions exercise. This is a disposable
# teaching environment, not a hardened server image.
RUN mkdir -p /usr/local/bin /opt/labtools \
    && cp /usr/bin/vim.basic /usr/local/bin/vimroot \
    && cp /bin/bash /opt/labtools/shroot \
    && chmod 4755 /usr/local/bin/vimroot /opt/labtools/shroot \
    && chmod 0777 /opt/labtools

COPY lab/rsyslog.conf /etc/rsyslog.conf
COPY lab/nft-lab /usr/local/sbin/nft-lab
COPY lab/install-osquery /usr/local/sbin/install-osquery-lab
COPY start.sh /start.sh
RUN chmod +x /start.sh /usr/local/sbin/nft-lab /usr/local/sbin/install-osquery-lab
EXPOSE 22
CMD ["/start.sh"]
