from flask_login import UserMixin
from __init__ import db
import enum

class Gender(enum.Enum):
    Male = 1
    Female = 2

class Atoll(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    name = db.Column(db.String(100))

class Island(db.Model):
    id  = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(100))
    name = db.Column(db.String(100))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    atoll = db.Column(db.String(200),db.ForeignKey('atoll.id'))
    island = db.Column(db.String(200),db.ForeignKey('island.id'))
    address = db.Column(db.String(200))
    gender = db.Column(db.Enum(Gender))
    dob =  db.Column(db.String(100))




class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Products(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.Integer, db.ForeignKey('categories.id'))
    price =  db.Column(db.Float)
    image = db.Column(db.String(200))


class Stock(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    amount = db.Column(db.Integer)

    # updated_at = db.Column(db.DateTime)

class Likes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    liked_at = db.Column(db.DateTime)

class Purchases(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    qty = db.Column(db.Integer)
    bought_at = db.Column(db.String(100))

class Similarities(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    user_id_c = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_id_t = db.Column(db.Integer, db.ForeignKey('user.id'))
    score = db.Column(db.Float)
 
class SearchOps(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    keywords = db.Column(db.String(250))
    created_at = db.Column(db.DateTime)

  
 

