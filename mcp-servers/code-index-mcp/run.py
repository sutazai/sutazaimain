#!/usr/bin/env python
"""
Development convenience script to run the Code Index MCP server.
"""
import sys
import os

# Add src directory to path
src_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src')
sys.path.insert(0, src_path)

try:
    from code_index_mcp.server import main

    if __name__ == "__main__":
        main()
except Exception:
    # Exit silently on failure without printing any messages
    raise SystemExit(1)
