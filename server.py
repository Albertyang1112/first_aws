from flask_app import app
from flask_app.controllers import controller_user, controller_recipe, controller_route

if __name__ == "__main__":
    app.run(debug=True)