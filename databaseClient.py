import sqlite3
class DataBaseClient():
    def __init__(self):
        self.db = sqlite3.connect('Clients.db')
        self.sql = self.db.cursor()

        self.sql.execute("""CREATE TABLE IF NOT EXISTS clients(
                                    name TEXT,
                                    surname TEXT,
                                    email TEXT,
                                    tcno TEXT,
                                    telno TEXT,
                                    id BIGINT
                        )""")
        self.db.commit()

    def validate(self,email):
        self.sql.execute(f"SELECT email FROM clients WHERE email = '{email}'")
        if self.sql.fetchone() is None:
            return -1
        else:
            return 1

    def add_client(self,name,surname, email, tcno, telno, userId):
        if self.validate(email) == -1:
            self.sql.execute("INSERT INTO clients VALUES(?, ?, ?, ?, ?, ?)",
                             (name, surname, email, tcno, telno, userId))
            self.db.commit()
            return 1
        else:
            return -1


    def getClientsInfo(self, idNum):
        self.db = sqlite3.connect('Clients.db')
        self.sql = self.db.cursor()
        self.sql.execute(f"SELECT name,email,surname,tcno,telno FROM clients WHERE id = ?",(idNum,))
        sa = []
        for record in self.sql.fetchall():
            sa.append(record)
        return sa








