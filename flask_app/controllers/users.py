from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    data = {
        'firstname' : request.form['firstname'],
        'lastname' : request.form['lastname'],
        'email' : request.form['email'],
        'password' : bcrypt.generate_password_hash(request.form['password'])
    }
    if not User.validate_registration(request.form):
        flash('Please fill out all fields.')
        return redirect('/')
    User.user_registration(data) # saving user to database
    flash('You have successfully registered!')
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    user = User.get_user_by_email(request.form)
    if not user:
        flash('Email does not exists!')
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password is incorrect!')
        return redirect('/')

    session['user_id'] = user.id
    session['firstname'] = user.first_name
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have successfully logged out!")
    return redirect('/')
