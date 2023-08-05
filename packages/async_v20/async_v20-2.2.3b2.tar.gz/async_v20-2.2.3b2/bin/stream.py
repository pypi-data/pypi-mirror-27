import asyncio

from async_v20 import OandaClient


async def stream(instruments):
    async with OandaClient() as client:
        async for data in await client.stream_pricing(instruments):
            price = data.get('PRICE', None)
            if price:
                print(price.series())


loop = asyncio.get_event_loop()
loop.run_until_complete(stream('AUD_USD,EUR_USD'))
