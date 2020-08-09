from webshop.bot.main import bot, start_bot
from webshop.bot import config
from flask import Flask, request, abort
from flask_restful import Api
from telebot.types import Update


app = Flask(__name__)



if __name__ == '__main__':
    start_bot()    


