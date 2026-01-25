from async_websocket_client import AsyncWebsocketClient
import json
import uasyncio as asyncio

class AsyncWebsocketMetricsCollector:
    def __init__(self, endpoint, interval):
        self.endpoint = endpoint
        self.interval = interval
        self.websocket_client = AsyncWebsocketClient()
        self.is_connection_alive = False
    
    def __aiter__(self):
        return self
    
    def __anext__(self):
        return self._get_metrics()
    
    async def _get_metrics(self):
        if not self.is_connection_alive:
            await self._setup_connection()
            
        try:
            data = await asyncio.wait_for(self._try_receive_data(), self.interval * 3)
        except asyncio.TimeoutError:
            raise Exception("Metrics server response timeout.")
        return data
        
    async def _setup_connection(self):
        await self.websocket_client.open()
        await self.websocket_client.handshake(self.endpoint)
        await self.websocket_client.send('{"interval": '+str(self.interval) +'}')
        self.is_connection_alive = True
        
    async def _try_receive_data(self):
        try:
            json_text = await self.websocket_client.recv()
            return json.loads(json_text)
        except Exception as e:
            self.is_connection_alive = False
            raise e