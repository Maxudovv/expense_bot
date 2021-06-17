import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("DATABASE.db")
        self.cur = self.conn.cursor()

        self.execute("""CREATE TABLE IF NOT EXISTS users(
            user_id BIGINT,
            data BLOB
        )""")

    def execute(self, sql, params:tuple=tuple()):
        result = self.cur.execute(sql, params)
        self.conn.commit()
        return result

    def add_user(self, user_id, data):
        with self.conn:
            return self.execute("INSERT INTO users VALUES (?,?)", (user_id, data))

    def update_data(self, user_id, data):
        return self.execute("UPDATE users SET data = ? WHERE user_id = ?", (data, user_id))

    def get_data(self, user_id):
        return self.execute("SELECT data FROM users WHERE user_id = ?", (user_id,)).fetchall()[0][0]

    def __del__(self):
        self.conn.close()
