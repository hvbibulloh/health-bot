from aiogram import types
from config import ADMINS
from keyboard.default.menu_keyboard import menu, admin_menu
from keyboard.inline.inline_uz import website
from loader import dp, db, BASE, bot


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    media = await db.get_media()
    if message.from_user.id in ADMINS:
        if media[3] == 1:
            file_path = f"{BASE}/admin/media/{media[2]}"
            await message.answer_photo(photo=open(file_path, 'rb'), caption=media[1],
                                       reply_markup=website)
            await message.answer(f"Выберите нужный язык 🌐", reply_markup=admin_menu)
        if media[3] == 0:
            file_path = f"{BASE}/admin/media/{media[2]}"
            await bot.send_video(chat_id=message.from_user.id, video=open(file_path, 'rb'), caption=media[1],
                                 reply_markup=website)
            await bot.send_message(chat_id=message.from_user.id, text="Выберите нужный язык 🌐", reply_markup=admin_menu)

    else:
        if media[3] == 1:
            file_path = f"{BASE}/admin/media/{media[2]}"
            await message.answer_photo(photo=open(file_path, 'rb'), caption=media[1],
                                       reply_markup=website)
            await message.answer(f"Выберите нужный язык 🌐", reply_markup=menu)
        if media[3] == 0:
            file_path = f"{BASE}/admin/media/{media[2]}"
            await bot.send_video(chat_id=message.from_user.id, video=open(file_path, 'rb'), caption=media[1],
                                 reply_markup=website)
            await bot.send_message(chat_id=message.from_user.id, text="Выберите нужный язык 🌐", reply_markup=menu)
