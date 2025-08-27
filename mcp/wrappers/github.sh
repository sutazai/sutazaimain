#!/bin/bash

# GitHub MCP Wrapper
# Provides GitHub API access

set -e

# Handle selfcheck
if [[ "$1" == "--selfcheck" ]]; then
    echo "GitHub MCP wrapper operational"
    exit 0
fi

# GitHub token must be set as environment variable
: ${GITHUB_TOKEN:?"GITHUB_TOKEN environment variable must be set"}

# Start the MCP server using npx
exec npx -y @modelcontextprotocol/server-github "$@"
