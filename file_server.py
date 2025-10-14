#!/usr/bin/env python3
"""
Minimal MCP File Server MVP
Provides access to .md files in data/ directory
"""

import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("File Server")

@mcp.tool()
def list_files() -> list[str]:
    """List all .md files in data/ directory"""
    try:
        files = os.listdir("data")
        md_files = [f for f in files if f.endswith(".md")]
        return md_files
    except Exception as e:
        return [f"Error: {str(e)}"]

@mcp.tool()
def read_file(filename: str) -> str:
    """Read a .md file from data/ directory"""
    try:
        # Basic security validation
        if ".." in filename or not filename.endswith(".md"):
            return "Error: Invalid filename"
        
        file_path = Path("data") / filename
        return file_path.read_text()
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    mcp.run()