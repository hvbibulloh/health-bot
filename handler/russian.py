from aiogram import types
from aiogram.dispatcher.storage import FSMContext
import re
from keyboard.default.menu_keyboard import asosiy_menu_ru, menu
from keyboard.default.russian import contact_ru, tuman_ru, malumotim_ru, chiqish_ru, vakansiya_ru_button, ishlamoq_ru, \
    javobi_ru
from keyboard.inline.inline_uz import website
from loader import dp, bot, db, BASE

from aiogram.dispatcher.filters.state import State, StatesGroup


class Russian(StatesGroup):
    telefon = State()


class KondidantRu(StatesGroup):
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


class TaklifRu(StatesGroup):
    telefon = State()
    about = State()


@dp.message_handler(text="Русский язык 🇧🇬")
async def uzbek(message: types.Message):
    vakansiya_button = await vakansiya_ru_button()
    user_id = await db.get_user(str(message.from_user.id))
    if user_id:
        await message.answer("Вакансии в нашей компании", reply_markup=asosiy_menu_ru)

    else:
        await message.answer("Пожалуйста, введите свой номер телефона ☎", reply_markup=contact_ru)
        await Russian.telefon.set()


@dp.message_handler(state=Russian.telefon, content_types=types.ContentTypes.ANY)
async def telefoni(message: types.Message, state: FSMContext):
    try:
        if message.contact:
            async with state.proxy() as data:
                data["telefon"] = message.contact.phone_number

                await message.answer('Выберите нужный раздел 🛎', reply_markup=asosiy_menu_ru)
                await state.finish()


        elif re.match(r'^\+998[0-9]{9}$', message.text):
            async with state.proxy() as data:
                data["telefon"] = message.text
                await message.answer('Выберите нужный раздел 🛎', reply_markup=asosiy_menu_ru)
                await state.finish()

        else:
            raise ValueError('ERROR')

    except:
        await message.answer(
            "Пожалуйста, введите номер телефона пример +998991234567 ! или нажмите кнопку отправить номер 😊",
            reply_markup=contact_ru)


@dp.message_handler(text="Вакансии 💼")
async def menuse_ru(message: types.Message, state: FSMContext):
    vakansiya_button = await vakansiya_ru_button()
    user_id = await db.get_user(str(message.from_user.id))
    if user_id:
        await message.answer(
            "Вы закончили выдвигать свою кандидатуру на вакансию,\n вы можете снова выдвинуть свою кандидатуру через 3 дня",
            reply_markup=asosiy_menu_ru)

    else:
        await bot.send_message(chat_id=message.from_user.id, text="Введите свой номер телефона 📝",
                               reply_markup=contact_ru)

        await KondidantRu.telefon.set()



@dp.message_handler(state=KondidantRu.telefon, content_types=types.ContentTypes.ANY)
async def telefoni(message: types.Message, state: FSMContext):
    try:
        if message.contact:
            async with state.proxy() as data:
                data["telefon"] = message.contact.phone_number

                await message.answer('Введите свое имя и фамилию 📝', reply_markup=types.ReplyKeyboardRemove())
                await KondidantRu.ism.set()


        elif re.match(r'^\+998[0-9]{9}$', message.text):
            async with state.proxy() as data:
                data["telefon"] = message.text
                await message.answer('Введите свое имя и фамилию 📝', reply_markup=types.ReplyKeyboardRemove())
                await KondidantRu.ism.set()

        else:
            raise ValueError('ERROR')

    except:
        await message.answer(
            "Пожалуйста, введите номер телефона пример +998991234567 ! или нажмите кнопку отправить номер 😊",
            reply_markup=contact_ru)


