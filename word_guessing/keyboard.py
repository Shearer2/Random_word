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
    urlkb = InlineKeyboardMarkup(row_width=1)
    urlbtn = InlineKeyboardButton(text='Github', url='https://github.com/Shearer2?tab=repositories')
    urlkb.add(urlbtn)

    return urlkb


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
    urlkb = InlineKeyboardMarkup(row_width=1)
    urlbtn = InlineKeyboardButton(text='Линия слова', url='https://t.me/s/Line_words_bot/')
    urlbtn1 = InlineKeyboardButton(text='Заметки', url='https://t.me/s/saved_notes_bot/')
    urlbtn2 = InlineKeyboardButton(text='Висельница', url='https://t.me/s/Game_Gallow_Bot/')
    urlkb.add(urlbtn, urlbtn1, urlbtn2)

    return urlkb
