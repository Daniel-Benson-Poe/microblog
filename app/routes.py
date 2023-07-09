from flask import render_template, flash, redirect, url_for
from flask import request
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm


@app.route('/')
@app.route('/index')
@login_required # Flask-Login decorator requiring the user to be logged in before they are allowed to view the webpage (in this case the /index)
def index():
    posts = [
        {
            'author' : {'username' : 'John'},
            'body' : 'Beautiful day in Portland!'
        },
        {
            'author' : {'username' : 'Susan'},
            'body' : 'The Avengers movie was so cool!'
        }
    ]
    
    return render_template('index.html', title="Home Page", posts=posts)
    # return render_template('index.html', user=user) # Testing the default title

@app.route('/login', methods=['GET', 'POST'])
def login():
    # A user can accidentally (or intentionally) reroute to the /login URL even after logging in and we don't want to allow that; the following two lines of code reroute the logged-in user back to the home page
    if current_user.is_authenticated: # current_user comes from Flask-Login representing the client of the request
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit(): # on submit query the data entered into the form
        user = User.query.filter_by(username=form.username.data).first() # filtering the query to only include objects having a matching username; query is completed by calling first() since we know there will only ever be 1 or 0 results, returning either the user object if it exists or returning None if it does not exist
        if user is None or not user.check_password(form.password.data): # check_password compares the password data entered into the form with the existing password hash stored with the username; if either the username is invalid OR the password does not mach a message is flashed informing the user and they are redirected to the login prompt to try again
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data) # If all entered data is correct the user is logged in and any future pages that are navigated to will have the current_user variable set to that user
        next_page = request.args.get('next') # the @login_required decorator creates a 'next' query string that reroutes the user to a subsequent webpage after they have logged in, so the redirect URL will look like: /login?next=/<next page>
        if not next_page or url_parse(next_page).netloc != '': # an attacker could insert a URL to a malicious site in the 'next' argument; to improve security, we will only allow the application to redirect when the URL is relative, ensuring the redirect stays within the same site as the application; url_parse is used to determine if the URL is relative or absolute, then netloc is checked to see if it is set or not
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)