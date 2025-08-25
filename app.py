from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
db = SQLAlchemy(app)

#database model
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer, nullable=False)

#create db table
with app.app_context():
    db.create_all()


#home route
@app.route('/')
def home():
    return jsonify({"message": "Welcome to Book Management REST API!"})

#Add new book
@app.route('/books', methods=['POST'])
def add_book():
    data = request.json
    if not data.get('title') or not data.get('author') or not data.get('year'):
        return jsonify({"error": "Title, author, and year are required"}), 400
    new_book = Book(title=data['title'], author=data['author'], year=data['year'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({"message": "Book added!", "book": {
        "id": new_book.id,
        "title": new_book.title,
        "author": new_book.author,
        "year": new_book.year
    }}), 201

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    result = [{"id": b.id, "title": b.title, "author": b.author, "year": b.year} for b in books]
    return jsonify(result)

# Get a single book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    return jsonify({"id": book.id, "title": book.title, "author": book.author, "year": book.year})

# Update a book by ID
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    data = request.json
    book.title = data.get("title", book.title)
    book.author = data.get("author", book.author)
    book.year = data.get("year", book.year)
    db.session.commit()
    return jsonify({"message": "Book updated!", "book": {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "year": book.year
    }})

#Delete book by id
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    db.session.delete(book)
    db.session.commit()
    return jsonify({"message": "Book deleted!"})

if __name__ == '__main__':
    app.run(debug=True)
