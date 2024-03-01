from aiogram import types
from aiogram.dispatcher.storage import FSMContext
import re
from keyboard.default.menu_keyboard import menu
from keyboard.default.russian import contact_ru, tuman_ru, malumotim_ru, chiqish_ru, vakansiya_ru_button, ishlamoq_ru, \
    javobi_ru
from loader import dp, bot, db, BASE

from aiogram.dispatcher.filters.state import State, StatesGroup


class Russian(StatesGroup):
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


@dp.message_handler(text="Русский язык 🇧🇬")
async def uzbek(message: types.Message):
    vakansiya_button = await vakansiya_ru_button()
    user_id = await db.get_user(str(message.from_user.id))
    if user_id and user_id[-1] == None:
        await message.answer("Вакансии в нашей компании", reply_markup=vakansiya_button)

    elif user_id and user_id[-1]:
        await message.answer("Ваша кандидатура находится на рассмотрении, мы просим вас немного подождать ☺",
                             reply_markup=menu)
    else:
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
            vakansiya_button = await vakansiya_ru_button()
            data['tilbilishi'] = message.text
            await message.answer("Вакансии в нашей компании", reply_markup=vakansiya_button)
            await state.finish()
            phone_number = data['telefon']
            full_name = data['ism']
            birthday = data['sana']
            city = data['tuman']
            information = data['malumoti']
            db.create_user(message.from_user.id, phone_number, full_name, birthday, city, information, message.text)


@dp.message_handler()
async def vakansiya_send_ru(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['vakansiya_name'] = message.text
        vakansiya_name = message.text[:-2]
        vakansiya = await db.get_vakansiyaru(vakansiya_name)
        if vakansiya:
            file_path = f"{BASE}/admin/{vakansiya[3]}"

            await bot.send_photo(message.chat.id, photo=open(file_path, 'rb'), caption=vakansiya[2],
                                 reply_markup=ishlamoq_ru)

            await VakansiyaTest.test1.set()


        else:
            await bot.send_message(message.from_user.id, text="Такой вакансии не нашлось.")


@dp.message_handler(state=VakansiyaTest.test1, content_types=types.ContentTypes.TEXT)
async def vakansiya_test1ru(message: types, state: FSMContext):
    try:
        vakansiya_button = await vakansiya_ru_button()
        if message.text == "Назад 🔙":
            await message.answer(text="Вы на странице вакансии 📝", reply_markup=vakansiya_button)
            await state.finish()

        else:
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya:
                    await message.answer(text="Пожалуйста, отвечайте на вопросы внимательно 😊")
                    await bot.send_message(message.from_user.id, text=f"{vakansiya[6]}", reply_markup=javobi_ru)

                    await VakansiyaTest.javob1.set()


    except:
        await message.answer(text="Ошибка появилась нажмите еще раз !", reply_markup=menu)
        await state.finish()


@dp.message_handler(state=VakansiyaTest.javob1, content_types=types.ContentTypes.TEXT)
async def vakansiya_javobi1(message: types.Message, state: FSMContext):
    try:
        if message.text == "Да":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[7] == 0:
                    data["ball"] = 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi_ru)
                    await VakansiyaTest.test2.set()

                elif vakansiya[7] == 1:
                    data["ball"] = 0
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi_ru)
                    await VakansiyaTest.test2.set()
        elif message.text == "Нет":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[7] == 1:
                    data["ball"] = 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi_ru)
                    await VakansiyaTest.test2.set()

                elif vakansiya[7] == 0:
                    data["ball"] = 0
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[8]}", reply_markup=javobi_ru)
                    await VakansiyaTest.test2.set()
    except Exception as e:
        await message.answer("Ударьте еще раз !", reply_markup=javobi_ru)


@dp.message_handler(state=VakansiyaTest.test2, content_types=types.ContentTypes.TEXT)
async def test2(message: types.Message, state: FSMContext):
    try:
        if message.text == "Да":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[9] == 0:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi_ru)
                    await VakansiyaTest.test3.set()

                elif vakansiya[9] == 1:

                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi_ru)
                    await VakansiyaTest.test3.set()
        elif message.text == "Нет":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[9] == 1:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi_ru)
                    await VakansiyaTest.test3.set()

                elif vakansiya[9] == 0:

                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[10]}", reply_markup=javobi_ru)
                    await VakansiyaTest.test3.set()
    except Exception as e:
        await message.answer("Ударьте еще раз !", reply_markup=javobi_ru)



@dp.message_handler(state=VakansiyaTest.test3, content_types=types.ContentTypes.TEXT)
async def test3(message: types.Message, state: FSMContext):
    try:
        if message.text == "Да":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[11] == 0:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi_ru)
                    await VakansiyaTest.test4.set()

                elif vakansiya[11] == 1:

                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi_ru)
                    await VakansiyaTest.test4.set()
        elif message.text == "Нет":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[11] == 1:
                    data["ball"] += 1
                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi_ru)
                    await VakansiyaTest.test4.set()

                elif vakansiya[11] == 0:

                    await bot.send_message(chat_id=message.chat.id, text=f"{vakansiya[12]}", reply_markup=javobi_ru)
                    await VakansiyaTest.test4.set()
    except Exception as e:
        await message.answer("Ударьте еще раз !", reply_markup=javobi_ru)



@dp.message_handler(state=VakansiyaTest.test4, content_types=types.ContentTypes.TEXT)
async def test4(message: types.Message, state: FSMContext):
    try:
        if message.text == "Да":
            async with state.proxy() as data:
                vakansiya_name = data['vakansiya_name']
                vakansiya = await db.get_vakansiyaru(vakansiya_name[:-2])
                if vakansiya[13] == 0:
                    data["ball"] += 1

                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Спасибо за ответ и терпение скоро с вами свяжутся наши администраторы 😊", reply_markup=menu)

                    db.get_ball(str(message.from_user.id), str(data['ball']))
                    await state.finish()

                elif vakansiya[13] == 1:
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Спасибо за ответ и терпение скоро с вами свяжутся наши администраторы 😊",
                                           reply_markup=menu)
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
                                           reply_markup=menu)
                    db.get_ball(str(message.from_user.id), str(data['ball']))
                    await state.finish()

                elif vakansiya[13] == 0:
                    await bot.send_message(chat_id=message.from_user.id,
                                           text="Спасибо за ответ и терпение скоро с вами свяжутся наши администраторы 😊",
                                           reply_markup=menu)
                    db.get_ball(str(message.from_user.id), str(data['ball']))
                    await state.finish()

    except Exception as e:
        await message.answer("Ударьте еще раз !", reply_markup=javobi_ru)
        await state.finish()