@dp.message_handler(state=KondidantRu.ism, content_types=types.ContentTypes.TEXT)
async def kondidant_ismi(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['ism'] = message.text
        await message.answer("Введите дату своего рождения 📅 01.01.1990")
        await KondidantRu.sana.set()


@dp.message_handler(state=KondidantRu.sana, content_types=types.ContentTypes.TEXT)
async def kondidant_sana(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['sana'] = message.text
        await message.answer("Qaysi tumanda istiqomat qilasiz? 🏠", reply_markup=tuman_ru)
        await KondidantRu.tumani.set()


@dp.message_handler(state=KondidantRu.tumani, content_types=types.ContentTypes.TEXT)
async def kondidant_tumana(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tuman'] = message.text
        await message.answer("Ma'lumotingizni kiriting yoki o'zingiz yozishingiz ham mumkin", reply_markup=malumotim_ru)
        await KondidantRu.malumoti.set()


@dp.message_handler(state=KondidantRu.malumoti, content_types=types.ContentTypes.TEXT)
async def kondidant_malumoti(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['malumoti'] = message.text
        await message.answer(
            "Какой у Вас опыт работы? ----\n- компания\n- должность\n- период работы\nПример: ООО 'Работа мечты', Кассир, 2015-2018.",
            reply_markup=types.ReplyKeyboardRemove())
        await KondidantRu.tajriba.set()


@dp.message_handler(state=KondidantRu.tajriba, content_types=types.ContentTypes.TEXT)
async def kondidant_tajriba(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['tajriba'] = message.text
        await message.answer("Какие языки вы знаете? \n\nУзбекский, Русский, Английский \n\nв этом варианте напишите ✍",
                             reply_markup=types.ReplyKeyboardRemove())
        await KondidantRu.til_bilishi.set()


@dp.message_handler(state=KondidantRu.til_bilishi, content_types=types.ContentTypes.TEXT)
async def kondidant_til_bilishi(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        vakansiya_button = await vakansiya_ru_button()
        data['tilbilishi'] = message.text
        phone_number = data['telefon']
        full_name = data['ism']
        birthday = data['sana']
        city = data['tuman']
        information = data['malumoti']
        tajriba = data['tajriba']
        db.create_user(message.from_user.id, phone_number, full_name, birthday, city, information, message.text,
                       tajriba)

        await KondidantRu.vakansiya_send.set()

        await message.answer("Вакансии в нашей компании", reply_markup=vakansiya_button)


@dp.message_handler(state=KondidantRu.vakansiya_send, content_types=types.ContentTypes.TEXT)
async def vakansiya_sende(message: types.Message, state: FSMContext):
    if message.text == "Выход":
        await message.answer("Главное Меню", reply_markup=asosiy_menu_ru)
        await state.finish()

    else:
        async with state.proxy() as data:
            data['vakansiya_name'] = message.text
            vakansiya_name = message.text[:-2]
            vakansiya = await db.get_vakansiyaru(vakansiya_name)
            if vakansiya:
                file_path = f"{BASE}/admin/media/{vakansiya[3]}"

                await bot.send_photo(message.chat.id, photo=open(file_path, 'rb'), caption=vakansiya[2],
                                     reply_markup=ishlamoq_ru)

                await KondidantRu.test1.set()


            else:
                await bot.send_message(message.from_user.id, text="Такой вакансии не нашлось.")


@dp.message_handler(state=KondidantRu.test1, content_types=types.ContentTypes.TEXT)
async def vakansiya_test1(message: types, state: FSMContext):
    try:
        vakansiya_button = await vakansiya_ru_button()
        if message.text == "Назад 🔙":
            await message.answer(text="Вы на странице вакансии 📝", reply_markup=vakansiya_button)
            await KondidantRu.vakansiya_send.set()

        else:
            async with state.proxy() as data:
                vakansiya_name = data["vakansiya_name"]
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya:
                    await message.answer(text="Пожалуйста, отвечайте на вопросы внимательно 😊")
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[6]}", reply_markup=javobi_ru)

                    await KondidantRu.javob1.set()


    except:
        await message.answer(
            "Ошибка появилась нажмите еще раз !",
            reply_markup=menu)
        await state.finish()


@dp.message_handler(state=KondidantRu.javob1, content_types=types.ContentTypes.TEXT)
async def vakansiya_javobi1(message: types.Message, state: FSMContext):
    try:
        if message.text == "Да":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[7] == 0:
                    data["ball"] = 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi_ru)
                    await KondidantRu.test2.set()

                elif vakansiya[7] == 1:
                    data["ball"] = 0
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi_ru)
                    await KondidantRu.test2.set()

        elif message.text == "Нет":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[7] == 1:
                    data["ball"] = 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi_ru)
                    await KondidantRu.test2.set()

                elif vakansiya[7] == 0:
                    data["ball"] = 0
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi_ru)
                    await KondidantRu.test2.set()

    except Exception as e:
        await message.answer("Нажмите еще раз !", reply_markup=javobi_ru)


@dp.message_handler(state=KondidantRu.test2, content_types=types.ContentTypes.TEXT)
async def test2(message: types.Message, state: FSMContext):
    try:
        if message.text == "Да":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[9] == 0:
                    data["ball"] += 1

                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi_ru)
                    await KondidantRu.test3.set()

                elif vakansiya[9] == 1:

                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi_ru)
                    await KondidantRu.test3.set()

        elif message.text == "Нет":
            async with state.proxy() as data:

                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[9] == 1:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi_ru)
                    await KondidantRu.test3.set()

                elif vakansiya[9] == 0:
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi_ru)
                    await KondidantRu.test3.set()

    except Exception as e:
        await message.answer("Нажмите еще раз !", reply_markup=javobi_ru)


@dp.message_handler(state=KondidantRu.test3, content_types=types.ContentTypes.TEXT)
async def test3(message: types.Message, state: FSMContext):
    try:
        if message.text == "Да":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[11] == 0:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi_ru)
                    await KondidantRu.test4.set()

                elif vakansiya[11] == 1:
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi_ru)
                    await KondidantRu.test4.set()

        elif message.text == "Нет":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[11] == 1:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi_ru)
                    await KondidantRu.test4.set()

                elif vakansiya[11] == 0:
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi_ru)
                    await KondidantRu.test4.set()

    except Exception as e:
        await message.answer("Нажмите еще раз !", reply_markup=javobi_ru)


