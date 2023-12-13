from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, InputFile, MediaGroup, ParseMode
from datetime import datetime, timedelta, date
import sqlite3, time

API_TOKEN = '6605154512:AAEvQOY2iS9dgcE6HYcJdGdaU508rpFKEiA'


admin = 6130091130

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

feedback_messages = {}



db = sqlite3.connect('users.db')
sql = db.cursor()




@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):

    if message.from_user.id == admin:
        await message.answer("Отлично, оповещения включены!")
        while True:
            dt_now = date.today()
            date_passed = dt_now - timedelta(days=0)
            for id in sql.execute(f"SELECT ID FROM users WHERE DATE='{date_passed}' "):
                await bot.send_message(id[0], 'Привет, красотка! \n\nКак тебе наша юбка? Все ли тебе понравилось? \n\n\nМы хотим подарить тебе приятный бонус💸 \nМожешь оставить отзыв на Wildberries о нашей юбке.\nЗа положительный отзыв - переведем 100 рублей на твой номер телефона, за положительный отзыв с фото - 150 рублей. \n\nПосле публикации отзыва присылай скрин и мы тебе отправим бонус🥰💸')
            time.sleep(86400)
                



    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton(text=f'Меню')
        keyboard.add(btn)

        sql.execute(f"INSERT INTO users (ID) VALUES ({message.from_user.id})")
        sql.execute(f"UPDATE users SET DATE='{date.today()}' WHERE ID={message.from_user.id}")
        db.commit()

        await message.answer(
            "Привет, Красавица! Спасибо тебе за выбор нашей юбки. Мы уверены, она тебе очень понравится, "
            "принесет тебе много радостных эмоций и отлично дополнит твой гардероб!",
            reply_markup=keyboard
        )

        await message.answer("Какой у тебя вопрос?", reply_markup=get_main_menu())

@dp.message_handler()
async def start_command(message: types.Message):
    msg = message.text

    if msg == 'Меню':
        await message.answer("Меню: ", reply_markup=get_main_menu())


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'feedback')
async def feedback_callback_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(user_id, callback_query.message.message_id)
    feedback_messages[user_id] = {'question': "Обратная связь"}
    keyboard = types.InlineKeyboardMarkup()
    ikback = types.InlineKeyboardButton(text='Вернуться назад', callback_data='back')
    keyboard.add(ikback)
    await bot.send_message(user_id, "<b>Мы тебя внимательно слушаем :)</b>\n\n<i>Отправь свое сообщение, и мы ответим в ближайшее время.</i>", parse_mode=ParseMode.HTML, reply_markup=keyboard)


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'lottery')
async def lottery_callback_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(user_id, callback_query.message.message_id)
    await bot.send_message(user_id, "Для того, чтобы участвовать в розыгрыше, необходимо выполнить следующие условия:\n1)перейти и вступить в канал https://t.me/duobelan (в данном канале вы можете следить за процессом конкурса и в нем же мы выберем победителя)\n2)оставить отзыв с фото (❗️критерии к  отзыву: юбку обязательно нужно примерить на себе и сфотографировать) и прислать скриншот @duo_belan\nВсего 2 простых условия, чтобы выиграть поход в Spa-комплекс в твоем городе 🥰\n\nВыбирать победителя мы будем среди участников канала https://t.me/duobelan с помощью генератора случайных чисел RandStuff.\nИтого конкурса подведем 31.12.\nЖелаем тебе удачи 🤞🏼❤️\n\n Если остались вопросы, вернись в предыдущее меню и нажми 'Связаться с поддержкой", reply_markup=get_back_inline_keyboard())
    


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'care')
async def care_callback_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(user_id, callback_query.message.message_id)
    await bot.send_message(user_id, "Рекомендации по уходу за юбкой:\n\n1)Перед стиркой снять декоративные элементы, вывернуть вещь, застегнуть молнию.\n2)Стирать в прохладной воде при 30 °C.\n3)Выбрать деликатный режим.\n4)Применять жидкое средство для стирки.\n5)Количество стирального средства – минимальное, иначе на поверхности могут образоваться белые разводы.\n6)Нельзя использовать агрессивную химию, в том числе и хлорсодержащие средства.\n7)Не подвергать сильному механическому воздействию: минимальное количество оборотов, не выкручивать, не тянуть и не сжимать.\n8)После стирки дать воде стечь, повесить на плечики, подходящие по размеру – во избежание деформации изделия.\n9)Небольшие загрязнения протирать салфеткой, слегка смоченной водой или средством для стирки.\n10)Хранить вещь только в вертикальном положении во избежание заломов.\n\nЕсли остались вопросы, вернись в предыдущее меню и нажми 'Связаться с поддержкой", reply_markup=get_back_inline_keyboard())



