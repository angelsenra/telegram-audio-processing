import logging

from flask import request, url_for

from backend import TELEGRAM_TOKEN, app, bot

LOG = logging.getLogger(__name__)


@app.route("/set-telegram-webhook/")
def set_telegram_webhook():
    webhook_url = url_for(".telegram_webhook", _external=True)
    logging.info(f"Setting webhook to {webhook_url=}")
    result = bot.setWebhook(webhook_url)
    if not result:
        LOG.error("Telegram webhook setup failed!")
        return tuple([500, "failed"])

    LOG.info("Telegram webhook setup success")
    return tuple([200, "success"])


@app.route(f"/{TELEGRAM_TOKEN}")
def telegram_webhook():
    logging.info(request.text)
    logging.info(request.json)
