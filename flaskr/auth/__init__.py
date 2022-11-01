
from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, Response
from flask_login import current_user, login_user, login_required, logout_user
from . forms import RegisterForm, UserForm
from . models import User
from flaskr import db
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.datastructures import ImmutableMultiDict
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
            user = User.query.filter_by(email=email).first()
            
            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    flash('Logged in successfully', category='success')
                    return Response(status=200)
                errors = get_error_items(form)
                errors['password'] = ['Incorrect Password']
                return Response(json.dumps([errors, fields]), status=499, mimetype='application/json')
        
            else:
                errors = get_error_items(form)
                errors['email'] = ['Email does not exist']
                return Response(json.dumps([errors, fields]), status=499, mimetype='application/json')
        else:
            print(fields)
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
        user = User.query.filter_by(email=email).first()
        if form.validate():
            if user:
                errors = get_error_items(form)
                errors['email']= ['Email is already taken.']
                return Response(json.dumps([errors, fields]), status=499, mimetype='application/json')

            new_user = User(
                email=email, 
                password=generate_password_hash(password,method='sha256')
                )
            db.session.add(new_user)
            db.session.commit()
            flash('Successfuly created an account! Please log in.', category='success')
            return Response(status=200)
        else:
            errors = get_error_items(form)
            if user:
                errors['email']= ['Email is already taken.']
            return Response(json.dumps([errors, fields]), status=499, mimetype='application/json')
                


@auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@auth.route('/about')
def about():
    return render_template('auth/about.html')


def get_error_items(form):
    errors = {}
    for fieldName, errorMessages in form.errors.items():
        errors[fieldName] = errorMessages
    return errors

def get_form_fields(form):
    fields = []
    for keys in form.data.keys():
        fields.append(keys)
    return fields