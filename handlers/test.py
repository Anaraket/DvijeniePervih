from aiogram import Router, Bot, F
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from keyboards.start_test import kb
from utils.states import QuestionsState
from keyboards.test import question
from utils.questions import questions
from keyboards.result import result_kb
from aiogram.types import Message
from aiogram.filters import Command
import os
from utils.db import Database

router = Router()


def send_questions(number: int):
    message = questions[number - 1]["question"]
    return message


def fio_correct(message: Message):
    return message.text == message.text.isalpha() or ' ' in message.text


# @router.message(Command(commands=['start']))
# async def command_start(message: Message, bot: Bot):
#     db = Database(os.getenv('DATABASE_NAME'))
#     await bot.send_message(chat_id=message.from_user.id, text="👋 Привет! Это бот для прохождения теста")

@router.message(F.text.lower().in_(['/test', 'пройти тест', 'тест']), StateFilter(None))
async def check_subscription(message: Message, bot: Bot, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id=-1002004860176, user_id=message.from_user.id)
    if user_channel_status.status not in ['left', 'kicked']:
        # Занесение пользователя в базу данных
        # cursor.execute('''
        #     INSERT OR IGNORE INTO users (telegram_id, status)
        #     VALUES (?, ?)
        # ''', (message.from_user.id, user_channel_status.status))
        # conn.commit()
        print(user_channel_status.status)
        await message.answer('Желаете пройти тест? (да/нет)', reply_markup=kb)
        await state.set_state(QuestionsState.passed)
    else:
        await message.answer('Для начала подпишись на наш канал: https://t.me/+iv10xEEruWNmOWJi')


@router.message(F.text.lower().in_(['да', 'хочу', 'желаю']), QuestionsState.passed)
async def pozitive_answer(message: Message, state: FSMContext):
    # set_passed_null()
    # пока что так:
    await state.update_data(passed=0)
    await message.answer(f"Замечательно!\nВведите ФИО:")
    await state.set_state(QuestionsState.fio)


@router.message(QuestionsState.passed, F.text.lower().in_(['нет', 'не хочу', 'в другой раз', 'неет']))
async def negative_answer(message: Message, state: FSMContext):
    await message.answer(text='Очень жаль :(\nВы всегда сможете пройти тест, воспользовавшись командой "/test"')
    await state.set_state(None)


@router.message(QuestionsState.fio, fio_correct)
async def correct_fio(message: Message, state: FSMContext):
    # save_fio()
    await state.update_data(fio=message.text)
    await message.answer('Класс! Начнём тест')
    await message.answer(text=f'<u>1-й вопрос:</u>\n\n<b>{send_questions(1)}</b>', reply_markup=await question(1))
    await state.set_state(QuestionsState.first)


@router.message(QuestionsState.fio)
async def incorrect_fio(message: Message, state: FSMContext):
    await message.answer('Введите ФИО (Иванов Иван Иванович - пример)')


@router.message(QuestionsState.first)
async def first(message: Message, state: FSMContext):
    # save_first()
    await state.update_data(first=message.text)
    await message.answer(text=f'<u>2-й вопрос:</u>\n\n<b>{send_questions(2)}</b>', reply_markup=await question(2))
    await state.set_state(QuestionsState.second)


@router.message(QuestionsState.second)
async def second(message: Message, state: FSMContext):
    # save_second()
    await state.update_data(second=message.text)
    await message.answer(text=f'<u>3-й вопрос:</u>\n\n<b>{send_questions(3)}</b>', reply_markup=await question(3))
    await state.set_state(QuestionsState.third)


@router.message(QuestionsState.third)
async def third(message: Message, state: FSMContext):
    # save_third()
    await state.update_data(third=message.text)
    await message.answer(text=f'<u>4-й вопрос:</u>\n\n<b>{send_questions(4)}</b>', reply_markup=await question(4))
    await state.set_state(QuestionsState.fourth)


@router.message(QuestionsState.fourth)
async def fourth(message: Message, state: FSMContext):
    # save_fourth()
    await state.update_data(fourth=message.text)
    await message.answer(text=f'<u>5-й вопрос:</u>\n\n<b>{send_questions(5)}</b>', reply_markup=await question(5))
    await state.set_state(QuestionsState.fifth)


@router.message(QuestionsState.fifth)
async def fifth(message: Message, state: FSMContext):
    # save_fifth()
    await state.update_data(fifth=message.text)
    await message.answer(text=f'<u>6-й вопрос:</u>\n\n<b>{send_questions(6)}</b>', reply_markup=await question(6))
    await state.set_state(QuestionsState.sixth)


@router.message(QuestionsState.sixth)
async def sixth(message: Message, state: FSMContext):
    # save_sixth()
    await state.update_data(sixth=message.text)
    await message.answer(text=f'<u>7-й вопрос:</u>\n\n<b>{send_questions(7)}</b>', reply_markup=await question(7))
    await state.set_state(QuestionsState.seventh)


@router.message(QuestionsState.seventh)
async def seventh(message: Message, state: FSMContext):
    # save_seventh()
    await state.update_data(seventh=message.text)
    await message.answer(text=f'<u>8-й вопрос:</u>\n\n<b>{send_questions(8)}</b>', reply_markup=await question(8))
    await state.set_state(QuestionsState.eighth)


@router.message(QuestionsState.eighth)
async def eighth(message: Message, state: FSMContext):
    # save_eighth()
    await state.update_data(eighth=message.text)
    await message.answer(text=f'<u>9-й вопрос:</u>\n\n<b>{send_questions(9)}</b>', reply_markup=await question(9))
    await state.set_state(QuestionsState.ninth)


@router.message(QuestionsState.ninth)
async def ninth(message: Message, state: FSMContext):
    # save_ninth()
    await state.update_data(ninth=message.text)
    await message.answer(text=f'<u>10-й вопрос:</u>\n\n<b>{send_questions(10)}</b>', reply_markup=await question(10))
    await state.set_state(QuestionsState.tenth)


@router.message(QuestionsState.tenth)
async def tenth(message: Message, state: FSMContext):
    # save_tenth()
    await state.update_data(tenth=message.text)
    await state.set_state(None)
    await message.answer(text='Ура', reply_markup=result_kb)
    # Ваш результат
