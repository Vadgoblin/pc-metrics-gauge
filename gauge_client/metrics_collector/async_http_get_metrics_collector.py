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


class AsyncHttpGetMetricsCollector:
    def __init__(self, endpoint, interval):
        self.url = endpoint
        if interval:
            self.url += f"?interval={interval}"
            
        self.interval = interval
        
    async def get(self):
        response = await aiohttp.request("GET", self.url)
    
        try:
            response_data = await response.read()
            decoded_response = (response_data).decode()
            metrics = json.loads(decoded_response)
            return metrics
        finally:
            await response.aclose()
    
    def __aiter__(self):
        return self
    
    def __anext__(self):
        return self.get()