from flask import Flask, render_template
from models import db, Book, Author


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)


@app.route('/')
def books_with_authors():
    books = Book.query.all()
    return render_template('books.html', books=books)


@app.cli.command("init-db")
def init_db():
    db.create_all()
    print('OK')