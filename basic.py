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
from webscrape import Book, thriftbooks, cheapest_textbooks
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
        books = cheapest_textbooks(title=title)
        books.update(thriftbooks(title))
        return render_template('index.html')
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        registered = database.register(form.username.data,
                          form.email.data,
                          form.password.data)
        if not registered:
            print('An account already exists with this username/email')
        else:
            print(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register Here!', form=form)


@app.route("/book-of-the-day")
def bookOfDay(): # a temporary test run
    return render_template('book-of-the-day.html', title="Chemistry 101", summary="This is a textbook about Chemistry. It is for the introductory course, CHEM 101. blah blah blah", price="$69.00")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
