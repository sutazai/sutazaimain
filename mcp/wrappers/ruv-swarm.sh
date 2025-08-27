#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "ruv-swarm MCP wrapper operational"
    exit 0
fi
exec npx -y ruv-swarm@latest mcp start
