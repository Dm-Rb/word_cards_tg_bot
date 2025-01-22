from aiogram import Router, F
from aiogram.types import Message
from bot.templates import text
from bot.globals import database
from bot.services.words_training import words_training
from bot.handlers.states import TrainingStates
from aiogram.fsm.context import FSMContext


# Импортируем функцию или объект для работы с базой данных
# Создаем роутер для регистрации хендлеров
router = Router()
word_pairs = [("apple", "яблоко"), ("dog", "собака"), ("book", "книга")]

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




# Обработка команды /training
@router.message(F.text.startswith("/training"))
async def start_training(message: Message, state: FSMContext):
    await state.update_data(current_index=0)
    await send_next_word(message, state)


async def send_next_word(message: Message, state: FSMContext):
    data = await state.get_data()
    current_index = data.get('current_index', 0)

    if current_index < len(word_pairs):
        english_word = word_pairs[current_index][0]
        await message.answer(f"Переведите слово: {english_word}")
        await state.set_state(TrainingStates.waiting_for_translation)
    else:
        await message.answer("Тренировка завершена!")
        await state.clear()

@router.message(TrainingStates.waiting_for_translation)
async def check_translation(message: Message, state: FSMContext):
    data = await state.get_data()
    current_index = data.get('current_index', 0)
    correct_translation = word_pairs[current_index][1]

    if message.text.lower() == correct_translation.lower():
        await message.answer("Правильно!")
    else:
        await message.answer(f"Неправильно. Правильный ответ: {correct_translation}")

    await state.update_data(current_index=current_index + 1)
    await send_next_word(message, state)


@router.message(F.text.startswith("/stop"))
async def stop_training(message: Message, state: FSMContext):
    await message.answer("Тренировка прервана.")
    await state.clear()