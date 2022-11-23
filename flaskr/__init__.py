from flask import Flask
from config import DB_USERNAME, DB_PASSWORD, DB_NAME, DB_HOST, SECRET_KEY
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import create_database, database_exists
import pymysql
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager



db_url = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}" 
db = SQLAlchemy()
if not database_exists(db_url):
    print('DB CREATED')
    create_database(db_url)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']=SECRET_KEY
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    db.init_app(app)
    CSRFProtect(app)

    from .auth import auth, page_not_found
    from .student import student_view
    from .courses import courses_view
    from .colleges import colleges_view

    from .auth.models import User
    from .student.models import Students
    from .colleges.models import Colleges
    from .courses.models import Courses

    app.register_blueprint(auth,url_prefix='/')
    app.register_blueprint(student_view,url_prefix='/')
    app.register_blueprint(courses_view,url_prefix='/')
    app.register_blueprint(colleges_view,url_prefix='/')
    app.register_error_handler(404, page_not_found)

    
    with app.app_context():
        db.create_all()

    
    login_manager=LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    login_manager.login_message = None

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

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