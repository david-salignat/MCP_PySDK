#!/usr/bin/env python3
"""
Test error cases for MCP file server
"""
import asyncio
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_error_cases():
    """Test error handling in our file server"""
    print("=== Testing Error Cases ===")
    
    python_path = Path("venv/Scripts/python.exe").absolute()
    server_path = Path("file_server.py").absolute()
    
    server_params = StdioServerParameters(
        command=str(python_path),
        args=[str(server_path)]
    )
    
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Test invalid filename
                print("1. Testing invalid filename...")
                result = await session.call_tool("read_file", {"filename": "../secret.txt"})
                print(f"Security test result: {result.content}")
                
                # Test missing file
                print("2. Testing missing file...")
                result = await session.call_tool("read_file", {"filename": "missing.md"})
                print(f"Missing file result: {result.content}")
                
                # Test wrong extension
                print("3. Testing wrong extension...")
                result = await session.call_tool("read_file", {"filename": "test.txt"})
                print(f"Wrong extension result: {result.content}")
                
                print("\n✓ Error handling tests completed!")
                
    except Exception as e:
        print(f"✗ Error test failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_error_cases())