#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "everything MCP wrapper operational"
    exit 0
fi
exec npx -y @modelcontextprotocol/server-everything
