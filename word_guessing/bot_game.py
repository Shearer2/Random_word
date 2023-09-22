import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from game import get_word, display_hangman, check
from keyboard import get_kb, get_github, get_projects, get_cancel


# Загружаем переменные окружения.
load_dotenv()

# Подключаем память для хранения состояний.
storage = MemoryStorage()
bot = Bot(token=os.getenv('TOKEN_API'))
dp = Dispatcher(bot, storage=storage)
help_inf = """
<b>/start</b> - <em>начало работы с ботом.</em>
<b>/play</b> - <em>начать игру.</em>
<b>/link</b> - <em>перейти в репозиторий github.</em>
<b>/projects</b> - <em>ознакомиться с проектами.</em>
<b>/description</b> - <em>описание проекта.</em>
<b>/help</b> - <em>вывести список команд.</em>
"""


# Делаем обработчик команды cancel, а чтобы указать любое возможное состояние достаточно указать *.
@dp.message_handler(commands=['cancel'], state='*')
async def bot_cancel(message: types.Message, state: FSMContext) -> None:
    # При вводе cancel или при нажатии на соответствующую кнопку прерываем игру.
    await state.finish()
    await message.reply('Вы прервали игру.',
                        reply_markup=get_kb())


# Обработчик команды start.
@dp.message_handler(commands=['start'])
async def bot_start(message: types.Message) -> None:
    await message.answer('Добро пожаловать в игру Висельница!', reply_markup=get_kb())


# Обработчик команды начала игры.
@dp.message_handler(commands=['play'])
async def bot_play(message: types.Message) -> None:
    # Объявляем глобальные переменные, чтобы их можно было изменять.
    global word, tries, word_completion, guessed_letters, guessed_words, word1, word2, text
    # Записываем в переменную полученное случайное слово.
    word = get_word()
    # Указываем количество доступных попыток.
    tries = 6
    # Создаём список для вывода букв в виде скобок.
    word_completion = ['[]'] * len(word)
    # Создаём список уже названных букв.
    guessed_letters = []
    # Создаём список уже названных слов.
    guessed_words = []
    # Создаём три переменные, в первой храним список из отсортированных букв загаданного слова, во втором список из
    # букв слова, в третьем пустой список.
    word1, word2, text = list(word), list(word), []
    word1.sort()
    await message.answer(f'Ваше текущее состояние игры: {display_hangman(tries)}')
    await message.answer(f'Количество доступных попыток: {tries}')
    # Делаем вывод первоначальной информации в виде строки, а не в виде списка.
    await message.answer(f'{" ".join(word_completion)}', reply_markup=get_cancel())


# Вывод репозитория github.
@dp.message_handler(commands=['link'])
async def bot_link(message: types.Message) -> None:
    await message.answer('Репозиторий github:', reply_markup=get_github())


# Вывод всех проектов в телеграм.
@dp.message_handler(commands=['projects'])
async def bot_projects(message: types.Message) -> None:
    await message.answer('Мои проекты:', reply_markup=get_projects())


# Описание данного бота.
@dp.message_handler(commands=['description'])
async def bot_description(message: types.Message) -> None:
    await message.answer('Данный бот предназначен для игры в висельницу. Можно угадывать как по одной букве, так и '
                         'целое слово. Если буква или слово были не правильно угаданы, то забирается одна попытка. '
                         'При правильном угадывании буквы открывается соответствующая буква в слове. Игра продолжается '
                         'до тех пор, пока не будет угадано слово или не будут исчерпаны все попытки.')


# Вывод всех доступных команд.
@dp.message_handler(commands=['help'])
async def bot_help(message: types.Message) -> None:
    await message.answer(help_inf, parse_mode='HTML')


# Обработка всех сообщений поступающих на вход.
@dp.message_handler()
async def bot_all(message: types.Message, state: FSMContext) -> None:
    # Объявляем глобальные переменные.
    global word, tries, word_completion, guessed_letters, guessed_words, word1, word2, text
    # Получаем букву или слово, которое ввёл пользователь.
    letter = message.text
    # Если буквы не принадлежат русскому алфавиту, то выводим сообщение.
    if check(letter):
        await message.answer('Введите букву русского алфавита или слово!')
    # Иначе если введённая буква содержится в списке вводимых букв, то вывести сообщение об этом.
    elif letter.upper() in guessed_letters:
        await message.answer('Вы уже вводили эту букву!')
    # Иначе если введённое слово содержится в списке вводимых слов, то вывести сообщение об этом.
    elif letter.upper() in guessed_words:
        await message.answer('Вы уже вводили это слово!')
    # Иначе начинаем обработку буквы или слова.
    else:
        # Если отсортированный список из правильно введённых букв не равняется отсортированному списку загаданного
        # слова и количество попыток не равно нулю, то продолжаем игру.
        if text != word1 and tries != 0:
            # Обрабатываем введение буквы.
            if len(letter) == 1:
                # Добавляем введённую букву в список вводимых букв.
                guessed_letters.append(letter.upper())
                # Если буква содержится в списке букв загаданного слова, то проходим циклом по списку и если буква
                # равняется букве из списка по заданному индексу, то осуществляем замену пустых скобок по заданному
                # индексу на соответствующую букву.
                if letter.upper() in word2:
                    for i in range(len(word2)):
                        if letter.upper() == word2[i]:
                            word_completion[i] = letter.upper()
                            # Добавляем букву в список и сортируем.
                            text.append(letter.upper())
                            text.sort()
                    await message.answer(f'Ваше текущее состояние игры: {display_hangman(tries)}')
                    await message.answer(f'Количество доступных попыток: {tries}')
                    await message.answer(f'{" ".join(word_completion)}')
                # Иначе отнимаем одну попытку.
                else:
                    tries -= 1
                    await message.answer(f'Ваше текущее состояние игры: {display_hangman(tries)}')
                    await message.answer(f'Количество доступных попыток: {tries}')
                    await message.answer(f'{" ".join(word_completion)}')
            # Иначе если было введено слово, то добавляем его в список уже вводимых слов.
            elif len(letter) > 1:
                guessed_words.append(letter.upper())
                # Если слово равно загаданному слову, то завершаем игру.
                if letter.upper() == word:
                    await message.answer('Поздравляем, вы угадали слово! Вы победили!')
                    await state.finish()
                # Иначе отнимаем одну попытку.
                else:
                    tries -= 1
                    await message.answer(f'Ваше текущее состояние игры: {display_hangman(tries)}')
                    await message.answer(f'Количество доступных попыток: {tries}')
                    await message.answer(f'{" ".join(word_completion)}')
        # Иначе если попытки закончились, то завершаем игру.
        elif tries == 0:
            await message.answer(f'Вы исчерпали все попытки.\nЗагаданное слово: {word}')
            await state.finish()
        # Иначе если слово было угадано, то завершаем игру.
        elif text == word1:
            await message.answer('Поздравляем, вы угадали слово! Вы победили!')
            await state.finish()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
