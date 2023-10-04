from aiogram.dispatcher.filters.state import StatesGroup, State

class Form(StatesGroup):
  start = State()
  AddUser = State()
  CheckMessage = State()
  DelUser = State()
  ReplyMessage = State()
 