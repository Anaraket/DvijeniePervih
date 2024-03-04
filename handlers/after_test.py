import os

from aiogram import Router, F, Bot
from aiogram.types import Message

from utils.db import Database
from utils.questions import questions

router = Router()

request = ['user_id',
           'status',
           'passed',
           'fio',
           'first_question',
           'second_question',
           'third_question',
           'fourth_question',
           'fifth_question',
           'sixth_question',
           'seventh_question',
           'eighth_question',
           'ninth_question',
           'tenth_question',
           'result']


@router.message(F.text.lower().in_(['посмотреть ошибки']))
async def show_mistakes(message: Message, bot: Bot):
    db = Database(os.getenv('DATABASE_NAME'))
    mistakes = []
    answers = db.select_columns(column_names=request[4:-1], user_id=message.from_user.id)
    correct_answers = [question['correct_answer'] for question in questions]

    # print(mistakes)
    # print(answers)
    # print(correct_answers)
    # print('--------------')
    for index, answer in enumerate(answers):
        if answer != correct_answers[index]:
            mistakes.append((index + 1, answer))
    # print(mistakes)
    # print('**************')
    mistakes_answer = []
    for j in mistakes:
        # j - кортеж (j[0] - номер вопроса, j[1] - неправильный ответ)
        # print(j, j[0], j[1])
        mistake_str = f'Вопрос {j[0]}: {questions[j[0] - 1]["question"]}\nВаш ответ: {j[1]}\nПравильный ответ: {correct_answers[j[0] - 1]}'
        # print(mistake_str)
        # print('/\/\/\/\/\/\/\/\/')
        mistakes_answer.append(mistake_str)
        # print(mistakes_answer)
    # Объединяем все строки в одну
    message_text = '\n\n'.join(mistakes_answer)
    if db.select_columns(['result'], message.from_user.id)[0] != 10:
        # Отправляем одно сообщение с объединенными строками
        await message.answer(message_text)
    else:
        await message.answer(text='У вас нет ошибок! Круто!')


@router.message(F.text.lower().in_(['получить сертификат']))
async def get_certificate(message: Message, bot: Bot):
    await message.answer('Сертификат')


@router.message(F.text.lower().in_(['/channel']))
async def get_chanel(message: Message, bot: Bot):
    await message.answer('https://t.me/PervueBelgorod')
