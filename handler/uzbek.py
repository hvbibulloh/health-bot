from aiogram import types
from aiogram.dispatcher.storage import FSMContext
import re
from keyboard.default.menu_keyboard import menu
from keyboard.default.uzbek import contact_uz, chiqish, tuman, malumotim, vakansiya_uz_button
from loader import dp, bot, db

from aiogram.dispatcher.filters.state import State, StatesGroup


class Uzbek(StatesGroup):
    telefon = State()
    ism = State()
    sana = State()
    tumani = State()
    malumoti = State()
    til_bilishi = State()


@dp.message_handler(text="O'zbek tili 🇺🇿")
async def uzbek(message: types.Message):
    await message.answer("Iltimos telefon raqamingizni kiriting ☎", reply_markup=contact_uz)
    await Uzbek.telefon.set()


@dp.message_handler(state=Uzbek.telefon, content_types=types.ContentTypes.ANY)
async def telefoni(message: types.Message, state: FSMContext):
    try:
        if message.contact:
            async with state.proxy() as data:
                data["telefon"] = message.contact.phone_number

                await message.answer('Ism va familiyangizni kiriting 📄', reply_markup=chiqish)
                await Uzbek.ism.set()


        elif re.match(r'^\+998[0-9]{9}$', message.text):
            async with state.proxy() as data:
                data["telefon"] = message.text
                await message.answer('Ism va familiyangizni kiriting 📄', reply_markup=chiqish)
                await Uzbek.ism.set()

        else:
            raise ValueError('ERROR')

    except:
        await message.answer(
            "Iltimos telefon raqam kiriting misol +998991234567 ! yoki Raqam yuborish tugmasini bosing 😊",
            reply_markup=contact_uz)


@dp.message_handler(state=Uzbek.ism, content_types=types.ContentTypes.TEXT)
async def ismi(message: types.Message, state: FSMContext):
    if message.text == 'Chiqish':
        await message.answer('Bosh sahifa 🏠', reply_markup=menu)
        await state.finish()

    else:
        async with state.proxy() as data:
            data['ism'] = message.text
            await message.answer("Tug'ulgan sanangizni kiriting 📅", reply_markup=chiqish)
            await Uzbek.sana.set()


@dp.message_handler(state=Uzbek.sana, content_types=types.ContentTypes.TEXT)
async def sanasi(message: types.Message, state: FSMContext):
    if message.text == 'Chiqish':
        await message.answer('Bosh Sahifa 🏠', reply_markup=menu)
        await state.finish()

    else:
        async with state.proxy() as data:
            data['sana'] = message.text
            await message.answer("Qaysi tumanda istiqomat qilasiz", reply_markup=tuman)
            await Uzbek.tumani.set()


@dp.message_handler(state=Uzbek.tumani, content_types=types.ContentTypes.TEXT)
async def tumani(message: types.Message, state: FSMContext):
    if message.text == 'Chiqish':
        await message.answer('Bosh Sahifa 🏠', reply_markup=menu)
        await state.finish()

    else:
        async with state.proxy() as data:
            data['tuman'] = message.text
            await message.answer("Malumotingizni kiriting yoki o'zingiz yozishingiz ham mumkin ✍",
                                 reply_markup=malumotim)
            await Uzbek.malumoti.set()


@dp.message_handler(state=Uzbek.malumoti, content_types=types.ContentTypes.TEXT)
async def malumoti(message: types.Message, state: FSMContext):
    if message.text == 'Chiqish':
        await message.answer('Bosh Sahifa 🏠', reply_markup=menu)
        await state.finish()

    else:
        async with state.proxy() as data:
            data['malumoti'] = message.text
            await message.answer("Qaysi tillarni bilasiz? ✍🌐", reply_markup=chiqish)
            await Uzbek.til_bilishi.set()


@dp.message_handler(state=Uzbek.til_bilishi, content_types=types.ContentTypes.TEXT)
async def til_bilishi(message: types.Message, state: FSMContext):
    if message.text == 'Chiqish':
        await message.answer('Bosh Sahifa 🏠', reply_markup=menu)
        await state.finish()

    else:
        async with state.proxy() as data:
            data['tilbilishi'] = message.text
            await message.answer("Kompaniyamizning bo'sh ish o'rinlari", reply_markup=vakansiya_uz_button())
            await state.finish()
            phone_number = data['telefon']
            full_name = data['ism']
            birthday = data['sana']
            city = data['tuman']
            information = data['malumoti']
            await db.create_user(phone_number, full_name, birthday, city, information, message.text)
