# Code Index MCP

<div align="center">

[![MCP Server](https://img.shields.io/badge/MCP-Server-blue)](https://modelcontextprotocol.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-green)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

**Intelligent code indexing and analysis for Large Language Models**

Transform how AI understands your codebase with advanced search, analysis, and navigation capabilities.

</div>

<a href="https://glama.ai/mcp/servers/@johnhuang316/code-index-mcp">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/@johnhuang316/code-index-mcp/badge" alt="code-index-mcp MCP server" />
</a>

## Overview

Code Index MCP is a [Model Context Protocol](https://modelcontextprotocol.io) server that bridges the gap between AI models and complex codebases. It provides intelligent indexing, advanced search capabilities, and detailed code analysis to help AI assistants understand and navigate your projects effectively.

**Perfect for:** Code review, refactoring, documentation generation, debugging assistance, and architectural analysis.

## Quick Start

### 🚀 **Recommended Setup (Most Users)**

The easiest way to get started with any MCP-compatible application:

**Prerequisites:** Python 3.10+ and [uv](https://github.com/astral-sh/uv)

1. **Add to your MCP configuration** (e.g., `claude_desktop_config.json` or `~/.claude.json`):
   ```json
   {
     "mcpServers": {
       "code-index": {
         "command": "uvx",
         "args": ["code-index-mcp"]
       }
     }
   }
   ```

2. **Restart your application** – `uvx` automatically handles installation and execution

3. **Start using** (give these prompts to your AI assistant):
   ```
   Set the project path to /Users/dev/my-react-app
   Find all TypeScript files in this project  
   Search for "authentication" functions
   Analyze the main App.tsx file
   ```

## Typical Use Cases

**Code Review**: "Find all places using the old API"  
**Refactoring Help**: "Where is this function called?"  
**Learning Projects**: "Show me the main components of this React project"  
**Debugging**: "Search for all error handling related code"

## Key Features

### 🔍 **Intelligent Search & Analysis**
- **Dual-Strategy Architecture**: Specialized tree-sitter parsing for 7 core languages, fallback strategy for 50+ file types
- **Direct Tree-sitter Integration**: No regex fallbacks for specialized languages - fail fast with clear errors
- **Advanced Search**: Auto-detects and uses the best available tool (ugrep, ripgrep, ag, or grep)
- **Universal File Support**: Comprehensive coverage from advanced AST parsing to basic file indexing
- **File Analysis**: Deep insights into structure, imports, classes, methods, and complexity metrics

### 🗂️ **Multi-Language Support**  
- **7 Languages with Tree-sitter AST Parsing**: Python, JavaScript, TypeScript, Java, Go, Objective-C, Zig
- **50+ File Types with Fallback Strategy**: C/C++, Rust, Ruby, PHP, and all other programming languages
- **Document & Config Files**: Markdown, JSON, YAML, XML with appropriate handling
- **Web Frontend**: Vue, React, Svelte, HTML, CSS, SCSS
- **Database**: SQL variants, NoSQL, stored procedures, migrations
- **Configuration**: JSON, YAML, XML, Markdown
- **[View complete list](#supported-file-types)**

### ⚡ **Real-time Monitoring & Auto-refresh**
- **File Watcher**: Automatic index updates when files change
- **Cross-platform**: Native OS file system monitoring
- **Smart Processing**: Batches rapid changes to prevent excessive rebuilds
- **Rich Metadata**: Captures symbols, references, definitions, and relationships

### ⚡ **Performance & Efficiency**
- **Tree-sitter AST Parsing**: Native syntax parsing for accurate symbol extraction
- **Persistent Caching**: Stores indexes for lightning-fast subsequent access
- **Smart Filtering**: Intelligent exclusion of build directories and temporary files
- **Memory Efficient**: Optimized for large codebases
- **Direct Dependencies**: No fallback mechanisms - fail fast with clear error messages

## Supported File Types

<details>
<summary><strong>📁 Programming Languages (Click to expand)</strong></summary>

**Languages with Specialized Tree-sitter Strategies:**
- **Python** (`.py`, `.pyw`) - Full AST analysis with class/method extraction and call tracking
- **JavaScript** (`.js`, `.jsx`, `.mjs`, `.cjs`) - ES6+ class and function parsing with tree-sitter
- **TypeScript** (`.ts`, `.tsx`) - Complete type-aware symbol extraction with interfaces
- **Java** (`.java`) - Full class hierarchy, method signatures, and call relationships
- **Go** (`.go`) - Struct methods, receiver types, and function analysis
- **Objective-C** (`.m`, `.mm`) - Class/instance method distinction with +/- notation
- **Zig** (`.zig`, `.zon`) - Function and struct parsing with tree-sitter AST

**All Other Programming Languages:**
All other programming languages use the **FallbackParsingStrategy** which provides basic file indexing and metadata extraction. This includes:
- **System & Low-Level:** C/C++ (`.c`, `.cpp`, `.h`, `.hpp`), Rust (`.rs`)
- **Object-Oriented:** C# (`.cs`), Kotlin (`.kt`), Scala (`.scala`), Swift (`.swift`)
- **Scripting & Dynamic:** Ruby (`.rb`), PHP (`.php`), Shell (`.sh`, `.bash`)
- **And 40+ more file types** - All handled through the fallback strategy for basic indexing

</details>

<details>
<summary><strong>🌐 Web & Frontend (Click to expand)</strong></summary>

**Frameworks & Libraries:**
- Vue (`.vue`)
- Svelte (`.svelte`)
- Astro (`.astro`)

**Styling:**
- CSS (`.css`, `.scss`, `.less`, `.sass`, `.stylus`, `.styl`)
- HTML (`.html`)

**Templates:**
- Handlebars (`.hbs`, `.handlebars`)
- EJS (`.ejs`)
- Pug (`.pug`)

</details>

<details>
<summary><strong>🗄️ Database & SQL (Click to expand)</strong></summary>

**SQL Variants:**
- Standard SQL (`.sql`, `.ddl`, `.dml`)
- Database-specific (`.mysql`, `.postgresql`, `.psql`, `.sqlite`, `.mssql`, `.oracle`, `.ora`, `.db2`)

**Database Objects:**
- Procedures & Functions (`.proc`, `.procedure`, `.func`, `.function`)
- Views & Triggers (`.view`, `.trigger`, `.index`)

**Migration & Tools:**
- Migration files (`.migration`, `.seed`, `.fixture`, `.schema`)
- Tool-specific (`.liquibase`, `.flyway`)

**NoSQL & Modern:**
- Graph & Query (`.cql`, `.cypher`, `.sparql`, `.gql`)

</details>

<details>
<summary><strong>📄 Documentation & Config (Click to expand)</strong></summary>

- Markdown (`.md`, `.mdx`)
- Configuration (`.json`, `.xml`, `.yml`, `.yaml`)

</details>

### 🛠️ **Development Setup**

For contributing or local development:

1. **Clone and install:**
   ```bash
   git clone https://github.com/johnhuang316/code-index-mcp.git
   cd code-index-mcp
   uv sync
   ```

2. **Configure for local development:**
   ```json
   {
     "mcpServers": {
       "code-index": {
         "command": "uv",
         "args": ["run", "code-index-mcp"]
       }
     }
   }
   ```

3. **Debug with MCP Inspector:**
   ```bash
   npx @modelcontextprotocol/inspector uv run code-index-mcp
   ```

<details>
<summary><strong>Alternative: Manual pip Installation</strong></summary>

If you prefer traditional pip management:

```bash
pip install code-index-mcp
```

Then configure:
```json
{
  "mcpServers": {
    "code-index": {
      "command": "code-index-mcp",
      "args": []
    }
  }
}
```

</details>


## Available Tools

### 🏗️ **Project Management**
| Tool | Description |
|------|-------------|
| **`set_project_path`** | Initialize indexing for a project directory |
| **`refresh_index`** | Rebuild the project index after file changes |
| **`get_settings_info`** | View current project configuration and status |

### 🔍 **Search & Discovery**
| Tool | Description |
|------|-------------|
| **`search_code_advanced`** | Smart search with regex, fuzzy matching, and file filtering |
| **`find_files`** | Locate files using glob patterns (e.g., `**/*.py`) |
| **`get_file_summary`** | Analyze file structure, functions, imports, and complexity |

### 🔄 **Monitoring & Auto-refresh**
| Tool | Description |
|------|-------------|
| **`get_file_watcher_status`** | Check file watcher status and configuration |
| **`configure_file_watcher`** | Enable/disable auto-refresh and configure settings |

### 🛠️ **System & Maintenance**
| Tool | Description |
|------|-------------|
| **`create_temp_directory`** | Set up storage directory for index data |
| **`check_temp_directory`** | Verify index storage location and permissions |
| **`clear_settings`** | Reset all cached data and configurations |
| **`refresh_search_tools`** | Re-detect available search tools (ugrep, ripgrep, etc.) |

## Usage Examples

### 🎯 **Quick Start Workflow**

**1. Initialize Your Project**
```
Set the project path to /Users/dev/my-react-app
```
*Automatically indexes your codebase and creates searchable cache*

**2. Explore Project Structure**
```
Find all TypeScript component files in src/components
```
*Uses: `find_files` with pattern `src/components/**/*.tsx`*

**3. Analyze Key Files**
```
Give me a summary of src/api/userService.ts
```
*Uses: `get_file_summary` to show functions, imports, and complexity*

### 🔍 **Advanced Search Examples**

<details>
<summary><strong>Code Pattern Search</strong></summary>

```
Search for all function calls matching "get.*Data" using regex
```
*Finds: `getData()`, `getUserData()`, `getFormData()`, etc.*

</details>

<details>
<summary><strong>Fuzzy Function Search</strong></summary>

```
Find authentication-related functions with fuzzy search for 'authUser'
```
*Matches: `authenticateUser`, `authUserToken`, `userAuthCheck`, etc.*

</details>

<details>
<summary><strong>Language-Specific Search</strong></summary>

```
Search for "API_ENDPOINT" only in Python files
```
*Uses: `search_code_advanced` with `file_pattern: "*.py"`*

</details>

<details>
<summary><strong>Auto-refresh Configuration</strong></summary>

```
Configure automatic index updates when files change
```
*Uses: `configure_file_watcher` to enable/disable monitoring and set debounce timing*

</details>

<details>
<summary><strong>Project Maintenance</strong></summary>

```
I added new components, please refresh the project index
```
*Uses: `refresh_index` to update the searchable cache*

</details>

## Troubleshooting

### 🔄 **Auto-refresh Not Working**

If automatic index updates aren't working when files change, try:
- `pip install watchdog` (may resolve environment isolation issues)
- Use manual refresh: Call the `refresh_index` tool after making file changes
- Check file watcher status: Use `get_file_watcher_status` to verify monitoring is active

## Development & Contributing

### 🔧 **Building from Source**
```bash
git clone https://github.com/johnhuang316/code-index-mcp.git
cd code-index-mcp
uv sync
uv run code-index-mcp
```

### 🐛 **Debugging**
```bash
npx @modelcontextprotocol/inspector uvx code-index-mcp
```

### 🤝 **Contributing**
Contributions are welcome! Please feel free to submit a Pull Request.

---

### 📜 **License**
[MIT License](LICENSE)

### 🌐 **Translations**
- [繁體中文](README_zh.md)
- [日本語](README_ja.md)
