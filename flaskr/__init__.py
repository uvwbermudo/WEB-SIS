from flask import Flask
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists
import pymysql
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_mysql_connector import MySQL
from flaskr.sql_init import create_db


db_url = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}" 
mysql = MySQL()



def create_app():
    create_db()
    app = Flask(__name__)
    app.config['SECRET_KEY']=SECRET_KEY
    app.config['MYSQL_HOST'] = DB_HOST
    app.config['MYSQL_USER'] = DB_USERNAME
    app.config['MYSQL_PASSWORD'] = DB_PASSWORD
    app.config['MYSQL_DATABASE'] = DB_NAME
    mysql.init_app(app)
    CSRFProtect(app)

    from .auth import auth, page_not_found
    from .student import student_view
    from .courses import courses_view
    from .colleges import colleges_view

    from .auth.models import User   

    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(student_view,url_prefix='/')
    app.register_blueprint(courses_view,url_prefix='/')
    app.register_blueprint(colleges_view,url_prefix='/')
    app.register_error_handler(404, page_not_found)

    
    login_manager=LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(email):
        return User.query_current_user(email=email)

    return app

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