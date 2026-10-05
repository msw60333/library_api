from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('library.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()

    genre = request.args.get('genre')
    author_id = request.args.get('author_id')

    conditions = []
    params = []

    if genre is not None:
        conditions.append('LOWER(genre) = LOWER(?)')
        params.append(genre)

    if author_id is not None:
        conditions.append('author_id = ?')
        params.append(author_id)

    query = 'SELECT * FROM books'
    if conditions:
        query += ' WHERE ' + ' AND '.join(conditions)

    books = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(book) for book in books])


@app.route('/books/<int:id>', methods=['GET'])
def get_book(id):
    conn = get_db_connection()
    book = conn.execute(
        '''
        SELECT b.id, b.title, b.genre, b.year, b.author_id,
               a.name AS author_name
        FROM books b
        LEFT JOIN authors a ON a.id = b.author_id
        WHERE b.id = ?
        ''',
        (id,),
    ).fetchone()
    conn.close()

    if book is None:
        return jsonify({'error': 'Книга не найдена'}), 404

    return jsonify(dict(book))


if __name__ == '__main__':  
    app.run(debug=True)