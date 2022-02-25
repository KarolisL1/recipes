from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
# from flask_bcrypt import Bcrypt

# bcrypt = Bcrypt(app)

@app.route("/dashboard")
def recipes_all():
    if 'user_id' not in session:
        flash("Please login first!")
        return redirect('/')
    recipe = Recipe.recipes_all()
    return render_template("dashboard.html", recipe=recipe)

@app.route("/recipes/new")
def recipes_new():
    return render_template("recipes_new.html")

@app.route("/recipes/create", methods=["POST"])
def recipes_create():
    recipe = Recipe.validate_recipe(request.form)
    if not recipe:
        flash("Please fill out all fields")
        return redirect("/recipes/new")
    else:
        data = {
            "name": request.form['name'],
            "description": request.form['description'],
            "instructions": request.form['instructions'],
            "under_30_min": request.form['under_30_min'],
            "date_made_on": request.form['date_made_on'],
            "user_id": session['user_id']
        }
        print(data)
        Recipe.recipe_create(data)
        return redirect("/dashboard")

@app.route("/recipe/<int:recipe_id>")
def single_recipe(recipe_id):
    data = {
        "recipe_id": recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template("single_recipe.html", recipe=recipe)

@app.route("/recipe/<int:recipe_id>/edit")
def edit_recipe(recipe_id):
    data = {
        "recipe_id": recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template("edit_recipe.html", recipe=recipe)

@app.route("/recipe/<int:recipe_id>/update", methods=["POST"])
def update_recipe(recipe_id):
    #validate recipe
    recipe = Recipe.validate_recipe(request.form)
    if not recipe:
        flash("Please fill out all fields")
        return redirect(f"/recipe/{recipe_id}/edit")
    else:
        data = {
            "recipe_id": recipe_id,
            "name": request.form['name'],
            "description": request.form['description'],
            "instructions": request.form['instructions'],
            "under_30_min": request.form['under_30_min'],
            "date_made_on": request.form['date_made_on']
        }   
        Recipe.recipes_update(data)
        print("Validation works")
        return redirect(f"/recipe/{recipe_id}")

@app.route("/recipe/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    data = {
        "recipe_id": recipe_id
    }
    Recipe.recipes_delete(data)
    return redirect("/dashboard")

