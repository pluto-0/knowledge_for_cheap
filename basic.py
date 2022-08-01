from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_behind_proxy import FlaskBehindProxy
from flask_sqlalchemy import SQLAlchemy
# from api import secret_key
import requests
import json
import pandas as pd
import secrets
import sqlalchemy as db1

app = Flask(__name__)
proxied = FlaskBehindProxy(app)
# app.config['SECRET_KEY'] = secret_key
sec_key = secrets.token_hex(16)
app.config['SECRET_KEY'] = str(sec_key)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=True, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def __repr__(self):
    return f"User('{self.username}', '{self.email}')"


@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register Here!', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit() and 


@app.route("/book-of-the-day")
def bookOfDay(): # a temporary test run
    return render_template('book-of-the-day.html', title="Chemistry 101", summary="This is a textbook about Chemistry. It is for the introductory course, CHEM 101. blah blah blah", price="$69.00")


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
