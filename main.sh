#!/bin/bash

# Step 1: Generate the static site
echo "Generating the static site..."
uv run python src/main.py

# Step 2: Start the server and handle port conflicts
echo "Starting the server..."
uv run python server.py --dir docs --port 8888
