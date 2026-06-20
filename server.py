"""defi-mcp: An MCP server for DeFi data access.

Exposes tools for AI agents to interact with DeFi protocols on EVM chains.
Currently supports: Polygon.
"""
from mcp.server.fastmcp import FastMCP
from defi_mcp.tools.balance import get_token_balance as _get_token_balance

mcp = FastMCP("defi-mcp")


@mcp.tool()
def hello(name: str) -> str:
    """Say hello to someone. Use this to test the MCP server is working.

    Args:
        name: The name of the person to greet
    """
    return f"Hello {name}! Your defi-mcp server is alive."


@mcp.tool()
def get_token_balance(address: str, token_symbol: str, chain: str = "polygon") -> dict:
    """Get the balance of an ERC-20 token for a given wallet address.

    Supports common tokens on Polygon: USDC, USDC.e, USDT, WETH, WMATIC, WBTC, DAI, AAVE.

    Args:
        address: The wallet address to check
        token_symbol: The token symbol (e.g. USDC, USDT, WETH)
        chain: The blockchain to query. Default: polygon.

    Returns:
        A dictionary with the address, token symbol, balance, and raw balance.
    """
    return _get_token_balance(address, token_symbol, chain)


if __name__ == "__main__":
    mcp.run(transport="stdio")
