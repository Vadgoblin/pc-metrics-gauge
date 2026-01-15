from quart import Blueprint, request
from system_stats import get_stats_async

stats_blueprint = Blueprint('stats', __name__)

@stats_blueprint.get('/stats')
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