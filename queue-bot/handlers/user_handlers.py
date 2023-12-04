from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command
from data_base import mongo_db as db
from lexicon.lexicon_ru import LEXICON_RU


# инициализация роутера
router = Router()


@router.message(Command("start"))
async def process_start_command(message: Message):
    await message.answer(LEXICON_RU["/start"])


@router.message(Command("help"))
async def process_help_command(message: Message):
    await message.answer(LEXICON_RU["/help"])


@router.message(Command("get_in_line"))
async def process_get_in_line_command(message: Message):
    db.get_in_line(message)
    await message.answer(text=LEXICON_RU["/get_in_line"])


@router.message(Command("get_out_of_line"))
async def process_get_out_of_line_command(message: Message):
    db.get_out_of_the_line(message.from_user.id)
    await message.answer(text=LEXICON_RU["/get_out_of_line"])


async def send_captcha(user_id, bot: Bot):
    await bot.send_message(chat_id=user_id, text=LEXICON_RU["captcha"])


@router.message(Command("agree"))
async def process_agree_command(message: Message, bot: Bot):
    list_of_ids = db.get_request_ids(message.from_user.id)
    db.admin_swap(
        db.get_user_queue_number(list_of_ids[0]),
        db.get_user_queue_number(list_of_ids[1]),
    )
    db.delete_request(list_of_ids[0], list_of_ids[1])
    await bot.send_message(chat_id=list_of_ids[0], text=LEXICON_RU["agree_request"])
    await bot.send_message(chat_id=list_of_ids[1], text=LEXICON_RU["agree_recipient"])


@router.message(Command("disagree"))
async def process_disagree_command(message: Message, bot: Bot):
    list_of_ids = db.get_request_ids(message.from_user.id)
    db.delete_request(list_of_ids[0], list_of_ids[1])
    await bot.send_message(chat_id=list_of_ids[0], text=LEXICON_RU["disagree_request"])
    await bot.send_message(
        chat_id=list_of_ids[1], text=LEXICON_RU["disagree_recipient"]
    )


@router.message(Command("swap"))
async def process_swap_command(message: Message, bot: Bot):
    new_queue_number = int(message.text.split()[-1])
    new_user_id = db.get_user_id(new_queue_number)
    await send_captcha(new_user_id, bot)
    await message.answer(text=LEXICON_RU["/swap"])
    db.insert_request(message.from_user.id, new_user_id)


@router.message(Command("show"))
async def process_show_command(message: Message):
    text = ""
    for user in db.show():
        text += f'{user["queue_number"]}. {user["name"]}\n'
    await message.answer(text=text)


@router.message(Command("showme"))
async def process_showme_cimmand(message: Message):
    user = db.show_me(message.from_user.id)
    await message.answer(f'Вы {user["queue_number"]}-й в очереди')
