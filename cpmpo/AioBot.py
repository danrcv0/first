from aiogram import types, executor, Dispatcher, Bot
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardMarkup, InputFile, MediaGroup, ParseMode
from forms import Form
import sqlite3, re, time



TOKEN = '6554252134:AAGmT-Ulas9XQm6RZtJullXHhdo_HeWy0fI'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


db = sqlite3.connect('users.db')
sql = db.cursor()


plot = {
    '1' : ['Женское коварство', 8],
    '2' : ['Красавица и Хищник', 4],
    '3' : ['Мачеха и падчерица', 8],
    '4': ['Ожидающая пробуждения и спасения', 2],
    '5': ['Разборчивая невеста', 4],
    '6': ['Спасительница', 4],
    '7': ['Отшельница', 2]
} 

UserCount = {}

AuthUsers = {}


@dp.message_handler(commands=['start'])
async def StartFunction(message: types.Message):
    UserID = message.from_user.id
    sql.execute(f"INSERT INTO users (ID) VALUES ({UserID})")
    AuthUsers[UserID] = 0
    UserCount[UserID] = []

    
    if UserID == 1679448840:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton(text=f'Добавить пользователя')
        btn1 = types.KeyboardButton(text=f'Удалить пользоваеля')
        btn2 = types.KeyboardButton(text=f'Играть')
        keyboard.add(btn, btn1, btn2)
        await message.answer(f'<b>Добро пожаловать!</b>\n<i> Вам предоставлен расширенный список функций...</i>', reply_markup=keyboard, parse_mode=ParseMode.HTML)
        await Form.Admin.set()

    else:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton(text=f'начать')
        keyboard.add(btn)
        await message.answer(f'<b>Добро пожаловать в мир сюжетов отношений.</b>\nВ жизни женщины обычно активны 2-3 сюжета. Всего сюжетов 7. Пройдя игру, вы узнаете свои активные сюжеты, повторяющиеся сценарии в них, те ловушки, в которые вы попали и те уроки, которые предстоит вынести, чтобы завершить сюжет. И в добрый путь!', reply_markup=keyboard, parse_mode=ParseMode.HTML)
        await Form.start.set()



@dp.message_handler(state= Form.start)
async def CheckMessage(message: types.Message, state: FSMContext):
    UserID = message.from_user.id
    mes = message.text
    print(UserID)
    if mes == 'начать':
        if (AuthUsers[UserID] == 1) or (UserID == 1679448840):
            media = MediaGroup()
            MediaCount = 1
            for x in range(7):
                media.attach_photo(photo=InputFile(path_or_bytesio=f"imgs/{MediaCount}.jpg"))
                MediaCount += 1
            await message.answer_media_group(media=media)
            await message.answer(f'<i>Посмотрите на картинки (7 картинок под номерами) и выберите по цифрам те картинки, в которых узнали себя, не более 3</i>', parse_mode=ParseMode.HTML )
            await Form.image.set()

        
        if (AuthUsers[UserID] != 1) and (UserID != 1679448840):
            markup = types.InlineKeyboardMarkup(row_width=True)
            lk1 = types.InlineKeyboardButton(text='АДМИН', url='https://t.me/Tata_Rodnik')
            markup.add(lk1)
            await message.answer('<b>У вас нет досупа к миру сюжетов отношений</b>\n<i>Что-бы получить доступ обратитесь к администратору данной игры</i>', parse_mode=ParseMode.HTML, reply_markup=markup)
            await message.answer(f'<b>Ваш ID: </b> <i>{UserID}</i>', parse_mode=ParseMode.HTML)

    else:
        await message.answer(f'<b>Неверная команда, попробуйте еще раз!</b>', parse_mode=ParseMode.HTML)
        await Form.start.set()



@dp.message_handler(state= Form.image)
async def CheckMessage(message: types.Message, state: FSMContext):
    UserID = message.from_user.id
    mes = message.text

    if len(re.findall(r'\w', mes)) > 3:
        await message.answer(f'Неверно указано число, выберите не больше 3')
        await Form.image.set()
    else:
            sql.execute(f"UPDATE users SET IMAGELIST='{mes}' WHERE ID={UserID}")
            await message.answer(f'<b>Диагностическая шкала текстовая</b>\n\n<i>Прочитайте несколько описаний , в каких вы узнаете себя? Выберите не более 3 цифр </i>', parse_mode=ParseMode.HTML)
            doc= open('plots/description.txt', 'r', encoding='utf-8')
            time.sleep(0.5)
            await message.answer(doc.read())
            await Form.textlst.set()


