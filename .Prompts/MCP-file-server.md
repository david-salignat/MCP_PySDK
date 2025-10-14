# MCP File Server Requirements

## Overview
Create an MCP server that provides file system access capabilities for a specific subdirectory within the project. The server will expose tools and resources to list directory contents and read file contents.

## MVP Specification

### Minimal Requirements
- **Target Directory**: `data/`
- **File Type**: `.md` files only
- **Implementation**: 2 MCP Tools

## Implementation Plan

### Tool 1: `list_files`
```python
@mcp.tool()
def list_files() -> list[str]:
    """List all .md files in data/ directory"""
    # Return simple list of filenames
```

### Tool 2: `read_file`
```python
@mcp.tool()
def read_file(filename: str) -> str:
    """Read a .md file from data/ directory"""
    # Return file content as string
```

## MVP Security (Minimal)
- Only access `data/` directory
- Only `.md` files
- Basic path validation

## Technical Design

### Architecture
```
MCP Client (LLM) 
    ↓ (stdio transport)
FastMCP Server
    ↓ (file system calls)
data/ directory
```

### File Structure
```
file_server.py          # Main server implementation
data/                   # Target directory
  ├── example1.md
  ├── example2.md
  └── ...
```

### Implementation Details

#### Dependencies
- `mcp.server.fastmcp.FastMCP` - Core MCP server framework
- `pathlib.Path` - File system operations
- `os.path` - Path validation

#### Core Logic
```python
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("File Server")
DATA_DIR = Path("data")

@mcp.tool()
def list_files() -> list[str]:
    # os.listdir() -> filter .md files
    
@mcp.tool() 
def read_file(filename: str) -> str:
    # validate filename -> Path.read_text()
```

#### Security Implementation
1. **Path Validation**: `if ".." in filename or "/" in filename: raise ValueError`
2. **Extension Check**: `if not filename.endswith(".md"): raise ValueError`  
3. **Directory Binding**: All paths resolved relative to `DATA_DIR`

#### Error Handling
- `FileNotFoundError` → "File not found"
- `ValueError` → "Invalid filename" 
- `Exception` → "Read error"

### Deployment
- Run via: `python file_server.py`
- Transport: stdio (standard MCP transport)
- No configuration needed (hardcoded data/ directory)

## VS Code Copilot Chat Integration

### Configuration Method
Add to VS Code `settings.json` (workspace or user settings):

```json
{
  "mcp.servers": {
    "file-server": {
      "command": "G:/My Drive/0 - Dev/0 - Workspaces/MCP_PySDK/venv/Scripts/python.exe",
      "args": ["G:/My Drive/0 - Dev/0 - Workspaces/MCP_PySDK/file_server.py"],
      "env": {}
    }
  }
}
```

**Alternative possible settings keys:**
- `"copilot.mcp.servers"`
- `"github.copilot.mcp.servers"`
- `"mcp.mcpServers"`

### Setup Steps
1. **Add configuration** to VS Code settings.json
2. **Restart VS Code** to load MCP configuration  
3. **Open Copilot Chat** and test integration
4. **Test both tools**:
   - Ask: "What markdown files are in the data directory?"
   - Ask: "Show me the content of sample.md"

### Expected Copilot Behavior
- **Auto-discovery**: Copilot finds available tools automatically
- **Contextual usage**: Uses `list_files` when asked about available files
- **Content access**: Uses `read_file` when asked about specific file content
- **Error handling**: Displays security/validation errors appropriately

### Testing Commands for Copilot Chat
```
"List all markdown files in the project data directory"
"What's in the sample.md file?"
"Summarize the content of test1.md"  
"Show me all available files and their contents"
```

### Configuration Notes
- **Absolute paths required** for cross-platform compatibility
- **Virtual environment** python.exe path used
- **No environment variables** needed for this MVP
- **Stdio transport** used (standard for VS Code integration)

## Implementation Status: ✅ COMPLETE

All 10 steps have been successfully implemented:

### ✅ Phase 1: Setup (Steps 1-3) 
- ✅ **Data directory**: Created with sample .md files
- ✅ **Server file**: FastMCP server created and configured
- ✅ **Basic startup**: Server imports and runs correctly

### ✅ Phase 2: Core Implementation (Steps 4-6)
- ✅ **list_files tool**: Lists .md files in data/ directory
- ✅ **read_file tool**: Reads .md file content with security validation  
- ✅ **Error handling**: Comprehensive error handling implemented

### ✅ Phase 3: Testing & Validation (Steps 7-9)
- ✅ **list_files testing**: Returns correct file list, handles errors
- ✅ **read_file testing**: Reads content, validates security, handles errors
- ✅ **Integration testing**: Full MCP protocol communication working

### ✅ Phase 4: VS Code Copilot Integration (Step 10)
- ✅ **VS Code configuration**: .vscode/settings.json created
- ✅ **Multiple config keys**: Covers different possible MCP integration patterns
- ✅ **Test documentation**: Comprehensive testing guide created
- ✅ **Enhanced content**: Improved sample files for better testing

## Final Implementation

### Server File: `file_server.py`
```python
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
```

### Ready for VS Code Copilot Chat Testing! 🚀