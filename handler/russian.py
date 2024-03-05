from aiogram import types
from aiogram.dispatcher.storage import FSMContext
import re
from keyboard.default.menu_keyboard import asosiy_menu_ru, menu
from keyboard.default.russian import contact_ru, tuman_ru, malumotim_ru, chiqish_ru, vakansiya_ru_button, ishlamoq_ru, \
    javobi_ru
from keyboard.inline.inline_uz import website
from loader import dp, bot, db, BASE

from aiogram.dispatcher.filters.state import State, StatesGroup


class Registration(StatesGroup):
    phone = State()
    name = State()
    birth_date = State()
    region = State()
    information = State()
    experience = State()
    language_proficiency = State()
    send_resume = State()
    question1 = State()
    answer1 = State()
    question2 = State()
    question3 = State()
    question4 = State()


class Feedback(StatesGroup):
    phone = State()
    about = State()


@dp.message_handler(text="Русский язык 🇧🇬")
async def russian_start(message: types.Message):
    await message.answer("Главное меню 🏡", reply_markup=asosiy_menu_ru)


@dp.message_handler(text="Вакансии 💼")
async def russian_vacancy(message: types.Message):
    user_id = await db.get_user(str(message.from_user.id))
    if user_id:
        await message.answer(
            "Вы уже зарегистрировали свои данные по вакансии\nЧерез 3 дня вам будет предоставлена возможность повторной регистрации 😊",
            reply_markup=asosiy_menu_ru)

    else:
        await message.answer("Введите ваш номер телефона ☎", reply_markup=contact_ru)
        await Registration.phone.set()


@dp.message_handler(state=Registration.phone, content_types=types.ContentTypes.ANY)
async def russian_phone(message: types.Message, state: FSMContext):
    try:
        if message.contact:
            async with state.proxy() as data:
                data["phone"] = message.contact.phone_number

                await message.answer("Введите ваше имя и фамилию 📝", reply_markup=types.ReplyKeyboardRemove())
                await Registration.name.set()

        elif re.match(r"^\+998[0-9]{9}$", message.text):
            async with state.proxy() as data:
                data["phone"] = message.text
                await message.answer("Введите ваше имя и фамилию 📝", reply_markup=types.ReplyKeyboardRemove())
                await Registration.name.set()

        else:
            raise ValueError("Ошибка")

    except:
        await message.answer(
            "Пожалуйста, введите номер телефона, например +998991234567! или нажмите кнопку Отправить номер 😊",
            reply_markup=contact_ru)


@dp.message_handler(state=Registration.name, content_types=types.ContentTypes.TEXT)
async def russian_name(message: types.Message, state: FSMContext):
    try:
        if message.text.isalpha():
            async with state.proxy() as data:
                data["name"] = message.text
            await message.answer("Введите дату вашего рождения 📅 Например, 01.01.1990")
            await Registration.birth_date.set()
        else:
            raise ValueError("Имя должно содержать только буквы!")
    except ValueError as ve:
        await message.answer(str(ve))
    except Exception as e:
        await message.answer("Произошла ошибка при отправке имени! Пожалуйста, отправьте еще раз.")


