import asyncio
import logging

from aiogram import Bot, Dispatcher
from handlers import user_handlers, admin_handlers, other_handlers
from config.config import load_data


async def main():
    # подгрузка конфига
    path = None
    config = load_data(path)

    # создание бота и диспетчера и включение логирования
    bot = Bot(config.tg_bot.token)
    dp = Dispatcher()
    logging.basicConfig(level="INFO")

    # подключение роутеров
    dp.include_routers(
        admin_handlers.router, user_handlers.router, other_handlers.router
    )

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
