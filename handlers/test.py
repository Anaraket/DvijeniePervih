import os

from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from keyboards.result import result_kb
from keyboards.start_test import kb
from keyboards.test import question
from utils.db import Database
from utils.functions import send_questions, result, request
from utils.states import QuestionsState

router = Router()


# Проверяет правильность введённого ФИО
def fio_correct(message: Message):
    return message.text == message.text.isalpha() or ' ' in message.text


# Обработчик команды /start
@router.message(Command(commands=['start']))
async def command_start(message: Message):
    await message.answer(text="👋 Привет! Это бот для прохождения теста")


# Хэндлер для команды /test - запуск теста
@router.message(F.text.lower().in_(['/test', 'пройти тест', 'тест']), StateFilter(None))
async def check_subscription(message: Message, bot: Bot, state: FSMContext):
    # Проверка, что пользователь подписан на канал
    user_channel_status = await bot.get_chat_member(chat_id=(os.getenv('ID_CHANNEL')), user_id=message.from_user.id)
    if user_channel_status.status in ['member', 'creator', 'administrator']:
        db = Database(os.getenv('DATABASE_NAME'))
        try:
            # Пробуем узнать проходил ли пользователь тест
            users, *rest = db.select_passed(message.from_user.id)[0]
            #db.add_passed(0, message.from_user.id)
            if users == 1:
                # Если уже проходил
                await message.answer('Вы уже проходили тест')
            else:
                # Если ещё не проходил тест
                db.add_user(message.from_user.id, user_channel_status.status, 0)
                await message.answer('Желаете пройти тест?', reply_markup=kb)
                await state.set_state(QuestionsState.passed)
        except:
            # Если не получилось достать значение passed (Если пользователя ещё нет в БД)
            db.add_user(message.from_user.id, user_channel_status.status, 0)
            await message.answer('Желаете пройти тест?', reply_markup=kb)
            await state.set_state(QuestionsState.passed)
    else:
        # Если пользователь не подписан на канал
        await message.answer(f'Для начала подпишись на наш канал: {os.getenv('LINK')}')


# Хэндлер для начала самого теста (подтверждение от пользователя)
@router.message(QuestionsState.passed, F.text.lower().in_(['да', 'хочу', 'желаю']))
async def pozitive_answer(message: Message, state: FSMContext):
    await message.answer(f"Замечательно!\nВведите ФИО:")
    await state.set_state(QuestionsState.fio)


# Хэндлер на отмену теста
@router.message(QuestionsState.passed, F.text.lower().in_(['нет', 'не хочу', 'в другой раз', 'неет']))
async def negative_answer(message: Message, state: FSMContext):
    await message.answer(text='Очень жаль :(\nВы всегда сможете пройти тест, воспользовавшись командой "/test"')
    await state.clear()


# Переход в состояние ввода ФИО
@router.message(QuestionsState.fio, fio_correct)
async def correct_fio(message: Message, state: FSMContext):
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_fio(fio=message.text, user_id=message.from_user.id)
    await message.answer('Класс! Начнём тест')
    await message.answer(text=f'<u>1-й вопрос:</u>\n\n<b>{send_questions(1)}</b>', reply_markup=await question(1))
    await state.set_state(QuestionsState.first)


# Хэндлер на неправильно введённое имя
@router.message(QuestionsState.fio)
async def incorrect_fio(message: Message):
    await message.answer('Введите ФИО (Иванов Иван Иванович - пример)')


# Переход в состояние первого вопроса
@router.message(QuestionsState.first)
async def first(message: Message, state: FSMContext):
    # save_first()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_first(answer=message.text, user_id=message.from_user.id)
    await message.answer(text=f'<u>2-й вопрос:</u>\n\n<b>{send_questions(2)}</b>', reply_markup=await question(2))
    await state.set_state(QuestionsState.second)


