import os
from dotenv import load_dotenv
from web3 import Web3
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("defi-mcp")

RPC_URLS = {
    "polygon": os.getenv("POLYGON_RPC_URL"),
}

TOKEN_ADDRESSES = {
    "polygon": {
        "USDC": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
        "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
        "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "WMATIC": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        "WBTC": "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6",
        "DAI": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
        "AAVE": "0xD6DF932A45C0f255f85145f286eA0b292B21C90B",
    }
}

ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [{"name": "", "type": "string"}],
        "type": "function",
    },
]


def get_web3(chain):
    rpc_url = RPC_URLS.get(chain.lower())
    if not rpc_url:
        raise ValueError(f"Chain '{chain}' not supported or RPC URL not configured")
    return Web3(Web3.HTTPProvider(rpc_url))


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

    Supports common tokens on Polygon: USDC, USDT, WETH, WMATIC, WBTC, DAI, AAVE.

    Args:
        address: The wallet address to check
        token_symbol: The token symbol (e.g. USDC, USDT, WETH)
        chain: The blockchain to query. Default: polygon.

    Returns:
        A dictionary with the address, token symbol, balance, and raw balance.
    """
    chain = chain.lower()
    token_symbol = token_symbol.upper()

    if chain not in TOKEN_ADDRESSES:
        return {"error": f"Chain '{chain}' not supported. Supported: {list(TOKEN_ADDRESSES.keys())}"}

    if token_symbol not in TOKEN_ADDRESSES[chain]:
        supported = list(TOKEN_ADDRESSES[chain].keys())
        return {"error": f"Token '{token_symbol}' not supported on {chain}. Supported: {supported}"}

    try:
        w3 = get_web3(chain)

        if not Web3.is_address(address):
            return {"error": f"Invalid address: {address}"}
        address = Web3.to_checksum_address(address)

        token_address = Web3.to_checksum_address(TOKEN_ADDRESSES[chain][token_symbol])

        contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)

        raw_balance = contract.functions.balanceOf(address).call()
        decimals = contract.functions.decimals().call()

        balance = raw_balance / (10 ** decimals)

        return {
            "address": address,
            "token": token_symbol,
            "chain": chain,
            "balance": balance,
            "raw_balance": str(raw_balance),
            "decimals": decimals,
        }

    except Exception as e:
        return {"error": f"Failed to fetch balance: {str(e)}"}


if __name__ == "__main__":
    mcp.run(transport="stdio")
