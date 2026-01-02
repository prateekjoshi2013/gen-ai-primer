# Use official Python 3.12 slim image for smaller size
FROM python:3.12-slim

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
    locales \
    && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

# Create vscode user with sudo privileges and docker group
RUN useradd -m -s /bin/bash -G sudo vscode && \
    echo "vscode ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers.d/vscode && \
    chmod 0440 /etc/sudoers.d/vscode && \
    usermod -aG docker vscode

# Create workspace directory and set ownership
RUN mkdir -p /workspaces && \
    chown -R vscode:vscode /workspaces && \
    mkdir -p /home/vscode/venv && \
    chown -R vscode:vscode /home/vscode

# Switch to non-root user for security best practices
USER vscode
WORKDIR /workspaces

# Create virtual environment in user's home directory
RUN python3 -m venv /home/vscode/venv && \
    chown -R vscode:vscode /home/vscode/venv

# Set environment variables to activate venv automatically
ENV PATH="/home/vscode/venv/bin:$PATH" \
    VIRTUAL_ENV="/home/vscode/venv" \
    SHELL=/bin/bash \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US:en \
    LC_ALL=en_US.UTF-8

# Upgrade pip, setuptools, and wheel for better package installation
RUN pip install --no-cache-dir --upgrade pip setuptools wheel

# Copy requirements file (from parent directory)
COPY --chown=vscode:vscode ../requirements.txt /tmp/requirements.txt

# Install Python packages from requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Install oh-my-bash
# Install oh-my-bash for improved terminal UX
RUN curl -fsSL https://raw.githubusercontent.com/ohmybash/oh-my-bash/master/tools/install.sh | bash


# Configure oh-my-bash with git branch and venv in prompt
RUN sed -i 's/OSH_THEME=.*/OSH_THEME="vscode"/' ~/.bashrc && \
    echo '' >> ~/.bashrc && \
    echo '# Show virtual environment in prompt' >> ~/.bashrc && \
    echo 'export VIRTUAL_ENV_DISABLE_PROMPT=0' >> ~/.bashrc && \
    echo '' >> ~/.bashrc && \
    echo '# Activate venv automatically' >> ~/.bashrc && \
    echo 'source /home/vscode/venv/bin/activate' >> ~/.bashrc

# Create cache directories to avoid permission issues
RUN mkdir -p /home/vscode/.cache/huggingface && \
    mkdir -p /home/vscode/.cache/pip

# Configure git defaults
RUN git config --global init.defaultBranch main && \
    git config --global core.pager cat && \
    git config --global user.email "prateekjoshi2013@gmail.com" && \
    git config --global user.name "Prateek"