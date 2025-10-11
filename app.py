from flask import Flask, request, abort

from linebot.v3.exceptions import InvalidSignatureError

from food import app_config
from food.line_handler import linebot_handler


app = Flask(app_config.APP_NAME)


@app.route("/statusss", methods=['POST']) # 混淆
def status():
    # collected_status_str = ""
    # with get_stock_handler("test user", None) as stock_handler:
    #     with stock_handler.mongo_db.client.list_databases() as cursor:
    #         collected_status_str += "Mongo DB databases:\n" + "\n".join(map(str, cursor))
    # return collected_status_str
    return "OK"


@app.route("/webhook", methods=['POST'])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    try:
        linebot_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return "OK"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=app_config.PORT, debug=app_config.DEBUG, use_reloader=app_config.FLASK_USE_RELOADER)
