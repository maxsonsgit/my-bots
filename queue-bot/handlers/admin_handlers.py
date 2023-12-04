from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, BaseFilter
from data_base import mongo_db as db
from lexicon.lexicon_ru import LEXICON_RU
from config.config import load_data


class IsAdmin(BaseFilter):
    def __init__(self, admins_id: list[int]) -> None:
        self.admins_id = admins_id

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in self.admins_id


# инициализация роутера
router = Router()
router.message.filter(IsAdmin(load_data(".env").tg_bot.admins_id))


@router.message(Command("aswap"))
async def process_aswap_command(message: Message):
    text = message.text.split()
    queue_number1, queue_number2 = int(text[-2]), int(text[-1])
    db.admin_swap(queue_number1, queue_number2)
    await message.answer(text=LEXICON_RU["/aswap"])
