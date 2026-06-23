"""Token addresses and protocol configurations per chain."""

TOKEN_ADDRESSES = {
    "polygon": {
        "USDC": "0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359",
        "USDC.e": "0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174",
        "USDT": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
        "WETH": "0x7ceB23fD6bC0adD59E62ac25578270cFf1b9f619",
        "WMATIC": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",
        "WBTC": "0x1BFD67037B42Cf73acF2047067bd4F2C47D9BfD6",
        "DAI": "0x8f3Cf7ad23Cd3CaDbD9735AFf958023239c6A063",
        "AAVE": "0xD6DF932A45C0f255f85145f286eA0b292B21C90B",
    },
    "arbitrum": {
        # Native USDC deployed by Circle (preferred over bridged USDC.e)
        "USDC": "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
        # Bridged USDC from Ethereum (legacy, kept for compatibility)
        "USDC.e": "0xFF970A61A04b1cA14834A43f5dE4533eBDDB5CC8",
        "USDT": "0xFd086bC7CD5C481DCC9C85ebE478A1C0b69FCbb9",
        "WETH": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
        "WBTC": "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",
        "ARB": "0x912CE59144191C1204E64559FE8253a0e49E6548",
    },
}

# Aave v3 Pool proxy — same address on Polygon and Arbitrum (deterministic CREATE2 deployment).
AAVE_POOL_ADDRESSES = {
    "polygon": "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
    "arbitrum": "0x794a61358D6845594F94dc1DB02A252b5b4814aD",
}

# Uniswap v3 QuoterV2 — same address across all chains (deterministic CREATE2 deployment).
UNISWAP_V3_QUOTER_V2_ADDRESSES = {
    "polygon": "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
    "arbitrum": "0x61fFE014bA17989E743c5F6cB21bF9697530B21e",
}

# Chainlink price feed addresses (token/USD), per chain.
CHAINLINK_PRICE_FEEDS = {
    "polygon": {
        "ETH": "0xF9680D99D6C9589e2a93a78A04A279e509205945",
        "WETH": "0xF9680D99D6C9589e2a93a78A04A279e509205945",
        "MATIC": "0xAB594600376Ec9fD91F8e885dADF0CE036862dE0",
        "WMATIC": "0xAB594600376Ec9fD91F8e885dADF0CE036862dE0",
        "WBTC": "0xDE31F8bFBD8c84b5360CFACCa3539B938dd78ae6",
        "USDC": "0xfe4A8cc5b5B2366C1B58Bea3858e81843581b2F7",
        "USDT": "0x0A6513e40db6EB1b165753AD52E80663aeA50545",
    },
    "arbitrum": {
        "ETH": "0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612",
        "WETH": "0x639Fe6ab55C921f74e7fac1ee960C0B6293ba612",
        "WBTC": "0xd0C7101eACbB49F3deCcCc166d238410D6D46d57",
        "ARB": "0xb2A824043730FE05F3DA2efaFa1CBbe83fa548D6",
        "USDC": "0x50834F3163758fcC1Df9973b6e91f0F0F0434aD3",
        "USDT": "0x3f3f5dF88dC9F13eac63DF89EC16ef6e7E25DdE7",
    },
}