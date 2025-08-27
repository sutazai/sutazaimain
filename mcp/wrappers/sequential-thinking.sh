#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "sequential-thinking MCP wrapper operational"
    exit 0
fi
exec npx -y @modelcontextprotocol/server-sequential-thinking
