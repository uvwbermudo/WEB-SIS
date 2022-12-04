from flask_login import UserMixin
from sqlalchemy.sql import func
from os import path
from flaskr import mysql


class User():
    
    def __init__(self, email=None, password=None):
        self.email = email
        self.user_password = password 


    def add(self):
        cursor = mysql.connection.cursor()
        sql = f"INSERT INTO users(email, user_password) \
                VALUES('{self.email}','{self.user_password}')" 
        cursor.execute(sql)

    @classmethod
    def query_filter_by(cls, email=None):
        cursor = mysql.connection.cursor()
        sql = f"SELECT * FROM users WHERE email='{email}'"
        cursor.execute(sql)
        columns = []
        columns = [desc[0] for desc in cursor.description]
        rows = cursor.fetchall()
        result = []
        for row in rows:
            row = dict(zip(columns, row))
            result.append(row)
        if result:
            return result[0]
        return None

    @classmethod
    def query_current_user(cls, email):
        result = User.query_filter_by(email=email)
        current = None
        if result:
            current = CurrentUser(result)
            return current
        return current
    
class CurrentUser(UserMixin):
    def __init__(self, mykwargs={}):
        self.email = mykwargs['email']
        self.user_password = mykwargs['user_password']

    def get_id(self):
        return self.email
    


    


    