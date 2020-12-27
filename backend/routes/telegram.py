from backend import app, bot, BASE_URL, TELEGRAM_TOKEN

import logging

LOG = logging.getLogger(__name__)


@app.route("/set-telegram-webhook/")
def set_telegram_webhook():
    result = bot.setWebhook(f"{BASE_URL}{TELEGRAM_TOKEN}")
    if not result:
        LOG.error("Telegram webhook setup failed!")
        return 500, "failed"

    LOG.info("Telegram webhook setup success")
    return 200, "success"
