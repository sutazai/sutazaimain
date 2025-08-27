"""
Code Index MCP Server

This MCP server allows LLMs to index, search, and analyze code from a project directory.
It provides tools for file discovery, content retrieval, and code analysis.

This version uses a service-oriented architecture where MCP decorators delegate
to domain-specific services for business logic.
"""

# Standard library imports
import sys
import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, Dict, Any, Optional, List

# Third-party imports
from mcp import types
from mcp.server.fastmcp import FastMCP, Context

# Local imports
from .project_settings import ProjectSettings
from .services import (
    SearchService, FileService, SettingsService, FileWatcherService
)
from .services.settings_service import manage_temp_directory
from .services.file_discovery_service import FileDiscoveryService
from .services.project_management_service import ProjectManagementService
from .services.index_management_service import IndexManagementService
from .services.code_intelligence_service import CodeIntelligenceService
from .services.system_management_service import SystemManagementService
from .utils import (
    handle_mcp_resource_errors, handle_mcp_tool_errors
)

# Setup logging without writing to files
def setup_indexing_performance_logging():
    """Setup logging (stderr only); remove any file-based logging."""

    root_logger = logging.getLogger()
    root_logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # stderr for errors only
    stderr_handler = logging.StreamHandler(sys.stderr)
    stderr_handler.setFormatter(formatter)
    stderr_handler.setLevel(logging.ERROR)

    root_logger.addHandler(stderr_handler)
    root_logger.setLevel(logging.DEBUG)

# Initialize logging (no file handlers)
setup_indexing_performance_logging()

@dataclass
class CodeIndexerContext:
    """Context for the Code Indexer MCP server."""
    base_path: str
    settings: ProjectSettings
    file_count: int = 0
    index_manager: Optional['UnifiedIndexManager'] = None
    file_watcher_service: FileWatcherService = None

@asynccontextmanager
async def indexer_lifespan(_server: FastMCP) -> AsyncIterator[CodeIndexerContext]:
    """Manage the lifecycle of the Code Indexer MCP server."""
    # Don't set a default path, user must explicitly set project path
    base_path = ""  # Empty string to indicate no path is set

    # Initialize settings manager with skip_load=True to skip loading files
    settings = ProjectSettings(base_path, skip_load=True)

    # Initialize context - file watcher will be initialized later when project path is set
    context = CodeIndexerContext(
        base_path=base_path,
        settings=settings,
        file_watcher_service=None
    )

    try:
        # Provide context to the server
        yield context
    finally:
        # Stop file watcher if it was started
        if context.file_watcher_service:
            context.file_watcher_service.stop_monitoring()

        # Only save index if project path has been set
        if context.base_path and context.index_manager:
            context.index_manager.save_index()

# Create the MCP server with lifespan manager
mcp = FastMCP("CodeIndexer", lifespan=indexer_lifespan, dependencies=["pathlib"])

# ----- RESOURCES -----

@mcp.resource("config://code-indexer")
@handle_mcp_resource_errors
def get_config() -> str:
    """Get the current configuration of the Code Indexer."""
    ctx = mcp.get_context()
    return ProjectManagementService(ctx).get_project_config()

@mcp.resource("files://{file_path}")
@handle_mcp_resource_errors
def get_file_content(file_path: str) -> str:
    """Get the content of a specific file."""
    ctx = mcp.get_context()
    # Use FileService for simple file reading - this is appropriate for a resource
    return FileService(ctx).get_file_content(file_path)

@mcp.resource("structure://project")
@handle_mcp_resource_errors
def get_project_structure() -> str:
    """Get the structure of the project as a JSON tree."""
    ctx = mcp.get_context()
    return ProjectManagementService(ctx).get_project_structure()

# Removed: settings://stats resource - this information is available via get_settings_info() tool
# and is more of a debugging/technical detail rather than context AI needs

# ----- TOOLS -----

@mcp.tool()
@handle_mcp_tool_errors(return_type='str')
def set_project_path(path: str, ctx: Context) -> str:
    """Set the base project path for indexing."""
    return ProjectManagementService(ctx).initialize_project(path)

