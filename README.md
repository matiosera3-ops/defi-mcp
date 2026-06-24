# defi-mcp

An MCP (Model Context Protocol) server that gives AI agents direct, on-chain access to DeFi data on EVM chains — wallet balances, Aave v3 lending positions, and live token prices, with no centralized API in the middle.

**Status:** Live and functional. 5 tools available today, more on the roadmap.

## Why

Most "DeFi + AI" integrations route through a centralized API that can rate-limit, paywall, or simply disappear. `defi-mcp` talks directly to the chain (via your own RPC provider) and to first-party oracles (Chainlink), so the data your AI agent gets is exactly what's on-chain — verifiable, and not dependent on a third-party API staying online.

## Tools

### `get_token_balance`
Reads the ERC-20 balance of any wallet address for a supported token.

Supported tokens:
- **Polygon:** `USDC`, `USDC.e`, `USDT`, `WETH`, `WMATIC`, `WBTC`, `DAI`, `AAVE`
- **Arbitrum:** `USDC`, `USDC.e` (bridged), `USDT`, `WETH`, `WBTC`, `ARB`

```json
// get_token_balance(address="0x...", token_symbol="USDC", chain="polygon")
{
  "address": "0x...",
  "token": "USDC",
  "chain": "polygon",
  "balance": 268.21,
  "raw_balance": "268210000",
  "decimals": 6
}
```

### `get_aave_position`
Reads a user's full Aave v3 lending/borrowing position: collateral, debt, available borrowing power, and health factor — straight from the Aave v3 Pool contract.

```json
// get_aave_position(address="0x...", chain="polygon")
{
  "address": "0x...",
  "chain": "polygon",
  "total_collateral_usd": 969.78,
  "total_debt_usd": 288.16,
  "available_borrows_usd": 484.86,
  "liquidation_threshold_pct": 82.79,
  "ltv_pct": 79.71,
  "health_factor": 2.79,
  "has_active_position": true
}
```

A `health_factor` below `1.0` means the position is at risk of liquidation. A `null` health factor means the user has no outstanding debt.

### `get_token_price`
Reads the current USD price of a token directly from a Chainlink price feed — the same oracle DeFi protocols use internally, so the price is consistent with what `get_aave_position` reports.

Supported feeds:
- **Polygon:** `ETH`/`WETH`, `MATIC`/`WMATIC`, `WBTC`, `USDC`, `USDT`
- **Arbitrum:** `ETH`/`WETH`, `WBTC`, `ARB`, `USDC`, `USDT`

```json
// get_token_price(token_symbol="WBTC", chain="polygon")
{
  "token": "WBTC",
  "chain": "polygon",
  "price_usd": 63835.77,
  "decimals": 8,
  "updated_at": 1782032816
}
```

### `simulate_swap`
Simulates a Uniswap v3 swap on-chain via the QuoterV2 contract — no transaction submitted, no wallet needed. Tries all four fee tiers (0.01%, 0.05%, 0.3%, 1%) and returns the best available output amount.

Supported tokens:
- **Polygon:** `USDC`, `USDC.e`, `USDT`, `WETH`, `WMATIC`, `WBTC`, `DAI`, `AAVE`
- **Arbitrum:** `USDC`, `USDC.e` (bridged), `USDT`, `WETH`, `WBTC`, `ARB`

```json
// simulate_swap(token_in="WMATIC", token_out="USDC", amount_in=100.0, chain="polygon")
{
  "chain": "polygon",
  "token_in": "WMATIC",
  "token_out": "USDC",
  "amount_in": 100.0,
  "amount_out": 7.990547,
  "fee_tier_used_pct": 0.05,
  "fee_tier_used_bps": 500,
  "gas_estimate": 122770
}
```

If no pool exists for the pair at any fee tier, returns `{"error": "No liquidity found for this pair on any fee tier"}`.

### `hello`
Simple connectivity check — confirms the MCP server is reachable and responding.

## Supported chains

| Chain | `get_token_balance` | `get_aave_position` | `get_token_price` | `simulate_swap` |
|---|---|---|---|---|
| Polygon | ✅ | ✅ | ✅ | ✅ |
| Arbitrum | ✅ | ✅ | ✅ | ✅ |

## Installation

Requires Python 3.10+ and an RPC provider API key (e.g. [Alchemy](https://www.alchemy.com/), free tier works).

```bash
pip install defi-mcp
```

Create a `.env` file in your working directory (see `.env.example`):

```
POLYGON_RPC_URL=https://polygon-mainnet.g.alchemy.com/v2/YOUR_API_KEY
ARBITRUM_RPC_URL=https://arb-mainnet.g.alchemy.com/v2/YOUR_API_KEY
```

Each chain only needs its RPC URL configured. Tools called with `chain="arbitrum"` will fail gracefully if `ARBITRUM_RPC_URL` is not set.

## Usage with Claude Desktop

Add this to your Claude Desktop MCP config (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "defi-mcp": {
      "command": "uvx",
      "args": ["defi-mcp"],
      "env": {
        "POLYGON_RPC_URL": "https://polygon-mainnet.g.alchemy.com/v2/YOUR_API_KEY",
        "ARBITRUM_RPC_URL": "https://arb-mainnet.g.alchemy.com/v2/YOUR_API_KEY"
      }
    }
  }
}
```

Restart Claude Desktop, and the tools above will be available to the model.

## Testing locally

You can test the server directly with the official [MCP Inspector](https://github.com/modelcontextprotocol/inspector):

```bash
npx @modelcontextprotocol/inspector uvx defi-mcp
```

## Roadmap

- [ ] Track Uniswap v3 LP positions and impermanent loss
- [ ] Monitor protocol TVLs
- [ ] Additional chains (Ethereum, Base)
- [ ] `defi-mcp-cloud` — hosted tier with MEV-specific tools, caching, and higher rate limits

## Architecture

Open-core model: this repository (MIT licensed) covers standard on-chain read tools. A separate `defi-mcp-cloud` will offer a hosted version with MEV-related tools, request caching, and managed RPC access for users who don't want to run their own infrastructure.

## Resources

- [defi-storage-cheatsheet](https://github.com/matiosera3-ops/defi-storage-cheatsheet) — verified EVM storage slot layouts for Aave v3 and Uniswap v3, with `web3.py` snippets. Useful if you want to read on-chain state directly via `eth_getStorageAt` instead of calling `view` functions — the lower-level approach behind some of what this server does under the hood.

## Contributing

Issues and PRs welcome. This is an early-stage project — feedback on what tools would actually be useful to you is especially valuable.

## License

MIT

<!-- mcp-name: io.github.matiosera3-ops/defi-mcp -->
