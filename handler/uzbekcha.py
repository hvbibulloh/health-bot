from aiogram import types
from aiogram.dispatcher.storage import FSMContext
import re
from keyboard.default.menu_keyboard import menu, asosiy_menu
from keyboard.default.uzbek import contact_uz, chiqish, tuman, malumotim, vakansiya_uz_button, ishlamoq, javobi
from keyboard.inline.inline_uz import website, websiteuz
from loader import dp, bot, db, BASE

from aiogram.dispatcher.filters.state import State, StatesGroup


class Royxat(StatesGroup):
    telefon = State()
    ism = State()
    sana = State()
    tuman = State()
    malumotim = State()
    tajriba = State()
    til_bilishi = State()
    vakansiya_yubor = State()
    test1 = State()
    javob1 = State()
    test2 = State()
    test3 = State()
    test4 = State()


class Taklif(StatesGroup):
    telefon = State()
    about = State()


@dp.message_handler(text="O'zbek tili 🇺🇿")
async def uzbek_py(message: types.Message):
    await message.answer("Bosh Menyu 🏡", reply_markup=asosiy_menu)


@dp.message_handler(text="Vakansiyalar 💼")
async def uzbek_vakansiya(message: types.Message):
    user_id = await db.get_user(str(message.from_user.id))
    if user_id:
        await message.answer(
            "Siz Vakansiya bo'yicha o'z nomzodingizni qo'yib bo'ldingiz\n3 kundan so'ng sizga yana ro'yxatdan o'tishingizga ruxsat beriladi 😊",
            reply_markup=asosiy_menu)

    else:
        await message.answer("Telefon raqamingizni kiriting ☎", reply_markup=contact_uz)
        await Royxat.telefon.set()


@dp.message_handler(state=Royxat.telefon, content_types=types.ContentTypes.ANY)
async def telefon_py(message: types.Message, state: FSMContext):
    try:
        if message.contact:
            async with state.proxy() as data:
                data["telefon"] = message.contact.phone_number

                await message.answer("Ism va Familiyani kiriting 📝", reply_markup=types.ReplyKeyboardRemove())
                await Royxat.ism.set()


        elif re.match(r"^\+998[0-9]{9}$", message.text):
            async with state.proxy() as data:
                data["telefon"] = message.text
                await message.answer("Ism va Familiyani kiriting 📝", reply_markup=types.ReplyKeyboardRemove())
                await Royxat.ism.set()

        else:
            raise ValueError("Error")


    except:
        await message.answer(
            "Iltimos telefon raqam kiriting misol +998991234567 ! yoki Raqam yuborish tugmasini bosing 😊",
            reply_markup=contact_uz)


@dp.message_handler(state=Royxat.ism, content_types=types.ContentTypes.TEXT)
async def ism_py(message: types.Message, state: FSMContext):
    try:
        if message.text.isalpha():
            async with state.proxy() as data:
                data["ism"] = message.text
            await message.answer("Tug'ulgan sanangizni kiriting 📅 01.01,1990")
            await Royxat.sana.set()
        else:
            raise ValueError("Ism harflardan iborat bo'ladi!")
    except ValueError as ve:
        await message.answer(str(ve))
    except Exception as e:
        await message.answer("Ism yuborishda hatolik bor qayta yuboring !")


