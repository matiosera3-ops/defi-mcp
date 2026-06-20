"""Token balance tool."""
from web3 import Web3
from defi_mcp.lib.chains import get_web3
from defi_mcp.lib.abis import ERC20_ABI
from defi_mcp.config import TOKEN_ADDRESSES


def get_token_balance(address: str, token_symbol: str, chain: str = "polygon") -> dict:
    """Get the balance of an ERC-20 token for a given wallet address.

    Args:
        address: The wallet address to check
        token_symbol: The token symbol (e.g. USDC, USDT, WETH, USDC.e)
        chain: The blockchain to query. Default: polygon.

    Returns:
        A dictionary with the address, token symbol, balance, and raw balance.
    """
    chain = chain.lower()

    if chain not in TOKEN_ADDRESSES:
        return {"error": f"Chain '{chain}' not supported. Supported: {list(TOKEN_ADDRESSES.keys())}"}

    # Case-insensitive token symbol matching
    token_map = {k.upper(): k for k in TOKEN_ADDRESSES[chain].keys()}
    token_key = token_map.get(token_symbol.upper())

    if not token_key:
        supported = list(TOKEN_ADDRESSES[chain].keys())
        return {"error": f"Token '{token_symbol}' not supported on {chain}. Supported: {supported}"}

    try:
        w3 = get_web3(chain)

        if not Web3.is_address(address):
            return {"error": f"Invalid address: {address}"}
        address = Web3.to_checksum_address(address)

        token_address = Web3.to_checksum_address(TOKEN_ADDRESSES[chain][token_key])
        contract = w3.eth.contract(address=token_address, abi=ERC20_ABI)

        raw_balance = contract.functions.balanceOf(address).call()
        decimals = contract.functions.decimals().call()
        balance = raw_balance / (10 ** decimals)

        return {
            "address": address,
            "token": token_key,
            "chain": chain,
            "balance": balance,
            "raw_balance": str(raw_balance),
            "decimals": decimals,
        }

    except Exception as e:
        return {"error": f"Failed to fetch balance: {str(e)}"}