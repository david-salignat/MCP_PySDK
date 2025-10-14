#!/usr/bin/env python3
"""
Demonstration script for using the list_files MCP tool.
This shows how VS Code Copilot Chat would invoke your MCP server tools.
"""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.types import TextContent

async def demonstrate_list_files_tool():
    """Demonstrate the list_files tool functionality."""
    print("🔧 MCP File Server Tool Demonstration")
    print("=====================================")
    
    # Server configuration (same as in .vscode/mcp.json)
    server_params = StdioServerParameters(
        command="python",
        args=["file_server.py"],
        env=None
    )
    
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the session
            await session.initialize()
            
            print("✓ Connected to MCP file server")
            print()
            
            # List available tools
            tools = await session.list_tools()
            print(f"📋 Available tools: {[tool.name for tool in tools.tools]}")
            print()
            
            # Use the list_files tool
            print("🗂️  Calling list_files tool...")
            print("   This is equivalent to what VS Code Copilot Chat does when you ask:")
            print("   'List files in data directory using list-files tool'")
            print()
            
            try:
                result = await session.call_tool("list_files", {})
                print("📁 Files in data/ directory:")
                print("   " + "="*30)
                
                for content in result.content:
                    if content.type == 'text':
                        print(f"   📄 {content.text}")
                
                print("   " + "="*30)
                print("✓ list_files tool executed successfully!")
                
            except Exception as e:
                print(f"❌ Error calling list_files tool: {e}")
            
            print()
            print("🎯 How to use in VS Code Copilot Chat:")
            print("   1. Open Chat view (Ctrl+Alt+I)")
            print("   2. Switch to Agent mode")
            print("   3. Ask: 'List the files in the data directory'")
            print("   4. VS Code will automatically invoke the list_files tool")

if __name__ == "__main__":
    asyncio.run(demonstrate_list_files_tool())