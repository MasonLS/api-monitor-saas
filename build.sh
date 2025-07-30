#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p data

echo "Build completed!"
