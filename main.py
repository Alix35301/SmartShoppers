########################################################################################
######################          Import packages      ###################################
########################################################################################
import uuid

from flask.templating import render_template_string
from models import Atoll, Categories, Island, Likes, Products, Purchases, SearchOps, Similarities, Stock, User
from flask import Blueprint, render_template, flash, request, redirect, url_for, g
from flask_login import login_required, current_user
from datetime import datetime
from werkzeug.utils import secure_filename
from __init__ import create_app, db
import os
from sqlalchemy.sql.expression import func

########################################################################################
# our main blueprint
main = Blueprint('main', __name__)



@main.route('/') # home page that return 'index'
def index():
    
    products = Products.query.all()
    categories = Categories.query.all()

    from sqlalchemy import create_engine, engine
    import pandas as pd
    engine = create_engine('sqlite:///db.sqlite')
    c_user = current_user.get_id()
    recommends = None
    if c_user is not None:
        print(c_user)
        rp = Similarities.query.filter_by(user_id_t = c_user).order_by(Similarities.score.desc()).first()
        if rp is not None:
            similar_user = rp.user_id_c
            rec_products = [p.product_id for p in Purchases.query.filter_by(user_id=similar_user).order_by(func.random()).limit(5).all()]
            print(rec_products)
            recommends = Products.query.filter(Products.id.in_(rec_products)).all()
        # print(results_pur_hist)
    return render_template('index.html', products = products, categories = categories, recommends = recommends, searchbutton = True)

@main.route('/profile') # profile page that return 'profile'
@login_required
def profile():

    results_pur_hist = db.session.query(Products, Purchases).select_from(Products).join(Purchases).filter(Purchases.user_id ==current_user.get_id()).all()
    results_likes = db.session.query(Products, Likes).select_from(Products).join(Likes).filter(Likes.user_id ==current_user.get_id()).all()
    user = db.session.query(User,Atoll,Island).select_from(User).join(Atoll).join(Island).filter(User.id == current_user.get_id()).all()
    # purchase_history = Purchases.query.join(Products, Purchases.product_id == Products.id).all()
    # # for i in purchase_history:
    # print(results)
    # for product, purchases in results:
    #     print(product.name, purchases.product_id)

    return render_template('profile.html', user=user, results_pur_hist = results_pur_hist,  results_likes= results_likes)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/add-items', methods=['GET', 'POST']) # home page that return 'index'
def add_items():
    categories = Categories.query.all()
    print(categories)
    if request.method=='GET': # If the request is GET we return the sign up page and forms
        return render_template('add_items.html',value =  categories)    
    else: # if the request is POST, then we check if the email doesn't already exist and then we save data
         name = request.form.get('name')
         price = request.form.get('price')
         category = request.form.get('category')

         print(name, price, category)
         print(request.files)

         if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
         file = request.files['image']
        # if user does not select file, browser also
        # submit a empty part without filename
        
         if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
         if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            extension = filename.split()[-1]
            filename = f"{str(uuid.uuid4())}.{extension}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Product Saved!')
         new_product = Products(name=name,category=category,price=price,image=filename)
         db.session.add(new_product)
         db.session.commit()        
         return render_template('add_items.html',value =  categories)  

    #     name = request.form.get('name')
    #     password = request.form.get('password')
    #     user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
    #     if user: # if a user is found, we want to redirect back to signup page so user can try again
    #         flash('Email address already exists')
    #         return redirect(url_for('auth.signup'))
    #     # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    #     new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256')) #
    #     # add the new user to the database
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return redirect(url_for('auth.login'))

@main.route('/categories/<id>', methods=['GET']) # home page that return 'index'
def show_category_items(id):
    categories = Categories.query.all()

    category = Categories.query.filter_by(id=id).all()
    print(category[0].id)
    products = Products.query.filter_by(category=int(category[0].id)).all()
    print(products)
    return render_template("category.html", products =  products, categories = categories , searchbutton = True)

@main.route('/product/<id>')
def buy(id):
    stock = Stock.query.filter_by(product_id=id).first()
    if stock is None or stock is 0:
        stock = 0
    else:
        stock = stock.amount
    # print(stock[0].amount)
    categories = Categories.query.all()
    product = Products.query.filter_by(id=id).all()
    # print(product)
    from flask import g
    if current_user.is_authenticated:
        g.user = current_user.get_id()
    return render_template("product.html", categories = categories, product = product[0], stock=stock)

@main.route('/like/<id>', methods=['GET','POST'])
@login_required
def like(id):
    new_like = None
    # categories = Categories.query.all()
    # product_id = request.form.get('product_id')

    if current_user.is_authenticated:
        g.user = current_user.get_id()
        new_like = Likes(product_id = id, user_id =g.user, liked_at  =  datetime.now())
        if Likes.query.filter_by(product_id = id, user_id = g.user).first() is None:
            db.session.add(new_like)
            db.session.commit()
    return redirect(request.referrer)

@main.route('/purchase-item/<id>', methods=['POST'])
@login_required
def purchase_product(id):
    categories = Categories.query.all()

    req_qty = request.form.get('qty')
    if current_user.is_authenticated:
        g.user = current_user.get_id()
    qty = Stock.query.filter_by(product_id = id).first()
    if qty is not None:
        # deducting from the stock
        if int(req_qty) <= qty.amount:
            qty.amount = qty.amount-int(req_qty)
        # adding product to purchase table
        new_purchase = Purchases(product_id =  id, user_id = g.user, qty = req_qty, bought_at = datetime.now())
        db.session.add(new_purchase)
        db.session.commit()
    return redirect(request.referrer)

@main.route('/search-product', methods=['POST','GET'])
def search_results():
    keyword_from_form = request.form.get('name')
    categories = Categories.query.all()
    results =None
    # results = Products.query.filter_by(name = keyword_from_form).all()
    results = Products.query.filter(Products.name.ilike(keyword_from_form)).all()

    user_id  = None
    if current_user.is_authenticated:
        user_id = current_user.get_id()
    search_keyword = SearchOps(created_at = datetime.now(), keywords=keyword_from_form, user_id = user_id)
    db.session.add(search_keyword)
    db.session.commit()
    return render_template("search_results.html", categories = categories, results= results)

@main.route('/add-category', methods=['POST'])
def add_category():
    category_to_add = request.form.get('category')
    category = Categories(name=category_to_add)
    db.session.add(category)
    db.session.commit()
    return redirect(url_for('main.add_items'))


@main.route('/delete-account')
@login_required

def delete_account():
    user_id = current_user.get_id()
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect(url_for('auth.login'))

@main.route('/reports')
def report():
    return render_template("reports.html")

    
app = create_app() # we initialize our flask app using the __init__.py function
UPLOAD_FOLDER = 'static'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg','webp'])
if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    app.run(debug=True) # run the flask app on debug mode