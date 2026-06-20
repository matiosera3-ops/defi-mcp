import os
from dotenv import load_dotenv
from web3 import Web3

# Charge le .env
load_dotenv()

# Récupère l'URL Alchemy
rpc_url = os.getenv("POLYGON_RPC_URL")

if not rpc_url:
    print("ERREUR: POLYGON_RPC_URL non trouvée dans .env")
    exit(1)

print(f"URL chargée: {rpc_url[:50]}...")

# Connexion à Polygon
w3 = Web3(Web3.HTTPProvider(rpc_url))

if w3.is_connected():
    print("Connecte a Polygon")
    print(f"Bloc actuel: {w3.eth.block_number}")
    print(f"Chain ID: {w3.eth.chain_id}")
else:
    print("Echec de la connexion")