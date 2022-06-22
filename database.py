import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect ("users.db", timeout=10)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                user_id INT PRIMARY KEY,
                subscription INT DEFAULT 0,
                city TEXT DEFAULT "Не указано"
                )""")
        self.connection.commit()

    def user_registered(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id, )).fetchmany(1)
            return bool(len(result))

    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO 'users' ('user_id') VALUES (?)", (user_id,))

    def set_sub(self, user_id, city):
        with self.connection:
            user_status = 1
            data = user_status, city.capitalize(), user_id
            self.cursor.execute("UPDATE users SET subscription = ?, city = ? WHERE user_id = ?", data)
            self.connection.commit()

    def set_unsub(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE users SET subscription = ?, city = ? WHERE user_id = ?", (0, "NULL", user_id))
    