from quart import Quart
from routes import http_get_blueprint, websocket_blueprint

app = Quart(__name__)
app.register_blueprint(http_get_blueprint)
app.register_blueprint(websocket_blueprint)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4972, debug=True)
