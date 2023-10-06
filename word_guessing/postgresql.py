import os
import psycopg2
from dotenv import load_dotenv


# Загружаем переменные окружения.
load_dotenv()

# Подключаемся к базе данных.
connection = psycopg2.connect(
    host=os.getenv('host'),
    user=os.getenv('user'),
    password=os.getenv('password'),
    database=os.getenv('db_name')
)

# Устанавливаем автоматическое обновление данных в базе.
connection.autocommit = True


# Функция для получения всех доступных слов из базы данных.
def words_all():
    # При помощи контекстного менеджера забираем все слова.
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT word FROM words.all_words
        """)
        words = list(map(lambda x: x[0], cursor.fetchall()))
    return words


def information_id():
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT user_id FROM gallow_bot.game
        """)
        inf_id = list(map(lambda x: x[0], cursor.fetchall()))
    return inf_id


def information_game(user_id):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            SELECT word, tries, guessed_letters, guessed_words, word_completion FROM gallow_bot.game
            WHERE user_id = {user_id}
        """)
        inf_game = list(map(lambda x: x, cursor.fetchall()[0]))
    return inf_game


async def db_start():
    # При помощи контекстного менеджера создаём таблицу в базе данных, если она ещё не была создана.
    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gallow_bot.game (user_id bigserial PRIMARY KEY, word varchar(255),
            tries smallint, guessed_letters varchar(255), guessed_words varchar(255), word_completion varchar(255))
        """)


async def create_profile(user_id, word, tries, guessed_letters, guessed_words, word_completion):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            INSERT INTO gallow_bot.game (user_id, word, tries, guessed_letters, guessed_words, word_completion)
            VALUES ({user_id}, '{word}', {tries}, '{guessed_letters}', '{guessed_words}', '{" ".join(word_completion)}')
        """)


async def update_profile(user_id, word, tries, guessed_letters, guessed_words, word_completion):
    with connection.cursor() as cursor:
        cursor.execute(f"""
            UPDATE gallow_bot.game SET (word, tries, guessed_letters, guessed_words, word_completion) = ('{word}', 
            {tries}, '{guessed_letters}', '{guessed_words}', '{" ".join(word_completion)}') WHERE user_id = {user_id}
        """)

