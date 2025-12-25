# Import asyncio for running asynchronous functions
import asyncio

# Import Bot and Dispatcher from aiogram
from aiogram import Bot, Dispatcher

# Import configuration and router
from config.settings import TELEGRAM_TOKEN
from bot.handlers import router

# Main entry point for running the Telegram bot
async def main():
    # Initialize the bot with the token
    bot = Bot(token=TELEGRAM_TOKEN)

    # Initialize the dispatcher
    dp = Dispatcher()

    # Include all message handlers from the router
    dp.include_router(router)

    # Print a message indicating the bot has started
    print("Telegram bot started")

    # Start polling for updates
    await dp.start_polling(bot)


# Run the main function using asyncio
if __name__ == "__main__":
    asyncio.run(main())