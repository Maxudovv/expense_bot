import pickle
import sqlite3
from User import User


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("DATABASE.db")
        self.cur = self.conn.cursor()

        self.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id BIGINT,
            data BLOB
        )""")

    def execute(self, sql, params=tuple()):
        result = self.cur.execute(sql, params)
        self.conn.commit()
        return result

    def check_user_exits(self, user_id: int):
        res = self.cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,)).fetchall()
        return bool(len(res))

    def add_user(self, user_id):
        with self.conn:
            if not self.check_user_exits(user_id):
                us = User()
                self.execute("INSERT INTO users VALUES (?,?)", (user_id, pickle.dumps(us)))

    def update_data(self, user_id, data):
        if self.check_user_exits(user_id):
            return self.execute("UPDATE users SET data = ? WHERE user_id = ?", (pickle.dumps(data), user_id))
        self.add_user(user_id)
        self.update_data(user_id)

    def get_data(self, user_id):
        if self.check_user_exits(user_id):
            return pickle.loads(self.execute("SELECT data FROM users WHERE user_id = ?", (user_id,)).fetchall()[0][0])
        self.add_user(user_id)
        self.get_data(user_id)

    def __del__(self):
        self.conn.close()