@mcp.tool()
@handle_mcp_tool_errors(return_type='dict')
def search_code_advanced(
    pattern: str,
    ctx: Context,
    case_sensitive: bool = True,
    context_lines: int = 0,
    file_pattern: str = None,
    fuzzy: bool = False,
    regex: bool = None
) -> Dict[str, Any]:
    """
    Search for a code pattern in the project using an advanced, fast tool.

    This tool automatically selects the best available command-line search tool
    (like ugrep, ripgrep, ag, or grep) for maximum performance.

    Args:
        pattern: The search pattern. Can be literal text or regex (see regex parameter).
        case_sensitive: Whether the search should be case-sensitive.
        context_lines: Number of lines to show before and after the match.
        file_pattern: A glob pattern to filter files to search in
                     (e.g., "*.py", "*.js", "test_*.py").
                     All search tools now handle glob patterns consistently:
                     - ugrep: Uses glob patterns (*.py, *.{js,ts})
                     - ripgrep: Uses glob patterns (*.py, *.{js,ts})
                     - ag (Silver Searcher): Automatically converts globs to regex patterns
                     - grep: Basic glob pattern matching
                     All common glob patterns like "*.py", "test_*.js", "src/*.ts" are supported.
        fuzzy: If True, enables fuzzy/partial matching behavior varies by search tool:
               - ugrep: Native fuzzy search with --fuzzy flag (true edit-distance fuzzy search)
               - ripgrep, ag, grep, basic: Word boundary pattern matching (not true fuzzy search)
               IMPORTANT: Only ugrep provides true fuzzy search. Other tools use word boundary
               matching which allows partial matches at word boundaries.
               For exact literal matches, set fuzzy=False (default and recommended).
        regex: Controls regex pattern matching behavior:
               - If True, enables regex pattern matching
               - If False, forces literal string search
               - If None (default), automatically detects regex patterns and enables regex for patterns like "ERROR|WARN"
               The pattern will always be validated for safety to prevent ReDoS attacks.

    Returns:
        A dictionary containing the search results or an error message.

    """
    return SearchService(ctx).search_code(
        pattern=pattern,
        case_sensitive=case_sensitive,
        context_lines=context_lines,
        file_pattern=file_pattern,
        fuzzy=fuzzy,
        regex=regex
    )

@mcp.tool()
@handle_mcp_tool_errors(return_type='list')
def find_files(pattern: str, ctx: Context) -> List[str]:
    """
    Find files matching a glob pattern using pre-built file index.

    Use when:
    - Looking for files by pattern (e.g., "*.py", "test_*.js")
    - Searching by filename only (e.g., "README.md" finds all README files)
    - Checking if specific files exist in the project
    - Getting file lists for further analysis

    Pattern matching:
    - Supports both full path and filename-only matching
    - Uses standard glob patterns (*, ?, [])
    - Fast lookup using in-memory file index
    - Uses forward slashes consistently across all platforms

    Args:
        pattern: Glob pattern to match files (e.g., "*.py", "test_*.js", "README.md")

    Returns:
        List of file paths matching the pattern
    """
    return FileDiscoveryService(ctx).find_files(pattern)

@mcp.tool()
@handle_mcp_tool_errors(return_type='dict')
def get_file_summary(file_path: str, ctx: Context) -> Dict[str, Any]:
    """
    Get a summary of a specific file, including:
    - Line count
    - Function/class definitions (for supported languages)
    - Import statements
    - Basic complexity metrics
    """
    return CodeIntelligenceService(ctx).analyze_file(file_path)

@mcp.tool()
@handle_mcp_tool_errors(return_type='str')
def refresh_index(ctx: Context) -> str:
    """
    Manually refresh the project index when files have been added/removed/moved.

    Use when:
    - File watcher is disabled or unavailable
    - After large-scale operations (git checkout, merge, pull) that change many files
    - When you want immediate index rebuild without waiting for file watcher debounce
    - When find_files results seem incomplete or outdated
    - For troubleshooting suspected index synchronization issues

    Important notes for LLMs:
    - Always available as backup when file watcher is not working
    - Performs full project re-indexing for complete accuracy
    - Use when you suspect the index is stale after file system changes
    - **Call this after programmatic file modifications if file watcher seems unresponsive**
    - Complements the automatic file watcher system

    Returns:
        Success message with total file count
    """
    return IndexManagementService(ctx).rebuild_index()

