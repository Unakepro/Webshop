from webshop.bot.main import bot, start_bot
from webshop.bot import config
from flask import Flask, request, abort

from telebot.types import Update

if __name__ == "__main__":
    start_bot()
