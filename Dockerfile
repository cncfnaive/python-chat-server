# Lightweight Ubuntu container with Git for GitHub operations
FROM ubuntu:22.04

# Avoid interactive prompts during package installation
ENV DEBIAN_FRONTEND=noninteractive

# Install git and essential tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    openssh-client \
    ca-certificates \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create .ssh directory for SSH keys
RUN mkdir -p /root/.ssh && chmod 700 /root/.ssh

# Copy the GitHub setup script
COPY github-setup.sh /usr/local/bin/github-setup
RUN chmod +x /usr/local/bin/github-setup

# Set working directory where code will be mounted
WORKDIR /workspace

# Default command - start an interactive bash shell
CMD ["/bin/bash"]
