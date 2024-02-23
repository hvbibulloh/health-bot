from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Русский язык 🇧🇬"),
            KeyboardButton("O'zbek tili 🇺🇿")
        ]
    ], resize_keyboard=True
)