import logging

from flask import request, url_for
from telegram import Update

from backend import TELEGRAM_TOKEN, app, bot, update_queue

LOG = logging.getLogger(__name__)


@app.route("/set-telegram-webhook/")
def set_telegram_webhook():
    webhook_url = url_for(".telegram_webhook", _external=True)
    logging.info(f"Setting webhook to {webhook_url=}")
    result = bot.setWebhook(webhook_url)
    if not result:
        LOG.error("Telegram webhook setup failed!")
        return "failed"

    LOG.info("Telegram webhook setup success")
    return "success"


@app.route(f"/{TELEGRAM_TOKEN}/", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    update_queue.put(update)
    return "success"
