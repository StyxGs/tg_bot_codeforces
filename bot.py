import asyncio
import logging

import aioredis
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config.config import REDIS_HOST, REDIS_PORT, load_config
from handlers import other_handlers, user_handlers
from keyboards.set_menu import set_menu
from services.services import starting_update

logger = logging.getLogger(__name__)


async def main():
    """Функция для запуска бота"""

    logging.basicConfig(level=logging.INFO,
                        format=u'%(filename)s:%(lineno)d #%(levelname)-8s '
                               u'[%(asctime)s] - %(name)s - %(message)s')

    logger.info('Starting bot')

    config = load_config()

    redis = await aioredis.from_url(url=f'redis://{REDIS_HOST}:{REDIS_PORT}', db=0)

    storage: RedisStorage = RedisStorage(redis)

    bot: Bot = Bot(token=config.token, parse_mode='HTML')
    dp: Dispatcher = Dispatcher(storage=storage)

    apscheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    apscheduler.add_job(starting_update, trigger='interval', hours=1)
    apscheduler.start()

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await starting_update()
    await set_menu(bot)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error('Bot stopped!')
