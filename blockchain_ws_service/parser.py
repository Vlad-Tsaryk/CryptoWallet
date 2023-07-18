import asyncio
import json

import websockets
from loguru import logger
from propan import RabbitBroker, PropanApp

from config.config import settings

broker: RabbitBroker = RabbitBroker("amqp://guest:guest@localhost:5672")
app = PropanApp(broker)


@app.after_startup
async def parser():
    ws_url = settings.INFRA_WSS_URL
    async with websockets.connect(ws_url) as websocket:
        await websocket.send(
            '{"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]}',
        )
        subscription_response = await websocket.recv()
        logger.success(f"Parser start successfully {subscription_response}")
        while True:
            try:
                message = await asyncio.wait_for(websocket.recv(), timeout=2)
                response = json.loads(message)
                block_hash = response["params"]["result"]["hash"]
                logger.info(f"Block hash: {block_hash}")
                a = await broker.publish(
                    queue="block_parser", exchange="exchange", message=block_hash
                )
                logger.info(a)
            except:
                pass


if __name__ == "__main__":
    asyncio.run(app.run())
