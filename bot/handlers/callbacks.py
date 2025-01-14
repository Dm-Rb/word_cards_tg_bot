from aiogram import Router
from aiogram.types import CallbackQuery


router = Router()


@router.callback_query(lambda callback: callback.data.startswith("yes:") or callback.data.startswith("no:"))
async def process_word_response(callback: CallbackQuery):
    # Извлекаем данные из callback_data
    action, word = callback.data.split(":")

    if action == "yes":
        # Логика для добавления слова в словарь
        await callback.message.answer(f"Слово '{word}' добавлено в ваш словарь!")
    elif action == "skip_word":
        # Логика для пропуска слова
        await callback.message.answer(f"Слово '{word}' пропущено.")

    # Уведомляем Telegram, что callback обработан
    await callback.answer()