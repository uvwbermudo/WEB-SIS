
from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_user, login_required, logout_user
from . forms import RegisterForm, UserForm
from . models import User
from flaskr import db
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)


@auth.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('student_view.students'))
    else:
        return redirect(url_for('auth.login'))


@auth.route('/login', methods=['GET','POST'])
def login():
    form = UserForm(request.form)
    if request.method =='POST':
        if form.validate_on_submit():
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            
            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    return redirect(url_for('student_view.students'))
                flash('Incorrect password', category='error')
            else:
                flash('Email does not exist', category='error')
            
    return render_template('auth/login.html', form=form)


@auth.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            email = request.form.get('email')
            user = User.query.filter_by(email=email).first()

            if user:
                flash('Email is already in use', category='error')
            else:
                email = request.form.get('email')
                password = request.form.get('password')
                new_user = User(
                    email=email, 
                    password=generate_password_hash(password,method='sha256')
                    )
                db.session.add(new_user)
                db.session.commit()
                flash('Successfuly created an account! Please log in.', category='success')
                return redirect(url_for('.login'))
                
    return render_template('auth/register.html', form=form)


@auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    return redirect('/')


@auth.route('/about')
def about():
    return render_template('auth/about.html')
