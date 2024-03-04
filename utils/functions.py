from utils.questions import questions
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
        if values['correct_answer'] == user_answers[0][idx-1]:
            score += 1
        else:
            incorrect_answers.append(user_answers[0][idx-1])
    return score
