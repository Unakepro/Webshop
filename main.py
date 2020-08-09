from webshop.bot.main import bot,start_bot
from webshop.bot import config
from flask import Flask, request, abort
from flask_restful import Api
from telebot.types import Update


app = Flask(__name__)

bot.remove_webhook()
start_bot()




