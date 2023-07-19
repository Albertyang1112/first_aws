from flask_app import app
from flask_app.models.model_recipe import Recipe
from flask_app.models.model_user import User
from flask import render_template, redirect, request, session


@app.route("/recipes")
def recipes():
    if not session:
        return redirect("/")
    
    user = User.get_user_by_email(session['data'])
    print("*" * 100)
    print(user)
    print("*" * 100)
    recipes = Recipe.get_all()
    return render_template("dashboard.html", user = user, recipes = recipes)

@app.route("/recipes/new")
def newRecipe():
    user = User.get_user_by_email(session['data'])
    return render_template("addRecipe.html", user = user)

@app.route("/recipes/create", methods=["POST"])
def createRecipe():
    data = {**request.form}
    Recipe.save(data)
    return redirect("/recipes")

@app.route("/recipes/edit/<int:recipe_id>")
def editRecipe(recipe_id):
    recipe = Recipe.get_one(recipe_id)
    return render_template("editRecipe.html", recipe = recipe)

@app.route("/recipes/update", methods=["POST"])
def updateRecipe():
    data = {**request.form}
    Recipe.update(data)
    return redirect("/recipes")

@app.route("/recipes/<int:recipe_id>")
def viewRecipe(recipe_id):
    recipe = Recipe.get_one(recipe_id)
    user = User.get_user_by_email(session['data'])
    return render_template("viewRecipe.html", recipe = recipe, user = user)

@app.route("/recipes/delete/<int:recipe_id>")
def deleteRecipe(recipe_id):
    Recipe.delete(recipe_id)
    return redirect("/recipes")