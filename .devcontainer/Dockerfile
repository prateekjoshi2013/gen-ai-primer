FROM continuumio/miniconda3:latest

# Install system dependencies including Docker
RUN apt-get update && apt-get install -y \
    git \
    build-essential \
    docker.io \
    docker-compose \
    curl \
    wget \
    sudo \
    openssh-client \
    && rm -rf /var/lib/apt/lists/*

# Copy environment file
COPY environment.yml /tmp/environment.yml

# Create conda environment
RUN conda env create -f /tmp/environment.yml && \
    conda clean -afy

# Create vscode user with sudo privileges
RUN useradd -m -s /bin/bash -G sudo vscode && \
    echo "vscode ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/vscode && \
    chmod 0440 /etc/sudoers.d/vscode

# Setup conda and directories
RUN mkdir -p /home/vscode/.conda && \
    chown -R vscode:vscode /home/vscode && \
    mkdir -p /workspaces && \
    chown -R vscode:vscode /workspaces

# Set environment variables for conda activation
ENV PATH="/opt/conda/envs/myenv/bin:$PATH" \
    CONDA_DEFAULT_ENV=myenv \
    CONDA_PREFIX=/opt/conda/envs/myenv \
    SHELL=/bin/bash

# Switch to non-root user for security best practices
USER vscode
WORKDIR /workspaces

# Initialize conda for vscode user - this modifies .bashrc for this user
RUN conda init bash && \
    echo "conda activate myenv" >> ~/.bashrc

# Configure git defaults for vscode user
RUN git config --global init.defaultBranch main && \
    git config --global core.editor "vi" && \
    git config --global user.email "prateekjoshi2013@gmail.com" && \
    git config --global user.name "Prateek"