@dp.message_handler(state= Form.textlst)
async def CheckMessage(message: types.Message, state: FSMContext):
    UserID = message.from_user.id
    mes = message.text

    if len(re.findall(r'\w', mes)) > 3:
        await message.answer(f'Неверно указано число, выберите не больше 3')
        await Form.textlst.set()

    else:
        try:
            sql.execute(f"UPDATE users SET TEXTLIST='{mes}' WHERE ID={UserID}")
            for TextList in sql.execute(f"SELECT TEXTLIST FROM users WHERE ID={UserID}"):
                text = re.findall(r'\w', TextList[0])
                UserCount[UserID] = text
                with open(f'plots/{text[0]}/сюжет.doc', 'rb') as doc:
                    await bot.send_document(message.chat.id, document=doc, caption=f'<i>В каждом сюжете есть свои ловушки и уроки, напишите 2 цифры от 1 до {plot[text[0]][1]} , первая  - ловушка, вторая  - урок.</i>', parse_mode=ParseMode.HTML)
                    await Form.MainDef1.set()
                    return
        except:
            await message.answer(f'<b>Неверная команда, попробуйте еще раз!</b>', parse_mode=ParseMode.HTML)
            await Form.textlst.set()


@dp.message_handler(state= Form.MainDef1)
async def CheckMessage(message: types.Message, state: FSMContext):
    UserID = message.from_user.id
    mes = message.text

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton(text=f'далее')
    keyboard.add(btn)



    try:
        if mes !='Получить все сюжеты':
          if mes != 'далее':
            if len(re.findall(r'\w', mes)) > 5:
                await message.answer(f'Неверно указано число, выберите не больше 3')
                await Form.MainDef1.set()

        if mes == 'далее':
                with open(f'plots/{UserCount[UserID][0]}/сюжет.doc', 'rb') as doc:
                    await bot.send_document(message.chat.id, document=doc, caption=f'<i>В каждом сюжете есть свои ловушки и уроки, напишите 2 цифры от 1 до {plot[UserCount[UserID][0]][1]}, без использования запятых, пробелов и других символов\n первая  - ловушка, вторая  - урок.</i>', parse_mode=ParseMode.HTML)
                    return await Form.MainDef1.set()

        if mes =='Получить все сюжеты':
            markup = types.InlineKeyboardMarkup(row_width=True)
            lk1 = types.InlineKeyboardButton(text='ПЕРЕЙТИ К СПИСКУ', url='https://drive.google.com/drive/folders/1Dj0mK-Lq5z42HUhvoNLB34aQAjzkb1n4?usp=sharing')
            markup.add(lk1)
            with open('plots/сюжеты.rar', 'rb') as doc:
                await message.answer_document(document=doc, caption='<i> Предоставляем вам доступ ко всем сюжетам мира отношений! </i>', reply_markup=markup , parse_mode=ParseMode.HTML)
            await Form.start.set()
        
        else:
                    text = UserCount[UserID]
                    mes = re.findall(r'\w', mes)
                    try:
                        with open(f'plots/{text[0]}/Урок {mes[0]}.doc', 'rb') as doc:
                            await bot.send_document(message.chat.id, document=doc, caption='Урок к вашему сюжету...', reply_markup=keyboard)
                    except:
                        with open(f'plots/{text[0]}/Урок 1.doc', 'rb') as doc:
                            await bot.send_document(message.chat.id, document=doc, caption='Урок к вашему сюжету...', reply_markup=keyboard)
                    time.sleep(0.5)

                    try:
                        with open(f'plots/{text[0]}/Ловушка {mes[1]}.doc', 'rb') as doc:
                            await bot.send_document(message.chat.id, document=doc, caption='Ловушка к вашему сюжету...', reply_markup=keyboard)
                    except:
                        with open(f'plots/{text[0]}/Ловушка 1.doc', 'rb') as doc:
                            await bot.send_document(message.chat.id, document=doc, caption='Ловушка к вашему сюжету...', reply_markup=keyboard)
                    text.pop(0)
                    UserCount[UserID] = text
                    print(UserCount[UserID])
                    await Form.MainDef1.set()

    except:
        if UserID == 1679448840:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton(text=f'Добавить пользователя')
            btn1 = types.KeyboardButton(text=f'Удалить пользоваеля')
            btn2 = types.KeyboardButton(text=f'Играть')
            keyboard.add(btn, btn1, btn2)
            await message.answer("<b><i>Благодарю за ваше путешествие по сюжетам отношений, уверена, вы нашли ответы на свои вопросы и расширили свое  видение. Если нужна консультация по теме , обращайтесь и мои контакты в ВК</i></b>\nWhatsApp - +79257726575\nVKontakte - <a href='https://vk.com/id712483144'>Татьяна Ковалькова</a>", reply_markup=keyboard, parse_mode=ParseMode.HTML)
            await message.answer(f'<i>Вы были переведены в меню...</i>', reply_markup=keyboard, parse_mode=ParseMode.HTML)
            await Form.Admin.set()
        else:
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn = types.KeyboardButton(text=f'Получить все сюжеты')
            keyboard.add(btn)
            await message.answer("<b><i>Благодарю за ваше путешествие по сюжетам отношений, уверена, вы нашли ответы на свои вопросы и расширили свое  видение. Если нужна консультация по теме , обращайтесь и мои контакты в ВК</i></b>\nWhatsApp - +79257726575\nVKontakte - <a href='https://vk.com/id712483144'>Татьяна Ковалькова</a>", reply_markup=keyboard, parse_mode=ParseMode.HTML)
            await Form.MainDef1.set()


