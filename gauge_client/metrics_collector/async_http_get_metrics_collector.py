import uaiohttpclient as aiohttp
import json


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