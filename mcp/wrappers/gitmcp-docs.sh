#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "gitmcp-docs MCP wrapper operational"
    exit 0
fi
# Using git-mcp-server for documentation repositories
exec npx -y @cyanheads/git-mcp-server@latest