# # Переход в состояние второго вопроса
@router.message(QuestionsState.second)
async def second(message: Message, state: FSMContext):
    # save_second()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_second(answer=message.text, user_id=message.from_user.id)
    await message.answer(text=f'<u>3-й вопрос:</u>\n\n<b>{send_questions(3)}</b>', reply_markup=await question(3))
    await state.set_state(QuestionsState.third)


# Переход в состояние третьего вопроса
@router.message(QuestionsState.third)
async def third(message: Message, state: FSMContext):
    # save_third()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_third(answer=message.text, user_id=message.from_user.id)
    await message.answer(text=f'<u>4-й вопрос:</u>\n\n<b>{send_questions(4)}</b>', reply_markup=await question(4))
    await state.set_state(QuestionsState.fourth)


# Переход в состояние четвёртого вопроса
@router.message(QuestionsState.fourth)
async def fourth(message: Message, state: FSMContext):
    # save_fourth()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_fourth(answer=message.text, user_id=message.from_user.id)
    await message.answer(text=f'<u>5-й вопрос:</u>\n\n<b>{send_questions(5)}</b>', reply_markup=await question(5))
    await state.set_state(QuestionsState.fifth)


# Переход в состояние пятого вопроса
@router.message(QuestionsState.fifth)
async def fifth(message: Message, state: FSMContext):
    # save_fifth()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_fifth(answer=message.text, user_id=message.from_user.id)
    await message.answer(text=f'<u>6-й вопрос:</u>\n\n<b>{send_questions(6)}</b>', reply_markup=await question(6))
    await state.set_state(QuestionsState.sixth)


# Переход в состояние шестого вопроса
@router.message(QuestionsState.sixth)
async def sixth(message: Message, state: FSMContext):
    # save_sixth()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_sixth(answer=message.text, user_id=message.from_user.id)
    await message.answer(text=f'<u>7-й вопрос:</u>\n\n<b>{send_questions(7)}</b>', reply_markup=await question(7))
    await state.set_state(QuestionsState.seventh)


# Переход в состояние седьмого вопроса
@router.message(QuestionsState.seventh)
async def seventh(message: Message, state: FSMContext):
    # save_seventh()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_seventh(answer=message.text, user_id=message.from_user.id)
    await message.answer(text=f'<u>8-й вопрос:</u>\n\n<b>{send_questions(8)}</b>', reply_markup=await question(8))
    await state.set_state(QuestionsState.eighth)


# Переход в состояние восьмого вопроса
@router.message(QuestionsState.eighth)
async def eighth(message: Message, state: FSMContext):
    # save_eighth()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_eighth(answer=message.text, user_id=message.from_user.id)
    await message.answer(text=f'<u>9-й вопрос:</u>\n\n<b>{send_questions(9)}</b>', reply_markup=await question(9))
    await state.set_state(QuestionsState.ninth)


# Переход в состояние девятого вопроса
@router.message(QuestionsState.ninth)
async def ninth(message: Message, state: FSMContext):
    # save_ninth()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_ninth(answer=message.text, user_id=message.from_user.id)
    await message.answer(text=f'<u>10-й вопрос:</u>\n\n<b>{send_questions(10)}</b>', reply_markup=await question(10))
    await state.set_state(QuestionsState.tenth)


# Переход в состояние десятого вопроса и завершение теста
@router.message(QuestionsState.tenth)
async def tenth(message: Message, state: FSMContext):
    # save_tenth()
    db = Database(os.getenv('DATABASE_NAME'))
    db.add_tenth(answer=message.text, user_id=message.from_user.id)
    db.add_passed(1, message.from_user.id)
    await state.clear()
    # Ваш результат (result - импортированная функция для подсчёта баллов)
    db.add_result(answer=result(db.select_columns(request, message.from_user.id)), user_id=message.from_user.id)
    await message.answer(
        text=f'Поздравляю!\nВаш результат: {result(db.select_columns(request, message.from_user.id))}/10',
        reply_markup=result_kb)
