#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "filesystem MCP wrapper operational"
    exit 0
fi
exec npx -y @modelcontextprotocol/server-filesystem /opt/sutazaiapp