@dp.callback_query_handler(lambda callback_query: callback_query.data == 'support')
async def support_callback_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.delete_message(user_id, callback_query.message.message_id)
    await bot.send_message(user_id, "<b>Мы тебя внимательно слушаем)</b> \n\n<i>Что случилось?</i>", parse_mode=ParseMode.HTML, reply_markup=get_back_inline_keyboard())
    feedback_messages[user_id] = {'question': "Связь с поддержкой"}


@dp.callback_query_handler(text='back')
async def CheckMessage(message: types.CallbackQuery):
        await bot.delete_message(message.from_user.id, message.message.message_id)
        await bot.send_message(message.from_user.id, "Какой у тебя вопрос?", reply_markup=get_main_menu())

def get_main_menu():
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text="Хочу оставить обратную связь 💌", callback_data="feedback")
    button2 = types.InlineKeyboardButton(text="Хочу участвовать в розыгрыше 🎁", callback_data="lottery")
    button3 = types.InlineKeyboardButton(text="Рекомендации по уходу за юбкой ✅", callback_data="care")
    button4 = types.InlineKeyboardButton(text="Связаться с поддержкой 💬", callback_data="support")

    keyboard.add(button1)
    keyboard.add(button2)
    keyboard.add(button3)
    keyboard.add(button4)

    return keyboard


def get_back_inline_keyboard():
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Назад", callback_data="back")
    keyboard.add(button)
    return keyboard


@dp.callback_query_handler(lambda callback_query: callback_query.data == 'back')
async def back_inline_handler(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    await bot.answer_callback_query(callback_query.id)
    await bot.send_message(user_id, "Какой у тебя вопрос?", reply_markup=get_main_menu())


@dp.message_handler(lambda message: message.from_user.id in feedback_messages)
async def handle_feedback(message: types.Message):
    user_id = message.from_user.id
    feedback_type = feedback_messages[user_id]['question']
    del feedback_messages[user_id]  # Удаляем пользователя из словаря обратной связи

    admin_id = 6510879921
    await bot.send_message(admin_id, f"{feedback_type} от @{message.from_user.username}:\n{message.text}",
                           reply_markup=get_reply_inline_keyboard(user_id))
    await bot.send_message(user_id, f"Мы приняли твое обращение. Ответим в ближайшее время",
                           reply_markup=get_back_inline_keyboard())


def get_reply_inline_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton(text="Ответить", callback_data=f"reply_{user_id}")
    keyboard.add(button)
    return keyboard


@dp.callback_query_handler(lambda callback_query: callback_query.data.startswith('reply_'))
async def reply_inline_handler(callback_query: types.CallbackQuery):
    user_id = int(callback_query.data.split('_')[1])
    await bot.answer_callback_query(callback_query.id)

    # Отправляем администратору уведомление о необходимости написать ответ
    admin_id = 6510879921  # Замените на фактический ID вашего администратора
    await bot.send_message(admin_id, "Напишите свой ответ:")

    # Убираем кнопку "Ответить" и меняем текст сообщения
    await bot.edit_message_text(chat_id=callback_query.message.chat.id,
                                message_id=callback_query.message.message_id,
                                text=callback_query.message.text + "\n\nОтвет отправлен",
                                reply_markup=None)

    # Ожидаем ответ от администратора
    async def reply_handler(msg: types.Message):
        # Проверяем, что ответ от правильного администратора
        if msg.from_user.id == admin_id:
            # Отправляем ответ пользователю
            await bot.send_message(user_id, f"Ответ от поддержки: {msg.text}")

            # Уведомляем пользователя об успешной отправке ответа
            await bot.send_message(admin_id, "Ответ отправлен")

            # Удаляем временный обработчик
            dp.message_handlers.unregister(reply_handler)(reply_handler)
        else:
            # Если ответ от другого пользователя, просим администратора отвечать
            await bot.send_message(user_id, "Пожалуйста, дождитесь ответа от администратора")

    # Добавляем временный обработчик для ответа от администратора
    dp.message_handlers.register(reply_handler)


if __name__ == '__main__':
    executor.start_polling(dp)