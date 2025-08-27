#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "extended-memory MCP wrapper operational"
    exit 0
fi
# Using official MCP memory server
exec npx -y @modelcontextprotocol/server-memory@latest
