from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db

contact_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Отправить номер", request_contact=True)
        ]
    ], resize_keyboard=True
)

tuman_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Бектемирский район"),
            KeyboardButton("Чиланзарский район"),
            KeyboardButton("Мирабадский район")
        ],
        [
            KeyboardButton("Мирзо Улугбекский район"),
            KeyboardButton("Алмазарский район"),
            KeyboardButton("Сергелийский район")
        ],
        [
            KeyboardButton("Шайхонтохурский район"),
            KeyboardButton("Учтепинский район"),
            KeyboardButton("Якасарайский район")
        ],
        [
            KeyboardButton("Яшнаабадский район"),
            KeyboardButton("Юнусабадский район")
        ],
        [
            KeyboardButton("Выход")
        ]
    ], resize_keyboard=True
)

malumotim_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Высший"),
            KeyboardButton("Средний (колледж-Лицей)"),
            KeyboardButton("Началный (школа)")
        ]
    ], resize_keyboard=True
)

chiqish_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Выход")
        ]
    ], resize_keyboard=True
)


async def vakansiya_ru_button():
    vakansiya = await db.get_vakansiya_keyru()
    btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    for i in vakansiya:
        btn.add(f"{i[1]} 💼")

    return btn


ishlamoq_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Хочу работать 🤝")
        ]
    ], resize_keyboard=True
)

javobi_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Да"),
            KeyboardButton("Нет")
        ]
    ], resize_keyboard=True
)


