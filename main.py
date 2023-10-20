from webshop.bot.main import bot
from webshop.bot import config
from flask import Flask, request, abort
from telebot.types import Update
from webshop.api.products import blue_products, blue_products_post
from webshop.api.category import blue_category, blue_category_post
import time

app = Flask(__name__)


@app.route(config.WEBHOOK_PATH, methods=['POST'])
def webhook():
    if request.headers.get('content-type') == "application/json":
        json_string = request.get_data().decode('utf-8')
        update = Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        abort(403)

app.register_blueprint(blue_products)
app.register_blueprint(blue_category)
app.register_blueprint(blue_products_post)
app.register_blueprint(blue_category_post)

if __name__ == '__main__':

    bot.remove_webhook()
    time.sleep(1)

    bot.set_webhook(
        config.WEBHOOK_URL,
        certificate=open('webhook_cert.pem', 'r')
    )
    app.run(debug=True)
