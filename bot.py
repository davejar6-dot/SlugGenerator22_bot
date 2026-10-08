import logging
import os
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from slugify import slugify

# ----------------------------
# Logging setup
# ----------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ----------------------------
# /start command
# ----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Greets the user and explains how to use the bot."""
    user = update.effective_user
    name = user.first_name if user and user.first_name else "there"
    await update.message.reply_text(
        f"Hello {name}! 👋\n\n"
        "I am a *Slug Generator Bot* 🐌\n\n"
        "Send me any text and I will convert it into a clean, "
        "URL-friendly slug!\n\n"
        "Example:\n"
        "`Hello World! This is a Test`\n"
        "⬇️\n"
        "`hello-world-this-is-a-test`",
        parse_mode="Markdown",
    )


# ----------------------------
# /help command
# ----------------------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📖 *How to use this bot:*\n\n"
        "1. Just send me any text\n"
        "2. I will return a clean, URL-friendly slug\n\n"
        "Commands:\n"
        "/start - Start the bot\n"
        "/help - Show this help message",
        parse_mode="Markdown",
    )


# ----------------------------
# Core: generate slug from message
# ----------------------------
async def generate_slug(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Parses the user's message and generates a URL-friendly slug."""
    user_input = update.message.text.strip()

    if not user_input:
        await update.message.reply_text(
            "⚠️ Please send some text to convert into a slug."
        )
        return

    try:
        # Generate the slug using python-slugify
        # This automatically handles accents, emojis, punctuation, etc.
        generated_slug = slugify(user_input)

        if not generated_slug:
            await update.message.reply_text(
                "❌ I couldn't generate a slug from that text.\n"
                "Please make sure it contains some letters or numbers."
            )
            return

        response = (
            f"🔗 *Your Slug:*\n\n"
            f"`{generated_slug}`\n\n"
            f"_Copy and paste it into your URL!_"
        )
        await update.message.reply_text(response, parse_mode="Markdown")

    except Exception as e:
        logger.error(f"Error generating slug: {e}")
        await update.message.reply_text(
            "⚠️ Sorry, something went wrong. Please try again."
        )


# ----------------------------
# Main entry point
# ----------------------------
def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN is not set. Exiting.")
        return

    application = Application.builder().token(token).build()

    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, generate_slug)
    )

    logger.info("Slug Generator Bot is starting...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
