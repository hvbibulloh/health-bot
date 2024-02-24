from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

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
            KeyboardButton("Высокий"),
            KeyboardButton("Средний"),
            KeyboardButton("Стартер")
        ],
        [
            KeyboardButton("Выход")
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