@dp.message_handler(state=Registration.birth_date, content_types=types.ContentTypes.TEXT)
async def russian_birth_date(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data["birth_date"] = message.text
        await message.answer("В каком регионе вы планируете работать? ", reply_markup=tuman_ru)
        await Registration.region.set()
    except Exception as e:
        await message.answer(f" Произошла ошибка при отправке даты рождения! Пожалуйста, отправьте еще раз.")


@dp.message_handler(state=Registration.region, content_types=types.ContentTypes.TEXT)
async def russian_region(message: types.Message, state: FSMContext):
    if message.text:
        async with state.proxy() as data:
            data['region'] = message.text
            await message.answer("Введите свою информацию или напишите ее сами ",
                                 reply_markup=malumotim_ru)
            await Registration.information.set()

    else:
        await message.answer("Введите правильно, пожалуйста!")


@dp.message_handler(state=Registration.information, content_types=types.ContentTypes.TEXT)
async def russian_information(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['information'] = message.text
            await message.answer(
                "Какой у вас опыт работы? ----\n- компания\n- должность\n- срок службы\nПример: 'Dream Work' MCHJ, кассир, 2015-2018.",
                reply_markup=types.ReplyKeyboardRemove())
            await Registration.experience.set()

    except Exception as e:
        print(f" Исключение при {e}")


@dp.message_handler(state=Registration.experience, content_types=types.ContentTypes.TEXT)
async def russian_experience(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['experience'] = message.text
        await message.answer("Какие языки вы знаете? \n\nУзбекский, Русский, Английский \n\nнапишите в этом формате ✍",
                             reply_markup=types.ReplyKeyboardRemove())
        await Registration.language_proficiency.set()


@dp.message_handler(state=Registration.language_proficiency, content_types=types.ContentTypes.TEXT)
async def russian_language_proficiency(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['language_proficiency'] = message.text
        phone_number = data['phone']
        full_name = data['name']
        birthday = data['birth_date']
        city = data['region']
        information = data['information']
        experience = data['experience']
        language_proficiency = data['language_proficiency']
        vacancy_button = await vakansiya_ru_button()
        user = await db.get_user(str(message.from_user.id))
        if user:
            await message.answer("Свободные рабочие места в нашей компании ", reply_markup=vacancy_button)

        else:
            try:
                db.create_user(telegram_id=str(message.from_user.id), phone_number=phone_number, full_name=full_name,
                               date_of_birth=birthday, city=city, information=information, languages=message.text,
                               tajriba=experience)
                await message.answer("Свободные рабочие места в нашей компании", reply_markup=vacancy_button)
                await Registration.send_resume.set()
            except:
                await message.answer("Ошибка", reply_markup=asosiy_menu_ru)
                await state.finish()


@dp.message_handler(state=Registration.send_resume, content_types=types.ContentTypes.TEXT)
async def russian_send_resume(message: types.Message, state: FSMContext):
    try:
        if message.text == "Выход":
            await message.answer("Главное меню", reply_markup=asosiy_menu_ru)
            await state.finish()

        else:
            async with state.proxy() as data:
                data['resume_name'] = message.text
                resume_names = message.text[:-2]
                resume = await db.get_vakansiyaru(resume_names)
                if resume:
                    file_path = f"{BASE}/admin/media/{resume[3]}"

                    caption = resume[2] if resume[2] else None

                    await message.answer_photo(photo=open(file_path, 'rb'), caption=caption, reply_markup=ishlamoq_ru)
                    await Registration.question1.set()

                else:
                    await message.answer("Такого резюме не найдено")

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")


@dp.message_handler(state=Registration.question1, content_types=types.ContentTypes.TEXT)
async def russian_question1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        resume_name = data['resume_name']
        resume = await db.get_vakansiyaru(resume_name[:-2])
        if resume:
            data['question1'] = resume[6]
            await message.answer(f"{resume[6]}", reply_markup=javobi_ru)

            await Registration.answer1.set()


@dp.message_handler(state=Registration.answer1, content_types=types.ContentTypes.TEXT)
async def russian_answer1(message: types.Message, state: FSMContext):
    try:
        if message.text == "Да":
            async with state.proxy() as data:
                resume_name = data['resume_name']
                resume = await db.get_vakansiyaru(resume_name[:-2])
                data['question2'] = resume[8]
                if resume[7] == 0:
                    data["answer1"] = 1

                    await message.answer(f"{resume[8]}", reply_markup=javobi_ru)
                    await Registration.question2.set()

                elif resume[7] == 1:
                    data["answer1"] = 0
                    await message.answer(f"{resume[8]}", reply_markup=javobi_ru)
                    await Registration.question2.set()

        elif message.text == "Нет":
            async with state.proxy() as data:
                resume_name = data['resume_name']
                resume = await db.get_vakansiyaru(resume_name[:-2])
                data['question2'] = resume[8]
                if resume[7] == 1:
                    data["answer1"] = 1
                    await message.answer(f"{resume[8]}", reply_markup=javobi_ru)
                    await Registration.question2.set()

                elif resume[7] == 0:
                    data["answer1"] = 0
                    await message.answer(f"{resume[8]}", reply_markup=javobi_ru)
                    await Registration.question2.set()

    except Exception as e:
        await message.answer("Повторите запрос!", reply_markup=javobi_ru)


@dp.message_handler(state=Registration.question2, content_types=types.ContentTypes.TEXT)
async def russian_question2(message: types.Message, state: FSMContext):
    try:
        if message.text == "Да":
            async with state.proxy() as data:
                resume_name = data['resume_name']
                resume = await db.get_vakansiyaru(resume_name[:-2])
                data['question3'] = resume[10]
                if resume[9] == 0:
                    data["answer2"] = 1

                    await message.answer(f"{resume[10]}", reply_markup=javobi_ru)
                    await Registration.question3.set()

                elif resume[9] == 1:
                    data["answer2"] = 0
                    await message.answer(f"{resume[10]}", reply_markup=javobi_ru)
                    await Registration.question3.set()

        elif message.text == "Нет":
            async with state.proxy() as data:
                resume_name = data['resume_name']
                resume = await db.get_vakansiyaru(resume_name[:-2])
                data['question3'] = resume[10]
                if resume[9] == 1:
                    data["answer2"] = 1
                    await message.answer(f"{resume[10]}", reply_markup=javobi_ru)
                    await Registration.question3.set()

                elif resume[9] == 0:
                    data["answer2"] = 0
                    await message.answer(f"{resume[10]}", reply_markup=javobi_ru)
                    await Registration.question3.set()

    except Exception as e:
        await message.answer("Повторите запрос!", reply_markup=javobi_ru)

@dp.message_handler(state=Registration.question3, content_types=types.ContentTypes.TEXT)
async def russian_question3(message: types.Message, state: FSMContext):
    try:
        if message.text == "Да":
            async with state.proxy() as data:
                resume_name = data['resume_name']
                resume = await db.get_vakansiyaru(resume_name[:-2])
                data['question4'] = resume[12]
                if resume[11] == 0:
                    data["answer3"] = 1

                    await message.answer(f"{resume[12]}", reply_markup=javobi_ru)
                    await Registration.question4.set()

                elif resume[11] == 1:
                    data["answer3"] = 0
                    await message.answer(f"{resume[12]}", reply_markup=javobi_ru)
                    await Registration.question4.set()

        elif message.text == "Нет":
            async with state.proxy() as data:
                resume_name = data['resume_name']
                resume = await db.get_vakansiyaru(resume_name[:-2])
                data['question4'] = resume[12]
                if resume[11] == 1:
                    data["answer3"] = 1
                    await message.answer(f"{resume[12]}", reply_markup=javobi_ru)
                    await Registration.question4.set()

                elif resume[11] == 0:
                    data["answer3"] = 0
                    await message.answer(f"{resume[12]}", reply_markup=javobi_ru)
                    await Registration.question4.set()

    except Exception as e:
        await message.answer("Повторите запрос!", reply_markup=javobi_ru)


@dp.message_handler(state=Registration.question4, content_types=types.ContentTypes.TEXT)
async def russian_question4(message: types.Message, state: FSMContext):
    try:
        if message.text == "Да" or message.text == "Нет":
            async with state.proxy() as data:
                resume_name = data['resume_name']
                resume = await db.get_vakansiyaru(resume_name[:-2])

                correct_answer = 1 if message.text == "Да" else 0

                if resume[13] == correct_answer:
                    data['answer4'] = 0
                else:
                    data['answer4'] = 1
                await message.answer(
                    f"За ваш ответ и терпение вас свяжутся с нашими администраторами в ближайшее время 😊",
                    reply_markup=javobi_ru)
                await state.finish()
                await message.answer_location(latitude=41.2159400, longitude=69.1895840)
                await message.answer(
                    "Республика Узбекистан, 111802,\nг. Ташкент, Янгиҳаётcкий р-н,\nУзгариш, ул, Навруз, д. 236а")

                text = f"Vakansiya: {data['resume_name']} \n1 - Savol {data['question1']} - {data['answer1']}\n2 - Savol {data['answer4']} - {data['answer2']}\n3 - Savol {data['question3']} - {data['answer3']}\n4 - Savol {data['question4']} - {data['answer4']}"
                db.get_ball(str(message.chat.id), str(text))

        else:
            await message.answer("Нажмите еще раз !", reply_markup=asosiy_menu_ru)
            await state.finish()

    except Exception as e:
        await message.answer(f"{e} Нажмите еще раз !", reply_markup=asosiy_menu_ru)
        await state.finish()



@dp.message_handler(text="Контакт ☎")
async def kontakt(message: types.Message):
    await message.answer("Наш Номер Телефона ☎\n\n+998935472544", reply_markup=website)


@dp.message_handler(text="О нас 🏢")
async def okompany(message: types.Message):
    company = await db.okompaniyaru()
    if company:
        file_path = f"{BASE}/admin/media/{company[2]}"
        print(file_path)
        if company[3] == 0:
            await message.answer_video(video=open(file_path, 'rb'), caption=company[1],
                                       reply_markup=website)

        elif company[3] == 1:
            await message.answer_photo(photo=open(file_path, 'rb'), caption=company[1],
                                       reply_markup=website)

    else:
        await message.answer("⌛ Нет ссылки ")


@dp.message_handler(text="Предложения и жалобы 🗣")
async def taklif(message: types.Message, state: FSMContext):
    await message.answer("Отправить свой номер телефона ☎", reply_markup=contact_ru)
    await Feedback.phone.set()


@dp.message_handler(state=Feedback.phone, content_types=types.ContentTypes.ANY)
async def telefoni(message: types.Message, state: FSMContext):
    try:
        if message.contact:
            async with state.proxy() as data:
                data["taklif_tel"] = message.contact.phone_number

                await message.answer("Отправьте свое предложение или жалобу на скоро рассмотрение ",
                                     reply_markup=types.ReplyKeyboardRemove())
                await Feedback.about.set()

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


@dp.message_handler(state=Feedback.about, content_types=types.ContentTypes.TEXT)
async def about(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["taklif_about"] = message.text
        about_m = message.text
        telefon = data.get("taklif_tel")

        await message.answer("Спасибо за ваше сообщение  😊", reply_markup=asosiy_menu_ru)
        await state.finish()

        db.create_shikoyat(str(message.from_user.id), message.from_user.username, telefon, about_m)