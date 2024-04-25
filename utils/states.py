from aiogram.fsm.state import StatesGroup, State


# Состояния бота
class QuestionsState(StatesGroup):
    passed = State()
    fio = State()
    age = State()
    first = State()
    second = State()
    third = State()
    fourth = State()
    fifth = State()
    sixth = State()
    seventh = State()
    eighth = State()
    ninth = State()
    tenth = State()
