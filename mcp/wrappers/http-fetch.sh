#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "http-fetch MCP wrapper operational"
    exit 0
fi
# Using tokenizin's fetch MCP server
exec npx -y @tokenizin/mcp-npx-fetch@latest
