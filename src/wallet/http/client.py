import aiohttp


# from pydantic import Json


async def send_get_request(url: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            res = await response.json()
            return res


async def send_post_request(url: str, payload: dict):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, payload=payload) as response:
            res = await response.json()
            return res
