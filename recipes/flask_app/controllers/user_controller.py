from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# I got super confused with this one still gonna get it working on my own time just don't want it to be late

@app.route('/')
def index():
    return render_template("index.html")

@app.route("/recipes")
def success():
    if 'user_id' not in session:
        flash("You need to log in before accessing this page")
        return ('/')
    users = User.get_all()
    recipe = Recipe.get_all()
    return render_template("recipes.html", all_users = users, user = User.get_user_by_id(session['user_id']), all_recipes = User.get_single_user())
    
@app.route("/create_user", methods=[ "post"])
def create_user():
    if  User.get_by_email(request.form) == True:
        flash("email is already in use or password  and confrim password do not match")
        return redirect('/')
    
    data = {
        'fname' :request.form['fname'],
        'lname' :request.form['lname'],
        'email' :request.form['email'],
        'password' :request.form['password'],
        'cpass' :request.form['cpass']
    }

    if not User.validate_user(data):
        return redirect('/')

    data['password'] = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    del data['cpass']

    user_id = User.save(data)
    session['user_id'] = user_id
    return redirect("/")

@app.route("/login", methods =['post'])
def login():
    data = {
        'email' :request.form['email']
    }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Email or password not correct')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Email or password not correct')
        return redirect("/")
    session['user_id'] = user_in_db.id
    return redirect("/recipes")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

def clear_first_name():
    session.pop('fname')
    return redirect("/")

@app.route("/delete/<int:id>")
def delete_user(id):
    User.delete_user(id)
    return redirect("/success")