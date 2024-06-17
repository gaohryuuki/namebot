# 1. Импортируем библиотеки
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters.command import Command

from string import punctuation

# 2. Инициализация объектов
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
# bot = Bot(token='7060128802:AAF6AYAlZU1OnfrfW0tFvXe7asFjcd5vfaM')
dp = Dispatcher()
logging.basicConfig(level=logging.INFO, 
                    filename='botlog.log')

# 3. Обработка команды start
@dp.message(Command(commands=['start']))
async def process_command_start(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = f'Здраствуйте, {user_name}. Далее всё, что вы будете писать, будет восприниматься как ФИО на Кириллице и я буду вам возвращать это же ФИО, но уже на Латинице согласно приказу МИД России от 12.02.2020 № 2113. Можете писать с заглавной или прописными, через запятую или другие знаки препинания, но главное: ставьте хотя бы 1 пробел между ФИО.'
    logging.info(f'{user_name} {user_id} запустил бота')
    await bot.send_message(chat_id=user_id, text=text)


# 4. Обработка всех сообщений
@dp.message()
async def send_echo(message: Message):
    user_name = message.from_user.full_name
    user_id = message.from_user.id
    text = message.text
    logging.info(f'{user_name} {user_id} оправил данное ФИО: {text}')

    # Логика обработки ФИО
    # Убераем знаки препинания
    for char in punctuation:
        if char in text:
            text = text.replace(char,'')
    
    # ФИО заглавными для замены
    text = text.upper()

    # Словарь замены с Кириллицы на Латиницу
    cyr_to_lat = {
        'А':'A',
        'Б':'B',
        'В':'V',
        'Г':'G',
        'Д':'D',
        'Е':'E',
        'Ё':'E',
        'Ж':'ZH',
        'З':'Z',
        'И':'I',
        'Й':'I',
        'К':'K',
        'Л':'L',
        'М':'M',
        'Н':'N',
        'О':'O',
        'П':'P',
        'Р':'R',
        'С':'S',
        'Т':'T',
        'У':'U',
        'Ф':'F',
        'Х':'KH',
        'Ц':'TS',
        'Ч':'CH',
        'Ш':'SH',
        'Щ':'SHCH',
        'Ы':'Y',
        'Ъ':'IE',
        'Э':'E',
        'Ю':'IU',
        'Я':'IA',
        'Ь':''
    }

    # Заменяем Кириллицу на Латиницу в строке
    for char in text:
        if char in cyr_to_lat:
            text = text.replace(char,cyr_to_lat[char])
    
    # Переводим в заглавный вид
    result = [x.lower().capitalize() for x in text.split()]

    # Собираем строку ФИО на Латинице
    text = ' '.join(result)

    logging.info(f'{user_name} {user_id} получил данное ФИО: {text}')
    await message.answer(text=text)

# 5. Запустит процесс пулинга
if __name__ == '__main__':
    dp.run_polling(bot)