from webshop.bot.main import bot
from webshop.bot import config
from telebot.types import Update
from webshop.api.products import blue_products, blue_products_post
from webshop.api.category import blue_category, blue_category_post
import time


if __name__ == '__main__':
    bot.infinity_polling()