#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "memory MCP wrapper operational"
    exit 0
fi
exec npx -y @modelcontextprotocol/server-memory
