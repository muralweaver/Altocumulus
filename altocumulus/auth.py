import requests
from flask import Blueprint, render_template, url_for, request, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/signup')
def signup():
    # code to validate and add user to database goes here
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.signup'))
    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(email=email, password=generate_password_hash(password, method='sha256'))
    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('auth.login'))


@auth.route('/logout')
def logout():
    return 'Logout'