@dp.message_handler(state=KondidantRu.test4, content_types=types.ContentTypes.TEXT)
async def test4(message: types.Message, state: FSMContext):
    try:
        if message.text == "Да":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[13] == 0:
                    data["ball"] += 1

                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Спасибо за ответ и терпение скоро с вами свяжутся наши администраторы 😊",
                                           reply_markup=asosiy_menu_ru)
                    await bot.send_location(chat_id=message.from_user.id, latitude=41.2159400, longitude=69.1895840)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Республика Узбекистан, 111802,\nг. Ташкент, Янгиҳаётcкий р-н,\nУзгариш, ул, Навруз, д. 236а")
                    db.get_ball(str(message.from_user.id), str(data['ball']))
                    await state.finish()

                elif vakansiya[13] == 1:

                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Спасибо за ответ и терпение скоро с вами свяжутся наши администраторыi 😊",
                                           reply_markup=asosiy_menu_ru)
                    await bot.send_location(chat_id=message.from_user.id, latitude=41.2159400, longitude=69.1895840)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Республика Узбекистан, 111802,\nг. Ташкент, Янгиҳаётcкий р-н,\nУзгариш, ул, Навруз, д. 236а")
                    db.get_ball(str(message.from_user.id), str(data['ball']))
                    await state.finish()
        elif message.text == "Нет":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[13] == 1:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Спасибо за ответ и терпение скоро с вами свяжутся наши администраторы 😊",
                                           reply_markup=asosiy_menu_ru)
                    await bot.send_location(chat_id=message.from_user.id, latitude=41.2159400, longitude=69.1895840)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Республика Узбекистан, 111802,\nг. Ташкент, Янгиҳаётcкий р-н,\nУзгариш, ул, Навруз, д. 236а")
                    db.get_ball(str(message.from_user.id), str(data['ball']))
                    await state.finish()

                elif vakansiya[13] == 0:
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Спасибо за ответ и терпение скоро с вами свяжутся наши администраторы 😊",
                                           reply_markup=asosiy_menu_ru)
                    await bot.send_location(chat_id=message.from_user.id, latitude=41.2159400, longitude=69.1895840)
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Республика Узбекистан, 111802,\nг. Ташкент, Янгиҳаётcкий р-н,\nУзгариш, ул, Навруз, д. 236а")
                    db.get_ball(str(message.from_user.id), str(data['ball']))
                    await state.finish()

    except Exception as e:
        await message.answer("Нажмите еще раз !", reply_markup=asosiy_menu_ru)
        await state.finish()


@dp.message_handler(text="Контакт ☎")
async def kontakt(message: types.Message):
    await message.answer("Наш Номер Телефона ☎\n\n+998935472544", reply_markup=website)


@dp.message_handler(text="О нас 🏢")
async def okompany(message: types.Message):
    company = await db.okompaniyaru()
    if company:
        file_path = f"{BASE}/admin/media/{company[2]}"
        if company[3] == 0:
            await bot.send_video(chat_id=message.from_user.id, video=open(file_path, 'rb'), caption=company[1],
                                 reply_markup=website)

    else:
        await message.answer("⌛ Нет ссылки ")


@dp.message_handler(text="Предложения и жалобы 🗣")
async def taklif(message: types.Message, state: FSMContext):
    await message.answer("Отправить свой номер телефона ☎", reply_markup=contact_ru)
    await TaklifRu.telefon.set()


@dp.message_handler(state=TaklifRu.telefon, content_types=types.ContentTypes.ANY)
async def telefoni(message: types.Message, state: FSMContext):
    try:
        if message.contact:
            async with state.proxy() as data:
                data["taklif_tel"] = message.contact.phone_number

                await message.answer("Отправьте свое предложение или жалобу на скоро рассмотрение ",
                                     reply_markup=types.ReplyKeyboardRemove())
                await TaklifRu.about.set()

        elif re.match(r'^\+998[0-9]{9}$', message.text):
            async with state.proxy() as data:
                data["taklif_tel"] = message.text
                await message.answer("Отправьте свое предложение или жалобу", reply_markup=types.ReplyKeyboardRemove())
                await state.finish()
        else:
            raise ValueError('ERROR')

    except:
        await message.answer(
            "Пожалуйста, введите номер телефона пример +998991234567 ! или нажмите кнопку отправить номер 😊",
            reply_markup=contact_ru)


@dp.message_handler(state=TaklifRu.about, content_types=types.ContentTypes.TEXT)
async def about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["taklif_about"] = message.text
        about_m = message.text
        telefon = data.get("taklif_tel")

        await message.answer("Спасибо за ваше сообщение  😊", reply_markup=asosiy_menu_ru)
        await state.finish()

        db.create_shikoyat(str(message.from_user.id), message.from_user.username, telefon, about_m)
