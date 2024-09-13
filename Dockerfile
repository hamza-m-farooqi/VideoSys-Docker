# Use the NVIDIA CUDA base image
FROM nvidia/cuda:12.0.1-runtime-ubuntu22.04
# FROM nvidia/cuda:12.6.1-base-ubuntu22.04

# Set environment variables to avoid issues with prompts (uncomment if needed)
# ENV HF_TOKEN=""
ENV HF_HOME=/app/huggingface

# Use Docker BuildKit to enable caching
# Install apt packages with cache
RUN --mount=type=cache,target=/var/cache/apt \
    apt-get update && apt-get install -y \
    ffmpeg \
    libomp-dev \
    build-essential \
    libssl-dev \
    libffi-dev \
    libgl1-mesa-glx \
    python3-pip \
    gdb \
    valgrind \
    git && \
    rm -rf /var/lib/apt/lists/*

# Update pip to the latest version with cache
RUN --mount=type=cache,target=/root/.cache/pip \
    python3 -m pip install --upgrade pip

# Copy all files into the /app directory
COPY . /app

# Set the working directory
WORKDIR /app

# Clone the VideoSys repository
RUN git clone https://github.com/NUS-HPC-AI-Lab/VideoSys


# Install the VideoSys package
RUN --mount=type=cache,target=/root/.cache/pip \
cd VideoSys && python3 -m pip install -e .

# Install Python dependencies
RUN pip3 install requests python-decouple boto3 rotary-embedding-torch
# Optionally, add an entrypoint or CMD
# CMD ["python3", "main.py"]
