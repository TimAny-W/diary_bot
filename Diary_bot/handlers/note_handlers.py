from aiogram import types, Dispatcher
from aiogram.utils import markdown as md
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from database import Database
from keyboards import start_kb, cancel_kb, choice_kb

db = Database('user.db')


class GetNoteFSM(StatesGroup):
    get_num_note = State()


class AddNoteFSM(StatesGroup):
    get_text_note = State()


class SupplementNote(StatesGroup):
    get_text_note = State()


class DeleteNote(StatesGroup):
    get_text_note = State()


async def start_message(message: types.Message):
    """Start message"""
    await message.answer('Привет,я твой личный дневник!\nМожешь писать суда все что угодно', reply_markup=start_kb)


async def supplement_note(message: types.Message, state: FSMContext):
    """Complements the existing note of today"""
    id = int(message.from_user.id)
    if not db.check_no_notes(id):
        await message.answer('У тебя еще нет записей\nсоздай с помощью /add_note')
        return

    note = db.get_note(id, db.get_amount_of_days(id))
    await message.answer(f'Последняя запись \n {note[2]}', reply_markup=cancel_kb)
    await message.answer('Введите текст')
    await SupplementNote.next()


async def get_text_for_supplement(message: types.Message, state: FSMContext):
    """Get new text for note"""
    text = message.text

    db.edit_last_note(message.from_user.id, text)
    await message.answer('Запись успешно дополнена!', reply_markup=start_kb)
    await state.finish()


async def get_note(message: types.Message, state: FSMContext):
    """Entry in process to getting note,by day number"""
    user_id = message.from_user.id

    if not db.check_no_notes(user_id):
        await message.answer('У вас еще нет записей\nСоздайте с помощью /add_note')
        return
    else:
        await message.answer(f'Выберите запись 1 - {db.get_amount_of_days(user_id)}',
                             reply_markup=cancel_kb)
        await GetNoteFSM.next()


async def delete_last_note(message: types.Message, state: FSMContext):
    """Delete note"""
    if not db.check_no_notes(message.from_user.id):
        await message.answer('У вас еще нет записей\nСоздайте с помощью /add_note')
        return
    else:
        await message.answer('Удалить последнюю запись?', reply_markup=choice_kb)

        await DeleteNote.next()


async def get_delete_text(message: types, state: FSMContext):
    """Getting num of day to delete"""

    if message.text.lower() == 'да':
        db.delete(message.from_user.id, db.get_amount_of_days(message.from_user.id))
        await message.answer('Запись успешно удалена', reply_markup=start_kb)

    elif message.text.lower() == 'нет':
        await message.answer('Отменяем...', reply_markup=start_kb)

    else:
        await message.answer("Неверный формат ввода", reply_markup=start_kb)

    await state.finish()


async def get_text_note(message: types.Message, state: FSMContext):
    """Getting sequence number of note"""
    try:
        note = db.get_note(message.from_user.id, int(message.text))
    except ValueError:
        await message.answer("Неверный формат ввода")
        return

    await message.answer(md.text(f'Запись #{note[2]}'))
    await message.answer(md.text(f'{note[3]}'), reply_markup=start_kb)

    await state.finish()


async def add_note(message: types.Message, state: FSMContext):
    """Entry in process of creating note"""
    await message.answer('Введите текст', reply_markup=cancel_kb)
    await AddNoteFSM.next()


async def get_add_text(message: types.Message, state: FSMContext):
    """Getting text of note and creating note, after doing command 'add_note'"""
    text = message.text
    user_id = message.from_user.id

    db.add_note(user_id, text)

    await message.answer('Запись успешно добавлена', reply_markup=start_kb)
    await state.finish()


async def cancel_command(message: types.Message, state: FSMContext):
    """Cancel action"""
    await state.finish()
    await message.answer("Действие успешно отменено", reply_markup=start_kb)


def register_handlers(dp: Dispatcher):
    """Register handlers"""
    dp.register_message_handler(cancel_command, Text(equals=['Отменить', '/cancel']), state='*')

    dp.register_message_handler(start_message, commands=['start'])

    dp.register_message_handler(get_note, Text(equals=['Мои записи', '/my_notes']))
    dp.register_message_handler(get_text_note, state=GetNoteFSM.get_num_note)

    dp.register_message_handler(add_note, Text(equals=['Добавить запись', '/add_note']), state='*')
    dp.register_message_handler(get_add_text, state=AddNoteFSM.get_text_note)

    dp.register_message_handler(supplement_note, Text(equals=['Дополнить запись', '/edit_last_note']),
                                state='*')
    dp.register_message_handler(get_text_for_supplement, state=SupplementNote.get_text_note)

    dp.register_message_handler(delete_last_note, Text(equals=['Удалить запись', '/delete_note']), state='*')
    dp.register_message_handler(get_delete_text, state=DeleteNote.get_text_note)
