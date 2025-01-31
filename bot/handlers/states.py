from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from bot.services.words_training import words_training


router = Router()


class TrainingStates(StatesGroup):
    waiting_for_translation = State()


async def traversing_an_array(message: Message, state: FSMContext):
    """
    Итерация по элементам списка с пользовательскими данными.
    Массив думерный (внутри элемента массива имеет подмассив)
    """
    user_id = message.from_user.id  # Получаем ID пользователя
    # Просим массив с данными для тренировки у объекта <words_training>
    user_data = await words_training.get_user_data_array(user_id)
    if not user_data:
        await message.answer(text="Ваш словарь пуст. Сперва добавьте слова для тенировки")
        await state.clear()
        return
    # Получаем данные, которые хранятся в состоянии
    state_data = await state.get_data()
    # Получаем из state_data индексы, по котым будем обращаться к объектам массива user_data.
    index_array = state_data.get('index_array', 0)
    index_subarray = state_data.get('index_subarray', 0)
    # Если индекс подмассива перевалил за len подмассива, перейти к следующему элемету массива (на верхнем уровне).
    if index_array < len(user_data) and index_subarray >= len(user_data[index_array]['translations']):
        index_array += 1
        index_subarray = 0
    # Если индекс элементов верхнего уровня больше или равно len массива - обход закончен
    if index_array >= len(user_data):
        # сброс состояния, обход массива завершён
        await message.answer(text=words_training.show_training_result(user_id), parse_mode='HTML',
                             reply_markup=ReplyKeyboardRemove())
        await state.clear()
        # Очищаем объект со результатами тренинга
        words_training.users_training_statistics[user_id].clear()
        return
    # Записывает индексы в хранилище объекта состояния
    await state.update_data(index_subarray=index_subarray, index_array=index_array)
    ###
    question_data = words_training.questions_controller(user_id, index_array, index_subarray)
    await message.answer(text=question_data['message_text'], parse_mode='HTML', reply_markup=question_data['keyboard'])


@router.message(TrainingStates.waiting_for_translation)
async def check_translation(message: Message, state: FSMContext):
    state_data = await state.get_data()
    index_array = state_data.get('index_array', 0)
    index_subarray = state_data.get('index_subarray', 0)
    # Проверяем ответ пользователя
    words_training.check_answer_without_context(message.text, message.from_user.id, index_array, index_subarray)
    #  инкрементируемся по единице на каждый индекс
    index_subarray += 1
    # аписываем в state
    await state.update_data(index_subarray=index_subarray)
    # вызываем функцию обхода массива
    await traversing_an_array(message, state)



