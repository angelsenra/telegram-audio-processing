from backend import TELEGRAM_PERSONAL_ID


def start(update, context):
    context.bot.send_message(
        chat_id=TELEGRAM_PERSONAL_ID,
        text=f"{update.update_id=}; {update.effective_user.username} started a conversation",
    )
    context.bot.send_message(chat_id=update.effective_chat.id, text="Start!")


def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")
