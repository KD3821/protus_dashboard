import asyncio
import os

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from dashboard.utils import get_report_time

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(
        f"Приветствую, {html.bold(message.from_user.full_name)}!\n"
        f"Если Вы ИЗБРАННЫЙ - я пришлю Вам отчет по складу в указанное время."
    )


@dp.message()
async def echo_handler(message: Message) -> None:
    report_time = await get_report_time()
    await message.answer(
        f"Ожидайте, {html.bold(message.from_user.full_name)}...\n"
        f"Время ежедневного отчета: {report_time}"
    )


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
