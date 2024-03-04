from aiogram import types
from aiogram.dispatcher.storage import FSMContext
import re
from keyboard.default.menu_keyboard import menu, asosiy_menu
from keyboard.default.uzbek import contact_uz, chiqish, tuman, malumotim, vakansiya_uz_button, ishlamoq, javobi
from keyboard.inline.inline_uz import website, websiteuz
from loader import dp, bot, db, BASE

from aiogram.dispatcher.filters.state import State, StatesGroup


class Uzbek(StatesGroup):
    telefon = State()


class Kondidant(StatesGroup):
    telefon = State()
    ism = State()
    sana = State()
    tumani = State()
    malumoti = State()
    tajriba = State()
    til_bilishi = State()
    vakansiya_send = State()
    test1 = State()
    javob1 = State()
    test2 = State()
    test3 = State()
    test4 = State()


class Taklif(StatesGroup):
    telefon = State()
    about = State()


@dp.message_handler(text="O'zbek tili 🇺🇿")
async def uzbek(message: types.Message):
    vakansiya_button = await vakansiya_uz_button()
    user_id = await db.get_user(str(message.from_user.id))
    if user_id:
        await message.answer("Asosiy menyu 🏠", reply_markup=asosiy_menu)

    else:
        await message.answer("Iltimos telefon raqamingizni kiriting ☎", reply_markup=contact_uz)
        await Uzbek.telefon.set()


@dp.message_handler(state=Uzbek.telefon, content_types=types.ContentTypes.ANY)
async def telefoni(message: types.Message, state: FSMContext):
    try:
        if message.contact:
            async with state.proxy() as data:
                data["telefon"] = message.contact.phone_number

                await message.answer("Kerakli bo'limni tanlang 🛎", reply_markup=asosiy_menu)
                await state.finish()

        elif re.match(r'^\+998[0-9]{9}$', message.text):
            async with state.proxy() as data:
                data["telefon"] = message.text
                await message.answer("Kerali bo'limni tanlang 🛎", reply_markup=asosiy_menu)
                await state.finish()
        else:
            raise ValueError('ERROR')

    except:
        await message.answer(
            "Iltimos telefon raqam kiriting misol +998991234567 ! yoki Raqam yuborish tugmasini bosing 😊",
            reply_markup=contact_uz)


@dp.message_handler(text="Vakansiyalar 💼")
async def menuse(message: types.Message, state: FSMContext):
    vakansiya_button = await vakansiya_uz_button()
    user_id = await db.get_user(str(message.from_user.id))
    if user_id:
        await message.answer(
            "Siz Vakansiya bo'yicha o'z nomzodingizni qo'yib bo'ldingiz\n3 kundan so'ng sizga yana ro'yxatdan o'tishingizga ruxsat beriladi 😊",
            reply_markup=asosiy_menu)
    else:
        await bot.send_message(chat_id=message.from_user.id, text="Ism Familiyangizni kiriting 📝",
                               reply_markup=types.ReplyKeyboardRemove())
        await Kondidant.ism.set()


