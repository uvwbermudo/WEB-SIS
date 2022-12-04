from flask import Blueprint, render_template, request, flash, redirect, url_for, session, Response
from flask_login import current_user, login_user, login_required, logout_user
from .models import Students
from .forms import AddStudent
from flaskr.courses.models import Courses
from flaskr import get_error_items, get_form_fields, mysql
import json
import wtforms_json
import time
from hashlib import sha256
from config import CLOUDINARY_API_CLOUD, CLOUDINARY_API_KEY, CLOUDINARY_API_CLOUD_FOLDER, CLOUDINARY_API_SECRET
import mysql.connector as mcr

student_view = Blueprint('student_view', __name__)

        
@student_view.route('/students')
@login_required
def students():
    form = AddStudent(request.form)
    courses = Courses.query_all()
    courses = [(course['course_code'],course['course_name']) for course in courses]
    form.course.choices = courses
    session['course_choices'] = courses
    students = Students.query_all()

    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    return render_template('student/students.html', form=form, students=students)

@student_view.route('/student-verify', methods=['POST','GET'])
@login_required
def student_verify():
    temp_json = request.get_json()
    form = AddStudent.from_json(temp_json)
    form.course.choices = session['course_choices']
    fields = get_form_fields(form)
    if request.method == 'POST':
        id_number = request.json['id']
        last_name = request.json['last_name']
        first_name = request.json['first_name']
        year = request.json['year']
        gender = request.json['gender']
        course = request.json['course']
        old_id = request.json['hid']
        check = Students.query_get(id=id_number)
        mode = request.json['mode']
        if form.validate_on_submit():
            upload_params = {}      #setting up parameters for cloudinary upload
            upload_params['timestamp'] = str(int(time.time()))
            upload_params['public_id'] = id_number+ upload_params['timestamp']
            upload_params['folder'] = str(CLOUDINARY_API_CLOUD_FOLDER)
            upload_params['api_key'] = str(CLOUDINARY_API_KEY)
            upload_params['api_secret'] = str(CLOUDINARY_API_SECRET)
            signature=f"folder={upload_params['folder']}&public_id={upload_params['public_id']}&timestamp={upload_params['timestamp']}{upload_params['api_secret']}"
            print(signature)
            signature = sha256(signature.encode()).hexdigest()   
            upload_params['signature']=signature
            
            if mode == 1:               # mode = 1 is for editing
                errors = get_error_items(form)
                if check and check['id'] != old_id:
                    errors['id']= ['ID Number is already being used.']
                    return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
                else:
                    target_id = old_id
                    target = Students.query_get(target_id)
                    Students.update(
                        old_id=old_id,
                        new_course=course,
                        new_year_level=year,
                        new_fname=first_name,
                        new_gender=gender,
                        new_lname=last_name,
                        new_id=id_number
                        )
                    mysql.connection.commit()
                    flash(f"Successfully updated {target['id']} - {target['last_name']}, {target['first_name']}")
                    return Response(json.dumps([upload_params]),status=299)
   
            if check:
                errors = get_error_items(form)
                errors['id'] = ['Id Number is already being used.']
                return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
            else:
                new_student = Students(
                    last_name=last_name,
                    first_name=first_name, 
                    id=id_number, year=year, 
                    gender=gender, 
                    course_code=course,
                    )
                new_student.add()
                mysql.connection.commit()
                flash(f'Successfully added "{id_number} - {"".join((last_name,first_name))}"')
                return Response(json.dumps([upload_params]),status=299)

        else:
            errors = get_error_items(form)
            if mode == 1:
                if check and check['id'] != old_id:
                    errors['id']= ['ID Number is already being used.']
            else:
                if check:
                    errors['id']= ['ID Number is already being used.']
            return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
        


@student_view.route('/student-delete', methods=['POST'])
@login_required
def student_delete():
    if request.method == 'POST':
        target_id= request.form.get('hid')
        target = Students.query_get(target_id)
        flash(f"Deleted {target['last_name']}, {target['first_name']} successfully", category='success')
        Students.delete_student(target_id)
        mysql.connection.commit()
    return redirect(url_for('student_view.students'))

@student_view.route('/upload-profile', methods=['POST'])
def upload_profile():
    if request.method == 'POST':
        profile_url = request.json['profile_pic']
        student = request.json['student_id']
        Students.update_pfp(id=student, url=profile_url)        
        mysql.connection.commit()
        return Response(status=299)

@student_view.route('/student-search', methods=['POST'])
@login_required
def student_search():
    if request.method == 'POST':
        search = request.json['search_query']
        filter = request.json['search_filter']
        gender_filter = request.json['gender_filter']
        result = searchbar_query(filter=filter, search_query=search, gender_filter=gender_filter)
        result = col_to_list(result)
        return Response(json.dumps([result]), status=298, mimetype='application/json')

def col_to_list(list):
    temp = []
    for student in list:
        if student['course_code']:
            course_name = student['course_name']
        else:
            course_name = None
        temp.append([
            student['id'],
            student['last_name'],
            student['first_name'],
            course_name,
            student['year_level'],
            student['gender'], 
            student['course_code'],
            student['profile_pic']
            ])
    return temp

def searchbar_query(filter, search_query, gender_filter):  
    if search_query.isspace() or search_query =='':
        return Students.query_all(gender=gender_filter)
    if filter == 'id':
        return Students.query_filter(id=search_query, search_pattern=True, gender=gender_filter)
    elif filter == 'name':
        return Students.query_filter(name=search_query, search_pattern=True, gender=gender_filter)
    elif filter =='course':
        course = Courses.query_filter(all=search_query, search_pattern=True)[0]
        course = course['course_code']
        return Students.query_filter(course=course, search_pattern=True, gender=gender_filter)
    else:
        return Students.query_filter(all=search_query, search_pattern=True, gender=gender_filter)
