from aiogram import types

from keyboard.default.menu_keyboard import menu
from keyboard.inline.inline_uz import website
from loader import dp, db, BASE, bot


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    media = await db.get_media()

    if media[3] == 1:
        file_path = f"{BASE}/admin/media/{media[2]}"
        await bot.send_photo(chat_id=message.from_user.id, photo=open(file_path, 'rb'), caption=media[1],
                             reply_markup=website)
        await bot.send_message(chat_id=message.from_user.id, text="Выберите нужный язык 🌐", reply_markup=menu)
    if media[3] == 0:
        file_path = f"{BASE}/admin/media/{media[2]}"
        await bot.send_video(chat_id=message.from_user.id, video=open(file_path, 'rb'), caption=media[1],
                             reply_markup=website)
        await bot.send_message(chat_id=message.from_user.id, text="Выберите нужный язык 🌐", reply_markup=menu)

