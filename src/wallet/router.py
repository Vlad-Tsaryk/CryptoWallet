from propan.fastapi import RabbitRouter

router = RabbitRouter(
    "amqps://uqnpfzpe:wua4EvAERgdFe7ieVPOskYXu09AHHiEH@sparrow.rmq.cloudamqp.com/uqnpfzpe"
)


@router.get("/test")
async def hello_http():
    await router.broker.publish("Hello, Rabbit!", "test")
    return "Hello, HTTP!"