@dp.message_handler(state=Royxat.sana, content_types=types.ContentTypes.TEXT)
async def sana_py(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["sana"] = message.text
        await message.answer("Qaysi tumanda istiqomat qilasiz ? ", reply_markup=tuman)
        await Royxat.tuman.set()
    except Exception as e:
        await message.answer(f" Sana yuborishda hatolik bor qayta yuboring !")


@dp.message_handler(state=Royxat.tuman, content_types=types.ContentTypes.TEXT)
async def tumani_py(message: types.Message, state: FSMContext):
    if message.text:
        async with state.proxy() as data:
            data['tuman'] = message.text
            await message.answer("Ma'lumotingizni kiriting yoki o'zingiz yozishingiz ham mumkin ",
                                 reply_markup=malumotim)
            await Royxat.malumotim.set()

    else:
        await message.answer("To'g'ri kiriting iltimos !")


@dp.message_handler(state=Royxat.malumotim, content_types=types.ContentTypes.TEXT)
async def malumoti_py(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['malumoti'] = message.text
            await message.answer(
                "Sizning ish tajribangiz qanday? ----\n- kompaniya\n- lavozim\n- ish davri\nMisol: 'Dream Work' MCHJ, kassir, 2015-2018.",
                reply_markup=types.ReplyKeyboardRemove())
            await Royxat.tajriba.set()

    except Exception as e:
        print(f"Exception while {e}")


@dp.message_handler(state=Royxat.tajriba, content_types=types.ContentTypes.TEXT)
async def tajriba_py(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tajriba'] = message.text
        await message.answer("Qaysi tillarni bilasiz? \n\nO'zbek, Rus, Ingliz \n\nshu variantda yozing ✍",
                             reply_markup=types.ReplyKeyboardRemove())
        await Royxat.til_bilishi.set()


@dp.message_handler(state=Royxat.til_bilishi, content_types=types.ContentTypes.TEXT)
async def til_bilishi_py(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['til_bilishi'] = message.text
        phone_number = data['telefon']
        full_name = data['ism']
        birthday = data['sana']
        city = data['tuman']
        information = data['malumoti']
        tajriba = data['tajriba']
        vakansiya_button = await vakansiya_uz_button()
        user = await db.get_user(str(message.from_user.id))
        if user:
            await message.answer("Kompaniyamizning bo'sh ish o'rinlari ", reply_markup=vakansiya_button)

        else:
            try:
                db.create_user(telegram_id=str(message.from_user.id), phone_number=phone_number, full_name=full_name,
                               date_of_birth=birthday, city=city, information=information, languages=message.text,
                               tajriba=tajriba)
                await message.answer("Kompaniyamizning bo'sh ish o'rinlari", reply_markup=vakansiya_button)
                await Royxat.vakansiya_yubor.set()
            except:
                await message.answer("Xatolik", reply_markup=asosiy_menu)
                await state.finish()


@dp.message_handler(state=Royxat.vakansiya_yubor, content_types=types.ContentTypes.TEXT)
async def vakansiya_yuborishm(message: types.Message, state: FSMContext):
    try:
        if message.text == "Chiqish":
            await message.answer("Asosiy Menu", reply_markup=asosiy_menu)
            await state.finish()

        else:
            async with state.proxy() as data:
                data['vakansiya_name'] = message.text
                vakansiya_names = message.text[:-2]
                vakansiya = await db.get_vakansiya(vakansiya_names)
                if vakansiya:
                    file_path = f"{BASE}/admin/media/{vakansiya[3]}"

                    caption = vakansiya[2] if vakansiya[2] else None

                    await message.answer_photo(photo=open(file_path, 'rb'), caption=caption, reply_markup=ishlamoq)
                    await Royxat.test1.set()

                else:
                    await message.answer("Bunday vakansiya topilmadi")

    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: {e}")


@dp.message_handler(state=Royxat.test1, content_types=types.ContentTypes.TEXT)
async def test1_py(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        vakansiya_name = data['vakansiya_name']
        vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
        if vakansiya:
            data['savol1'] = vakansiya[6]
            await message.answer(f"{vakansiya[6]}", reply_markup=javobi)

            await Royxat.javob1.set()


@dp.message_handler(state=Royxat.javob1, content_types=types.ContentTypes.TEXT)
async def javob1_py(message: types.Message, state: FSMContext):
    try:
        if message.text == "Ha":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                data['savol2'] = vakansiya[8]
                if vakansiya[7] == 0:
                    data["javobi1"] = 1

                    await message.answer(f"{vakansiya[8]}", reply_markup=javobi)
                    await Royxat.test2.set()

                elif vakansiya[7] == 1:
                    data["javobi1"] = 0
                    await message.answer(f"{vakansiya[8]}", reply_markup=javobi)
                    await Royxat.test2.set()

        elif message.text == "Yo'q":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                data['savol2'] = vakansiya[8]
                if vakansiya[7] == 1:
                    data["javobi1"] = 1
                    await message.answer(f"{vakansiya[8]}", reply_markup=javobi)
                    await Royxat.test2.set()

                elif vakansiya[7] == 0:
                    data["javobi1"] = 0
                    await message.answer(f"{vakansiya[8]}", reply_markup=javobi)
                    await Royxat.test2.set()


    except Exception as e:
        await message.answer("Qaytadan uruning !", reply_markup=javobi)


@dp.message_handler(state=Royxat.test2, content_types=types.ContentTypes.TEXT)
async def test2_py(message: types.Message, state: FSMContext):
    try:
        if message.text == "Ha":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                data['savol3'] = vakansiya[10]
                if vakansiya[9] == 0:
                    data['javobi2'] = 1

                    await message.answer(f"{vakansiya[10]}", reply_markup=javobi)
                    await Royxat.test3.set()

                elif vakansiya[9] == 1:
                    data['javobi2'] = 0
                    await message.answer(f"{vakansiya[10]}", reply_markup=javobi)
                    await Royxat.test3.set()

        elif message.text == "Yo'q":
            async with state.proxy() as data:

                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                data['savol3'] = vakansiya[10]
                if vakansiya[9] == 1:
                    data['javobi2'] = 1
                    await message.answer(f"{vakansiya[10]}", reply_markup=javobi)
                    await Royxat.test3.set()

                elif vakansiya[9] == 0:
                    data['javobi2'] = 0
                    await message.answer(f"{vakansiya[10]}", reply_markup=javobi)
                    await Royxat.test3.set()

    except Exception as e:
        await message.answer("Qaytadan uruning !", reply_markup=javobi)


@dp.message_handler(state=Royxat.test3, content_types=types.ContentTypes.TEXT)
async def test3_py(message: types.Message, state: FSMContext):
    try:
        if message.text == "Ha":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                data['savol4'] = vakansiya[12]
                if vakansiya[11] == 0:
                    data['javobi3'] = 1
                    await message.answer(f"{vakansiya[12]}", reply_markup=javobi)
                    await Royxat.test4.set()

                elif vakansiya[11] == 1:
                    data['javobi3'] = 0
                    await message.answer(f"{vakansiya[12]}", reply_markup=javobi)
                    await Royxat.test4.set()

        elif message.text == "Yo'q":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])
                data['savol4'] = vakansiya[12]
                if vakansiya[11] == 1:
                    data['javobi3'] = 1

                    await message.answer(f"{vakansiya[12]}", reply_markup=javobi)
                    await Royxat.test4.set()

                elif vakansiya[11] == 0:
                    data['javobi3'] = 0
                    await message.answer(f"{vakansiya[12]}", reply_markup=javobi)
                    await Royxat.test4.set()
    except Exception as e:
        await message.answer("Qaytadan uruning !", reply_markup=javobi)


@dp.message_handler(state=Royxat.test4, content_types=types.ContentTypes.TEXT)
async def test4py(message: types.Message, state: FSMContext):
    try:
        if message.text == "Ha" or message.text == "Yo'q":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiya(vakansiya_name[:-2])

                correct_answer = 1 if message.text == "Ha" else 0

                if vakansiya[13] == correct_answer:
                    data['javobi4'] = 0
                else:
                    data['javobi4'] = 1
                await message.answer(
                    f"Javobingiz va sabringiz uchun rahmat tez orada siz bilan adminlarimiz bog'lanishadi 😊",
                    reply_markup=asosiy_menu)
                await state.finish()
                await message.answer_location(latitude=41.2159400, longitude=69.1895840)
                await message.answer(
                    "Республика Узбекистан, 111802,\nг. Ташкент, Янгиҳаётcкий р-н,\nУзгариш, ул, Навруз, д. 236а")

                text = f"Vakansiya: {data['vakansiya_name']} \n1 - Savol {data['savol1']} - {data['javobi1']}\n2 - Savol {data['savol2']} - {data['javobi2']}\n3 - Savol {data['savol3']} - {data['javobi3']}\n4 - Savol {data['savol4']} - {data['javobi4']}"
                db.get_ball(str(message.chat.id), str(text))


        else:
            await message.answer("Qaytadan uruning !", reply_markup=asosiy_menu)
            await state.finish()

    except Exception as e:
        await message.answer(f"{e} Qaytadan uruning !", reply_markup=asosiy_menu)
        await state.finish()


@dp.message_handler(text="Kontakt ☎")
async def kontakt_py(message: types.Message):
    await message.answer("Bizning Telefon Raqam ☎\n\n+998935472544", reply_markup=websiteuz)


@dp.message_handler(text="Biz haqimizda 🏢")
async def okompany(message: types.Message):
    company = await db.okompaniya()
    if company:
        file_path = f"{BASE}/admin/media/{company[2]}"

        await message.answer_photo(photo=open(file_path, 'rb'),caption=company[1], reply_markup=websiteuz)

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


