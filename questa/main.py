from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup
from datetime import datetime
import time, random
from forms import Form
import sqlite3, os
import openai


TOKEN = '6680313031:AAHngzCZtLmEJblDD38uczdgRbRId_VwdO4'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

Admin = 390884327
users = {}



@dp.message_handler(commands=['start'])
async def StartFunction(message: types.Message):
    UserID = message.from_user.id
    UserName = message.from_user.full_name
    if UserID == Admin:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton(text=f'Добавить пользователя')
        btn1 = types.KeyboardButton(text=f'Удалить пользователя')
        btn2 = types.KeyboardButton(text=f'Проверенные блоги✔️')
        keyboard.add(btn, btn1, btn2)
        await message.answer(f'Привет! {UserName}', reply_markup=keyboard)
        await Form.CheckMessage.set()
    if UserID != Admin:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton(text=f'Проверенные блоги✔️')
        keyboard.add(btn2)
        await message.answer(f'Привет! {UserName}', reply_markup=keyboard)
        await Form.ReplyMessage.set()



@dp.message_handler()
async def DeleteMessage(message: types.Message):
    mes = message.text
    UserID = message.from_user.id

    if mes == 'Проверенные блоги✔️':
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn2 = types.KeyboardButton(text=f'Проверенные блоги✔️')
        keyboard.add(btn2)
        markup = types.InlineKeyboardMarkup(row_width=True)
        lk1 = types.InlineKeyboardButton(text='ПЕРЕЙТИ К СПИСКУ♻️', url='https://t.me/goose_check')
        lk2 = types.InlineKeyboardButton(text='ОТЗЫВЫ💬', url='https://t.me/goose_check')
        markup.add(lk1,lk2)
        img = open(f"image.jpg", 'rb')
        BotMes = await message.answer_photo(photo=img, caption=f'❌Собрали для вас список проверенных Блогеров, что бы ваш закуп был более эффективным, и вы не попали на мошенников. 🧐\n\nЧто бы попасть в список, каждый блог детально проверяется на накрутку и наличие живой аудитории. \n\n*Этим блогерам уже доверяют тысячи поставщиков, отзывы постоянно обновляются. \n\nЕсли ты блогер и хочешь попасть в список\nПиши 👉🏻@karinakamalova1', reply_markup=markup)
        
        
        time.sleep(30)
        await message.delete()
        await BotMes.delete()

    else:
        try:
            if users[UserID] == 1:
                pass
        except:
                markup = types.InlineKeyboardMarkup(row_width=True)
                lk1 = types.InlineKeyboardButton(text='ПЕРЕЙТИ К СПИСКУ♻️', url='https://t.me/goose_check')
                
                    
                keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn2 = types.KeyboardButton(text=f'Проверенные блоги✔️')
                keyboard.add(btn2)
                markup.add(lk1)
                await message.delete()
                msg = await message.answer(f'‼Ваше сообщение удалено в чате. Размещение возможно только через администратора: @karinakamalova1 (или переходите через описание) \n\n Для того чтобы избежать мошенников и сделать эффективный закуп, мы собрали для вас Список Проверенных Блогеров ✅', reply_markup=markup)
                time.sleep(30)
                await msg.delete()

        
@dp.message_handler(content_types=['new_chat_members'])
async def DeleteMessage(message: types.Message):
        UserName = message.from_user.full_name
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton(text=f'Проверенные блоги✔️')
        keyboard.add(btn)
        msg = await message.answer(f'☑️', reply_markup=keyboard)


@dp.message_handler(state= Form.CheckMessage)
async def CheckMessage(message: types.Message, state: FSMContext):
    mes = message.text
    UserID = message.from_user.id
    if (mes == 'Добавить пользователя') and (UserID == Admin):
        await message.answer('Введите ID пользователя: ')
        await Form.AddUser.set()

    if (mes == 'Удалить пользователя') and (UserID == Admin):
         await message.answer('Введите ID пользователя: ')
         await Form.DelUser.set()

    if mes == 'Проверенные блоги✔️':
        markup = types.InlineKeyboardMarkup(row_width=True)
        lk1 = types.InlineKeyboardButton(text='ПЕРЕЙТИ К СПИСКУ♻️', url='https://t.me/goose_check')
        lk2 = types.InlineKeyboardButton(text='ОТЗЫВЫ💬', url='https://t.me/goose_check')
        markup.add(lk1,lk2)
        img = open(f"image.jpg", 'rb')
        BotMes = await message.answer_photo(photo=img, caption=f'❌Собрали для вас список проверенных Блогеров, что бы ваш закуп был более эффективным, и вы не попали на мошенников. 🧐\n\nЧто бы попасть в список, каждый блог детально проверяется на накрутку и наличие живой аудитории. \n\n*Этим блогерам уже доверяют тысячи поставщиков, отзывы постоянно обновляются. \n\nЕсли ты блогер и хочешь попасть в список\nПиши 👉🏻@karinakamalova1', reply_markup=markup)
        await Form.CheckMessage.set()
            
            
@dp.message_handler(state= Form.AddUser)
async def AddUser(message: types.Message, state: FSMContext):
    mes = message.text
    try:
        users[int(mes)] = 1
        await message.answer('Пользователь был добавлен \nВы были переведены в меню')
        await Form.CheckMessage.set()
    except:
        await message.answer('Что-то пошло не так, попробуйте заново \nВы были переведены в меню')
        await Form.CheckMessage.set()

@dp.message_handler(state= Form.DelUser)
async def AddUser(message: types.Message, state: FSMContext):
    mes = message.text
    try:
        del users[int(mes)]
        await message.answer('Пользователь был удален \nВы были переведены в меню')
        await Form.CheckMessage.set()
    except:
        await message.answer('Что-то пошло не так, попробуйте заново \nВы были переведены в меню')
        await Form.CheckMessage.set()


@dp.message_handler(state= Form.ReplyMessage)
async def CheckMessage(message: types.Message, state: FSMContext):
    mes = message.text
    if mes == 'Проверенные блоги✔️':
        markup = types.InlineKeyboardMarkup(row_width=True)
        lk1 = types.InlineKeyboardButton(text='ПЕРЕЙТИ К СПИСКУ♻️', url='https://t.me/goose_check')
        lk2 = types.InlineKeyboardButton(text='ОТЗЫВЫ💬', url='https://t.me/goose_check')
        markup.add(lk1,lk2)
        img = open(f"image.jpg", 'rb')
        await message.answer_photo(photo=img, caption=f'❌Собрали для вас список проверенных Блогеров, что бы ваш закуп был более эффективным, и вы не попали на мошенников. 🧐\n\nЧто бы попасть в список, каждый блог детально проверяется на накрутку и наличие живой аудитории. \n\n*Этим блогерам уже доверяют тысячи поставщиков, отзывы постоянно обновляются. \n\nЕсли ты блогер и хочешь попасть в список\nПиши 👉🏻@karinakamalova1', reply_markup=markup)
        await Form.ReplyMessage.set()




if __name__ == "__main__":
    executor.start_polling(dp)
