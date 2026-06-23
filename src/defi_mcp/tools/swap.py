"""Uniswap v3 swap simulation tool."""
from web3 import Web3
from defi_mcp.lib.chains import get_web3
from defi_mcp.lib.abis import ERC20_ABI, UNISWAP_V3_QUOTER_V2_ABI
from defi_mcp.config import TOKEN_ADDRESSES, UNISWAP_V3_QUOTER_V2_ADDRESSES

# Uniswap v3 fee tiers in ppm (100=0.01%, 500=0.05%, 3000=0.3%, 10000=1%)
FEE_TIERS = [100, 500, 3000, 10000]


def simulate_swap(token_in: str, token_out: str, amount_in: float, chain: str = "polygon") -> dict:
    """Simulate a Uniswap v3 swap on-chain via QuoterV2, without submitting a transaction.

    Tries all four fee tiers (0.01%, 0.05%, 0.3%, 1%) and returns the best quote.
    Fee tiers with no pool or no liquidity are silently skipped.

    Args:
        token_in: The input token symbol (e.g. WMATIC on Polygon, ARB on Arbitrum, WETH on both)
        token_out: The output token symbol (e.g. USDC, WETH, USDT)
        amount_in: Amount of token_in to swap (human-readable, e.g. 100.0 for 100 USDC)
        chain: The blockchain to query. Default: polygon.

    Returns:
        A dictionary with amount_out, fee_tier_used_pct, and swap metadata.
    """
    chain = chain.lower()

    if chain not in TOKEN_ADDRESSES:
        return {"error": f"Chain '{chain}' not supported. Supported: {list(TOKEN_ADDRESSES.keys())}"}

    if chain not in UNISWAP_V3_QUOTER_V2_ADDRESSES:
        return {"error": f"Uniswap v3 QuoterV2 not configured for chain '{chain}'"}

    token_map = {k.upper(): k for k in TOKEN_ADDRESSES[chain].keys()}

    token_in_key = token_map.get(token_in.upper())
    if not token_in_key:
        supported = list(TOKEN_ADDRESSES[chain].keys())
        return {"error": f"Token '{token_in}' not supported on {chain}. Supported: {supported}"}

    token_out_key = token_map.get(token_out.upper())
    if not token_out_key:
        supported = list(TOKEN_ADDRESSES[chain].keys())
        return {"error": f"Token '{token_out}' not supported on {chain}. Supported: {supported}"}

    try:
        w3 = get_web3(chain)

        token_in_address = Web3.to_checksum_address(TOKEN_ADDRESSES[chain][token_in_key])
        token_out_address = Web3.to_checksum_address(TOKEN_ADDRESSES[chain][token_out_key])

        token_in_contract = w3.eth.contract(address=token_in_address, abi=ERC20_ABI)
        token_out_contract = w3.eth.contract(address=token_out_address, abi=ERC20_ABI)

        decimals_in = token_in_contract.functions.decimals().call()
        decimals_out = token_out_contract.functions.decimals().call()

        amount_in_raw = int(amount_in * (10 ** decimals_in))

        quoter_address = Web3.to_checksum_address(UNISWAP_V3_QUOTER_V2_ADDRESSES[chain])
        quoter = w3.eth.contract(address=quoter_address, abi=UNISWAP_V3_QUOTER_V2_ABI)

        best_amount_out_raw = 0
        best_fee_tier = None
        best_gas_estimate = None

        for fee in FEE_TIERS:
            try:
                result = quoter.functions.quoteExactInputSingle({
                    "tokenIn": token_in_address,
                    "tokenOut": token_out_address,
                    "amountIn": amount_in_raw,
                    "fee": fee,
                    "sqrtPriceLimitX96": 0,
                }).call()

                amount_out_raw, _, _, gas_estimate = result

                if amount_out_raw > best_amount_out_raw:
                    best_amount_out_raw = amount_out_raw
                    best_fee_tier = fee
                    best_gas_estimate = gas_estimate

            except Exception:
                # Pool for this fee tier doesn't exist or has no liquidity
                continue

        if best_fee_tier is None:
            return {"error": "No liquidity found for this pair on any fee tier"}

        amount_out = best_amount_out_raw / (10 ** decimals_out)
        # fee tiers are in ppm (parts per million): divide by 10000 to get percent
        fee_tier_pct = best_fee_tier / 10000

        return {
            "chain": chain,
            "token_in": token_in_key,
            "token_out": token_out_key,
            "amount_in": amount_in,
            "amount_out": amount_out,
            "fee_tier_used_pct": fee_tier_pct,
            "fee_tier_used_bps": best_fee_tier,
            "gas_estimate": best_gas_estimate,
        }

    except Exception as e:
        return {"error": f"Failed to simulate swap: {str(e)}"}
