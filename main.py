import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from handlers import user_commands, daily_stats, echo_handler, get_excel_handler



load_dotenv()
bot = Bot(token=os.getenv("API_TOKEN"))
dp = Dispatcher()


async def main():
    bot = Bot(token=os.getenv("API_TOKEN"))
    dp = Dispatcher()

    dp.include_routers(
        user_commands.router,
        get_excel_handler.router,
        daily_stats.router,
        echo_handler.router
    )

    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands([
        BotCommand(command="/start", description="Start bot"),
        BotCommand(command="/daily_report", description="Отчет по дням"),
        BotCommand(command="/work_report", description="Отчет по работе"),
        BotCommand(command="/last_bets", description="Последние ставки"),
        BotCommand(command="/accs_report", description="Ответ по аккаунтам")
    ])

    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())

