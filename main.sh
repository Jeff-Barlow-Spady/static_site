#!/bin/bash

# Step 1: Generate the static site
echo "Generating the static site..."
python src/main.py

# Step 2: Start the server and handle port conflicts
echo "Starting the server..."
python server.py --dir public --port 8888
