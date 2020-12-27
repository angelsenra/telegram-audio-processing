import logging
import os
from queue import Queue
from threading import Thread

from flask import Flask, redirect
from telegram import Bot
from telegram.ext import CommandHandler, Dispatcher, Filters, MessageHandler

INDEX_REDIRECT_URL = os.environ["INDEX_REDIRECT_URL"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

#
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#custom-solution
#

update_queue = Queue()

dispatcher = Dispatcher(bot, update_queue)

from handlers.command import start, unknown
from handlers.text import echo

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))

# Start the thread
thread = Thread(target=dispatcher.start, name="dispatcher")
thread.start()

# END

from backend.routes.telegram import set_telegram_webhook


@app.route("/")
def index():
    return redirect(INDEX_REDIRECT_URL)
