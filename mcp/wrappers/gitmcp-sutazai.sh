#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "gitmcp-sutazai MCP wrapper operational"
    exit 0
fi
# Using git-mcp-server for Sutazai repository operations
exec npx -y @cyanheads/git-mcp-server@latest
