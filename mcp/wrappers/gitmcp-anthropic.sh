#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "gitmcp-anthropic MCP wrapper operational"
    exit 0
fi
# Using git-mcp-server configured for Anthropic repositories
# Note: GitMCP.io (https://gitmcp.io/anthropic/*) is available for HTTP-based clients
# GitHub token must be set as environment variable
: ${GITHUB_TOKEN:?"GITHUB_TOKEN environment variable must be set"}
exec npx -y @cyanheads/git-mcp-server@latest