@dp.message_handler(state=Kondidant.ism, content_types=types.ContentTypes.TEXT)
async def kondidant_ismi(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ism'] = message.text
        await message.answer("Tug'ulgan sanangizni kiriting 📅 01.01.1990")
        await Kondidant.sana.set()


@dp.message_handler(state=Kondidant.sana, content_types=types.ContentTypes.TEXT)
async def kondidant_sana(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sana'] = message.text
        await message.answer("Qaysi tumanda istiqomat qilasiz? 🏠", reply_markup=tuman)
        await Kondidant.tumani.set()


@dp.message_handler(state=Kondidant.tumani, content_types=types.ContentTypes.TEXT)
async def kondidant_tumana(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tuman'] = message.text
        await message.answer("Ma'lumotingizni kiriting yoki o'zingiz yozishingiz ham mumkin", reply_markup=malumotim)
        await Kondidant.malumoti.set()


@dp.message_handler(state=Kondidant.malumoti, content_types=types.ContentTypes.TEXT)
async def kondidant_malumoti(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['malumoti'] = message.text
        await message.answer(
            "Sizning ish tajribangiz qanday? ----\n- kompaniya\n- lavozim\n- ish davri\nMisol: 'Dream Work' MCHJ, kassir, 2015-2018.",
            reply_markup=types.ReplyKeyboardRemove())
        await Kondidant.tajriba.set()


@dp.message_handler(state=Kondidant.tajriba, content_types=types.ContentTypes.TEXT)
async def kondidant_tajriba(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tajriba'] = message.text
        await message.answer("Qaysi tillarni bilasiz? \n\nO'zbek, Rus, Ingliz \n\nshu variantda yozing ✍",
                             reply_markup=types.ReplyKeyboardRemove())
        await Kondidant.til_bilishi.set()


@dp.message_handler(state=Kondidant.til_bilishi, content_types=types.ContentTypes.TEXT)
async def kondidant_til_bilishi(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        vakansiya_button = await vakansiya_uz_button()
        data['tilbilishi'] = message.text
        phone_number = data['telefon']
        full_name = data['ism']
        birthday = data['sana']
        city = data['tuman']
        information = data['malumoti']
        tajriba = data['tajriba']
        db.create_user(message.from_user.id, phone_number, full_name, birthday, city, information, message.text,
                       tajriba)

        await Kondidant.vakansiya_send.set()

        await message.answer("Kompaniyamizning bo'sh ish o'rinlari", reply_markup=vakansiya_button)


@dp.message_handler(state=Kondidant.vakansiya_send, content_types=types.ContentTypes.TEXT)
async def vakansiya_sende(message: types.Message, state: FSMContext):
    if message.text == "Chiqish":
        await message.answer("Asosiy Menyu", reply_markup=asosiy_menu)
        await state.finish()

    else:
        async with state.proxy() as data:
            data['vakansiya_name'] = message.text
            vakansiya_name = message.text[:-2]
            vakansiya = await db.get_vakansiya(vakansiya_name)
            if vakansiya:
                file_path = f"{BASE}/admin/media/{vakansiya[3]}"

                await bot.send_photo(message.chat.id, photo=open(file_path, 'rb'), caption=vakansiya[2],
                                     reply_markup=ishlamoq)

                await Kondidant.test1.set()


            else:
                await bot.send_message(message.from_user.id, text="Bunday vakansiya topilmadi.")


@dp.message_handler(state=Kondidant.test1, content_types=types.ContentTypes.TEXT)
async def vakansiya_test1(message: types, state: FSMContext):
    try:
        vakansiya_button = await vakansiya_uz_button()
        if message.text == "Orqaga 🔙":
            await message.answer(text="Vakansiya sahifasidasiz 📝", reply_markup=vakansiya_button)
            await Kondidant.vakansiya_send.set()

        else:
            async with state.proxy() as data:
                vakansiya_name = data["vakansiya_name"]
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya:
                    await message.answer(text="Iltimos savollarga e'tibor bilan javob bering 😊")
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[6]}", reply_markup=javobi)

                    await Kondidant.javob1.set()


    except:
        await message.answer(
            "Hatolik paydo bo'ldi qaytadan uruning !",
            reply_markup=menu)
        await state.finish()


@dp.message_handler(state=Kondidant.javob1, content_types=types.ContentTypes.TEXT)
async def vakansiya_javobi1(message: types.Message, state: FSMContext):
    try:
        if message.text == "Ha":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[7] == 0:
                    data["ball"] = 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi)
                    await Kondidant.test2.set()

                elif vakansiya[7] == 1:
                    data["ball"] = 0
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi)
                    await Kondidant.test2.set()

        elif message.text == "Yo'q":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[7] == 1:
                    data["ball"] = 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi)
                    await Kondidant.test2.set()

                elif vakansiya[7] == 0:
                    data["ball"] = 0
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi)
                    await Kondidant.test2.set()

    except Exception as e:
        await message.answer("Qaytadan uruning !", reply_markup=javobi)


@dp.message_handler(state=Kondidant.test2, content_types=types.ContentTypes.TEXT)
async def test2(message: types.Message, state: FSMContext):
    try:
        if message.text == "Ha":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[9] == 0:
                    data["ball"] += 1

                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi)
                    await Kondidant.test3.set()

                elif vakansiya[9] == 1:

                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi)
                    await Kondidant.test3.set()

        elif message.text == "Yo'q":
            async with state.proxy() as data:

                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[9] == 1:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi)
                    await Kondidant.test3.set()

                elif vakansiya[9] == 0:
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi)
                    await Kondidant.test3.set()

    except Exception as e:
        await message.answer("Qaytadan uruning !", reply_markup=javobi)


@dp.message_handler(state=Kondidant.test3, content_types=types.ContentTypes.TEXT)
async def test3(message: types.Message, state: FSMContext):
    try:
        if message.text == "Ha":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[11] == 0:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi)
                    await Kondidant.test4.set()

                elif vakansiya[11] == 1:
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi)
                    await Kondidant.test4.set()

        elif message.text == "Yo'q":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[11] == 1:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi)
                    await Kondidant.test4.set()

                elif vakansiya[11] == 0:
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi)
                    await Kondidant.test4.set()

    except Exception as e:
        await message.answer("Qaytadan uruning !", reply_markup=javobi)


