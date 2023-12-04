from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from data_base import mongo_db as db
from lexicon.lexicon_ru import LEXICON_RU
from config.config import load_data

# инициализация роутера
router = Router()


@router.message()
async def process_other_message(message: Message):
    await message.answer(text=LEXICON_RU["other_message"])
