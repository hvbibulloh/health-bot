from aiogram import types
from aiogram.dispatcher.storage import FSMContext
import re
from keyboard.default.menu_keyboard import menu
from keyboard.default.uzbek import contact_uz, chiqish, tuman, malumotim, vakansiya_uz_button, ishlamoq, javobi
from loader import dp, bot, db, BASE

from aiogram.dispatcher.filters.state import State, StatesGroup


class Uzbek(StatesGroup):
    telefon = State()
    ism = State()
    sana = State()
    tumani = State()
    malumoti = State()
    til_bilishi = State()


class VakansiyaTest(StatesGroup):
    test1 = State()
    javob1 = State()
    test2 = State()
    test3 = State()
    test4 = State()


@dp.message_handler(text="O'zbek tili 🇺🇿")
async def uzbek(message: types.Message):
    vakansiya_button = await vakansiya_uz_button()
    user_id = await db.get_user(str(message.from_user.id))
    if user_id:
        await message.answer("Kompaniyamizning bo'sh ish o'rinlari", reply_markup=vakansiya_button)
    else:
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
            vakansiya_button = await vakansiya_uz_button()
            data['tilbilishi'] = message.text
            await message.answer("Kompaniyamizning bo'sh ish o'rinlari", reply_markup=vakansiya_button)
            await state.finish()
            phone_number = data['telefon']
            full_name = data['ism']
            birthday = data['sana']
            city = data['tuman']
            information = data['malumoti']
            db.create_user(message.from_user.id, phone_number, full_name, birthday, city, information,
                           message.text)


@dp.message_handler()
async def vakansiya_send(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['vakansiya_name'] = message.text
        vakansiya_name = message.text[:-2]
        vakansiya = await db.get_vakansiya(vakansiya_name)
        if vakansiya:
            file_path = f"{BASE}/admin/{vakansiya[3]}"

            await bot.send_photo(message.chat.id, photo=open(file_path, 'rb'), caption=vakansiya[2],
                                 reply_markup=ishlamoq)

            await VakansiyaTest.test1.set()


        else:
            await bot.send_message(message.from_user.id, text="Bunday vakansiya topilmadi.")


@dp.message_handler(state=VakansiyaTest.test1, content_types=types.ContentTypes.TEXT)
async def vakansiya_test1(message: types, state: FSMContext):
    try:
        vakansiya_button = await vakansiya_uz_button()
        if message.text == "Orqaga 🔙":
            await message.answer(text="Vakansiya sahifasidasiz 📝", reply_markup=vakansiya_button)
            await state.finish()

        else:
            async with state.proxy() as data:
                vakansiya_name = data["vakansiya_name"]
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya:
                    print(vakansiya)
                    await message.answer(text="Iltimos savollarga e'tibor bilan javob bering 😊")
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[6]}", reply_markup=javobi)

                    await VakansiyaTest.javob1.set()


    except:
        await message.answer(
            "Hatolik paydo bo'ldi qaytadan uruning !",
            reply_markup=menu)
        await state.finish()


@dp.message_handler(state=VakansiyaTest.javob1, content_types=types.ContentTypes.TEXT)
async def vakansiya_javobi1(message: types.Message, state: FSMContext):
    try:
        if message.text == "Ha":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[7] == 0:
                    data["ball"] = 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi)
                    await VakansiyaTest.test2.set()

                elif vakansiya[7] == 1:
                    data["ball"] = 0
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi)
                    await VakansiyaTest.test2.set()

        elif message.text == "Yo'q":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[7] == 1:
                    data["ball"] = 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi)
                    await VakansiyaTest.test2.set()

                elif vakansiya[7] == 0:
                    data["ball"] = 0
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi)
                    await VakansiyaTest.test2.set()

    except Exception as e:
        await message.answer("Qaytadan uruning !", reply_markup=javobi)


@dp.message_handler(state=VakansiyaTest.test2, content_types=types.ContentTypes.TEXT)
async def test2(message: types.Message, state: FSMContext):
    try:
        if message.text == "Ha":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[9] == 0:
                    data["ball"] += 1

                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi)
                    await VakansiyaTest.test3.set()

                elif vakansiya[9] == 1:

                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi)
                    await VakansiyaTest.test3.set()

        elif message.text == "Yo'q":
            async with state.proxy() as data:

                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[9] == 1:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi)
                    await VakansiyaTest.test3.set()

                elif vakansiya[9] == 0:
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi)
                    await VakansiyaTest.test3.set()

    except Exception as e:
        await message.answer("Qaytadan uruning !", reply_markup=javobi)


@dp.message_handler(state=VakansiyaTest.test3, content_types=types.ContentTypes.TEXT)
async def test3(message: types.Message, state: FSMContext):
    try:
        if message.text == "Ha":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[11] == 0:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi)
                    await VakansiyaTest.test4.set()

                elif vakansiya[11] == 1:
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi)
                    await VakansiyaTest.test4.set()

        elif message.text == "Yo'q":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[11] == 1:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi)
                    await VakansiyaTest.test4.set()

                elif vakansiya[11] == 0:
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi)
                    await VakansiyaTest.test4.set()

    except Exception as e:
        await message.answer("Qaytadan uruning !", reply_markup=javobi)


@dp.message_handler(state=VakansiyaTest.test4, content_types=types.ContentTypes.TEXT)
async def test4(message: types.Message, state: FSMContext):
    try:
        if message.text == "Ha":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[13] == 0:
                    data["ball"] += 1

                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Javobingiz va sabringiz uchun rahmat tez orada siz bilan adminlarimiz bog'lanishadi 😊",
                                           reply_markup=menu)
                    await state.finish()

                elif vakansiya[13] == 1:

                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Javobingiz va sabringiz uchun rahmat tez orada siz bilan adminlarimiz bog'lanishadi 😊",
                                           reply_markup=menu)
                    await state.finish()
        elif message.text == "Yo'q":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[13] == 1:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Javobingiz va sabringiz uchun rahmat tez orada siz bilan adminlarimiz bog'lanishadi 😊",
                                           reply_markup=menu)
                    await state.finish()

                elif vakansiya[13] == 0:
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Javobingiz va sabringiz uchun rahmat tez orada siz bilan adminlarimiz bog'lanishadi 😊",
                                           reply_markup=menu)
                    await state.finish()

    except Exception as e:
        await message.answer("Qaytadan uruning !", reply_markup=javobi)
