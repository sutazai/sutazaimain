#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "context7 MCP wrapper operational"
    exit 0
fi
exec npx -y @upstash/context7-mcp@latest
