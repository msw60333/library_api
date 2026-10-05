import sqlite3

DB_NAME = 'library.db'


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS authors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            country TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            year INTEGER,
            author_id INTEGER NOT NULL,
            FOREIGN KEY(author_id) REFERENCES authors(id) ON DELETE CASCADE
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS loans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            reader_name TEXT NOT NULL,
            loan_date TEXT NOT NULL,
            returned INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY(book_id) REFERENCES books(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()

def seed_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    cursor.execute('DELETE FROM loans')
    cursor.execute('DELETE FROM books')
    cursor.execute('DELETE FROM authors')

    authors = [
        ('Джордж Оруэлл', 'Великобритания'),
        ('Джейн Остин', 'Великобритания'),
        ('Габриэль Гарсия Маркес', 'Колумбия'),
    ]
    cursor.executemany(
        'INSERT INTO authors (name, country) VALUES (?, ?)',
        authors,
    )

    books = [
        ('1984', 'Антиутопия', 1949, 1),
        ('Скотный двор', 'Сатира', 1945, 1),
        ('Гордость и предубеждение', 'Роман', 1813, 2),
        ('Эмма', 'Классика', 1815, 2),
        ('Сто лет одиночества', 'Магический реализм', 1967, 3),
        ('Любовь во время холеры', 'Роман', 1985, 3),
    ]
    cursor.executemany(
        'INSERT INTO books (title, genre, year, author_id) VALUES (?, ?, ?, ?)',
        books,
    )

    loans = [
        (1, 'Алиса', '2026-09-15', 1),
        (2, 'Борис', '2026-09-20', 0),
        (3, 'Виктор', '2026-09-25', 1),
        (5, 'Дарья', '2026-10-01', 0),
    ]
    cursor.executemany(
        'INSERT INTO loans (book_id, reader_name, loan_date, returned) VALUES (?, ?, ?, ?)',
        loans,
    )

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_tables()
    seed_db()
    print(f'База данных создана: {DB_NAME}')

