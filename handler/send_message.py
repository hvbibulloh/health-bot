from aiogram import types
from aiogram.dispatcher.storage import FSMContext
import re

from keyboard.default.admin import chiqishrek
from keyboard.default.menu_keyboard import menu, asosiy_menu, admin_menu
from keyboard.default.uzbek import contact_uz, chiqish, tuman, malumotim, vakansiya_uz_button, ishlamoq, javobi
from keyboard.inline.inline_uz import website, websiteuz
from loader import dp, bot, db, BASE
from config import ADMINS

from aiogram.dispatcher.filters.state import State, StatesGroup


class SendMessage(StatesGroup):
    id = State()
    message = State()


@dp.message_handler(text="Yuborish 🎙")
async def send_xabar(message: types.Message):
    if message.from_user.id in ADMINS:
        await message.answer(text="Foydalanuvchi ID sini kiriting !", reply_markup=chiqishrek)
        await SendMessage.id.set()

    else:
        await message.answer(text="Siz admin emassiz !")


@dp.message_handler(state=SendMessage.id, content_types=types.ContentTypes.TEXT)
async def send_text(message: types.Message, state: FSMContext):
    if message.text == "Chiqish":
        await message.answer("Bosh Menu ", reply_markup=asosiy_menu)
        await state.finish()


    elif message.text.isdigit():
        await message.answer("Xabaringizni yuboring ‼", reply_markup=chiqishrek)
        await SendMessage.message.set()
        async with state.proxy() as data:
            data["id"] = message.text

    else:
        await message.answer("Id yuboring !", reply_markup=chiqishrek)


@dp.message_handler(state=SendMessage.message, content_types=types.ContentTypes.ANY)
async def send_media(message: types.Message, state: FSMContext):
    try:
        if message.text == "Chiqish":
            await message.answer("Bosh menu", reply_markup=asosiy_menu)
            await state.finish()
        else:
            async with state.proxy() as data:
                if message.video:
                    await bot.send_video(chat_id=int(data['id']), video=message.video.file_id, caption=message.caption)
                elif message.audio:
                    await bot.send_audio(chat_id=int(data['id']), audio=message.audio.file_id, caption=message.caption)
                elif message.photo:
                    await bot.send_photo(chat_id=int(data['id']), photo=message.photo[-1].file_id, caption=message.caption)
                elif message.text:
                    await bot.send_message(chat_id=int(data['id']), text=message.text)
                elif message.location:
                    latitude = message.location.latitude
                    longitude = message.location.longitude
                    await bot.send_location(chat_id=int(data['id']), latitude=latitude, longitude=longitude)
                else:
                    await message.answer("Bu turdagi ma'lumot yubora olmayman ", reply_markup=chiqishrek)

                await message.answer("Yuborildi", reply_markup=admin_menu)
                await state.finish()

    except Exception as e:
        await message.answer(f"{e} Foydalanuvchi sizni blocklab qo'ygan !", reply_markup=admin_menu)
        await state.finish()
