from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from handlers.handler import router
from aiogram.enums import ParseMode
from core.settings import settings
import asyncio
import logging

bot = Bot(token=settings.token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

async def main():
    dp.include_routers(router)
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    try:
        logging.basicConfig(level=logging.INFO)
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stop Bot!')    
        