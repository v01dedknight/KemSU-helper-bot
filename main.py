# Logging initialisation
from config import logging as _

# Import asyncio for running asynchronous functions
import asyncio

# Import Bot and Dispatcher from aiogram
from aiogram import Bot, Dispatcher

# Import configuration and router
from config.settings import TELEGRAM_TOKEN
from bot.handlers import router

# log imp
import logging

logger = logging.getLogger(__name__)

# Main entry point for running the Telegram bot
async def main():
    # Initialize the bot with the token
    bot = Bot(token=TELEGRAM_TOKEN)

    # Initialize the dispatcher
    dp = Dispatcher()

    # Include all message handlers from the router
    dp.include_router(router)

    # Print a message indicating the bot has started
    logger.info("Telegram bot started")
    
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.exception(f"Telegram bot crashed: {e}")
        raise

    # Start polling for updates
    await dp.start_polling(bot)


# Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())