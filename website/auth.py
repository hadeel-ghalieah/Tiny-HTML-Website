from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash  ## for "Hashing" the password
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        ## checking if the entered email is valid, i.e., if it is in the database
        user = User.query.filter_by(email=email).first() ## return the first result   
        if user:
            ## checking if the entered Password is equal to the stored HASH.
            ##              user.password =? password
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            ## define a user
            new_user = User(email=email, first_name=first_name, password=
                            generate_password_hash(password1, method='sha256'))
            ## add this user to the database
            db.session.add(new_user)
            ## telling the database to update itself 
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            ## redirect the user to the HOME page in order to loging to his/her
            ##                  account to access the main page
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)




