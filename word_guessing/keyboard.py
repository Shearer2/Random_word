from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# Функция для создания встроенной клавиатуры.
def get_kb() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text='/play'),
            KeyboardButton(text='/link'),
            KeyboardButton(text='/projects')
        ],
        [
            KeyboardButton(text='/description'),
            KeyboardButton(text='/help')
        ],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


# Функция для прикрепления к сообщению ссылки на репозиторий github.
def get_github() -> InlineKeyboardMarkup:
    url_kb = InlineKeyboardMarkup(row_width=1)
    url_btn = InlineKeyboardButton(text='Github', url='https://github.com/Shearer2?tab=repositories')
    url_kb.add(url_btn)

    return url_kb


# Функция для прерывания игры.
def get_cancel() -> ReplyKeyboardMarkup:
    kb = [
        [
            KeyboardButton(text='/cancel')
        ],
    ]

    keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

    return keyboard


# Функция для прикрепления к сообщению ссылок на проекты в телеграм.
def get_projects() -> InlineKeyboardMarkup:
    url_kb = InlineKeyboardMarkup(row_width=1)
    url_btn = InlineKeyboardButton(text='Линия слова', url='https://t.me/s/Line_words_bot/')
    url_btn1 = InlineKeyboardButton(text='Заметки', url='https://t.me/s/saved_notes_bot/')
    url_btn2 = InlineKeyboardButton(text='Висельница', url='https://t.me/s/Game_Gallow_Bot/')
    url_kb.add(url_btn, url_btn1, url_btn2)

    return url_kb
