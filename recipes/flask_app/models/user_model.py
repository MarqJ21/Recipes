from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.recipe_model import Recipe
from flask import flash
import re
import pprint

db = "recipes"
class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipe = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO user (first_name, last_name, email, password) VALUES (%(fname)s, %(lname)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM user"
        results = connectToMySQL(db).query_db(query)
        all_users  = []
        for user in results:
            all_users.append(cls(user))
        return all_users

    @classmethod
    def get_single_user(cls, data):
        query = "SELECT * from users where id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod 
    def get_single_user(cls):
        query = "SELECT * FROM user JOIN recipe ON recipe.user_id = user.id ORDER BY user.id ASC"
        results = connectToMySQL(db).query_db(query)
        user = []
        for recipe in results:
            if len(user) == 0:
                user.append(cls(recipe))
            else:
                last_user = user[len(user) - 1]
                if last_user.id != recipe['id']:
                    user.append(cls(recipe))
            last_user = user[len(user) - 1]
            recipe_dictionary ={
                'id' : recipe["recipe.id"],
                'name' : recipe['name'],
                'description' : recipe['description'],
                'instruction' : recipe['instruction'],
                'date' : recipe['date'],
                'under' : recipe['under'],
                'created_at' : recipe['created_at'],
                'updated_at' : recipe['updated_at']
            }
            last_user.recipe.append(Recipe(recipe_dictionary))
        return user
    
    @classmethod 
    def get_single_recipe(cls,data):
        query = "SELECT * FROM user left join recipe ON recipe.user_id = user.id where recipe.id = %(id)s"
        results = connectToMySQL(db).query_db(query,data)
        user = cls(results[0])
        for recipe in results:
            recipe_dictionary ={
                'id' : recipe["recipe.id"],
                'name' : recipe['name'],
                'description' : recipe['description'],
                'instruction' : recipe['instruction'],
                'date' : recipe['date'],
                'under' : recipe['under'],
                'created_at' : recipe['recipe.created_at'],
                'updated_at' : recipe['recipe.updated_at']
            }
            user.recipe.append(Recipe(recipe_dictionary)) 
        return user

    @classmethod
    def validate_user(cls, User):
        is_valid = True
        if len(User['fname']) < 2:
            flash("First name must be at least 3 characters")
            is_valid = False
        if len(User['lname']) < 2:
            flash("Last name must be at least 3 characters")
            is_valid = False
        if User['password'] != User['cpass']:
            flash("Passwords don't match")
            is_valid = False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, User['email']):
            flash("Invalid email address")
            is_valid = False
        return is_valid


    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM user WHERE email = %(email)s"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False 
        return cls(results[0])

    @classmethod
    def get_user_by_id(cls,id):
        query = "SELECT * FROM user WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query,{'id':id})
        if len(results) < 1:
            return False 
        return cls(results[0])

    @classmethod
    def delete_user(cls,id):
        query = f"DELETE FROM users WHERE id = {id}"
        return connectToMySQL(db).query_db(query)

    