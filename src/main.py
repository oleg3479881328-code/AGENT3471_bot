import getpass
import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters


def setup_logging() -> None:
    os.makedirs("logs", exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.FileHandler("logs/bot.log", encoding="utf-8"),
            logging.StreamHandler(),
        ],
    )


def get_bot_token() -> str:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if token:
        return token.strip()

    token = getpass.getpass("Paste Telegram bot token: ").strip()
    if not token:
        raise RuntimeError("Telegram bot token is empty.")

    return token


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    name = user.first_name if user and user.first_name else "there"

    await update.message.reply_text(
        f"Hello, {name}. AGENT3471_bot is running."
    )


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text if update.message else ""
    logging.info("Incoming message: %s", text)

    await update.message.reply_text(
        f"You said: {text}"
    )


def main() -> None:
    setup_logging()
    token = get_bot_token()

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    logging.info("AGENT3471_bot started")
    app.run_polling()


if __name__ == "__main__":
    main()
