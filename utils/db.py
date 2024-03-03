import sqlite3


class Database():
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_db()

    def create_db(self):
        try:
            query = ('''CREATE TABLE IF NOT EXISTS users (
                    telegram_id INTEGER PRIMARY KEY UNIQUE,
                    status TEXT,
                    passed INTEGER,
                    fio TEXT,
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
            self.connection.commit()
        except sqlite3.Error as Error:
            print('Ошибка при создании:', Error)

    def __del__(self):
        self.cursor.close()
        self.connection.close()




# # Подключение к базе данных
# conn = sqlite3.connect('quiz_users.db')
# cursor = conn.cursor()
#
# # Создание таблицы, если её ещё нет
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         telegram_id INTEGER PRIMARY KEY UNIQUE,
#         status TEXT,
#         passed INTEGER,
#         fio TEXT,
#         first_question TEXT,
#         second_question TEXT,
#         third_question TEXT,
#         fourth_question TEXT,
#         fifth_question TEXT,
#         sixth_question TEXT,
#         seventh_question TEXT,
#         eighth_question TEXT,
#         ninth_question TEXT,
#         tenth_question TEXT,
#         result INTEGER
#     )
# ''')
# conn.commit()
