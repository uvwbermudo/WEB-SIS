
from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import current_user, login_user, login_required, logout_user
from . forms import RegisterForm, UserForm
from . models import User, CurrentUser
from flaskr import mysql
from flaskr import get_error_items, get_form_fields
from werkzeug.security import generate_password_hash, check_password_hash
import json
import wtforms_json


wtforms_json.init()
auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('student_view.students'))
    else:
        return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('student_view.students'))

    form = UserForm()
    if request.method =='POST':
        form_json = request.get_json()
        form = UserForm.from_json(form_json)
        fields = get_form_fields(form)
        if form.validate_on_submit():
            email = request.json['email']
            password = request.json['password']
            user = User.query_filter_by(email=email)
            
            if user:
                if check_password_hash(user['user_password'], password):
                    my_current_user = User.query_current_user(user['email'])
                    login_user(my_current_user)
                    flash('Logged in successfully', category='success')
                    return Response(status=299)
                errors = get_error_items(form)
                errors['password'] = ['Incorrect Password']
                return Response(json.dumps([errors, fields]), status=499, mimetype='application/json')
        
            else:
                errors = get_error_items(form)
                errors['email'] = ['Email does not exist']
                return Response(json.dumps([errors, fields]), status=499, mimetype='application/json')
        else:
            errors = get_error_items(form)
            return Response(json.dumps([errors, fields]), status=499, mimetype='application/json')
 
            
    return render_template('auth/login.html', form=form)


@auth.route('/register')
def register():
    form = RegisterForm()
    return render_template('auth/register.html', form=form)


@auth.route('/register-user', methods=['GET','POST'])
def register_user():
    temp_json = request.get_json()
    form = RegisterForm.from_json(temp_json)
    fields = get_form_fields(form)
    if request.method == 'POST':
        email = request.json['email']
        password = request.json['password']
        user = User.query_filter_by(email=email)
        if form.validate():
            if user:
                errors = get_error_items(form)
                errors['email']= ['Email is already taken.']
                return Response(json.dumps([errors, fields]), status=499, mimetype='application/json')
            new_user = User(
                email=email, 
                password=generate_password_hash(password,method='sha256')
                )
            new_user.add()
            mysql.connection.commit()
            flash('Successfuly created an account! Please log in.', category='success')
            return Response(status=299)
        else:
            errors = get_error_items(form)
            if user:
                errors['email']= ['Email is already taken.']
            return Response(json.dumps([errors, fields]), status=499, mimetype='application/json')
                


@auth.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect('/')


@auth.route('/about')
def about():
    return render_template('auth/about.html')


@auth.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

