"""defi-mcp: An MCP server for DeFi data access.

Exposes tools for AI agents to interact with DeFi protocols on EVM chains.
Currently supports: Polygon.
"""
from defi_mcp.tools.price import get_token_price as _get_token_price
from defi_mcp.tools.aave_position import get_aave_position as _get_aave_position
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

@mcp.tool()
def get_aave_position(address: str, chain: str = "polygon") -> dict:
    """Get a user's Aave v3 lending/borrowing position on a given chain.

    Returns total collateral, total debt, available borrowing power,
    liquidation threshold, LTV, and health factor — all in USD where applicable.
    A health factor below 1.0 means the position is at risk of liquidation.
    A null health factor means the user has no outstanding debt.

    Args:
        address: The wallet address to check
        chain: The blockchain to query. Default: polygon.
    """
    return _get_aave_position(address, chain)

@mcp.tool()
def get_token_price(token_symbol: str, chain: str = "polygon") -> dict:
    """Get the current USD price of a token from a Chainlink price feed.

    Supports: ETH, WETH, MATIC, WMATIC, WBTC, USDC, USDT on Polygon.

    Args:
        token_symbol: The token symbol (e.g. ETH, WBTC, USDC)
        chain: The blockchain to query. Default: polygon.
    """
    return _get_token_price(token_symbol, chain)


def main():
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
