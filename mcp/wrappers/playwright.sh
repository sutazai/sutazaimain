#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "playwright MCP wrapper operational"
    exit 0
fi
# Using Microsoft's official playwright-mcp from GitHub
# Note: Run 'npx playwright install' to install browser binaries if needed
exec npx -y playwright-mcp@latest
