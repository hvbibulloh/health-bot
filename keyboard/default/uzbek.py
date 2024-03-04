from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from loader import db

contact_uz = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Raqam yuborish", request_contact=True)
        ]
    ], resize_keyboard=True
)

chiqish = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Chiqish")
        ]
    ], resize_keyboard=True
)

tuman = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Bektemir tumani"),
            KeyboardButton("Chilonzor tumani"),
            KeyboardButton("Mirobod tumani")
        ],
        [
            KeyboardButton("Mirzo Ulug'bek tumani"),
            KeyboardButton("Olmazor tumani"),
            KeyboardButton("Sergeli tumani")
        ],
        [
            KeyboardButton("Shayhontohur tumani"),
            KeyboardButton("Uchtepa tumani"),
            KeyboardButton("Yakkasaroy tumani")
        ],
        [
            KeyboardButton("Yashnaobod tumani"),
            KeyboardButton("Yunusobod tumani")
        ]
    ], resize_keyboard=True
)

malumotim = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Oliy"),
            KeyboardButton("O'rta"),
            KeyboardButton("Boshlang'ich")
        ]
    ], resize_keyboard=True
)


async def vakansiya_uz_button():
    vakansiya = await db.get_vakansiya_key()
    btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    for i in vakansiya:
        if i[4] == True:
            btn.add(f"{i[1]} 💼")
    return btn


ishlamoq = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ishlamoqchiman 🤝"),

        ]
    ], resize_keyboard=True
)

javobi = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Ha"),
            KeyboardButton("Yo'q")
        ]
    ], resize_keyboard=True
)
