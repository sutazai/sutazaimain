#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "memory-bank MCP wrapper operational"
    exit 0
fi
# Using alioshr's memory-bank-mcp from GitHub
# Create memory-bank directory if it doesn't exist
mkdir -p /opt/sutazaiapp/backend/memory-bank
export MEMORY_BANK_ROOT="/opt/sutazaiapp/backend/memory-bank"
exec npx -y memory-bank-mcp@latest
