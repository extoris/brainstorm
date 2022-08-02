from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from random import shuffle
from data.db_control import get_example_words
from data.config import DATABASE_NAME


begin_exersice = InlineKeyboardMarkup(inline_keyboard=[
    [
    InlineKeyboardButton(text="выбрать слова", callback_data="begin")
    ]
])

end_exersice = InlineKeyboardMarkup(inline_keyboard=[
    [
    InlineKeyboardButton(text="закончить", callback_data="end")
    ]
])

check_word_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [
    InlineKeyboardButton(text="YES", callback_data='check_word_yes'),
    InlineKeyboardButton(text="NO", callback_data='check_word_no')
    ]
])

def trans_list_keyboard(word):
    example_words = get_example_words(DATABASE_NAME)
    list_buttons=[
        [
            InlineKeyboardButton(text=word, callback_data=f'trans_list_{word}')
        ],
        [
            InlineKeyboardButton(text=example_words[0], callback_data=f'trans_list_{example_words[0]}')
        ],
        [
            InlineKeyboardButton(text=example_words[1], callback_data=f'trans_list_{example_words[1]}')
        ],
        [
            InlineKeyboardButton(text=example_words[2], callback_data=f'trans_list_{example_words[2]}')
        ],
        [
            InlineKeyboardButton(text=example_words[3], callback_data=f'trans_list_{example_words[3]}')
        ]
        ]
    shuffle(list_buttons)
    return InlineKeyboardMarkup(inline_keyboard=list_buttons)

def trans_litters_keyboard(word):
    litters = list(word)
    shuffle(litters)
    list_buttons = []
    for litter in litters:
        list_buttons.append(InlineKeyboardButton(text=litter, callback_data=f'trans_litters_{litter}'))
    keyboard = InlineKeyboardMarkup(row_width=5)
    keyboard.add(*list_buttons)
    return keyboard