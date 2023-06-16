from typing import List

from config.config import settings
from src.wallet.http.client import send_get_request


async def get_address_balance(address: str):
    request_url = (
        "https://api-sepolia.etherscan.io/api"
        "?module=account"
        "&action=balance"
        f"&address={address}"
        "&tag=latest"
        f"&apikey={settings.ETHERSCAN_API_KEY}"
    )
    result = await send_get_request(request_url)
    return result


async def get_multiple_addresses_balance(addresses: str) -> List[dict]:
    request_url = (
        "https://api-sepolia.etherscan.io/api"
        "?module=account"
        "&action=balancemulti"
        f"&address={addresses}"
        "&tag=latest"
        f"&apikey={settings.ETHERSCAN_API_KEY}"
    )
    result = await send_get_request(request_url)
    return result.get("result")
