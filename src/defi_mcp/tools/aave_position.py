"""Aave v3 user position tool."""
from web3 import Web3
from defi_mcp.lib.chains import get_web3
from defi_mcp.lib.abis import AAVE_POOL_ABI
from defi_mcp.config import AAVE_POOL_ADDRESSES

# Aave v3 base currency is USD with 8 decimals on both Polygon and Arbitrum (price feed precision).
BASE_CURRENCY_DECIMALS = 8


def get_aave_position(address: str, chain: str = "polygon") -> dict:
    """Get a user's Aave v3 lending/borrowing position on a given chain.

    Args:
        address: The wallet address to check
        chain: The blockchain to query. Default: polygon.

    Returns:
        A dictionary with total collateral, total debt, available borrows,
        liquidation threshold, LTV, and health factor (all in USD where applicable).
    """
    chain = chain.lower()

    if chain not in AAVE_POOL_ADDRESSES:
        return {"error": f"Chain '{chain}' not supported. Supported: {list(AAVE_POOL_ADDRESSES.keys())}"}

    try:
        w3 = get_web3(chain)

        if not Web3.is_address(address):
            return {"error": f"Invalid address: {address}"}
        address = Web3.to_checksum_address(address)

        pool_address = Web3.to_checksum_address(AAVE_POOL_ADDRESSES[chain])
        contract = w3.eth.contract(address=pool_address, abi=AAVE_POOL_ABI)

        result = contract.functions.getUserAccountData(address).call()
        (
            total_collateral_base,
            total_debt_base,
            available_borrows_base,
            current_liquidation_threshold,
            ltv,
            health_factor_raw,
        ) = result

        # Base amounts use the price feed's decimals (8 on both Polygon and Arbitrum).
        total_collateral_usd = total_collateral_base / (10 ** BASE_CURRENCY_DECIMALS)
        total_debt_usd = total_debt_base / (10 ** BASE_CURRENCY_DECIMALS)
        available_borrows_usd = available_borrows_base / (10 ** BASE_CURRENCY_DECIMALS)

        # Health factor and LTV/liquidation threshold are 18-decimal fixed point.
        # If there's no debt, Aave returns max uint256 for health factor -> treat as infinite.
        max_uint256 = 2**256 - 1
        if health_factor_raw == max_uint256:
            health_factor = None  # represents infinite / no debt
        else:
            health_factor = health_factor_raw / (10 ** 18)

        return {
            "address": address,
            "chain": chain,
            "total_collateral_usd": total_collateral_usd,
            "total_debt_usd": total_debt_usd,
            "available_borrows_usd": available_borrows_usd,
            "liquidation_threshold_pct": current_liquidation_threshold / 100,
            "ltv_pct": ltv / 100,
            "health_factor": health_factor,
            "has_active_position": total_collateral_usd > 0 or total_debt_usd > 0,
        }

    except Exception as e:
        return {"error": f"Failed to fetch Aave position: {str(e)}"}