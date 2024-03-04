from utils.questions import questions
# from utils.db import Database
# import os
#
# request = ['user_id',
#            'status',
#            'passed',
#            'fio',
#            'first_question',
#            'second_question',
#            'third_question',
#            'fourth_question',
#            'fifth_question',
#            'sixth_question',
#            'seventh_question',
#            'eighth_question',
#            'ninth_question',
#            'tenth_question',
#            'result']


# Отправляет пользователю вопрос из списка
def send_questions(number: int):
    message = questions[number - 1]["question"]
    return message


# Высчитывает количество правильных ответов
def result(answers: list):
    score = 0
    incorrect_answers = []
    user_answers = [item[4:14] for item in answers]
    for idx, values in enumerate(questions, start=1):
        if values['correct_answer'] == user_answers[0][idx - 1]:
            score += 1
        else:
            incorrect_answers.append(user_answers[0][idx - 1])
    return score

# def show_mistakes(user_id):
#     db = Database(os.getenv('DATABASE_NAME'))
#     mistakes = []
#     answers = db.select_columns(column_names=request[4:-1], user_id=message.from_user.id)
#     correct_answers = [question['correct_answer'] for question in questions]
#     for index, answer in enumerate(answers):
#         if answer != correct_answers[index]:
#             mistakes.append((index + 1, answer))
#     mistakes_answer = []
#     for j in mistakes:
#         mistake_str = f'Вопрос {j[0]}: {questions[j[0]]["question"]}\nВаш ответ: {j[1]}\nПравильный ответ: {correct_answers[j[0] - 1]}'
#         mistakes_answer.append(mistake_str)
#
#     # Объединяем все строки в одну
#     message_text = '\n\n'.join(mistakes_answer)