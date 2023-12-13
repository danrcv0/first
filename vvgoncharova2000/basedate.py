import sqlite3



db = sqlite3.connect('users.db')
sql = db.cursor()


sql.execute("""CREATE TABLE IF NOT EXISTS users (
    ID INTEGER,
    DATE TEXT
)""")

db.commit()
db.close()