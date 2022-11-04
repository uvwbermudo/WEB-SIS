
from sqlalchemy import exc
from flask import Blueprint, render_template, request, flash, redirect, url_for, session, Response
from flask_login import current_user, login_user, login_required, logout_user
from flaskr import db
from .forms import AddCourse
from flaskr.colleges.models import Colleges
from flaskr import get_error_items, get_form_fields
from .models import Courses
import json
import wtforms_json


courses_view = Blueprint('courses_view', __name__)


@courses_view.route('/courses')
@login_required
def courses():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    form = AddCourse(request.form)
    colleges = Colleges.query.all()
    colleges = [(college.college_code,college.college_name) for college in colleges]
    form.college.choices = colleges
    session['college_choices'] = colleges
    courses = Courses.query.all()
            
    return render_template('courses/courses.html', form=form, courses=courses)

@courses_view.route('/course-verify', methods=['GET','POST'])
@login_required
def course_verify():
    temp_json = request.get_json()
    form = AddCourse.from_json(temp_json)
    form.college.choices = session['college_choices']
    fields = get_form_fields(form)
    if request.method == 'POST':
        course_name = request.json['course_name']
        course_code = request.json['course_code']
        college = request.json['college']
        old_code = request.json['hid']
        check = Courses.query.get(course_code)
        check_name = Courses.query.filter(Courses.course_name==course_name).first()
        mode = request.json['mode']
        if form.validate_on_submit():
            if mode == 1:               # mode = 1 is for editing
                errors = get_error_items(form)
                if check and check.course_code != old_code:
                    errors['course_code']= ['Course Code is already being used.']
                    if check_name and check_name.course_code != old_code:
                        errors['course_name']= ['Course name is already being used.']
                    return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
            
                else:
                    target = Courses.query.get(old_code)
                    target.course_code = course_code
                    target.course_name = course_name
                    try: 
                        db.session.commit()
                    except exc.IntegrityError as e:
                        print(e)
                        errors['course_name']= ['Course name is already being used.']
                        return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
                    else:
                        flash(f'Successfully updated "{target}"')
                    return Response(status=299)

            if check:
                errors = get_error_items(form)
                errors['course_code'] = ['Course code is already being used.']
                if check_name:
                    errors['course_name']= ['Course name is already being used.']
                return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
            else:
                new_course = Courses(
                    course_name=course_name,
                    course_code=course_code, 
                    college_code=college,
                    )   
                db.session.add(new_course)
                try:
                    db.session.commit()
                except exc.IntegrityError:
                    errors = get_error_items(form)
                    errors['course_name']= ['Course name is already being used.']
                    return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
                else:
                    flash(f'Successfully added "{new_course.course_code} - {new_course.course_name}"')
                    return Response(status=299)

        else:
            errors = get_error_items(form)
            if check:
                errors['course_code']= ['Course Code is already being used.']
            if check_name:
                errors['course_name']= ['Course name is already being used.']
            return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
    

@courses_view.route('/course-delete', methods=['POST'])
@login_required
def course_delete():
    if request.method == 'POST':
        target = request.form.get('hid')
        target = Courses.query.get(target)
        flash(f'Deleted "{target.course_name}" successfully', category='success')
        db.session.delete(target)
        db.session.commit()
    return redirect(url_for('courses_view.courses'))

@courses_view.route('/course-search', methods=['POST'])
@login_required
def course_search():
    if request.method == 'POST':
        search = request.json['search_query']
        filter = request.json['search_filter']
        result = searchbar_query(filter=filter, search_query=search)
        result = col_to_list(result)
        return Response(json.dumps([result]), status=298, mimetype='application/json')


def col_to_list(list):
    temp = []
    for course in list:
        if course.college:
            college_name = course.college.college_name
        else:
            college_name = None
        temp.append([course.course_code, course.course_name, college_name])
    return temp


def searchbar_query(filter, search_query):
    if filter == 'course_code':
        return Courses.query.filter(
            Courses.course_code.contains(search_query)
            ).all()
    elif filter == 'course_name':
        return Courses.query.filter(
            Courses.course_name.contains(search_query)
            ).all() 
    elif filter == 'college':
        if search_query.isspace() or search_query =='':
            return Courses.query.all()
        college = Colleges.query.filter(
            Colleges.college_name.contains(search_query)|
            Colleges.college_code.contains(search_query)).first()

        college = college.college_code
        return Courses.query.filter(
            Courses.college_code == college).all()
    else:
        return Courses.query.filter(
            Courses.course_code.contains(search_query)|
            Courses.course_name.contains(search_query)
            ).all()