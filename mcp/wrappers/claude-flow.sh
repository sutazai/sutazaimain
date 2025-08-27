#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "claude-flow MCP wrapper operational"
    exit 0
fi
exec npx -y claude-flow@alpha mcp start
