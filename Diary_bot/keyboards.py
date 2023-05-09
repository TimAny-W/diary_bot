from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, \
    KeyboardButton

start_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton('Мои записи'),
    KeyboardButton('Добавить запись'),
    KeyboardButton('Дополнить запись'),
    KeyboardButton('Удалить запись')
)
cancel_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton('Отменить')
)
choice_kb = ReplyKeyboardMarkup(resize_keyboard=True).row(
    KeyboardButton('Да'),
    KeyboardButton('Нет')
)
# start_kb = InlineKeyboardMarkup(resize_keyboard=True).row(
# InlineKeyboardButton('Мои записи', callback_data='all_notes'),
# InlineKeyboardButton('Дополнить запись этого дня', callback_data='update_note')
# )
