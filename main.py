from quart import Quart, websocket, request
from system_stats import get_stats, get_stats_async
from time import sleep
import json


app = Quart(__name__)

@app.websocket('/ws')
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

@app.get('/stats')
async def stats():
    interval = request.args.get('interval')
    if not interval:
        interval = 1

    try:
        interval = float(interval)
        if interval <= 0:
            raise ValueError
    except ValueError:
        return {"message":"interval must be a number that is greater then 0"}, 400

    return await get_stats_async(interval)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4972, debug=True)
