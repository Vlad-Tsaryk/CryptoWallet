from src.wallet.http.client import send_post_request


async def send_transaction(payload: dict):
    request_url = (
        "https://wider-polished-forest.ethereum-sepolia.discover.quiknode.pro"
        "/6b5e96ed04428d9519f5e535fd0336e3fabb314f/"
    )
    result = await send_post_request(request_url, payload)
    return result
