from flask_app import app
from flask_app import bcrypt
from flask_app.models.model_user import User
from flask import redirect, request, session

@app.route("/register", methods=["POST"])
def register():
    data = {**request.form}

    if not User.validate_reg(data) :
        return redirect("/")
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data['password'] = pw_hash
    
    User.save(data)
    session['data'] = data

    return redirect("/recipes")

@app.route("/login/validate", methods=["POST"])
def loginValidate():
    data = {**request.form}

    if(not User.validate_login(data)):
        return redirect("/")
    
    session['data'] = data

    return redirect("/recipes")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")