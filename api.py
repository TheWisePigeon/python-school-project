import os
from tkinter import N
from xml.dom.minidom import Attr
from flask import Flask, abort, jsonify, make_response, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from itsdangerous import json
load_dotenv()
import credentials as cre
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{cre.user}:{cre.password}@localhost:5432/library"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#defining models
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(100), unique=False, nullable=False)
    books = db.relationship('Book', backref='book', lazy=True)

    def __init__(self, id, label):
        self.id = id
        self.label = label

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def format(self):
        return {
            'id' : self.id,
            'label' : self.label
        }

    def updateLabel(self):
        db.session.commit()

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    pub_date = db.Column(db.Date, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    editor = db.Column(db.String(50), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)

    def __init__(self, id, isbn, title, pub_date, author, editor, category_id):
        self.id = id
        self.isbn = isbn
        self.title = title
        self.pub_date = pub_date
        self.author = author
        self.editor = editor
        self.category_id = category_id

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return  {
            'id': self.id,
            'isbn' : self.isbn,
            'title' : self.title,
            'pub_date' : self.pub_date,
            'author' : self.author,
            'editor' : self.editor,
            'category_id' : self.category_id
        }

db.create_all()

#defining the routes

##get all books
@app.route('/books', methods=['GET'])
def getBooks():
    books = [book.format() for book in Book.query.all()]
    return jsonify({
        "Success" : True,
        "books" : books,
        "total" : len(books)
    })

##get a book by its id
@app.route('/books/<int:id>', methods=['GET'])
def getBook(id):
    book = (Book.query.get(id)).format()
    if book is None:
        abort(404)
        
    else:
        return jsonify({
            "Success" : True,
            "book" : book
        })

##get all books from a category
@app.route('/category/<int:id>/books', methods=['GET'])
def getBooksFromCat(id):
    books = [book.format() for book in Book.query.filter_by(category_id=id)]
    if books is None:
        abort(404)
    else :
        return jsonify({
            "Success" : True,
            "books" : books,
            "category label" : (Category.query.get(id)).format()["label"],
            "total" : len(books)
        })

##list a category


##get a category by its id
@app.route('/category/<int:id>', methods=['GET'])
def getCategory(id):
    category = (Category.query.get(id)).format()
    if category is None:
        abort(404)
    else:
        return jsonify({
            "Success" : True,
            "category" : category
        })

##get all categories
@app.route('/categories', methods=['GET'])
def getCategories():
    categories = [category.format() for category in Category.query.all()]
    return jsonify({
        "Success" : True,
        "categories" : categories,
        "total" : len(categories)
    })

##delete a book
@app.route('/books/<int:id>', methods=['DELETE'])
def deleteBook(id):
    book = Book.query.get(id)
    if book is None:
        abort(404)
    else:
        book.delete()
        return jsonify({
            "Success" : True,
            "deleted book" : book.format()
        })


##delete a category
@app.route('/categories/<int:id>', methods=['DELETE'])
def deleteCategory(id):
    category = Category.query.get(id)
    if category is None:
        abort(404)
    else:
        category.delete()
        return jsonify({
            "Success" : True,
            "deleted book" : category.format(),
            
        })

##update a book's infos
@app.route('/books/<int:id>', methods=['PATCH'])
def updateBook(id):
    body=request.args
    book = Book.query.get(id)
    book.isbn, book.title, book.pub_date, book.author, book.editor, book.category_id = body.get('isbn', None), body.get('title', None), body.get('pub_date', None), body.get('author', None), body.get('editor', None), body.get('category_id', None)
    values = [book.isbn, book.title, book.pub_date, book.author, book.editor, book.category_id]
    for i in range(len(values)):
        if values[i] is None:
            abort(400)
    book.update()
    return jsonify({
        "success" : True,
        "updated book" : book.format()
    })

##update a category
@app.route('/categories/<int:id>', methods=['PUT'])
def updateCategory(id):
    body=request.args
    print(body)
    category = Category.query.get(id)
    category.label = body.get('label', None)
    if category.label is None:
        abort(400)
    else:
        category.update()
        return jsonify({
            "Success" :True,
            "updated category" : category.format()
        })
# @app.route('/etudiants', methods=['GET'])
# def get_all_students():
#     etudiants = Person.query.all()
#     formatted_students = [ et.format() for et in etudiants]
#     return jsonify({
#         "Success": True,
#         "etudiants": formatted_students,
#         "total": Person.query.count()
#     })


# @app.route('/getEtudiant', methhods=['GET'])
# def get_one_student(int:id):
#     print(":)")


#set FLASK_APP=api.py
#set FLASK_ENV=development
#$env:FLASK_APP = "api.py"
#flask run
