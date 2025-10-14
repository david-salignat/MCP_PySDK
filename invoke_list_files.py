#!/usr/bin/env python3
"""
Direct invocation of the list_files MCP tool.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def invoke_list_files_tool():
    """Directly invoke the list_files tool."""
    print("🔧 Invoking list_files MCP Tool")
    print("===============================")
    
    # Server configuration
    server_params = StdioServerParameters(
        command="python",
        args=["file_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            print("✓ Connected to MCP server")
            
            # Invoke list_files tool
            print("\n📋 Calling list_files tool...")
            try:
                result = await session.call_tool("list_files", {})
                print("✓ Tool executed successfully!")
                print("\n📁 Results:")
                
                for i, content in enumerate(result.content, 1):
                    if content.type == 'text':
                        print(f"   {i}. {content.text}")
                
                print(f"\n📊 Total files found: {len(result.content)}")
                
            except Exception as e:
                print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(invoke_list_files_tool())