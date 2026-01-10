from flask import Flask, request
from system_stats import get_stats

app = Flask(__name__)

@app.get('/stats')
def stats():
    cpu_interval = request.args.get('cpu_interval')
    if not cpu_interval:
        return get_stats(1)

    try:
        cpu_interval = float(cpu_interval)
        if cpu_interval <= 0:
            raise ValueError
    except ValueError:
        return {"message":"cpu_interval must be a number that is greater then 0"}, 400

    return get_stats(cpu_interval)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4972, debug=True)
