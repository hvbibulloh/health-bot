from aiogram import types
from aiogram.dispatcher.storage import FSMContext
import re
from keyboard.default.menu_keyboard import menu
from keyboard.default.russian import contact_ru, tuman_ru, malumotim_ru, chiqish_ru
from loader import dp, bot, db

from aiogram.dispatcher.filters.state import State, StatesGroup


class Russian(StatesGroup):
    telefon = State()
    ism = State()
    sana = State()
    tumani = State()
    malumoti = State()
    til_bilishi = State()


@dp.message_handler(text="Русский язык 🇧🇬")
async def uzbek(message: types.Message):
    await message.answer("Пожалуйста, введите свой номер телефона ☎", reply_markup=contact_ru)
    await Russian.telefon.set()


@dp.message_handler(state=Russian.telefon, content_types=types.ContentTypes.ANY)
async def telefoni(message: types.Message, state: FSMContext):
    try:
        if message.contact:
            async with state.proxy() as data:
                data["telefon"] = message.contact.phone_number

                await message.answer('Введите свое имя и фамилию 📄', reply_markup=chiqish_ru)
                await Russian.ism.set()


        elif re.match(r'^\+998[0-9]{9}$', message.text):
            async with state.proxy() as data:
                data["telefon"] = message.text
                await message.answer('Введите свое имя и фамилию 📄', reply_markup=chiqish_ru)
                await Russian.ism.set()

        else:
            raise ValueError('ERROR')

    except:
        await message.answer(
            "Пожалуйста, введите номер телефона пример +998991234567 ! или нажмите кнопку отправить номер 😊",
            reply_markup=contact_ru)


@dp.message_handler(state=Russian.ism, content_types=types.ContentTypes.TEXT)
async def ismi(message: types.Message, state: FSMContext):
    if message.text == 'Выход':
        await message.answer('Главная 🏠', reply_markup=menu)
        await state.finish()

    else:
        async with state.proxy() as data:
            data['ism'] = message.text
            await message.answer("Введите дату своего рождения 📅", reply_markup=chiqish_ru)
            await Russian.sana.set()


@dp.message_handler(state=Russian.sana, content_types=types.ContentTypes.TEXT)
async def sanasi(message: types.Message, state: FSMContext):
    if message.text == 'Выход':
        await message.answer('Главная 🏠', reply_markup=menu)
        await state.finish()

    else:
        async with state.proxy() as data:
            data['sana'] = message.text
            await message.answer("В каком районе вы живете", reply_markup=tuman_ru)
            await Russian.tumani.set()


@dp.message_handler(state=Russian.tumani, content_types=types.ContentTypes.TEXT)
async def tumani(message: types.Message, state: FSMContext):
    if message.text == 'Выход':
        await message.answer('Главная 🏠', reply_markup=menu)
        await state.finish()

    else:
        async with state.proxy() as data:
            data['tuman'] = message.text
            await message.answer("Введите свою информацию или вы также можете написать свою ✍",
                                 reply_markup=malumotim_ru)
            await Russian.malumoti.set()


@dp.message_handler(state=Russian.malumoti, content_types=types.ContentTypes.TEXT)
async def malumoti(message: types.Message, state: FSMContext):
    if message.text == 'Выход':
        await message.answer('Главная 🏠', reply_markup=menu)
        await state.finish()

    else:
        async with state.proxy() as data:
            data['malumoti'] = message.text
            await message.answer("Какие языки вы знаете? ✍🌐", reply_markup=chiqish_ru)
            await Russian.til_bilishi.set()


@dp.message_handler(state=Russian.til_bilishi, content_types=types.ContentTypes.TEXT)
async def til_bilishi(message: types.Message, state: FSMContext):
    if message.text == 'Выход':
        await message.answer('Главная 🏠', reply_markup=menu)
        await state.finish()

    else:
        async with state.proxy() as data:
            data['tilbilishi'] = message.text
            await message.answer("Вакансии в нашей компании", reply_markup=menu)
            await state.finish()
            phone_number = data['telefon']
            full_name = data['ism']
            birthday = data['sana']
            city = data['tuman']
            information = data['malumoti']
            await db.create_user(phone_number, full_name, birthday, city, information, message.text)
