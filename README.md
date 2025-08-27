# MCP Server Configuration

Complete configuration for Model Context Protocol (MCP) servers integrated with Claude.

## Overview

This repository contains the configuration and wrapper scripts for 19 MCP servers that provide extended capabilities to Claude through the MCP protocol.

## MCP Servers Configured

All servers have been updated to use official npm packages from their respective maintainers:

### Core Functionality
- **filesystem** - File system operations
- **github** - GitHub API integration  
- **memory** - Persistent memory storage
- **everything** - Testing and demonstration server

### AI & Reasoning
- **sequential-thinking** - Multi-step reasoning engine
- **claude-flow** - AI swarm coordination
- **ruv-swarm** - Distributed agent management

### Documentation & Search
- **context7** - Official library documentation lookup
- **ddg** - DuckDuckGo web search (nickclyde/duckduckgo-mcp-server)
- **http-fetch** - Web content fetching (@tokenizin/mcp-npx-fetch)

### Git Integration
- **gitmcp-sutazai** - Sutazai repository documentation
- **gitmcp-anthropic** - Anthropic repository access
- **gitmcp-docs** - Generic documentation fetching

### Development Tools
- **playwright** - Browser automation (microsoft/playwright-mcp)
- **code-index** - Code search and indexing
- **github-project-manager** - GitHub project management

### Memory & Storage
- **extended-memory** - Extended memory capabilities
- **memory-bank** - Project-based memory storage (alioshr/memory-bank-mcp)

## Installation

All servers are configured to run via npx, so no local installation is required. They will be automatically downloaded and executed when called.

### Playwright Setup

For Playwright browser automation, you may need to install browser binaries:
```bash
npx playwright install
npx playwright install-deps
```

## Configuration

The main configuration file `.mcp.json` maps each server to its wrapper script:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "/path/to/wrapper/script.sh"
    }
  }
}
```

Each wrapper script in `scripts/mcp/wrappers/` handles:
- Self-check validation
- Environment variable setup
- Execution via npx with latest package version

## Environment Variables

Some servers require environment variables:
- `GITHUB_TOKEN` - For GitHub API authentication
- `GITHUB_OWNER` - GitHub organization/user
- `GITHUB_REPO` - Default repository name
- `MEMORY_BANK_ROOT` - Root directory for memory-bank storage

## Testing

All servers have been tested and validated. To test a specific server:
```bash
./scripts/mcp/wrappers/[server-name].sh --selfcheck
```

## License

MIT

## Credits

Built with official MCP server packages from:
- Microsoft (playwright-mcp)
- nickclyde (duckduckgo-mcp-server)
- alioshr (memory-bank-mcp)
- tokenizin (mcp-npx-fetch)
- cyanheads (git-mcp-server)
- And many other contributors to the MCP ecosystem