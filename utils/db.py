import sqlite3


class Database():
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_db()
        self.populate_questions()

    def create_db(self):
        try:
            # Создание таблицы пользователей
            query = ('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY UNIQUE,
                    status TEXT,
                    passed INTEGER,
                    fio TEXT,
                    class INTEGER,
                    first_question TEXT,
                    second_question TEXT,
                    third_question TEXT,
                    fourth_question TEXT,
                    fifth_question TEXT,
                    sixth_question TEXT,
                    seventh_question TEXT,
                    eighth_question TEXT,
                    ninth_question TEXT,
                    tenth_question TEXT,
                    result INTEGER
                )''')
            self.cursor.execute(query)

            # Создание таблицы вопросов
            query = ('''CREATE TABLE IF NOT EXISTS questions (
                    number INTEGER PRIMARY KEY,
                    question TEXT,
                    answer1 TEXT,
                    answer2 TEXT,
                    answer3 TEXT,
                    answer4 TEXT,
                    correct_answer TEXT,
                    category TEXT
                )''')
            self.cursor.execute(query)

            self.connection.commit()
        except sqlite3.Error as Error:
            print('Ошибка при создании:', Error)

    def add_user(self, user_id, status, passed):
        self.cursor.execute(f'INSERT OR IGNORE INTO users (user_id, status, passed) VALUES (?, ?, ?)',
                            (user_id, status, passed))
        self.connection.commit()

    def populate_questions(self):
        # Вставка вопросов в таблицу с соответствующими категориями
        questions_base = [
            {
                'number': 1,
                "question": "Что такое право?",
                "answers": ["а) Набор правил, которые нужно соблюдать",
                            "б) Система законов и правил, которые регулируют поведение людей",
                            "в) Совокупность личных прав и обязанностей каждого человека",
                            "г) Способность делать всё, что хочется"],
                "correct_answer": "б) Система законов и правил, которые регулируют поведение людей",
                "category": "1-4 класс"
            },
            {
                'number': 2,
                "question": "Какие права и обязанности есть у детей?",
                "answers": ["а) Право на образование и обязанность учиться", "б) Право на игру и обязанность играть",
                            "в) Право на свободу и обязанность быть свободным",
                            "г) Право на собственность и обязанность уважать чужую собственность"],
                "correct_answer": "а) Право на образование и обязанность учиться",
                "category": "1-4 класс"
            },
            {
                'number': 3,
                "question": "Что такое закон и зачем он нужен?",
                "answers": ["а) Набор правил, которые нужно соблюдать",
                            "б) Система законов и правил, которые регулируют поведение людей",
                            "в) Совокупность личных прав и обязанностей каждого человека",
                            "г) Способность делать все, что хочется"],
                "correct_answer": "б) Система законов и правил, которые регулируют поведение людей",
                "category": "1-4 класс"
            },
            {
                'number': 4,
                "question": "Какие правила поведения в школе ты знаешь?",
                "answers": ["а) Не бегать по коридорам\nб) Не драться",
                            "в) Не кричать на уроках\nг) Не брать чужие вещи",
                            "д) Не курить в школе\nе) Не приходить в школу в грязной одежде", "ж) все ответы верны"],
                "correct_answer": "ж) все ответы верны",
                "category": "1-4 класс"
            },
            {
                'number': 5,
                "question": "Что такое личная собственность и как ее нужно уважать?",
                "answers": ["а) Личная собственность - это вещи, которые принадлежат человеку",
                            "б) Личная собственность - это вещи, которые можно брать без разрешения",
                            "в) Личная собственность - это вещи, которые можно использовать только в школе",
                            "г) Личная собственность - это вещи, которые можно брать только у друзей"],
                "correct_answer": "а) Личная собственность - это вещи, которые принадлежат человеку",
                "category": "1-4 класс"
            },
            {
                'number': 6,
                "question": "Что такое кража?",
                "answers": ["а) Кража - это когда человек берет чужие вещи без разрешения",
                            "б) Кража - это когда человек берет чужие вещи и не возвращает их",
                            "в) Кража - это когда человек берет чужие вещи и продает их",
                            "г) Кража - это когда человек берет чужие вещи и использует их для себя"],
                "correct_answer": "а) Кража - это когда человек берет чужие вещи без разрешения",
                "category": "1-4 класс"
            },
            {
                'number': 7,
                "question": "Что такое договор и когда его заключают?",
                "answers": ["а) Договор - это когда два человека договариваются о чем-то",
                            "б) Договор - это когда два человека заключают сделку",
                            "в) Договор - это когда два человека обещают друг другу что-то",
                            "г) Договор - это когда два человека подписывают документ"],
                "correct_answer": "а) Договор - это когда два человека договариваются о чем-то",
                "category": "1-4 класс"
            },
            {
                'number': 8,
                "question": "Что такое уважение к старшим и почему это важно?",
                "answers": ["а) Уважение к старшим - это когда дети слушают и уважают взрослых",
                            "б) Уважение к старшим - это когда дети делают все, что им говорят взрослые",
                            "в) Уважение к старшим - это когда дети не спорят со взрослыми",
                            "г) Уважение к старшим - это когда дети не разговаривают со взрослыми"],
                "correct_answer": "а) Уважение к старшим - это когда дети слушают и уважают взрослых",
                "category": "1-4 класс"
            },
            {
                'number': 9,
                "question": "Что такое честность и почему это важно?",
                "answers": ["а) Честность - это когда человек говорит правду",
                            "б) Честность - это когда человек не обманывает других",
                            "в) Честность - это когда человек не скрывает свои ошибки",
                            "г) Честность - это когда человек не скрывает свои чувства"],
                "correct_answer": "б) Честность - это когда человек не обманывает других",
                "category": "1-4 класс"
            },
            {
                'number': 10,
                "question": "Что такое ответственность?",
                "answers": ["а) Ответственность - это когда человек отвечает за свои поступки",
                            "б) Ответственность - это когда человек выполняет свои обязанности",
                            "в) Ответственность - это когда человек не нарушает правила",
                            "г) Ответственность - это когда человек не делает ошибок"],
                "correct_answer": "а) Ответственность - это когда человек отвечает за свои поступки",
                "category": "1-4 класс"
            },
            {
                'number': 11,
                "question": "Что такое право?",
                "answers": ["а) Набор правил, которые нужно соблюдать",
                            "б) Система законов и правил, которые регулируют поведение людей",
                            "в) Совокупность личных прав и обязанностей каждого человека",
                            "г) Способность делать все, что хочется"],
                "correct_answer": "б) Система законов и правил, которые регулируют поведение людей",
                "category": "5-6 класс"
            },
            {
                'number': 12,
                "question": "Какие права и обязанности есть у детей?",
                "answers": ["а) Право на образование и обязанность учиться", "б) Право на игру и обязанность играть",
                            "в) Право на свободу и обязанность быть свободным",
                            "г) Право на собственность и обязанность уважать чужую собственность"],
                "correct_answer": "а) Право на образование и обязанность учиться",
                "category": "5-6 класс"
            },
            {
                'number': 13,
                "question": "Что такое закон?",
                "answers": ["а) Набор правил, которые нужно соблюдать",
                            "б) Система законов и правил, которые регулируют поведение людей",
                            "в) Совокупность личных прав и обязанностей каждого человека",
                            "г) Способность делать все, что хочется"],
                "correct_answer": "б) Система законов и правил, которые регулируют поведение людей",
                "category": "5-6 класс"
            },
            {
                'number': 14,
                "question": "Какие правила поведения в школе ты знаешь?",
                "answers": ["а) Не бегать по коридорам\nб) Не драться",
                            "в) Не кричать на уроках\nг) Не брать чужие вещи",
                            "д) Не курить в школе\nе) Не приходить в школу в грязной одежде", "ж) все ответы верны"],
                "correct_answer": "ж) все ответы верны",
                "category": "5-6 класс"
            },
            {
                'number': 15,
                "question": "Что такое личная собственность?",
                "answers": ["а) Личная собственность - это вещи, которые принадлежат человеку",
                            "б) Личная собственность - это вещи, которые можно брать без разрешения",
                            "в) Личная собственность - это вещи, которые можно использовать только в школе",
                            "г) Личная собственность - это вещи, которые можно брать только у друзей"],
                "correct_answer": "а) Личная собственность - это вещи, которые принадлежат",
                "category": "5-6 класс"
            },
            {
                'number': 16,
                "question": "Что такое кража и почему это плохо?",
                "answers": ["а) Кража - это когда человек берет чужие вещи без разрешения",
                            "б) Кража - это когда человек берет чужие вещи и не возвращает их",
                            "в) Кража - это когда человек берет чужие вещи и продает их",
                            "г) Кража - это когда человек берет чужие вещи и использует их для себя"],
                "correct_answer": "а) Кража - это когда человек берет чужие вещи без разрешения",
                "category": "5-6 класс"
            },
            {
                'number': 17,
                "question": "Что такое договор и когда его заключают?",
                "answers": ["а) Договор - это когда два человека договариваются о чем-то",
                            "б) Договор - это когда два человека заключают сделку",
                            "в) Договор - это когда два человека обещают друг другу что-то",
                            "г) Договор - это когда два человека подписывают документ"],
                "correct_answer": "а) Договор - это когда два человека договариваются о чем-то",
                "category": "5-6 класс"
            },
            {
                'number': 18,
                "question": "Что такое уважение к старшим и почему это важно?",
                "answers": ["а) Уважение к старшим - это когда дети слушают и уважают взрослых",
                            "б) Уважение к старшим - это когда дети делают все, что им говорят взрослые",
                            "в) Уважение к старшим - это когда дети не спорят со взрослыми",
                            "г) Уважение к старшим - это когда дети не разговаривают со взрослыми"],
                "correct_answer": "а) Уважение к старшим - это когда дети слушают и уважают взрослых",
                "category": "5-6 класс"
            },
            {
                'number': 19,
                "question": "Что такое честность?",
                "answers": ["а) Честность - это когда человек говорит правду",
                            "б) Честность - это когда человек не обманывает других",
                            "в) Честность - это когда человек не скрывает свои ошибки",
                            "г) Честность - это когда человек не скрывает свои чувства"],
                "correct_answer": "б) Честность - это когда человек не обманывает других",
                "category": "5-6 класс"
            },
            {
                'number': 20,
                "question": "Что такое ответственность?",
                "answers": ["а) Ответственность - это когда человек отвечает за свои поступки",
                            "б) Ответственность - это когда человек выполняет свои обязанности",
                            "в) Ответственность - это когда человек не нарушает правила",
                            "г) Ответственность - это когда человек не делает ошибок"],
                "correct_answer": "а) Ответственность - это когда человек отвечает за свои поступки",
                "category": "5-6 класс"
            },
            {
                'number': 21,
                "question": "Что такое право?",
                "answers": ["А) Система правил, регулирующих поведение людей",
                            "Б) Набор законов, установленных государством",
                            "В) Совокупность моральных норм и ценностей", "Г) Кодекс поведения, принятый обществом"],
                "correct_answer": "А) Система правил, регулирующих поведение людей",
                "category": "7-11 класс"
            },
            {
                'number': 22,
                "question": "Какие основные отрасли права существуют?",
                "answers": ["А) Гражданское право\nБ) Уголовное право", "В) Административное право\nГ) Семейное право",
                            "Д) Трудовое право\nЕ) Экологическое право", "Ж) Все ответы верны"],
                "correct_answer": "Ж) Все ответы верны",
                "category": "7-11 класс"
            },
            {
                'number': 23,
                "question": "Что такое Конституция?",
                "answers": ["А) Основной закон государства", "Б) Кодекс поведения граждан",
                            "В) Свод правил для чиновников",
                            "Г) Устав политической партии"],
                "correct_answer": "А) Основной закон государства",
                "category": "7-11 класс"
            },
            {
                'number': 24,
                "question": "Какие права и свободы гарантированы Конституцией РФ?",
                "answers": ["А) Право на жизнь\nБ) Право на свободу слова",
                            "В) Право на образование\nГ) Право на свободу передвижения",
                            "Д) Право на труд\nЕ) Право на охрану здоровья", "Ж) Все ответы верны"],
                "correct_answer": "Ж) Все ответы верны",
                "category": "7-11 класс"
            },
            {
                'number': 25,
                "question": "Что такое гражданство?",
                "answers": ["А) Статус гражданина определенного государства", "Б) Наличие паспорта гражданина",
                            "В) Право на участие в выборах", "Г) Наличие гражданских прав и обязанностей"],
                "correct_answer": "А) Статус гражданина определенного государства",
                "category": "7-11 класс"
            },
            {
                'number': 26,
                "question": "Что такое юридическая ответственность?",
                "answers": ["А) Обязанность лица нести наказание за совершенное правонарушение",
                            "Б) Возможность гражданина обратиться в суд",
                            "В) Обязанность государства защищать права и свободы граждан",
                            "Г) Система наказаний за нарушение законов"],
                "correct_answer": "А) Обязанность лица нести наказание за совершенное правонарушение",
                "category": "7-11 класс"
            },
            {
                'number': 27,
                "question": "Что такое административное правонарушение? (Укажите НЕВЕРНЫЙ ответ)",
                "answers": ["А) Нарушение правил дорожного движения", "Б) Нарушение общественного порядка",
                            "В) Нарушение трудовой дисциплины", "Г) Нарушение правил пожарной безопасности"],
                "correct_answer": "В) Нарушение трудовой дисциплины",
                "category": "7-11 класс"
            },
            {
                'number': 28,
                "question": "Что такое уголовное преступление?",
                "answers": ["А) Нарушение уголовного кодекса\nБ) Насилие над личностью", "В) Кража\nГ) Убийство",
                            "Д) Мошенничество", "Е) Все ответы верны"],
                "correct_answer": "Е) Все ответы верны",
                "category": "7-11 класс"
            },
            {
                'number': 29,
                "question": "Что такое гражданский процесс?",
                "answers": ["А) Разбирательство в суде по гражданским делам",
                            "Б) Разбирательство в суде по уголовным делам",
                            "В) Разбирательство в суде по административным делам",
                            "Г) Разбирательство в суде по трудовым спорам"],
                "correct_answer": "А) Разбирательство в суде по гражданским делам",
                "category": "7-11 класс"
            },
            {
                'number': 30,
                "question": "Что такое трудовое право?",
                "answers": ["А) Совокупность норм, регулирующих трудовые отношения",
                            "Б) Совокупность норм, регулирующих отношения между работодателем и работником",
                            "В) Совокупность норм, регулирующих отношения между работником и государством",
                            "Г) Все ответы верны"],
                "correct_answer": "Г) Все ответы верны",
                "category": "7-11 класс"
            }
        ]

        # Добавление вопросов в таблицу
        for question in questions_base:
            try:
                self.cursor.execute(
                    "INSERT INTO questions VALUES (:number, :question, :answer1, :answer2, :answer3, :answer4, :correct_answer, :category)",
                    {'number': question['number'], 'question': question['question'], 'answer1': question['answers'][0],
                     'answer2': question['answers'][1], 'answer3': question['answers'][2],
                     'answer4': question['answers'][3], 'correct_answer': question['correct_answer'],
                     'category': question['category']})
            except sqlite3.Error as e:
                print("Ошибка при вставке данных:", e)

        self.connection.commit()

    def is_database_empty(self):
        """
        Проверяет, пуста ли база данных.
        :return: True, если база данных пуста, и False в противном случае.
        """
        query = "SELECT COUNT(*) FROM users"
        self.cursor.execute(query)
        count = self.cursor.fetchone()[0]
        return count == 0

    def select_passed(self, user_id):
        passed = self.cursor.execute("SELECT passed FROM users WHERE user_id = ?", (user_id,))
        return passed.fetchall()

    def add_passed(self, passed: int, user_id):
        self.cursor.execute(f'UPDATE users SET passed = ? WHERE user_id = ?', (passed, user_id))
        self.connection.commit()

    def add_fio(self, fio, user_id):
        self.cursor.execute(f'UPDATE users SET fio = ? WHERE user_id = ?', (fio, user_id))
        self.connection.commit()

    def add_first(self, answer, user_id):
        self.cursor.execute(f'UPDATE users SET first_question = ? WHERE user_id = ?', (answer, user_id))
        self.connection.commit()

    def add_second(self, answer, user_id):
        self.cursor.execute(f'UPDATE users SET second_question = ? WHERE user_id = ?', (answer, user_id))
        self.connection.commit()

    def add_third(self, answer, user_id):
        self.cursor.execute(f'UPDATE users SET third_question = ? WHERE user_id = ?', (answer, user_id))
        self.connection.commit()

    def add_fourth(self, answer, user_id):
        self.cursor.execute(f'UPDATE users SET fourth_question = ? WHERE user_id = ?', (answer, user_id))
        self.connection.commit()

    def add_fifth(self, answer, user_id):
        self.cursor.execute(f'UPDATE users SET fifth_question = ? WHERE user_id = ?', (answer, user_id))
        self.connection.commit()

    def add_sixth(self, answer, user_id):
        self.cursor.execute(f'UPDATE users SET sixth_question = ? WHERE user_id = ?', (answer, user_id))
        self.connection.commit()

    def add_seventh(self, answer, user_id):
        self.cursor.execute(f'UPDATE users SET seventh_question = ? WHERE user_id = ?', (answer, user_id))
        self.connection.commit()

    def add_eighth(self, answer, user_id):
        self.cursor.execute(f'UPDATE users SET eighth_question = ? WHERE user_id = ?', (answer, user_id))
        self.connection.commit()

    def add_ninth(self, answer, user_id):
        self.cursor.execute(f'UPDATE users SET ninth_question = ? WHERE user_id = ?', (answer, user_id))
        self.connection.commit()

    def add_tenth(self, answer, user_id):
        self.cursor.execute(f'UPDATE users SET tenth_question = ? WHERE user_id = ?', (answer, user_id))
        self.connection.commit()

    def add_result(self, answer: int, user_id):
        self.cursor.execute(f'UPDATE users SET result = ? WHERE user_id = ?', (answer, user_id))
        self.connection.commit()

    def add_class(self, age: int, user_id):
        self.cursor.execute(f'UPDATE users SET class = ? WHERE user_id = ?', (age, user_id))
        self.connection.commit()

    def select_columns(self, column_names: list[str], user_id: int):
        """
        Функция для выбора значений из нескольких столбцов таблицы users по user_id.
        :param column_names: Список имен столбцов, значения которых нужно выбрать.
        :param user_id: Значение user_id для фильтрации.
        :return: Список значений из указанных столбцов для заданного user_id.
        """
        # Формируем строку запроса динамически
        query = f"SELECT {', '.join(column_names)} FROM users WHERE user_id = ?"
        # Выполняем запрос с переданным user_id
        self.cursor.execute(query, (user_id,))
        # Получаем результат запроса
        result = self.cursor.fetchone()
        return result
