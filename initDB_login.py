import sqlite3

conn = sqlite3.connect('database.db')
cur = conn.cursor()

sql_login = """
    CREATE TABLE IF NOT EXISTS login_user(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
"""
cur.execute(sql_login)


sql_farm = """
    CREATE TABLE IF NOT EXISTS farm(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        namefarm TEXT NOT NULL,
        description TEXT 
    )
"""
cur.execute(sql_farm)

conn.commit()
conn.close()
print("Đã tạo db")