@mcp.tool()
@handle_mcp_tool_errors(return_type='dict')
def get_settings_info(ctx: Context) -> Dict[str, Any]:
    """Get information about the project settings."""
    return SettingsService(ctx).get_settings_info()

@mcp.tool()
@handle_mcp_tool_errors(return_type='dict')
def create_temp_directory() -> Dict[str, Any]:
    """Create the temporary directory used for storing index data."""
    return manage_temp_directory('create')

@mcp.tool()
@handle_mcp_tool_errors(return_type='dict')
def check_temp_directory() -> Dict[str, Any]:
    """Check the temporary directory used for storing index data."""
    return manage_temp_directory('check')

@mcp.tool()
@handle_mcp_tool_errors(return_type='str')
def clear_settings(ctx: Context) -> str:
    """Clear all settings and cached data."""
    return SettingsService(ctx).clear_all_settings()

@mcp.tool()
@handle_mcp_tool_errors(return_type='str')
def refresh_search_tools(ctx: Context) -> str:
    """
    Manually re-detect the available command-line search tools on the system.
    This is useful if you have installed a new tool (like ripgrep) after starting the server.
    """
    return SearchService(ctx).refresh_search_tools()

@mcp.tool()
@handle_mcp_tool_errors(return_type='dict')
def get_file_watcher_status(ctx: Context) -> Dict[str, Any]:
    """Get file watcher service status and statistics."""
    return SystemManagementService(ctx).get_file_watcher_status()

@mcp.tool()
@handle_mcp_tool_errors(return_type='str')
def configure_file_watcher(
    ctx: Context,
    enabled: bool = None,
    debounce_seconds: float = None,
    additional_exclude_patterns: list = None
) -> str:
    """Configure file watcher service settings."""
    return SystemManagementService(ctx).configure_file_watcher(enabled, debounce_seconds, additional_exclude_patterns)

# ----- PROMPTS -----

@mcp.prompt()
def analyze_code(file_path: str = "", query: str = "") -> list[types.PromptMessage]:
    """Prompt for analyzing code in the project."""
    messages = [
        types.PromptMessage(role="user", content=types.TextContent(type="text", text=f"""I need you to analyze some code from my project.

{f'Please analyze the file: {file_path}' if file_path else ''}
{f'I want to understand: {query}' if query else ''}

First, let me give you some context about the project structure. Then, I'll provide the code to analyze.
""")),
        types.PromptMessage(
            role="assistant",
            content=types.TextContent(
                type="text",
                text="I'll help you analyze the code. Let me first examine the project structure to get a better understanding of the codebase."
            )
        )
    ]
    return messages

@mcp.prompt()
def code_search(query: str = "") -> types.TextContent:
    """Prompt for searching code in the project."""
    search_text = "\"query\"" if not query else f"\"{query}\""
    return types.TextContent(
        type="text",
        text=f"""I need to search through my codebase for {search_text}.

Please help me find all occurrences of this query and explain what each match means in its context.
Focus on the most relevant files and provide a brief explanation of how each match is used in the code.

If there are too many results, prioritize the most important ones and summarize the patterns you see."""
    )

@mcp.prompt()
def set_project() -> list[types.PromptMessage]:
    """Prompt for setting the project path."""
    messages = [
        types.PromptMessage(role="user", content=types.TextContent(type="text", text="""
        I need to analyze code from a project, but I haven't set the project path yet. Please help me set up the project path and index the code.

        First, I need to specify which project directory to analyze.
        """)),
        types.PromptMessage(role="assistant", content=types.TextContent(type="text", text="""
        Before I can help you analyze any code, we need to set up the project path. This is a required first step.

        Please provide the full path to your project folder. For example:
        - Windows: "C:/Users/username/projects/my-project"
        - macOS/Linux: "/home/username/projects/my-project"

        Once you provide the path, I'll use the `set_project_path` tool to configure the code analyzer to work with your project.
        """))
    ]
    return messages

def main():
    """Main function to run the MCP server."""
    mcp.run()

if __name__ == '__main__':
    main()
