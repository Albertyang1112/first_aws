from flask_app import app
from flask import render_template, redirect, session

@app.route("/")
def regLog():

    if 'data' not in session:
        return render_template("login.html")
    else:
        return redirect("/recipes")

    