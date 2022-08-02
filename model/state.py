from aiogram.dispatcher.filters.state import StatesGroup, State



class Exersice(StatesGroup):
    check_word = State()
    trans_list = State()
    trans_litters = State()    
    trans_voice = State()


