from aiogram.fsm.state import State, StatesGroup


class TrainingStates(StatesGroup):
    waiting_for_translation = State()
