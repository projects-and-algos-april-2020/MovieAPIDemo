from flask import render_template, redirect, request, flash, session
from models import User, Review
from config import bcrypt, db, API_KEY
import requests

import re
# from app import User
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


def index():

    return render_template("index.html", users=User.query.all())

def register():
    errors = []

    if len(request.form['first_name']) < 2:
        errors.append("First name must be at least 2 characters")
        valid = False

    if len(request.form['last_name']) < 2:
        errors.append("Last name must be at least 2 characters")
        valid = False

    if not EMAIL_REGEX.match(request.form['email']):
        errors.append("Email must be valid")
        valid = False

    if len(request.form['password']) < 8:
        errors.append("Password must be at least 8 characters")
        valid = False

    #TODO: Validate email is unique
    user_check = User.query.filter_by(email=request.form["email"]).first()
    if user_check is not None:
        errors.append("Email is in use")
    
    if request.form['password'] != request.form['confirm']:
        errors.append("Passwords must match")
        valid = False

    if errors:
        for e in errors:
            flash(e)
    else:
        hashed = bcrypt.generate_password_hash(request.form["password"])
        new_user = None
        #TODO: Create New User
        new_user = User(
            first_name = request.form["first_name"],
            last_name = request.form["last_name"],
            email = request.form["email"],
            password = hashed
        )
        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id
        return redirect("/dashboard")

    return redirect("/")

def login():
    errors = []

    user_attempt = User.query.filter_by(email=request.form["email"]).first()
    #TODO: Query for user wiith provided email
    
    if not user_attempt:
        flash("Email/Password Incorrect")
        return redirect("/")

    if not bcrypt.check_password_hash(user_attempt.password, request.form["password"]):
        flash("Email/Password Incorrect")
        return redirect("/")

    session["user_id"] = user_attempt.id
    return redirect('/dashboard')

def logout():
    session.clear()
    return redirect("/")

def dashboard():
    # get user from session
    if not "user_id" in session:
        return redirect("/")
  

    return render_template("dashboard.html")

def search():
    if request.form['year'] != "":
        response_movies = requests.get(f"http://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={request.form['query']}&year={request.form['year']}")
    else:
        response_movies = requests.get(f"http://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={request.form['query']}")
    result_movies = response_movies.json()['results']
    return render_template("dashboard.html", movies=result_movies)

def movie_details(id):
    reviews = Review.query.filter_by(movie_api_id=id).all()
    response = requests.get(f"http://api.themoviedb.org/3/movie/{id}?api_key={API_KEY}")
    result= response.json()
    return render_template("movie_details.html", movie=result, reviews=reviews)