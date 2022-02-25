from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
# from flask_app.models.recipe import Recipe
import re

class User():
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def user_registration(cls, data):
        query = "INSERT INTO users ( first_name, last_name, email, password ) VALUES ( %(firstname)s , %(lastname)s, %(email)s, %(password)s );"
        # data is a dictionary that will be passed into the save method from server.py
        return connectToMySQL('recipes_schema').query_db( query, data )

    @classmethod 
    def get_user_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"

        results = connectToMySQL('recipes_schema').query_db( query, data )

        if len(results) == 0:
            return False
        else:
            return cls(results[0])

    @staticmethod
    def validate_registration(data):
        is_valid = True
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        LETTER = re.compile(r'^[a-zA-Z]+$')

        if  not LETTER.match(data['firstname']):
            flash("Firstname should be just letter's only!")
            is_valid = False
        if len(data['firstname']) < 2 :
            flash("First name must be at least 2 characters long!")
            is_valid = False

        if  not LETTER.match(data['lastname']):
            flash("Lastname should be just letter's only!")
            is_valid = False
        if len(data['lastname']) < 2:
            flash("Last name must be at least 2 characters long!")
            is_valid = False

        if  User.get_user_by_email(data): #checking is it already in the database
            flash("Email already exists!")
            is_valid = False
        if  not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False

        if len(data['password']) < 8:
            flash("Password must be at least 8 characters long!")
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash("Passwords do not match!")
            is_valid = False

        return is_valid