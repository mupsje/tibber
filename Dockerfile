FROM python:3.12.5-alpine

# Install necessary packages and configure SSH
RUN apk update && \
    apk add --no-cache openssh nano dhclient gcc musl-dev libffi-dev tzdata openrc && \
    sed -i -e 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' \
           -e 's/^#PasswordAuthentication.*/PasswordAuthentication yes/' \
           /etc/ssh/sshd_config && \
    ssh-keygen -A && \
    rc-status && \
    touch /run/openrc/softlevel && \
    rc-update add sshd default

# Set the time zone
ENV TZ=Europe/Amsterdam

# Set the working directory in the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .
COPY dhclient.conf /etc/dhcp/dhclient.conf

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files to the container
COPY . .

# Start OpenRC and SSH, then run the Python script
CMD ["/bin/sh", "-c", "echo \"root:$SSH_PASSWORD\" | chpasswd && rc-service sshd start && dhclient -v eth0 && python tibber_energy_monitor.py"]
