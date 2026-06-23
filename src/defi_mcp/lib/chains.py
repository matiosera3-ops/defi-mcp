"""Web3 connection management per chain."""
import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

_RPC_ENV_VARS = {
    "polygon": "POLYGON_RPC_URL",
    "arbitrum": "ARBITRUM_RPC_URL",
}


def get_web3(chain: str) -> Web3:
    """Return a Web3 instance connected to the given chain."""
    chain = chain.lower()
    env_var = _RPC_ENV_VARS.get(chain)
    if env_var is None:
        raise ValueError(f"Chain '{chain}' not supported. Supported: {list(_RPC_ENV_VARS.keys())}")
    rpc_url = os.getenv(env_var)
    if not rpc_url:
        raise ValueError(f"RPC URL not configured: set the {env_var} environment variable")
    return Web3(Web3.HTTPProvider(rpc_url))


SUPPORTED_CHAINS = list(_RPC_ENV_VARS.keys())
