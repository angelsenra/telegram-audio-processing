import logging

from flask import request, url_for
from telegram import Update

from backend import DEVELOPMENT_MODE, TELEGRAM_TOKEN, app, bot, update_queue

LOG = logging.getLogger(__name__)

last_update_id = 0


@app.route(f"/{TELEGRAM_TOKEN}/", methods=["POST"])
def telegram_webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    update_queue.put(update)
    return "success"


@app.route("/set-telegram-webhook/")
def set_telegram_webhook():
    webhook_url = url_for(".telegram_webhook", _external=True)
    logging.info(f"Setting webhook to {webhook_url=}")
    result = bot.set_webhook(webhook_url)
    if not result:
        LOG.error("Telegram webhook setup failed!")
        return "failed"

    LOG.info("Telegram webhook setup success")
    return "success"


if DEVELOPMENT_MODE:

    @app.route("/disable-telegram-webhook/")
    def disable_telegram_webhook():
        logging.info(f"Disabling webhook")
        result = bot.set_webhook("")
        if not result:
            LOG.error("Telegram webhook disabling failed!")
            return "failed"

        LOG.info("Telegram webhook disabling success")
        return "success"

    @app.route("/process-last-message/")
    def process_last_message():
        global last_update_id
        updates = bot.get_updates(offset=last_update_id, limit=1, timeout=1)
        if not updates:
            LOG.info(f"Empty updates; {updates=}; {last_update_id=}")
            return "empty"

        last_update_id = updates[-1].update_id + 1
        LOG.info(f"Some updates; {len(updates)=}; {last_update_id=}")
        for update in updates:
            LOG.info(f"Enqueuing {update.update_id=}...")
            update_queue.put(update)
        return str(last_update_id)
