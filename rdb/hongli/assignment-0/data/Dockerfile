FROM ubuntu:22.04

ARG MY_USER_ID
ARG MY_GROUP_ID
ARG MY_USER_NAME

# Install without asking questions
ENV DEBIAN_FRONTEND=noninteractive

# Set timezone
ENV TZ="Europe/Berlin"

# Install Python and other useful tools
RUN apt-get update \
    && apt-get -y install \
    python3 \
    python3-pip \
    python3-tk \
    wget \
    unzip \
    postgresql-client \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists*

# Add a new user with the same UID and GID as the current host user
RUN addgroup --gid $MY_GROUP_ID user && \
    adduser --disabled-password --gecos '' --uid $MY_USER_ID --gid $MY_GROUP_ID $MY_USER_NAME && \
    usermod -aG user $MY_USER_NAME

# Switch to the new user
USER $MY_USER_NAME

# Install Python packages as the new user, add .local/bin to PATH and add alias
COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --user --no-cache-dir -r /tmp/requirements.txt && \
    rm -rf ~/.cache/pip && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && \
    echo 'alias p="python3"' >> ~/.bashrc

# Set the working directory
WORKDIR /data

# Run the command as the new user
CMD ["/bin/bash"]
