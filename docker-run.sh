#!/bin/bash

# Build and run the Ubuntu Git container with code mounted

# Build the image
docker build -t ubuntu-git .

# Run the container with:
# - Current directory mounted to /workspace
# - Interactive terminal
# Note: We don't mount .gitconfig so github-setup can create its own

docker run -it --rm \
    -v "$(pwd):/workspace" \
    ubuntu-git
