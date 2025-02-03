from aiogram import Router
from aiogram.types import CallbackQuery
from bot.globals import database
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from bot.handlers.states import traversing_an_array

router = Router()


@router.callback_query(lambda callback: callback.data.startswith("yes:") or callback.data.startswith("no:"))
async def process_word_response(callback: CallbackQuery):
    # Извлекаем данные из callback_data
    action, word, word_id, user_id, fuc_type = callback.data.split(":")
    # "yes:{word}:{str(word_id)}:{str(user_id)}:{fuc_type}"
    if action == "yes":
        if fuc_type == 'add':
            await database.add_row__user_data(user_id, int(word_id))
            await callback.answer(f"{word.capitalize()}\n добавлено в словарь изучения!", show_alert=False)
        elif fuc_type == 'del':
            await database.del_row__user_data(user_id, int(word_id))
            await callback.answer(f"{word.capitalize()}\n удалено из словаря изучения!", show_alert=False)

    # Удаляем сообщение вместе с клавиатурой
    await callback.message.delete()
    # Уведомляем Telegram, что callback обработан
    await callback.answer()

@router.callback_query(lambda callback: callback.data.startswith("continue:"))
async def process_continue(callback: CallbackQuery, state: FSMContext):
    # Извлекаем данные из callback_data
    action, index_array, index_subarray = callback.data.split(":")
    # "yes:{word}:{str(word_id)}:{str(user_id)}:{fuc_type}"

    # await callback.answer(f"{word.capitalize()}\n добавлено в словарь изучения!", show_alert=False)
    index_array = int(index_array) + 1
    # Не работает дозапись в state
    await state.update_data(index_subarray=index_subarray, index_array=int(index_array))
    await traversing_an_array(callback.message, state)
    # Удаляем сообщение вместе с клавиатурой
    await callback.message.delete()
    # Уведомляем Telegram, что callback обработан
    await callback.answer()
