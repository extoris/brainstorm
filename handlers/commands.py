from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart, CommandHelp
from data.db_control import dp_all_users_list, dp_user_create
from handlers.manager import check_word, exersice_list, manager
from keyboards.keyboards import end_exersice


async def set_commands(dp):
    await dp.bot.set_my_commands(
        [
            types.BotCommand("end", "Закончить упражнение"),
            types.BotCommand("begin", "Начать упражнение"),
            types.BotCommand("start", "Запустить бота"),
            types.BotCommand("help", "Вывести справку"),
        ]
    )


async def cmd_start(message: types.Message, state: FSMContext):
    print(message.from_user.first_name)
    await message.answer(f'Привет {message.from_user.full_name}, я помогу тебе выучить анлийский язык. \nТы можешь тренировать английские слова на в выборе из списка, правописании и аудировании. \nЧтобы начать нажми /begin')
    all_users_list = dp_all_users_list()
    if message.from_user.id not in all_users_list:
        dp_user_create(message.from_user.id)

async def cmd_help(message: types.Message, state: FSMContext):
    await message.answer('В упражнении будет 4 стадии: /nвыбор слов для тренировки /nвыбор перевода правильного перевода из списка /nправописание слова по буквам /nперевод на слух')
    await message.answer('Чтобы начать нажми /begin')
    await message.answer('Чтобы закончить тренировку не проходя её до конца нажми /end')
    print('help')

async def cmd_begin(message: types.Message, state: FSMContext):
    await message.answer('начинаем')
    await state.finish()
    async with state.proxy() as data:
        data['sequence'] = [[]] + [{'function': check_word}] + [{'function': exersice_list}]
        print(data['sequence'])
    await message.answer('выберете слова, которые будем тренировать')
    await state.update_data(check_word = [])
    await manager(message, state)

async def cmd_end(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer('Вы действительно хотите закончить? \nвесь прогресс не сохраниться', reply_markup=end_exersice)

    
def register_handler_commands(dp: Dispatcher):
    dp.register_message_handler(cmd_start, CommandStart(), state='*')
    dp.register_message_handler(cmd_start, commands='end', state='*')
    dp.register_message_handler(cmd_help, CommandHelp(), state='*')    
    dp.register_message_handler(cmd_begin, commands='begin', state='*')