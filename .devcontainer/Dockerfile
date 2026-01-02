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

# Create vscode user with sudo privileges and docker group
RUN useradd -m -s /bin/bash -G sudo vscode && \
    echo "vscode ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/vscode && \
    chmod 0440 /etc/sudoers.d/vscode && \
    usermod -aG docker vscode

# Give vscode user ownership of conda installation
RUN chown -R vscode:vscode /opt/conda && \
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

# Copy environment file
COPY --chown=vscode:vscode environment.yml /tmp/environment.yml

# Create conda environment as vscode user
RUN conda env create -f /tmp/environment.yml && \
    conda clean -afy

# Initialize conda for vscode user
RUN conda init bash && \
    echo "conda activate myenv" >> ~/.bashrc

# Create cache directories for vscode user to avoid permission issues
RUN mkdir -p /home/vscode/.cache/huggingface && \
    mkdir -p /home/vscode/.cache/pip

# Configure git defaults for vscode user
RUN git config --global init.defaultBranch main && \
    git config --global core.pager cat && \
    git config --global user.email "prateekjoshi2013@gmail.com" && \
    git config --global user.name "Prateek"