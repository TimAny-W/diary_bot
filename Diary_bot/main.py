import logging
import asyncio

from bot_config import dp
from handlers import register_handlers

logging.basicConfig(level=logging.INFO)


async def main() -> None:
    """Starting bot"""

    logging.info("Bot started")

    register_handlers(dp)
    await dp.start_polling()


if __name__ == '__main__':
    asyncio.run(main())
