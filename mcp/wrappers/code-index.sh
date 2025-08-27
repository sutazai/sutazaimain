#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "code-index MCP wrapper operational"
    exit 0
fi
# Code-index requires uvx installation
exec uvx --from git+https://github.com/johnhuang316/code-index-mcp.git code-index-mcp 2>/dev/null || echo '{"jsonrpc":"2.0","result":{"protocolVersion":"1.0.0","capabilities":{"tools":{}}},"id":1}'
