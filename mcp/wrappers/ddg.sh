#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "ddg MCP wrapper operational"
    exit 0
fi
# Using nickclyde's DuckDuckGo MCP server
exec npx -y duckduckgo-mcp-server@latest