@dp.message_handler(state= Form.Admin)
async def CheckMessage(message: types.Message, state: FSMContext):
    UserID = message.from_user.id
    mes = message.text

    if mes == 'Добавить пользователя':
        await message.answer('Введите ID пользователя')
        await Form.AddUser.set()

    if mes == 'Удалить пользоваеля':
        await message.answer('Введите ID пользователя')
        await Form.DelUser.set()

    if mes == 'Играть':
        media = MediaGroup()
        MediaCount = 1
        for x in range(7):
            media.attach_photo(photo=InputFile(path_or_bytesio=f"imgs/{MediaCount}.jpg"))
            MediaCount += 1
        await message.answer_media_group(media=media)
        await message.answer(f'<i>Посмотрите на картинки (7 картинок под номерами) и выберите по цифрам те картинки, в которых узнали себя, не более 3</i>', parse_mode=ParseMode.HTML )
        await Form.image.set()

@dp.message_handler(state= Form.AddUser)
async def CheckMessage(message: types.Message, state: FSMContext):
    mes = message.text

    try:
        AuthUsers[int(mes)] = 1
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton(text=f'Добавить пользователя')
        btn1 = types.KeyboardButton(text=f'Удалить пользоваеля')
        btn2 = types.KeyboardButton(text=f'Играть')
        keyboard.add(btn, btn1, btn2)
        await message.answer('Отлично, пользователь был добавлен! Вы переведены в меню', reply_markup=keyboard)
        await Form.Admin.set()


    except:
        await message.answer('Похоже вы что-то указали неправильно, попробуйте еще раз!')
        await Form.AddUser.set()


@dp.message_handler(state= Form.DelUser)
async def CheckMessage(message: types.Message, state: FSMContext):
    mes = message.text

    try:
        AuthUsers[int(mes)] = 0
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = types.KeyboardButton(text=f'Добавить пользователя')
        btn1 = types.KeyboardButton(text=f'Удалить пользоваеля')
        btn2 = types.KeyboardButton(text=f'Играть')
        keyboard.add(btn, btn1, btn2)
        await message.answer('Отлично, пользователь был успешно удален! Вы переведены в меню', reply_markup=keyboard)
        await Form.Admin.set()
    except:
        await message.answer('Похоже вы что-то указали неправильно, попробуйте еще раз!')
        await Form.DelUser.set()


if __name__ == "__main__":
    executor.start_polling(dp)

    