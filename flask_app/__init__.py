from flask import Flask
from flask_bcrypt import Bcrypt 
app = Flask(__name__)
app.secret_key = "OIAJFOIJASIOFASOJFOAISJDO3ASJFOASOIDJOIASIOFJAOSIJGOIJASOIFJASOIJFo"
bcrypt = Bcrypt(app)
DATABASE = "recipes_db"