
# from flask_login import LoginManager
from datetime import datetime
from setup import db
# from flask_login import UserMixin
from sqlalchemy.orm.collections import attribute_mapped_collection

# Table 1: ID, Date, Time, Text and Num of Calories and User ID (fk) (CRUD by User)
# Table 2: User ID (pk), Name, Email, Role ID, Password (CRUD by Manager)

class Record(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, default=datetime.now, nullable=False)
    # time = db.Column(db.Text, nullable=True)
    text = db.Column(db.String(250), nullable=False)
    num_calories = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # In user model, Test is started with capital letter because we are using the actual Test class.
    # But here we use 'user.id' with small u because it is actual table in db, and actual column
    # table and column name are simply lowercase by default

    def __repr__(self):
        return f"Record('{self.id}, {self.datetime}, {self.text}, {self.num_calories}, {self.user_id}')"

# Class for users
class User(db.Model): 
    # columns
    # __tablename__ = "users"  # to get old users
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role_id = db.Column(db.Integer, nullable=False) # 1 for user, 2 for user manager and 3 for admin
    expected_calories = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # password = db.Column(db.String(60), nullable=True)
    # hashing algorithm will make this string as 60 char long
    records = db.relationship('Record', backref='owner', lazy=True)
    # backref is similar to adding another column

    # Magic Method: How object is printed when we print it (also __scr__)
    def __repr__(self):
        return f"User('{self.id}, {self.name}, {self.email}, {self.role_id}')"
