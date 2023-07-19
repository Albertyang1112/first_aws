from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_user
from flask_app import DATABASE

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.user_id = data['user_id']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under = data['under']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, under, date_made, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under)s, %(date_made)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_one(cls, id):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, {"id": id})
        recipe = results[0]
        recipe_instance = cls(recipe)
        user_data = {
            "id": recipe['users.id'],
            "first_name": recipe['first_name'],
            "last_name": recipe['last_name'],
            "email": recipe['email'],
            "password": recipe['password'],
            "created_at": recipe['users.created_at'],
            "updated_at": recipe['users.updated_at']
        }
        recipe_instance.user = model_user.User(user_data)
        return recipe_instance
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        recipes = []
        for recipe in results:
            recipe_instance = cls(recipe)
            user_data = {
                **recipe,
                "id": recipe["users.id"],
                "created_at": recipe["users.created_at"],
                "updated_at": recipe['users.updated_at']
            }
            recipe_instance.user = model_user.User(user_data)
            recipes.append(recipe_instance)
        return recipes

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under = %(under)s, date_made = %(date_made)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def delete(cls, recipe_id):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, {"id": recipe_id})