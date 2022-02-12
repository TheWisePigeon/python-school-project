
from os import name
from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
import credentials as cre

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{cre.user}:{cre.password}@localhost:5432/flask"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Person(db.Model):
    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

    def __init__(self, nom):
        self.name = name

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            "id": self.id,
            "name" : self.name
        }

db.create_all()


@app.route('/etudiants', methods=['GET'])
def get_all_students():
    etudiants = Person.query.all()
    formatted_students = [ et.format() for et in etudiants]
    return jsonify({
        "Success": True,
        "etudiants": formatted_students,
        "total": Person.query.count()
    })


@app.route('/getEtudiant', methhods=['GET'])
def get_one_student(int:id):
    print(":)")


#set FLASK_APP=api.py
#set FLASK_ENV=development
#$env:FLASK_APP = "api.py"
#flask run






# @app.route('/')
# def index():
#     personnes = Person.query.all()
#     return render_template('index.html', data=personnes)

# @app.route('/create', methods=['GET'])
# def form():
#     return render_template('create.html')
    

# @app.route('/add', methods=['POST'])
# def add():
#     try:
#         nom = request.form.get('username')
#         person = Person(name=nom)
#         db.session.add(person)
#         db.session.commit()
#         return redirect(url_for('index'))
#     except:
#         db.session.rollback()
#     finally:
#         db.session.close()