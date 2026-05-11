import asyncio
import json
import logging
import time
import subprocess
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

class MCPClientManager:
    def __init__(self, server_configs):
        """
        server_configs is a dict: 
        {
            "puppeteer": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-puppeteer"]},
            ...
        }
        """
        self.server_configs = server_configs
        self.sessions = {} # name -> (session, read, write)
        self.tools = []
        self._loop = asyncio.new_event_loop()
        self._thread = None
        
    def start(self):
        """Start the background asyncio loop and connect to all configured servers."""
        from threading import Thread
        def run_loop():
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._connect_all())
            self._loop.run_forever()

        self._thread = Thread(target=run_loop, daemon=True)
        self._thread.start()
        
        # Wait a bit for servers to initialize
        time.sleep(2)

    async def _connect_all(self):
        for name, config in self.server_configs.items():
            try:
                server_params = StdioServerParameters(
                    command=config["command"],
                    args=config.get("args", []),
                    env=config.get("env", None)
                )
                
                # stdio_client is an async context manager, but we need to keep it alive
                # So we manually enter it
                from contextlib import AsyncExitStack
                self.stack = AsyncExitStack()
                read, write = await self.stack.enter_async_context(stdio_client(server_params))
                
                session = await self.stack.enter_async_context(ClientSession(read, write))
                await session.initialize()
                
                self.sessions[name] = session
                
                # Fetch tools
                tools_response = await session.list_tools()
                for t in tools_response.tools:
                    self.tools.append({
                        "name": t.name,
                        "description": t.description,
                        "server": name
                    })
            except Exception as e:
                logging.error(f"Failed to start MCP server {name}: {e}")

    def get_tool_descriptions(self):
        desc = ""
        for t in self.tools:
            desc += f"- {t['name']}: [MCP: {t['server']}] {t['description']}\n"
        return desc

    def call_tool(self, name, arguments):
        """Synchronous wrapper to call a tool."""
        # Find which server owns this tool
        server_name = None
        for t in self.tools:
            if t["name"] == name:
                server_name = t["server"]
                break
                
        if not server_name:
            return f"Error: MCP tool {name} not found."
            
        session = self.sessions.get(server_name)
        if not session:
            return f"Error: MCP server {server_name} is not connected."

        future = asyncio.run_coroutine_threadsafe(
            session.call_tool(name, arguments=arguments),
            self._loop
        )
        
        try:
            result = future.result(timeout=30)
            # result is a CallToolResult
            # Extract content text
            output = ""
            for content in result.content:
                if content.type == "text":
                    output += content.text + "\n"
            return output.strip() if output else "Success (No output)"
        except Exception as e:
            return f"MCP Tool execution failed: {e}"

    def stop(self):
        if self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
