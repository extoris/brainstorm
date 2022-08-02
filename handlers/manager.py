from aiogram import Dispatcher
from aiogram.types import CallbackQuery, Message, ContentTypes
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Text
from data.db_control import get_random_string
from data.config import DATABASE_NAME
from contextlib import suppress
from aiogram.utils.exceptions import MessageNotModified
from keyboards.keyboards import check_word_keyboard, trans_list_keyboard, trans_litters_keyboard
from model.state import Exersice


async def manager(message: Message, state: FSMContext):
    #функция по порядку вызывает функции с упражнениями
    async with state.proxy() as data:        
        data['sequence'].pop(0)
        try:
            current_function = data['sequence'][0].get('function')
            current_word = data['sequence'][0].get('word')
        except IndexError:
            current_function = the_end
            current_word = None
    await current_function(message, state, current_word)


async def exersice_list(message: Message, state: FSMContext, *args):
    # создаёт список упражнений
    exersices = [trans_list, trans_litters, trans_voice]
    async with state.proxy() as data:
        word_list = data['check_word']
        for exersice in exersices:
            for word in word_list:
                data['sequence'].append({'function': exersice, 'word': word})
    await manager(message, state)


async def the_end(message: Message, state: FSMContext, *args):
    await message.answer('Congratulation!!!')
    await message.answer('Чтобы повторить на жмите /begin')


async def check_word(message: Message, state: FSMContext, *args):
    await Exersice.check_word.set()
    set_word = get_random_string(DATABASE_NAME)
    async with state.proxy() as data:
        data['check_word'].append(set_word)
    await message.answer_voice(set_word[2], f'{set_word[0]} - {set_word[1]}' ,reply_markup=check_word_keyboard)

async def check_word_answer(call: CallbackQuery, state: FSMContext, **kwargs):
    if call.data == 'check_word_yes':
        async with state.proxy() as data:
            await call.answer()
            if len(data['check_word']) <4:
                await check_word(call.message, state)
            else:
                await manager(call.message, state)
            await call.answer("yes!")
    else:
        async with state.proxy() as data:
            data['check_word'].pop()
        await call.answer("no!")
        await check_word(call.message, state)        

def register_check_word(dp: Dispatcher):
    dp.register_callback_query_handler(check_word_answer, Text(startswith='check_word_'), state=Exersice.check_word)


async def trans_list(message: Message, state: FSMContext, word):
    await Exersice.trans_list.set()
    await state.update_data(trans_list = word)
    await message.answer("выбор перевода")
    current_word = word
    await message.answer_voice(current_word[2], current_word[0] ,reply_markup=trans_list_keyboard(current_word[1]))


async def trans_list_answer(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        word = data['trans_list']
        current_word = data['trans_list'][1]
    if call.data == 'trans_list_' + current_word:
        await call.answer("yes!")
        await manager(call.message, state)
    else:
        await add_mistakes(trans_list, word, state)
        await call.answer("no!")

def register_trans_list(dp: Dispatcher):
    dp.register_callback_query_handler(trans_list_answer, Text(startswith='trans_list_'), state=Exersice.trans_list)


async def trans_litters(message: Message, state: FSMContext, word: str):
    await Exersice.trans_litters.set()
    await state.update_data(trans_litters = {'word':word, 'litters': word[0]})
    await message.answer("перевод по буквам")
    current_word = word
    await message.answer(current_word[1] ,reply_markup=trans_litters_keyboard(current_word[0]))

async def trans_litters_answer(call: CallbackQuery, state: FSMContext):
    litter = call.data[-1]
    async with state.proxy() as data:
        current_word = data['trans_litters']['word']
        current_litter = data['trans_litters']['litters']
    if litter == current_litter[0]:
        if len(current_litter) == 1:
            await update_trans_litters(call, current_word, '')
            await manager(call.message, state)
        else:
            current_litter = current_litter[1:]
            async with state.proxy()as data:
                data['trans_litters']['litters'] = current_litter
            await update_trans_litters(call, current_word, current_litter)
        await call.answer('yes!')
    else:
        await add_mistakes(trans_litters, current_word, state)
        await call.answer('no!')

async def update_trans_litters(call: CallbackQuery, current_word: str, litters: str):
    with suppress(MessageNotModified):
        await call.message.edit_text(f'{current_word[1]}\n {str(current_word[0].replace(litters, "", 1))}', reply_markup=trans_litters_keyboard(litters))


def register_trans_litters(dp: Dispatcher):
    dp.register_callback_query_handler(trans_litters_answer, Text(startswith='trans_litters_'), state=Exersice.trans_litters)


async def trans_voice(message: Message, state: FSMContext, word: str):
    await Exersice.trans_voice.set()
    await state.update_data(trans_voice = word)
    current_word = word
    await message.answer_voice(current_word[2])

async def trans_voice_answer(message: Message, state: FSMContext):
    answer = message.text.lower()
    async with state.proxy() as data:
        current_word = data['trans_voice'][0]
        word = data['trans_voice']
    if answer == current_word:
        await message.answer("yes!")
        await manager(message, state)
    else:
        await add_mistakes(trans_voice, word, state)
        await message.answer('no!')


def register_trans_voice(dp: Dispatcher):
    dp.register_message_handler(trans_voice_answer, state=Exersice.trans_voice)


async def add_mistakes(exersice, word, state):
    mistake = {'function': exersice, 'word': word}
    async with state.proxy() as data:
        if data['sequence'][-1] != mistake:
            data['sequence'].append(mistake)



async def incorrect_answer(message: Message, state: FSMContext):
    await message.answer('Используйте клавиатуру на экране')

def register_incorrect_answer(dp: Dispatcher):
    dp.register_message_handler(incorrect_answer, state=Exersice.check_word, content_types=ContentTypes.ANY)
    dp.register_message_handler(incorrect_answer, state=Exersice.trans_list, content_types=ContentTypes.ANY)
    dp.register_message_handler(incorrect_answer, state=Exersice.trans_litters, content_types=ContentTypes.ANY)

