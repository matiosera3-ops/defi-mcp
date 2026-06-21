"""Direct test of eth_getLogs to see Alchemy's actual error message."""
import os
import requests
from dotenv import load_dotenv

load_dotenv()
rpc_url = os.getenv("POLYGON_RPC_URL")

pool_address = "0x794a61358D6845594F94dc1DB02A252b5b4814aD"
latest_block = 88884547
from_block = latest_block - 500

payload = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "eth_getLogs",
    "params": [{
        "address": pool_address,
        "fromBlock": hex(from_block),
        "toBlock": hex(latest_block),
    }]
}

response = requests.post(rpc_url, json=payload)
print("Status code:", response.status_code)
print("Response body:", response.text)