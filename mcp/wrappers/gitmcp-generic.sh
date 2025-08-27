#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "gitmcp-generic MCP wrapper operational"
    exit 0
fi
echo '{"capabilities":{"tools":{},"resources":{}}}'
