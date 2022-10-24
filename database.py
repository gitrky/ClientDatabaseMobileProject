import sqlite3
class DataBase1():

    def __init__(self):
        self.db = sqlite3.connect('Users.db')
        self.sql = self.db.cursor()
        self.sql.execute("""CREATE TABLE IF NOT EXISTS users(
                                            id integer PRIMARY KEY,
                                            name TEXT,
                                            email TEXT,
                                            password TEXT
                                    )""")

        self.db.commit()

    def validate(self,email,passw):
        self.sql.execute(f"SELECT email FROM users WHERE email = '{email}' AND password = '{passw}'")
        if self.sql.fetchone() is None:
            return -1
        else:
            return 1

    def add_user(self,name,email, passw):
        self.sql.execute(f"SELECT email FROM users WHERE email = '{email}'")
        if self.sql.fetchone() is None:
            self.sql.execute("INSERT INTO users (name,email,password) VALUES(?, ?, ?)",
                             (name, email, passw))


            self.db.commit()
            return 1
        else:
            return -1

    def userId(self, email, passw):
        self.db = sqlite3.connect('Users.db')
        self.sql = self.db.cursor()
        self.sql.execute(f"SELECT id FROM users WHERE email = '{email}' AND password = '{passw}'")

        record = self.sql.fetchone()
        return record[0]


    def update(self,id,newpassw):
        self.db = sqlite3.connect('Users.db')
        self.sql = self.db.cursor()
        self.sql.execute(f"UPDATE users SET password = {newpassw} WHERE id={id}")

        self.db.commit()

    def updateE(self, id, newemail):
        self.db = sqlite3.connect('Users.db')
        self.sql = self.db.cursor()
        self.sql.execute(f"UPDATE users SET email = ? WHERE id=?",(newemail,id))

        self.db.commit()








