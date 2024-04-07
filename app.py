from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from sqlalchemy import create_engine, text, or_ #import for textual query
from sqlalchemy.sql import exists   #import for exists


app = Flask(__name__)
app.config['SECRET_KEY'] = '84Br5667bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assignment3.db'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Instructors(db.Model):
    __tablename__ = 'Instructors'
    id = db.Column(db.Integer, primary_key=True) #id is for students and instructors
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    type = db.Column(db.String(10), nullable=False, default='instructor')
    password = db.Column(db.String(20), nullable = False)
    feedback = db.relationship('Feedback', backref='user', lazy=True)

    def __repr__(self):
        return f"Person('{self.username}', '{self.email}')"

class Students(db.Model):
    __tablename__ = 'Students'
    id = db.Column(db.Integer, primary_key=True) #id is for students and instructors
    username = db.Column(db.String(20), unique=True, nullable=False)
    firstname = db.Column(db.String(20), unique=False, nullable=False)
    password = db.Column(db.String(20), nullable = False)
    type = db.Column(db.String(10), nullable=False, default='student')
    grades = db.relationship('Grades', backref='get', lazy=True)
    remark = db.relationship('Remarks', backref='author', lazy=True)


    def __repr__(self):
        return f"Person('{self.username}', '{self.email}')"
    

class Grades(db.Model):
    __tablename__ = 'Grades'
    id = db.Column(db.Integer, primary_key=True)
    assignment_name = db.Column(db.String(100), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    remark_request = db.Column(db.Text, nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('Students.id'), nullable=False)

    def __repr__(self):
        return f"Grades('{self.assignment_name}', '{self.grade}')"
    
# store anonymous feedback form
class Feedback(db.Model):
    __tablename__ = 'Feedback'
    id = db.Column(db.Integer, primary_key=True) #instructor's id
    like = db.Column(db.Text)
    improve_teach = db.Column(db.Text)
    labs = db.Column(db.Text)
    improve_lab = db.Column(db.Text)
    instructors_id = db.Column(db.Integer, db.ForeignKey('Instructors.id'), nullable=False)

    #db.Column(db.Integer, db.ForeignKey('Person.id'), nullable=False)
    def __repr__(self):
        return f"Feedback('{self.id}', '{self.like}')"

# store remark requests
class Remarks(db.Model):
    __table__name = 'RemarkRequests'
    id = db.Column(db.Integer, primary_key=True) #student id
    reason = db.Column(db.Text) # reason for remark request 
    student_id = db.Column(db.Integer, db.ForeignKey('Students.id'), nullable=False)

    def __repr__(self):
        return f"Remarks('{self.id}', '{self.reason}')"

with app.app_context():
    db.create_all()


## Homepage

@app.route("/")
@app.route('/home')
def home():
    pagename='CSCB20 Course'
    return render_template("home.html", pagename=pagename)

@app.route("/login")
def login():
    pagename = 'Login'
    return render_template("login.html", pagename=pagename)

@app.route("/create-account")
def create_acc():
    pagename="Create Account"
    return render_template("create_acc.html", pagename=pagename)

@app.route("/grades-instructor")
def grades_instructor():
    pagename="Instructor's View of Grades"
    return render_template("grades_insview.html", pagename=pagename)

@app.route("/grades-student")
def grades_instructor():
    pagename="Student's View of Grades"
    return render_template("grades_stuview.html", pagename=pagename)

if __name__ == "__main__":
    app.run(debug=True)