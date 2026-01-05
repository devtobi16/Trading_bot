import asyncio
import sys
from mcp.server.fastmcp import FastMCP
from accounts import Account

mcp = FastMCP("accounts_server")

@mcp.tool()
async def get_balance(name: str) -> float:
    return Account.get(name).balance

@mcp.tool()
async def get_holdings(name: str) -> dict[str, int]:
    return Account.get(name).holdings

@mcp.tool()
async def buy_shares(name: str, symbol: str, quantity: int, rationale: str) -> float:
    return Account.get(name).buy_shares(symbol, quantity, rationale)

@mcp.tool()
async def sell_shares(name: str, symbol: str, quantity: int, rationale: str) -> float:
    return Account.get(name).sell_shares(symbol, quantity, rationale)

@mcp.tool()
async def change_strategy(name: str, strategy: str) -> str:
    return Account.get(name).change_strategy(strategy)

@mcp.resource("accounts://accounts_server/{name}")
async def read_account_resource(name: str) -> str:
    return Account.get(name.lower()).report()

@mcp.resource("accounts://strategy/{name}")
async def read_strategy_resource(name: str) -> str:
    return Account.get(name.lower()).get_strategy()

async def main():
    # IMPORTANT: logs go to stderr only
    print("Starting Accounts MCP Server", file=sys.stderr)
    await mcp.run_async(transport="stdio")

if __name__ == "__main__":
    asyncio.run(main())
