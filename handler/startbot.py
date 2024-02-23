from aiogram import types

from keyboard.default.menu_keyboard import menu
from loader import dp



@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(f"Assalomu aleykum {message.from_user.full_name}", reply_markup=menu)