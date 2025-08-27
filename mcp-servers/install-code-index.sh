#!/bin/bash
# Install code-index-mcp properly in project directory

set -e

echo "Installing code-index-mcp in /opt/sutazaiapp/mcp-servers..."

# Change to mcp-servers directory
cd /opt/sutazaiapp/mcp-servers

# Remove empty directory if it exists
if [ -d "code-index-mcp" ]; then
    rm -rf code-index-mcp
fi

# Clone the repository
git clone https://github.com/johnhuang316/code-index-mcp.git

# Change to the project directory
cd code-index-mcp

# Install uv if not present
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$PATH:$HOME/.local/bin"
fi

# Sync dependencies
echo "Installing dependencies with uv..."
uv sync

echo "✅ code-index-mcp installed successfully!"
echo "Location: /opt/sutazaiapp/mcp-servers/code-index-mcp"