"""Token price tool using Chainlink price feeds."""
from web3 import Web3
from defi_mcp.lib.chains import get_web3
from defi_mcp.lib.abis import CHAINLINK_AGGREGATOR_ABI
from defi_mcp.config import CHAINLINK_PRICE_FEEDS


def get_token_price(token_symbol: str, chain: str = "polygon") -> dict:
    """Get the current USD price of a token from a Chainlink price feed.

    Available price feeds vary by chain:
    - Polygon: ETH/WETH, MATIC/WMATIC, WBTC, USDC, USDT
    - Arbitrum: ETH/WETH, WBTC, ARB, USDC, USDT

    Args:
        token_symbol: The token symbol (e.g. ETH, WBTC, USDC)
        chain: The blockchain to query. Default: polygon.

    Returns:
        A dictionary with the token symbol, USD price, and feed update timestamp.
    """
    chain = chain.lower()

    if chain not in CHAINLINK_PRICE_FEEDS:
        return {"error": f"Chain '{chain}' not supported. Supported: {list(CHAINLINK_PRICE_FEEDS.keys())}"}

    # Case-insensitive token symbol matching
    feed_map = {k.upper(): k for k in CHAINLINK_PRICE_FEEDS[chain].keys()}
    feed_key = feed_map.get(token_symbol.upper())

    if not feed_key:
        supported = list(CHAINLINK_PRICE_FEEDS[chain].keys())
        return {"error": f"Token '{token_symbol}' has no price feed on {chain}. Supported: {supported}"}

    try:
        w3 = get_web3(chain)
        feed_address = Web3.to_checksum_address(CHAINLINK_PRICE_FEEDS[chain][feed_key])
        contract = w3.eth.contract(address=feed_address, abi=CHAINLINK_AGGREGATOR_ABI)

        round_data = contract.functions.latestRoundData().call()
        _, answer, _, updated_at, _ = round_data

        decimals = contract.functions.decimals().call()
        price_usd = answer / (10 ** decimals)

        return {
            "token": feed_key,
            "chain": chain,
            "price_usd": price_usd,
            "decimals": decimals,
            "updated_at": updated_at,
        }

    except Exception as e:
        return {"error": f"Failed to fetch price: {str(e)}"}