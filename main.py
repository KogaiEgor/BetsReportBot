import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher

from handlers import user_commands, daily_stats, echo_handler



load_dotenv()
bot = Bot(token=os.getenv("API_TOKEN"))
dp = Dispatcher()


async def main():
    bot = Bot(token=os.getenv("API_TOKEN"))
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        daily_stats.router,
        echo_handler.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

