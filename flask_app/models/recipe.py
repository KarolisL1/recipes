from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, redirect
from flask_app.models.user import User
import re

class Recipe():
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_30_min = data['under_30_min']
        self.date_made_on = data['date_made_on']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None

    @classmethod
    def recipes_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        # make sure to call the connectToMySQL function with the schema you are targeting.
        results = connectToMySQL('recipes_schema').query_db(query)
        # Create an empty list to append our instances of friends
        recipes = []
        # Iterate over the db results and create instances of friends with cls.
        # for recipe in results:
        #     recipes.append( cls(recipe) )
        # return recipes
        for item in results:
            new_recipe = Recipe(item)

            user_data = {
                "id": item['users.id'],
                "first_name": item['first_name'],
                "last_name": item['last_name'],
                "email": item['email'],
                "password": item['password'],
                "created_at": item['users.created_at'],
                "updated_at": item['users.updated_at']
            }
            new_recipe.user = User(user_data)
            recipes.append(new_recipe)

        return recipes

    @classmethod
    def recipe_create(cls, data):
        query = "INSERT INTO recipes ( name, description, instructions, under_30_min, date_made_on, user_id ) VALUES ( %(name)s , %(description)s, %(instructions)s, %(under_30_min)s, %(date_made_on)s, %(user_id)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipes_schema').query_db( query, data )

    @classmethod
    def get_recipe_by_id(cls, data):
        query = "SELECT * from recipes join users on recipes.user_id = users.id WHERE recipes.id = %(recipe_id)s;"
        results = connectToMySQL('recipes_schema').query_db( query, data )

        recipe = Recipe(results[0])

        user_data = {
            "id": results[0]['users.id'],
            "first_name": results[0]['first_name'],
            "last_name": results[0]['last_name'],
            "email" : results[0]['email'],
            "password": results[0]['password'],
            "created_at": results[0]['users.created_at'],
            "updated_at": results[0]['users.updated_at']
        }

        recipe.user = User(user_data)

        return recipe

    @classmethod
    def recipes_update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, under_30_min = %(under_30_min)s, date_made_on = %(date_made_on)s WHERE id = %(recipe_id)s;"
        return connectToMySQL('recipes_schema').query_db( query, data )

    @classmethod
    def recipes_delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
        return connectToMySQL('recipes_schema').query_db( query, data )

    @staticmethod
    def validate_recipe(data):
        is_valid = True
        LETTER = re.compile(r'^[a-zA-Z]+$')

        if len(data['name']) < 3:
            is_valid = False
            flash("Recipe name must be at least 3 characters")
        # if not LETTER.match(data['name']):
        #     is_valid = False
        #     flash("Recipe name must be letters only")

        if len(data['description']) < 3:
            is_valid = False
            flash("Recipe description must be at least 3 characters")
        # if not LETTER.match(data['description']):
        #     is_valid = False
        #     flash("Recipe description must be letters only")

        if len(data['instructions']) < 3:
            is_valid = False
            flash("Recipe instructions must be at least 3 characters")
        # if not LETTER.match(data['instructions']):
        #     is_valid = False
        #     flash("Recipe instructions must be letters only")
        return is_valid
