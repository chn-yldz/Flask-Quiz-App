import sqlite3

def create_table():
    conn = sqlite3.connect('database/users.db')
    c = conn.cursor()
    
    # Kullanıcı tablosunu oluştur
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            email TEXT NOT NULL,
            correct INTEGER NOT NULL,
            incorrect INTEGER NOT NULL,
            accuracy REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_table()
    print("Veritabanı ve tablo oluşturuldu.")
