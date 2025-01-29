from aiogram import Router, F
from aiogram.types import Message
from bot.templates import text
from bot.globals import database
from bot.handlers.states import TrainingStates, traversing_an_array
from aiogram.fsm.context import FSMContext
from bot.services.words_training import words_training

from aiogram.types import Message, ReplyKeyboardRemove

# Создаем роутер для регистрации хендлеров
router = Router()


@router.message(F.text.startswith("/start"))
async def command_start_handler(message: Message):
    user_id = message.from_user.id  # Получаем ID пользователя

    # # Передаем ID пользователя в функцию, которая проверяет наличие в базе возвращает t\f. Подставить в is_new_user
    is_new_user: bool = await database.is_userid_in__user_configs(user_id)
    #
    if not is_new_user:  # Если ID пользователя нет в БД (is_new_user=False)
        await database.add_row__user_configs(user_id)
        await message.answer(
            text.start_command(message.from_user.first_name, is_new_user)
        )
    else:
        await message.answer(
            text.start_command(message.from_user.first_name, is_new_user)
        )
    # Если пользователя уже нет в базе (False), ничего не делаем

@router.message(F.text.startswith("/help"))
async def command_start_handler(message: Message):
    await message.answer(text='логика комманды /help в процессе запила')


@router.message(F.text.startswith("/training"))
async def start_training(message: Message, state: FSMContext):
    await state.set_state(TrainingStates.waiting_for_translation)
    await traversing_an_array(message, state)


@router.message(F.text.startswith("/break"))
async def stop_training(message: Message, state: FSMContext):
    try:
        words_training.users_training_statistics[message.from_user.id].clear()
        await state.clear()
        await message.answer(text='Прервано',
                             reply_markup=ReplyKeyboardRemove())
    except KeyError:
        return


# @router.message(TrainingStates.waiting_for_translation)
# async def check_translation(message: Message, state: FSMContext):
#     data = await state.get_data()
#     current_index = data.get('current_index', 0)
#     correct_translation = word_pairs[current_index][1]
#
#     if message.text.lower() == correct_translation.lower():
#         await message.answer("Правильно!")
#     else:
#         await message.answer(f"Неправильно. Правильный ответ: {correct_translation}")
#
#     await state.update_data(current_index=current_index + 1)
#     await send_next_word(message, state)


