from flask_app import app
from flask import render_template, request, redirect, session, flash
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe


@app.route('/create_recipe')
def index_recipe():
    return render_template("new.html")

@app.route("/add_recipes", methods=[ "post"])
def create_recipe():
    
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "date": request.form['date'],
        "under": request.form['under'],
        "user_id": session['user_id']
    }
    Recipe.save(data)
    return redirect ("/recipes")

@app.route("/show/<int:id>")
def show_one_user(id):
    data = {
        'id' : id
    }
    return render_template("show.html", one_user = User.get_single_recipe(data))

@app.route("/edit/<int:id>")
def edit_one_user(id):
    data = {
        'id' : id
    }
    return render_template("edit.html", one_user = Recipe.get_recipe_by_id(data))

@app.route("/update_recipe", methods=[ "post"])
def update_recipe():
    
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "date": request.form['date'],
        "under": request.form['under'],
        "id": request.form['id']
    }
    Recipe.update_recipe(data)
    return redirect("/recipes")