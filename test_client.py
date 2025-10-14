#!/usr/bin/env python3
"""
Minimal MCP client to test our file server
"""
import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

async def test_integration():
    """Test integration with our file server"""
    print("=== MCP File Server Integration Test ===")
    
    # Get the python executable path from our venv
    python_path = Path("venv/Scripts/python.exe").absolute()
    server_path = Path("file_server.py").absolute()
    
    # Create server parameters
    server_params = StdioServerParameters(
        command=str(python_path),
        args=[str(server_path)]
    )
    
    try:
        # Connect to server
        print("Connecting to file server...")
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("Initializing session...")
                await session.initialize()
                print("✓ Connected successfully!")
                
                # Test list_tools
                print("\n1. Testing list_tools...")
                tools = await session.list_tools()
                print(f"Available tools: {[t.name for t in tools.tools]}")
                
                # Test list_files tool
                print("\n2. Testing list_files tool...")
                result = await session.call_tool("list_files", {})
                print(f"list_files result: {result.content}")
                
                # Test read_file tool
                print("\n3. Testing read_file tool...")
                result = await session.call_tool("read_file", {"filename": "sample.md"})
                print(f"read_file result: {str(result.content)[:100]}...")
                
                print("\n✓ All integration tests passed!")
                
    except Exception as e:
        print(f"✗ Integration test failed: {e}")
        return False
        
    return True

if __name__ == "__main__":
    success = asyncio.run(test_integration())