@dp.message_handler(state=Kondidant.test4, content_types=types.ContentTypes.TEXT)
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
                                           reply_markup=asosiy_menu)
                    await bot.send_location(chat_id=message.from_user.id, latitude=41.2159400, longitude=69.1895840)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Республика Узбекистан, 111802,\nг. Ташкент, Янгиҳаётcкий р-н,\nУзгариш, ул, Навруз, д. 236а")
                    db.get_ball(str(message.from_user.id), str(data['ball']))
                    await state.finish()

                elif vakansiya[13] == 1:

                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Javobingiz va sabringiz uchun rahmat tez orada siz bilan adminlarimiz bog'lanishadi 😊",
                                           reply_markup=asosiy_menu)
                    await bot.send_location(chat_id=message.from_user.id, latitude=41.2159400, longitude=69.1895840)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Республика Узбекистан, 111802,\nг. Ташкент, Янгиҳаётcкий р-н,\nУзгариш, ул, Навруз, д. 236а")
                    db.get_ball(str(message.from_user.id), str(data['ball']))
                    await state.finish()
        elif message.text == "Yo'q":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                if vakansiya[13] == 1:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Javobingiz va sabringiz uchun rahmat tez orada siz bilan adminlarimiz bog'lanishadi 😊",
                                           reply_markup=asosiy_menu)
                    await bot.send_location(chat_id=message.from_user.id, latitude=41.2159400, longitude=69.1895840)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Республика Узбекистан, 111802,\nг. Ташкент, Янгиҳаётcкий р-н,\nУзгариш, ул, Навруз, д. 236а")
                    db.get_ball(str(message.from_user.id), str(data['ball']))
                    await state.finish()

                elif vakansiya[13] == 0:
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Javobingiz va sabringiz uchun rahmat tez orada siz bilan adminlarimiz bog'lanishadi 😊",
                                           reply_markup=asosiy_menu)
                    await bot.send_location(chat_id=message.from_user.id, latitude=41.2159400, longitude=69.1895840)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Республика Узбекистан, 111802,\nг. Ташкент, Янгиҳаётcкий р-н,\nУзгариш, ул, Навруз, д. 236а")
                    db.get_ball(str(message.from_user.id), str(data['ball']))
                    await state.finish()

    except Exception as e:
        await message.answer("Qaytadan uruning !", reply_markup=asosiy_menu)
        await state.finish()


@dp.message_handler(text="Kontakt ☎")
async def kontakt(message: types.Message):
    await message.answer("Bizning Telefon Raqam ☎\n\n+998935472544", reply_markup=websiteuz)


@dp.message_handler(text="Biz haqimizda 🏢")
async def okompany(message: types.Message):
    company = await db.okompaniya()
    if company:
        file_path = f"{BASE}/admin/media/{company[2]}"
        if company[3] == 0:
            await bot.send_video(chat_id=message.from_user.id, video=open(file_path, 'rb'), caption=company[1],
                                 reply_markup=websiteuz)

    else:
        await message.answer("⌛ Malumot yo'q")


@dp.message_handler(text="Taklif va shikoyatlar 🗣")
async def taklif(message: types.Message, state: FSMContext):
    await message.answer("Telefon raqamingizni yuboring ☎", reply_markup=contact_uz)
    await Taklif.telefon.set()


@dp.message_handler(state=Taklif.telefon, content_types=types.ContentTypes.ANY)
async def telefoni(message: types.Message, state: FSMContext):
    try:
        if message.contact:
            async with state.proxy() as data:
                data["taklif_tel"] = message.contact.phone_number

                await message.answer("Taklif yoki Shikoyatingizni yuboring tez orada ko'rib chiqamiz ",
                                     reply_markup=types.ReplyKeyboardRemove())
                await Taklif.about.set()

        elif re.match(r'^\+998[0-9]{9}$', message.text):
            async with state.proxy() as data:
                data["taklif_tel"] = message.text
                await message.answer("Taklif yoki Shikoyatingizni yuboring", reply_markup=types.ReplyKeyboardRemove())
                await state.finish()
        else:
            raise ValueError('ERROR')

    except:
        await message.answer(
            "Iltimos telefon raqam kiriting misol +998991234567 ! yoki Raqam yuborish tugmasini bosing 😊",
            reply_markup=contact_uz)


@dp.message_handler(state=Taklif.about, content_types=types.ContentTypes.TEXT)
async def about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["taklif_about"] = message.text
        about_m = message.text
        telefon = data.get("taklif_tel")

        await message.answer("Xabaringiz uchun rahmat  😊", reply_markup=asosiy_menu)
        await state.finish()

        db.create_shikoyat(str(message.from_user.id), message.from_user.username, telefon, about_m)
