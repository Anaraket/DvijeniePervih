import os

from utils.db import Database

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
def send_questions(number: int, category: int):
    db = Database(os.getenv('DATABASE_NAME'))
    message = db.select_question(number, category)
    return message


# Высчитывает количество правильных ответов
def result(numbers: tuple, category: int, user_id: id):
    mistakes_answer = []  # Список сообщений с выводом вопросов, ошибок и правильных ответов
    db = Database(os.getenv('DATABASE_NAME'))
    score = 0
    for i in range(10):
        correct_answer = db.select_correct_answer(numbers[i], category)
        user_answer = db.select_from_users_table(request[i], user_id)
        if correct_answer == user_answer:
            score += 1
        else:
            mistake_str = (f'<u>Вопрос {i + 1}</u>: {db.select_question(numbers[i], category)}\n'
                           f'<u>Ваш ответ</u>: {user_answer}\n<u>Правильный ответ</u>: {correct_answer}')
            mistakes_answer.append(mistake_str)
    try:
        if db.select_columns_from_users_table(['result'], user_id=user_id)[0] != 10:
            # Объединяем все строки в одну
            message_text = '\n\n'.join(mistakes_answer)
            return score, message_text
        else:
            message_text = 'У вас нет ошибок!😱 Круто!🔥'
            return score, message_text
    except TypeError:
        # Объединяем все строки в одну
        message_text = '\n\n'.join(mistakes_answer)
        return score, message_text
