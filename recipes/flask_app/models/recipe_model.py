from flask_app.config.mysqlconnection import connectToMySQL
import pprint

db = "recipes"
class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date = data['date']
        self.under = data['under']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipe (name, description, instruction, date, under, user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(date)s, %(under)s, %(user_id)s);"
        return connectToMySQL(db).query_db(query, data)

    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipe"
        results = connectToMySQL(db).query_db(query)
        all_recipes  = []
        for ninja in results:
            all_recipes.append(cls(ninja))
        return all_recipes

    @classmethod
    def get_recipe_by_id(cls,data):
        query = "SELECT * FROM recipe WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipe set name = %(name)s, description = %(description)s, instruction = %(instruction)s, date = %(date)s, under = %(under)s WHERE id = %(id)s"
        return connectToMySQL(db).query_db(query, data)

        