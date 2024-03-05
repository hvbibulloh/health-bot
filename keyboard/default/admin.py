from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db

chiqishrek = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Chiqish")
        ]
    ], resize_keyboard=True
)

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Vakansiyalar 💼"),
            KeyboardButton("Kontakt ☎")
        ],
        [
            KeyboardButton("Biz haqimizda 🏢"),
            KeyboardButton("Taklif va shikoyatlar 🗣")
        ],
        [
            KeyboardButton("Xabar yuborish 🎙")
        ]
    ], resize_keyboard=True
)
