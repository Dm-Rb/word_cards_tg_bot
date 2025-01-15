from aiogram import Router
from aiogram.types import CallbackQuery


router = Router()


@router.callback_query(lambda callback: callback.data.startswith("yes:") or callback.data.startswith("no:"))
async def process_word_response(callback: CallbackQuery):
    # Извлекаем данные из callback_data
    action, word = callback.data.split(":")

    if action == "yes":
        # Логика для добавления слова в словарь
        print('y')
        await callback.answer(f"{word.capitalize()}; добавлено в ваш словарь!", show_alert=True)
    elif action == "no":
        print('n')

        # pass
        # Логика для пропуска слова

    # Удаляем сообщение вместе с клавиатурой
    await callback.message.delete()
    # Уведомляем Telegram, что callback обработан

    await callback.answer()