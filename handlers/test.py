import os
import random

from aiogram import Router, Bot, F, Dispatcher
from aiogram.exceptions import TelegramForbiddenError
from aiogram.filters import Command
from aiogram.filters import StateFilter
from aiogram.filters.chat_member_updated import \
    ChatMemberUpdatedFilter, MEMBER, KICKED, LEFT, RESTRICTED, ADMINISTRATOR, CREATOR
from aiogram.fsm.context import FSMContext, StorageKey
from aiogram.types import Message, ChatMemberUpdated

from keyboards.result import result_kb
from keyboards.start_test import kb
from keyboards.test import question
from utils.db import Database
from utils.functions import send_questions, result
from utils.states import QuestionsState

router = Router()


# Обработчик команды /start
@router.message(Command(commands=['start']), StateFilter(None))
async def start_test(message: Message, bot: Bot, state: FSMContext):
    # Проверка, что пользователь подписан на канал
    user_channel_status = await bot.get_chat_member(chat_id=(os.getenv('ID_CHANNEL')), user_id=message.from_user.id)
    if user_channel_status.status in ['member', 'creator', 'administrator']:
        db = Database(os.getenv('DATABASE_NAME'))
        try:
            # Пробуем узнать проходил ли пользователь тест
            user_passed = db.select_from_users_table(column_name='passed', user_id=message.from_user.id)
            db.update_user_data('passed', 0, user_id=message.from_user.id)
            if user_passed == 1:
                # Если уже проходил
                await message.answer('Вы уже проходили тест☺️')
            else:
                # Если ещё не проходил тест
                db.add_user(user_id=message.from_user.id, status=user_channel_status.status, passed=0)
                await message.answer('Желаете пройти тест?', reply_markup=kb)
                await state.set_state(QuestionsState.passed)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            # Если не получилось достать значение passed (Если пользователя ещё нет в БД)
            db.add_user(message.from_user.id, user_channel_status.status, 0)
            await message.answer('Желаете пройти тест?', reply_markup=kb)
            await state.set_state(QuestionsState.passed)
    else:
        # Если пользователь не подписан на канал
        await message.answer(f'Для начала подпишитесь на наш канал ☺️: {os.getenv("LINK")}')


@router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=(KICKED | LEFT | RESTRICTED) >> (ADMINISTRATOR | CREATOR | MEMBER)
                            )
)
async def on_channel_join(event: ChatMemberUpdated, bot: Bot):
    # Проверяем, что это обновление от нужного канала
    if event.chat.id == int(os.getenv('ID_CHANNEL')):
        try:
            await event.bot.send_message(chat_id=event.from_user.id,
                                         text="Поздравляю с подпиской!🎉\nПриступим к прохождению теста?",
                                         reply_markup=kb)
            db = Database(os.getenv('DATABASE_NAME'))
            db.add_user(event.from_user.id, event.new_chat_member.status, 0)
            dp = Dispatcher()
            state: FSMContext = FSMContext(
                storage=dp.storage,
                key=StorageKey(chat_id=event.from_user.id, user_id=event.from_user.id, bot_id=bot.id))
            await state.update_data()
            await state.set_state(QuestionsState.passed)
        except TelegramForbiddenError as e:
            print(f"Ошибка: бот был заблокирован пользователем. {e}")
        except Exception as e:
            print(f"Ошибка: {e}")


@router.chat_member(
    ChatMemberUpdatedFilter(member_status_changed=(ADMINISTRATOR | CREATOR | MEMBER) >> (KICKED | LEFT | RESTRICTED)
                            )
)
async def channel_left(event: ChatMemberUpdated, bot: Bot):
    if event.chat.id == int(os.getenv('ID_CHANNEL')):
        try:
            await event.bot.send_message(chat_id=event.from_user.id,
                                         text="Для продолжения тестирования, пожалуйста, подпишитесь на наш канал: https://t.me/mypervie31")
            db = Database(os.getenv('DATABASE_NAME'))
            db.add_user(event.from_user.id, event.new_chat_member.status, 0)
            dp = Dispatcher()
            state: FSMContext = FSMContext(
                storage=dp.storage,
                key=StorageKey(chat_id=event.from_user.id, user_id=event.from_user.id, bot_id=bot.id))
            await state.update_data()
            await state.set_state(QuestionsState.passed)
        except TelegramForbiddenError as e:
            print(f"Ошибка: бот был заблокирован пользователем. {e}")
        except Exception as e:
            print(f"Ошибка: {e}")


