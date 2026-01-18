import uaiohttpclient as aiohttp
import json

async def get_metrics(endpoint, interval):
    url = endpoint
    if interval:
        url += f"?interval={interval}"

    response = await aiohttp.request("GET", url)
    
    try:
        response_data = await response.read()
        decoded_response = (response_data).decode()
        metrics = json.loads(decoded_response)
        return metrics
    finally:
        await response.aclose()


async def iter_metrics(endpoint, interval):
    while True:
        yield await get_metrics(endpoint, interval)


