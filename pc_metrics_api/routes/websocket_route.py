from quart import Blueprint, websocket
from system_stats import get_stats_async
import json

websocket_blueprint = Blueprint('websocket', __name__)

@websocket_blueprint.websocket('/ws')
async def ws():
    interval = None

    # eg: {"interval": 1}
    data = await websocket.receive()

    try:
        data = json.loads(data)
        if 'interval' in data:
            interval = float(data['interval'])

    except:
        message = {"message":"incorrect parameter or missing parameter"}
        message = json.dumps(message)
        await websocket.send(message)
        return

    if interval < 0.1 or interval > 360:
        message = {"message": "interval must be  greater or equal to 0.1 and less or equal to 360"}
        message = json.dumps(message)
        await websocket.send(message)

    while True:
        stats = await get_stats_async(interval)
        stats_json = json.dumps(stats)
        await websocket.send(stats_json)