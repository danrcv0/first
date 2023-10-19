from aiogram.dispatcher.filters.state import StatesGroup, State

class Form(StatesGroup):
  start = State()
  image = State()
  textlst = State()
  MainDef1 = State()
  MainDef2 = State()
  Admin = State()
  AddUser = State()
  DelUser = State()
 