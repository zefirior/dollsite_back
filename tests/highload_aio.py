import asyncio
import aiohttp


async def fetch(session, url):
    async with session.get(url) as respons:
        file = await respons.read()
        # print(len(file))
        return file


async def main():
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[
            fetch(session, 'http://0.0.0.0:5000/file/image.png') for _ in range(100)
        ])

loop = asyncio.get_event_loop()

from time import time as tm
st = tm()
loop.run_until_complete(main())
print(tm() - st)
