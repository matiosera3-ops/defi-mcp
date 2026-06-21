"""Quick test for get_aave_position — also finds a real address with an active position."""
from defi_mcp.tools.aave_position import get_aave_position
from defi_mcp.lib.chains import get_web3
from web3 import Web3

w3 = get_web3("polygon")

# Step 1: sanity check against the Aave Pool contract itself (should return all zeros, health_factor=None)
pool_address = "0x794a61358D6845594F94dc1DB02A252b5b4814aD"
print("=== Sanity check (Pool contract itself) ===")
print(get_aave_position(pool_address))

# Step 2: find a real address with an active position by paginating Borrow events
# 10 blocks at a time (Alchemy free tier limit on eth_getLogs).
print("\n=== Scanning recent blocks for a real borrower (10-block pages) ===")

BORROW_EVENT_ABI = {
    "anonymous": False,
    "inputs": [
        {"indexed": True, "name": "reserve", "type": "address"},
        {"indexed": False, "name": "user", "type": "address"},
        {"indexed": True, "name": "onBehalfOf", "type": "address"},
        {"indexed": False, "name": "amount", "type": "uint256"},
        {"indexed": False, "name": "interestRateMode", "type": "uint8"},
        {"indexed": False, "name": "borrowRate", "type": "uint256"},
        {"indexed": True, "name": "referralCode", "type": "uint16"},
    ],
    "name": "Borrow",
    "type": "event",
}

contract = w3.eth.contract(
    address=Web3.to_checksum_address(pool_address),
    abi=[BORROW_EVENT_ABI],
)

latest_block = w3.eth.block_number
PAGE_SIZE = 10
MAX_PAGES = 300  # 300 * 10 blocks = 3000 blocks of history (~1-2h on Polygon)

found_addresses = []
to_block = latest_block

for page in range(MAX_PAGES):
    from_block = to_block - PAGE_SIZE + 1
    try:
        logs = contract.events.Borrow().get_logs(from_block=from_block, to_block=to_block)
        if logs:
            for log in logs:
                addr = log["args"]["onBehalfOf"]
                if addr not in found_addresses:
                    found_addresses.append(addr)
                    print(f"Found borrower at block {log['blockNumber']}: {addr}")
    except Exception as e:
        print(f"Page {page} (blocks {from_block}-{to_block}) failed: {e}")

    to_block = from_block - 1

    if len(found_addresses) >= 5:
        print(f"\nFound {len(found_addresses)} addresses, stopping early.")
        break

if not found_addresses:
    print("No Borrow events found in scanned range. Try increasing MAX_PAGES.")
else:
    print(f"\n=== Testing get_aave_position on found addresses ===\n")
    for addr in found_addresses[:5]:
        position = get_aave_position(addr)
        print(f"Address: {addr}")
        print(position)
        print()