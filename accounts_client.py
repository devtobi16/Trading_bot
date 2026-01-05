import mcp
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters
from agents import FunctionTool
import json
import sys
import os

# Get the directory where this script is located (6_mcp directory)
script_dir = os.path.dirname(os.path.abspath(__file__))
server_script = os.path.join(script_dir, "accounts_server.py")

# Set PYTHONPATH to include the 6_mcp directory so imports work
# Also preserve existing environment variables
env = os.environ.copy()
path_sep = ";" if sys.platform == "win32" else ":"
if "PYTHONPATH" in env:
    env["PYTHONPATH"] = f"{script_dir}{path_sep}{env['PYTHONPATH']}"
else:
    env["PYTHONPATH"] = script_dir

params = StdioServerParameters(
    command=sys.executable, 
    args=[server_script], 
    env=env
)


async def list_accounts_tools():
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            return tools_result.tools
        
async def call_accounts_tool(tool_name, tool_args):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, tool_args)
            return result
            
async def read_accounts_resource(name):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.read_resource(f"accounts://accounts_server/{name}")
            return result.contents[0].text
        
async def read_strategy_resource(name):
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.read_resource(f"accounts://strategy/{name}")
            return result.contents[0].text

async def get_accounts_tools_openai():
    openai_tools = []
    for tool in await list_accounts_tools():
        schema = {**tool.inputSchema, "additionalProperties": False}
        openai_tool = FunctionTool(
            name=tool.name,
            description=tool.description,
            params_json_schema=schema,
            on_invoke_tool=lambda ctx, args, toolname=tool.name: call_accounts_tool(toolname, json.loads(args))
                
        )
        openai_tools.append(openai_tool)
    return openai_tools