import asyncio
import json
import logging
import time
import subprocess
from contextlib import AsyncExitStack

try:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    HAS_MCP = True
except ImportError:
    HAS_MCP = False

logger = logging.getLogger("Aether.MCP")


class MCPRouter:
    """
    Lightweight intent-based router for MCP tools.
    Maps tool names to their owning server and provides
    keyword-based suggestion for tool selection.
    """

    # Keyword → tool name hints for intent matching
    KEYWORD_MAP = {
        "fetch": ["fetch", "url", "web", "http", "download", "scrape"],
        "memory": ["remember", "memory", "store", "recall", "forget", "knowledge"],
        "filesystem": ["file", "read", "write", "directory", "folder", "ls", "cat"],
        "search": ["search", "find", "query", "lookup", "duckduckgo", "ddg"],
    }

    def __init__(self):
        self._tool_to_server = {}   # tool_name → server_name
        self._server_to_tools = {}  # server_name → [tool_name, ...]

    def register(self, tool_name, server_name):
        self._tool_to_server[tool_name] = server_name
        self._server_to_tools.setdefault(server_name, []).append(tool_name)

    def route(self, tool_name):
        """Direct lookup: tool_name → server_name or None."""
        return self._tool_to_server.get(tool_name)

    def suggest_tools(self, user_intent):
        """
        Keyword heuristic: return tool names whose server category
        matches keywords in the user's intent string.
        """
        intent_lower = user_intent.lower()
        matched = set()
        for category, keywords in self.KEYWORD_MAP.items():
            if any(kw in intent_lower for kw in keywords):
                # Return all tools from servers in that category
                for tool_name, server_name in self._tool_to_server.items():
                    if category in server_name.lower():
                        matched.add(tool_name)
        return list(matched)


class MCPClientManager:
    """
    MCP Client Manager v2 — Multi-server lifecycle, schema forwarding,
    and intent-based routing.
    """

    def __init__(self, server_configs):
        """
        server_configs is a dict:
        {
            "fetch": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-fetch"]},
            "memory": {"command": "npx", "args": ["-y", "@modelcontextprotocol/server-memory"]},
            ...
        }
        """
        self.server_configs = server_configs
        self.sessions = {}          # name → ClientSession
        self._stacks = {}           # name → AsyncExitStack  (per-server lifecycle)
        self.tools = []             # [{name, description, server, input_schema}, ...]
        self.router = MCPRouter()
        self._loop = None
        self._thread = None

    def start(self):
        """Start the background asyncio loop and connect to all configured servers."""
        if not HAS_MCP:
            logger.warning("MCP SDK not installed (requires Python 3.10+). MCP features disabled. Install with: pip install mcp")
            return

        from threading import Thread

        self._loop = asyncio.new_event_loop()

        def run_loop():
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._connect_all())
            self._loop.run_forever()

        self._thread = Thread(target=run_loop, daemon=True)
        self._thread.start()

        # Wait for servers to initialize (bounded)
        deadline = time.monotonic() + 8
        while time.monotonic() < deadline:
            if len(self.sessions) >= len(self.server_configs):
                break
            time.sleep(0.25)

    async def _connect_all(self):
        """Connect to every configured MCP server independently."""
        for name, config in self.server_configs.items():
            await self._connect_server(name, config)

    async def _connect_server(self, name, config):
        """Connect to a single MCP server with its own AsyncExitStack."""
        try:
            server_params = StdioServerParameters(
                command=config["command"],
                args=config.get("args", []),
                env=config.get("env", None)
            )

            stack = AsyncExitStack()
            self._stacks[name] = stack

            read, write = await stack.enter_async_context(stdio_client(server_params))
            session = await stack.enter_async_context(ClientSession(read, write))
            await session.initialize()

            self.sessions[name] = session

            # Fetch and register tools with schema
            tools_response = await session.list_tools()
            for t in tools_response.tools:
                tool_entry = {
                    "name": t.name,
                    "description": t.description or "",
                    "server": name,
                    "input_schema": getattr(t, "inputSchema", None) or {},
                }
                self.tools.append(tool_entry)
                self.router.register(t.name, name)

            logger.info(f"MCP server '{name}' connected — {len(tools_response.tools)} tools registered.")

        except Exception as e:
            logger.warning(f"Failed to start MCP server '{name}': {e}  (continuing without it)")

    def get_tool_descriptions(self):
        """
        Return schema-aware tool descriptions for LLM prompt injection.
        Format:
          - tool_name(param1: type [required], param2: type): [MCP: server] Description.
        """
        lines = []
        for t in self.tools:
            sig = self._format_signature(t)
            lines.append(f"- {sig}: [MCP: {t['server']}] {t['description']}")
        return "\n".join(lines)

    @staticmethod
    def _format_signature(tool):
        """Build a human-readable function signature from JSON Schema."""
        schema = tool.get("input_schema", {})
        properties = schema.get("properties", {})
        required = set(schema.get("required", []))

        if not properties:
            return tool["name"] + "()"

        params = []
        for pname, pdef in properties.items():
            ptype = pdef.get("type", "any")
            req_tag = " [required]" if pname in required else ""
            params.append(f"{pname}: {ptype}{req_tag}")

        return f"{tool['name']}({', '.join(params)})"

    def get_tool_schemas(self):
        """Return the raw tool list with schemas (for programmatic use)."""
        return list(self.tools)

    def call_tool(self, name, arguments):
        """Synchronous wrapper to call an MCP tool by name."""
        server_name = self.router.route(name)
        if not server_name:
            return f"Error: MCP tool '{name}' not found in any connected server."

        session = self.sessions.get(server_name)
        if not session:
            return f"Error: MCP server '{server_name}' is not connected."

        if not self._loop or not self._loop.is_running():
            return "Error: MCP event loop is not running."

        future = asyncio.run_coroutine_threadsafe(
            session.call_tool(name, arguments=arguments),
            self._loop
        )

        try:
            result = future.result(timeout=30)
            output = ""
            for content in result.content:
                if content.type == "text":
                    output += content.text + "\n"
            return output.strip() if output else "Success (No output)"
        except Exception as e:
            return f"MCP tool execution failed: {e}"

    def get_server_status(self):
        """Return a dict of server_name → connected (bool) for health checks."""
        status = {}
        for name in self.server_configs:
            status[name] = name in self.sessions
        return status

    def stop(self):
        """Cleanly shut down all server connections and the event loop."""
        if self._loop and self._loop.is_running():
            # Close all stacks
            for name, stack in list(self._stacks.items()):
                try:
                    future = asyncio.run_coroutine_threadsafe(
                        stack.aclose(), self._loop
                    )
                    future.result(timeout=5)
                except Exception as e:
                    logger.warning(f"Error closing MCP server '{name}': {e}")

            self._loop.call_soon_threadsafe(self._loop.stop)

        self.sessions.clear()
        self._stacks.clear()
        self.tools.clear()
