import logging
import os
from queue import Queue
from threading import Thread

from flask import Flask, redirect
from telegram import Bot
from telegram.ext import CommandHandler, Dispatcher, Filters, MessageHandler

DEVELOPMENT_MODE = int(os.environ.get("DEVELOPMENT_MODE") or 0)
INDEX_REDIRECT_URL = os.environ["INDEX_REDIRECT_URL"]
TELEGRAM_PERSONAL_ID = os.environ["TELEGRAM_PERSONAL_ID"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger(__name__)
LOG.info("Starting app...")

app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

#
# https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#custom-solution
#

update_queue = Queue()

dispatcher = Dispatcher(bot, update_queue)

from backend.handlers.audio import echo_audio, echo_voice
from backend.handlers.command import start, unknown
from backend.handlers.text import echo

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.command, unknown))
dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
dispatcher.add_handler(MessageHandler(Filters.audio, echo_audio))
dispatcher.add_handler(MessageHandler(Filters.voice, echo_voice))

# Start the thread
thread = Thread(target=dispatcher.start, name="dispatcher")
thread.start()

# END

from backend.routes.telegram import set_telegram_webhook


@app.route("/")
def index():
    return redirect(INDEX_REDIRECT_URL)
