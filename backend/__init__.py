import logging
import os

from flask import Flask, redirect
from telegram import Bot

INDEX_REDIRECT_URL = os.environ["INDEX_REDIRECT_URL"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]

logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
bot = Bot(token=TELEGRAM_TOKEN)

from backend.routes.telegram import set_telegram_webhook


@app.route("/")
def index():
    return redirect(INDEX_REDIRECT_URL)
