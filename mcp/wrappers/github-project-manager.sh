#!/bin/bash
if [ "$1" == "--selfcheck" ]; then
    echo "github-project-manager MCP wrapper operational"
    exit 0
fi
# GitHub token will be read from environment
# Defaults provided but can be overridden
: ${GITHUB_TOKEN:?"GITHUB_TOKEN environment variable must be set"}
: ${GITHUB_OWNER:="sutazai"}
: ${GITHUB_REPO:="sutazaiapp"}
exec npx -y mcp-github-project-manager@latest