# Хэндлер для начала самого теста (подтверждение от пользователя)
@router.message(QuestionsState.passed and F.text.lower().in_(['да', 'хочу', 'желаю']))
async def positive_answer(message: Message, state: FSMContext):
    await message.answer(f"Замечательно! Введите ФИО: \n"
                         f"(тестирование можно пройти только один раз, поэтому внимательно вводите свои данные❗️)")
    await state.set_state(QuestionsState.fio)


# Хэндлер на отмену теста
@router.message(QuestionsState.passed and F.text.lower().in_(['нет', 'не хочу', 'в другой раз']))
async def negative_answer(message: Message, state: FSMContext):
    await message.answer(text='Очень жаль 😔\nВы всегда сможете пройти тест, воспользовавшись командой /start')
    await state.clear()


# Переход в состояние ввода ФИО. Реагирует только на корректно введённое ФИО
@router.message(QuestionsState.fio, lambda message: message.text == message.text.isalpha() or ' ' in message.text)
async def correct_fio(message: Message, state: FSMContext):
    db = Database(os.getenv('DATABASE_NAME'))
    db.update_user_data(column_name='fio', value=message.text, user_id=message.from_user.id)
    await message.answer('Молодец! В каком классе Вы учитесь (Введите только число):')
    await state.set_state(QuestionsState.age)


