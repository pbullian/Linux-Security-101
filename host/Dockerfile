FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends       openssh-server sudo vim nftables rsyslog iproute2 iputils-ping procps       libpam-modules libpam-modules-bin passwd fail2ban acl &&     rm -rf /var/lib/apt/lists/* &&     mkdir -p /var/run/sshd /artifacts &&     useradd -m -s /bin/bash student && echo 'student:student' | chpasswd &&     usermod -aG sudo student &&     sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config &&     sed -i 's/^#\?PermitRootLogin.*/PermitRootLogin prohibit-password/' /etc/ssh/sshd_config &&     sed -i 's/^#\?LogLevel.*/LogLevel VERBOSE/' /etc/ssh/sshd_config
RUN set -eux; \
    mkdir -p /usr/local/bin /opt/labtools; \
    cp /usr/bin/vim.basic /usr/local/bin/vimroot; \
    chown root:root /usr/local/bin/vimroot; \
    chmod 4755 /usr/local/bin/vimroot; \
    cp /bin/bash /opt/labtools/shroot; \
    chown root:root /opt/labtools/shroot; \
    chmod 4755 /opt/labtools/shroot; \
    chmod 0777 /opt/labtools
COPY start.sh /start.sh
RUN chmod +x /start.sh
EXPOSE 22
CMD ["/start.sh"]
