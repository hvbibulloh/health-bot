from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import db

admin_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Русский язык 🇧🇬"),
            KeyboardButton("O'zbek tili 🇺🇿")
        ],
        [
            KeyboardButton("Yuborish 🎙")
        ]
    ], resize_keyboard=True
)

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Русский язык 🇧🇬"),
            KeyboardButton("O'zbek tili 🇺🇿")
        ]
    ], resize_keyboard=True
)

asosiy_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Vakansiyalar 💼"),
            KeyboardButton("Kontakt ☎")
        ],
        [
            KeyboardButton("Biz haqimizda 🏢"),
            KeyboardButton("Taklif va shikoyatlar 🗣")
        ]
    ], resize_keyboard=True
)

asosiy_menu_ru = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton("Вакансии 💼"),
            KeyboardButton("Контакт ☎")
        ],
        [
            KeyboardButton("О нас 🏢"),
            KeyboardButton("Предложения и жалобы 🗣")
        ]
    ], resize_keyboard=True
)