# Бот реагирует только на правильно введённый возраст
@router.message(QuestionsState.age, lambda message: message.text.isdigit() and 1 <= int(message.text) <= 11)
async def correct_class(message: Message, state: FSMContext):
    db = Database(os.getenv('DATABASE_NAME'))
    db.update_user_data(column_name='class', value=int(message.text), user_id=message.from_user.id)
    if 1 <= int(message.text) <= 4:
        await state.update_data(category=1)
    elif 5 <= int(message.text) <= 6:
        await state.update_data(category=2)
    elif 7 <= int(message.text) <= 11:
        await state.update_data(category=3)
    await message.answer('Здорово! Начнём тест')
    await state.update_data(numbers=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    data = (await state.get_data())
    category = data['category']
    numbers = data['numbers']
    random.shuffle(numbers)
    number_of_question = numbers.pop()
    await message.answer(
        text=f'<u>1-й вопрос:</u>\n\n<b>{send_questions(number=number_of_question, category=category)}</b>',
        reply_markup=await question(number_of_question, category=category))
    await state.update_data(numbers=numbers, used_numbers=[number_of_question])
    await state.set_state(QuestionsState.first)


# Хэндлер на неправильно введённый класс
@router.message(QuestionsState.age)
async def incorrect_class(message: Message):
    await message.answer('В каком классе Вы учитесь? Введите число от 1 до 11')


# Хэндлер на неправильно введённое ФИО
@router.message(QuestionsState.fio)
async def incorrect_fio(message: Message):
    await message.answer('Введите ФИО (Иванов Иван Иванович - пример)')


# Переход в состояние первого вопроса
@router.message(QuestionsState.first)
async def first(message: Message, state: FSMContext):
    # save_first()
    db = Database(os.getenv('DATABASE_NAME'))
    db.update_user_data(column_name='first_question', value=message.text, user_id=message.from_user.id)
    data = (await state.get_data())
    category = data['category']
    numbers = data['numbers']
    number_of_question = numbers.pop()
    used_numbers = data['used_numbers']
    used_numbers.append(number_of_question)
    await message.answer(
        text=f'<u>2-й вопрос:</u>\n\n<b>{send_questions(number=number_of_question, category=category)}</b>',
        reply_markup=await question(number_of_question, category=category))
    await state.update_data(numbers=numbers,
                            used_numbers=used_numbers)
    await state.set_state(QuestionsState.second)


# Переход в состояние второго вопроса
@router.message(QuestionsState.second)
async def second(message: Message, state: FSMContext):
    # save_second()
    db = Database(os.getenv('DATABASE_NAME'))
    db.update_user_data(column_name='second_question', value=message.text, user_id=message.from_user.id)
    data = (await state.get_data())
    category = data['category']
    numbers = data['numbers']
    number_of_question = numbers.pop()
    used_numbers = data['used_numbers']
    used_numbers.append(number_of_question)
    await message.answer(
        text=f'<u>3-й вопрос:</u>\n\n<b>{send_questions(number=number_of_question, category=category)}</b>',
        reply_markup=await question(number_of_question, category=category))
    await state.update_data(numbers=numbers,
                            used_numbers=used_numbers)
    await state.set_state(QuestionsState.third)


# Переход в состояние третьего вопроса
@router.message(QuestionsState.third)
async def third(message: Message, state: FSMContext):
    # save_third()
    db = Database(os.getenv('DATABASE_NAME'))
    db.update_user_data(column_name='third_question', value=message.text, user_id=message.from_user.id)
    data = (await state.get_data())
    category = data['category']
    numbers = data['numbers']
    number_of_question = numbers.pop()
    used_numbers = data['used_numbers']
    used_numbers.append(number_of_question)
    await message.answer(
        text=f'<u>4-й вопрос:</u>\n\n<b>{send_questions(number=number_of_question, category=category)}</b>',
        reply_markup=await question(number_of_question, category=category))
    await state.update_data(numbers=numbers,
                            used_numbers=used_numbers)
    await state.set_state(QuestionsState.fourth)


# Переход в состояние четвёртого вопроса
@router.message(QuestionsState.fourth)
async def fourth(message: Message, state: FSMContext):
    # save_fourth()
    db = Database(os.getenv('DATABASE_NAME'))
    db.update_user_data(column_name='fourth_question', value=message.text, user_id=message.from_user.id)
    data = (await state.get_data())
    category = data['category']
    numbers = data['numbers']
    number_of_question = numbers.pop()
    used_numbers = data['used_numbers']
    used_numbers.append(number_of_question)
    await message.answer(
        text=f'<u>5-й вопрос:</u>\n\n<b>{send_questions(number=number_of_question, category=category)}</b>',
        reply_markup=await question(number_of_question, category=category))
    await state.update_data(numbers=numbers,
                            used_numbers=used_numbers)
    await state.set_state(QuestionsState.fifth)


# Переход в состояние пятого вопроса
@router.message(QuestionsState.fifth)
async def fifth(message: Message, state: FSMContext):
    # save_fifth()
    db = Database(os.getenv('DATABASE_NAME'))
    db.update_user_data(column_name='fifth_question', value=message.text, user_id=message.from_user.id)
    data = (await state.get_data())
    category = data['category']
    numbers = data['numbers']
    number_of_question = numbers.pop()
    used_numbers = data['used_numbers']
    used_numbers.append(number_of_question)
    await message.answer(
        text=f'<u>6-й вопрос:</u>\n\n<b>{send_questions(number=number_of_question, category=category)}</b>',
        reply_markup=await question(number_of_question, category=category))
    await state.update_data(numbers=numbers,
                            used_numbers=used_numbers)
    await state.set_state(QuestionsState.sixth)


# Переход в состояние шестого вопроса
@router.message(QuestionsState.sixth)
async def sixth(message: Message, state: FSMContext):
    # save_sixth()
    db = Database(os.getenv('DATABASE_NAME'))
    db.update_user_data(column_name='sixth_question', value=message.text, user_id=message.from_user.id)
    data = (await state.get_data())
    category = data['category']
    numbers = data['numbers']
    number_of_question = numbers.pop()
    used_numbers = data['used_numbers']
    used_numbers.append(number_of_question)
    await message.answer(
        text=f'<u>7-й вопрос:</u>\n\n<b>{send_questions(number=number_of_question, category=category)}</b>',
        reply_markup=await question(number_of_question, category=category))
    await state.update_data(numbers=numbers,
                            used_numbers=used_numbers)
    await state.set_state(QuestionsState.seventh)


# Переход в состояние седьмого вопроса
@router.message(QuestionsState.seventh)
async def seventh(message: Message, state: FSMContext):
    # save_seventh()
    db = Database(os.getenv('DATABASE_NAME'))
    db.update_user_data(column_name='seventh_question', value=message.text, user_id=message.from_user.id)
    data = (await state.get_data())
    category = data['category']
    numbers = data['numbers']
    number_of_question = numbers.pop()
    used_numbers = data['used_numbers']
    used_numbers.append(number_of_question)
    await message.answer(
        text=f'<u>8-й вопрос:</u>\n\n<b>{send_questions(number=number_of_question, category=category)}</b>',
        reply_markup=await question(number_of_question, category=category))
    await state.update_data(numbers=numbers,
                            used_numbers=used_numbers)
    await state.set_state(QuestionsState.eighth)


# Переход в состояние восьмого вопроса
@router.message(QuestionsState.eighth)
async def eighth(message: Message, state: FSMContext):
    # save_eighth()
    db = Database(os.getenv('DATABASE_NAME'))
    db.update_user_data(column_name='eighth_question', value=message.text, user_id=message.from_user.id)
    data = (await state.get_data())
    category = data['category']
    numbers = data['numbers']
    number_of_question = numbers.pop()
    used_numbers = data['used_numbers']
    used_numbers.append(number_of_question)
    await message.answer(
        text=f'<u>9-й вопрос:</u>\n\n<b>{send_questions(number=number_of_question, category=category)}</b>',
        reply_markup=await question(number_of_question, category=category))
    await state.update_data(numbers=numbers,
                            used_numbers=used_numbers)
    await state.set_state(QuestionsState.ninth)


# Переход в состояние девятого вопроса
@router.message(QuestionsState.ninth)
async def ninth(message: Message, state: FSMContext):
    # save_ninth()
    db = Database(os.getenv('DATABASE_NAME'))
    db.update_user_data(column_name='ninth_question', value=message.text, user_id=message.from_user.id)
    data = (await state.get_data())
    category = data['category']
    numbers = data['numbers']
    number_of_question = numbers.pop()
    used_numbers = data['used_numbers']
    used_numbers.append(number_of_question)
    await message.answer(
        text=f'<u>10-й вопрос:</u>\n\n<b>{send_questions(number=number_of_question, category=category)}</b>',
        reply_markup=await question(number_of_question, category=category))
    await state.update_data(numbers=numbers,
                            used_numbers=used_numbers)
    await state.set_state(QuestionsState.tenth)


# Переход в состояние десятого вопроса и завершение теста
@router.message(QuestionsState.tenth)
async def tenth(message: Message, state: FSMContext):
    # save_tenth()
    db = Database(os.getenv('DATABASE_NAME'))
    db.update_user_data(column_name='tenth_question', value=message.text, user_id=message.from_user.id)
    db.update_user_data(column_name='passed', value=1, user_id=message.from_user.id)
    data = (await state.get_data())
    used_numbers = data['used_numbers']
    category = data['category']
    # Занесение результата в базу данных (result - импортированная функция для подсчёта баллов)
    db.update_user_data(column_name='result', value=result(used_numbers, category, message.from_user.id)[0],
                        user_id=message.from_user.id)
    await message.answer(
        text=f'<b>Поздравляю!</b>🥳\nВаш результат: <u>{result(used_numbers, category, message.from_user.id)[0]}/10</u>')
    await message.answer(
        text=f"Ошибки❗️:\n\n{result(used_numbers, category, message.from_user.id)[1]}",
        reply_markup=result_kb)
    await state.clear()
