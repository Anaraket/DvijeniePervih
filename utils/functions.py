import os

from utils.db import Database
from utils.questions import questions

# Список вопросов для запроса к БД
request = ['first_question',
           'second_question',
           'third_question',
           'fourth_question',
           'fifth_question',
           'sixth_question',
           'seventh_question',
           'eighth_question',
           'ninth_question',
           'tenth_question']


# Отправляет пользователю вопрос из списка
def send_questions(number: int):
    message = questions[number - 1]["question"]
    return message


# Высчитывает количество правильных ответов
def result(answers: tuple):
    score = 0
    incorrect_answers = []
    for idx, values in enumerate(questions, start=1):
        if values['correct_answer'] == answers[idx - 1]:
            score += 1
        else:
            incorrect_answers.append(answers[idx - 1])
    return score


def show_mistakes(user_id):
    db = Database(os.getenv('DATABASE_NAME'))
    mistakes = []  # список неправильных ответов [(1, Munhen), ...]
    answers = db.select_columns(column_names=request, user_id=user_id)  # Кортеж ответов пользователя
    correct_answers = [question['correct_answer'] for question in questions]  # Список правильных ответов
    for index, answer in enumerate(answers):
        if answer != correct_answers[index]:
            mistakes.append((index + 1, answer))
    mistakes_answer = []  # Список сообщений с выводом вопросов, ошибок и правильных ответов
    for j in mistakes:
        # j - кортеж (j[0] - номер вопроса, j[1] - неправильный ответ)
        mistake_str = f'Вопрос {j[0]}: {questions[j[0] - 1]["question"]}\nВаш ответ: {j[1]}\nПравильный ответ: {correct_answers[j[0] - 1]}'
        mistakes_answer.append(mistake_str)

    # Отправляем одно сообщение с объединенными строками
    if db.select_columns(['result'], user_id=user_id)[0] != 10:
        # Объединяем все строки в одну
        message_text = '\n\n'.join(mistakes_answer)
    else:
        message_text = 'У вас нет ошибок! Круто!'

    return message_text
