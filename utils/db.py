import sqlite3


class Database():
    def __init__(self, db_name):
        self.connection = sqlite3.connect(db_name)
        self.cursor = self.connection.cursor()
        self.create_db()

    def create_db(self):
        try:
            query = ('''CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY UNIQUE,
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

    def add_user(self, user_id, status, passed):
        self.cursor.execute(f'INSERT OR IGNORE INTO users (user_id, status, passed) VALUES (?, ?, ?)',
                            (user_id, status, passed))
        self.connection.commit()

    def __del__(self):
        self.cursor.close()
        self.connection.close()

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

    def select_all_answers(self, user_id):
        passed = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return passed.fetchall()

