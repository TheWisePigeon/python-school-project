import os
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{cre.user}:{cre.password}@localhost:5432/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#defining models
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String, unique=False, nullable=False)
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
    isbn = db.Column(db.String, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    pub_date = db.Column(db.Date, nullable=False)
    author = db.Column(db.String, nullable=False)
    editor = db.Column(db.String, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

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




    
