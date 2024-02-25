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
        ],
        [
            KeyboardButton("Chiqish")
        ]
    ], resize_keyboard=True
)

malumotim = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Oliy"),
            KeyboardButton("O'rta"),
            KeyboardButton("Boshlang'ich")
        ],
        [
            KeyboardButton("Chiqish")
        ]
    ], resize_keyboard=True
)


async def vakansiya_uz_button():
    vakansiya = await db.get_vakansiya_key()
    btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True, row_width=1)
    orqaga = KeyboardButton("Chiqish")
    btn.add(orqaga)
    for i in vakansiya:
        btn.add(f"{i[1]} 💼")

    return btn
