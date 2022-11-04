from flask import Blueprint, render_template, request, flash, redirect, url_for, session, Response
from flask_login import current_user, login_user, login_required, logout_user
from flaskr import db
from .models import Students
from .forms import AddStudent
from flaskr.courses.models import Courses
from flaskr import get_error_items, get_form_fields
import json
import wtforms_json

student_view = Blueprint('student_view', __name__)

        
@student_view.route('/students')
@login_required
def students():
    form = AddStudent(request.form)
    courses = Courses.query.all()
    courses = [(course.course_code,course.course_name) for course in courses]
    form.course.choices = courses
    session['course_choices'] = courses
    students = Students.query.all()

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
        check = Students.query.get(id_number)
        mode = request.json['mode']
        if form.validate_on_submit():
            if mode == 1:               # mode = 1 is for editing
                errors = get_error_items(form)
                if check and check.id != old_id:
                    print('!1111222')
                    errors['id']= ['ID Number is already being used.']
                    return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
            
                else:
                    target = Students.query.get(old_id)
                    print(temp_json)
                    print(target)
                    target.id = id_number
                    target.last_name = last_name
                    target.first_name = first_name
                    target.year = year
                    target.gender = gender
                    target.course_code = course
                    db.session.commit()
                    flash(f'Successfully updated "{target}"')
                    return Response(status=299)
                        
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
                db.session.add(new_student)
                db.session.commit()
                flash(f'Successfully added "{id_number} - {"".join((last_name,first_name))}"')
                return Response(status=299)

        else:
            errors = get_error_items(form)
            if check:
                errors['id']= ['ID Number is already being used.']
            return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
        


@student_view.route('/student-delete', methods=['POST'])
@login_required
def student_delete():
    if request.method == 'POST':
        target = request.form.get('hid')
        target = Students.query.get(target)
        flash(f'''Deleted "{', '.join((target.last_name,target.first_name))}" successfully''', category='success')
        db.session.delete(target)
        db.session.commit()
    return redirect(url_for('student_view.students'))

@student_view.route('/student-search', methods=['POST'])
@login_required
def student_search():
    if request.method == 'POST':
        search = request.json['search_query']
        filter = request.json['search_filter']
        result = searchbar_query(filter=filter, search_query=search)
        result = col_to_list(result)
        return Response(json.dumps([result]), status=298, mimetype='application/json')

def col_to_list(list):
    temp = []
    for student in list:
        if student.course_code:
            course_name = student.course.course_name
        else:
            course_name = None
        temp.append([student.id, student.last_name, student.first_name, course_name, student.year, student.gender])
    return temp

def searchbar_query(filter, search_query):  
    if filter == 'id':
        return Students.query.filter(
            Students.id.contains(search_query)
            ).all()
    elif filter == 'name':
        return Students.query.filter(
            Students.last_name.contains(search_query) |
            Students.first_name.contains(search_query)
            ).all()
    elif filter =='course':
        if search_query.isspace() or search_query =='':
            return Students.query.all()
        course = Courses.query.filter(
            Courses.course_name.contains(search_query)|
            Courses.course_code.contains(search_query)).first()

        course = course.course_code
        return Students.query.filter(
            Students.course_code == course).all()
        
    else:
        return Students.query.filter(
            Students.id.contains(search_query)|
            Students.last_name.contains(search_query)|
            Students.first_name.contains(search_query)
            ).all()