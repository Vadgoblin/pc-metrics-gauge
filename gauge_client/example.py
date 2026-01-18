#
# uaiohttpclient - fetch URL passed as command line argument.
#
import uasyncio as asyncio
import uaiohttpclient as aiohttp
import json

async def run(url):
    resp = await aiohttp.request("GET", url)
    #print(resp)
    try:
        r = (await resp.read()).decode()
        d = json.loads(r)
        print(r)
    finally:
        await resp.aclose()

import sys

url = "http://192.168.0.10:4972/stats"
loop = asyncio.get_event_loop()
loop.run_until_complete(run(url))
loop.close()