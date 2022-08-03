from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm
#from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
# from api import secret_key
import requests
import json
import pandas as pd
import secrets
import sys
sys.path.insert(0, 'model')
from webscrape import Book, thriftbooks, cheapest_textbooks, is_isbn
import googleBooks
import database

app = Flask(__name__)
#proxied = FlaskBehindProxy(app)
# app.config['SECRET_KEY'] = secret_key
sec_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = str(sec_key)
database.make_tables()


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        title = request.form['title']
        if is_isbn(title):
            title_2 = googleBooks.Book(title).getTitle()
        print(title_2)
        books = cheapest_textbooks(title=title)
        books.update(thriftbooks(title_2))
        return render_template('index.html', books=books)
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        registered = database.register(form.username.data,
                          form.email.data,
                          form.password.data)
        if not registered:
            flash('An account already exists with this username/email')
            return redirect(url_for('user'))
        else:
            flash(f'Account created for {form.username.data}!', 'success')
            database.create_wishlist(database.get_user_id(username=form.username.data))
            return redirect(url_for('login'))
    return render_template('register.html', title='Register Here!', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if database.login(form.username.data, form.password.data) == (True, True):
            global id
            id = database.get_user_id(username=form.username.data)
            flash(f'Signed in as {form.username.data}!', 'success')
            return redirect(url_for('user'))
        else:
            flash('Incorrect username/password')
            return redirect(url_for('login'))
    return render_template('login.html', form=form)


@app.route("/user", methods=['GET', 'POST'])
def user():
    if request.method == 'POST':
        title = request.form['title']
        books = cheapest_textbooks(title=title)
        books.update(thriftbooks(title))
        return render_template('user.html', books=books)
    return render_template('user.html')


@app.route('/wishlist', methods=['GET', 'POST'])
def wishlist():
    wishlist = database.get_wishlist(id)
    print(wishlist)
    return render_template('wishlist.html')


@app.route("/book-of-the-day")
def bookOfDay(): # a temporary test run
    return render_template('book-of-the-day.html', title="Chemistry 101", summary="This is a textbook about Chemistry. It is for the introductory course, CHEM 101. blah blah blah", price="$69.00")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
