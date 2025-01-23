from aiogram import Router, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from bot.services.words_training import words_training


router = Router()


class TrainingStates(StatesGroup):
    waiting_for_translation = State()


async def traversing_an_array(message: Message, state: FSMContext):
    print("<traversing_an_array>")
    user_id = message.from_user.id  # Получаем ID пользователя
    # Просим массив с данными для тренировки у объекта <words_training>
    user_data = await words_training.get_user_data_array(user_id)
    # Получаем данные, которые хранятся в состоянии
    state_data = await state.get_data()
    # получаем из state_data индексы, по котым будем выдёргивать объект из массива user_data. В сущности тут механика обхода массива
    curr_i_main = state_data.get('curr_i_main', 0)
    curr_i_translations = state_data.get('curr_i_translations', 0)
    print()
    if curr_i_main < len(user_data) and curr_i_translations >= len(user_data[curr_i_main]['translations']):
        curr_i_main += 1
        curr_i_translations = 0

    if curr_i_main >= len(user_data):
        # тут можно впихнуть отображение результатов тренировкки
        # сброс состояния, обход массива завершён
        print('Обход завершён')
        await state.clear()
        return
    await state.update_data(curr_i_translations=curr_i_translations, curr_i_main=curr_i_main)
    ###
    learning_word = user_data[curr_i_main]['word']
    learning_word_lang = user_data[curr_i_main]['lang']
    pos_en = user_data[curr_i_main]['translations'][curr_i_translations]['pos_en']
    pos_ru = user_data[curr_i_main]['translations'][curr_i_translations]['pos_ru']
    translation_words_list = user_data[curr_i_main]['translations'][curr_i_translations]['words_list']

    # Эмуляция отправци сообщения с вопросом пользователю
    print('тут эмуляция сообщения для пользователя')
    print(learning_word, pos_en, translation_words_list)



@router.message(TrainingStates.waiting_for_translation)
async def check_translation(message: Message, state: FSMContext):
    print("<check_translation>")
    state_data = await state.get_data()
    curr_i_main = state_data.get('curr_i_main', 0)
    curr_i_translations = state_data.get('curr_i_translations', 0)
    print('тут получаем элемент массива по индексам как в <traversing_an_array>')
    print('передаём ответ и элемент массива в обработчик')
    if message.text == 'Да':
        print('Выход из состояния')
        await state.clear()

    #  инкрементируемся по единице на каждый индекс
    curr_i_translations += 1

    # аписываем в state
    await state.update_data(curr_i_translations=curr_i_translations)
    # вызываем функцию обхода массива
    await traversing_an_array(message, state)

