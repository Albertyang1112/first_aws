from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE
from flask_app import bcrypt
from flask import flash
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self, data:dict):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data:dict) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s, password = %(password)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def delete(cls, data:dict) -> None:
        query = "DELETE FROM users WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    @classmethod
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)

        if not results:
            return False
        
        return cls(results[0])

    @staticmethod
    def validate_reg(user:dict):
        is_valid = True
        has_upper = False
        has_lower = False
        has_spec = False
        has_num = False
        spec_chars = re.compile('[@_!#$%^&*()<>?/\|}{~:]')

        results = User.get_user_by_email({"email": user['email']})

        if not results:
            if len(user['first_name']) < 2:
                flash("First name must be at least 2 characters long", "error")
                is_valid = False
            if len(user['last_name']) < 2:
                flash("Last name must be at least 2 characters long", "error")
                is_valid = False
            if not EMAIL_REGEX.match(user['email']):
                flash("Invalid email address!", "error")
                is_valid = False
            if len(user['password']) < 8:
                flash("Password must be at least 8 characters long", "error")
                is_valid = False
            if not user['password'] == user['confirm_password']:
                flash("Passwords don't match", "error")
                is_valid = False

            for chars in range(0, len(user['password'])):
                if user['password'][chars].islower():
                    has_lower = True
                if user['password'][chars].isupper():
                    has_upper = True
                if spec_chars.search(user['password'][chars]):
                    has_spec = True
                if user['password'][chars].isnumeric():
                    has_num = True
            if not has_lower or not has_upper or not has_spec or not has_num:
                flash("Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character", "error")
                is_valid = False

        else:
            flash("Email already taken!", "error")
            is_valid = False 

        return is_valid
    
    @staticmethod
    def validate_login(user:dict):
        is_valid = True
        results = User.get_user_by_email({"email": user['email']})

        if results:
            if not bcrypt.check_password_hash(results.password, user['password']):
                flash("Invalid email or password", "loginError")
                is_valid = False
        else:
            flash("Invalid email or password", "loginError")
            is_valid = False
        return is_valid