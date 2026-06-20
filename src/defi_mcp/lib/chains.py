"""Web3 connection management per chain."""
import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

RPC_URLS = {
    "polygon": os.getenv("POLYGON_RPC_URL"),
}


def get_web3(chain: str) -> Web3:
    """Return a Web3 instance connected to the given chain."""
    rpc_url = RPC_URLS.get(chain.lower())
    if not rpc_url:
        raise ValueError(f"Chain '{chain}' not supported or RPC URL not configured")
    return Web3(Web3.HTTPProvider(rpc_url))


SUPPORTED_CHAINS = list(RPC_URLS.keys())
