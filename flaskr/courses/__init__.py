from unicodedata import category
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, login_required, logout_user
from flaskr import db
from .forms import AddCourse
from flaskr.colleges.models import Colleges
from .models import Courses

courses_view = Blueprint('courses_view', __name__)


@courses_view.route('/courses')
@login_required
def courses():
    form = AddCourse(request.form)
    colleges = Colleges.query.all()
    colleges = [(college.college_code,college.college_name) for college in colleges]
    form.college.choices = colleges
    session['college_choices'] = colleges

    courses = Courses.query.all()
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))

    if 'from_search' in session and session['from_search'] == True:
        session['from_search'] = False
        search_filter = str(session['search_query'])
        courses = Courses.query.filter(
            Courses.course_name.contains(search_filter) | 
            Courses.course_code.contains(search_filter)).all()
    return render_template('courses/courses.html', form=form, courses=courses)

@courses_view.route('/course-add', methods=['GET','POST'])
@login_required
def course_add():
    form = AddCourse(request.form)
    form.college.choices = session['college_choices']
    if request.method == 'POST':
        if form.validate_on_submit():
            course_name = request.form.get('course_name')
            course_code = request.form.get('course_code')
            college = request.form.get('college')
            check = Courses.query.get(course_code)
            if check:
                flash(f'ERROR: Course code "{course_code}" already in use', category='error')
            else:
                new_course = Courses(course_name=course_name,course_code=course_code, college_code=college)
                db.session.add(new_course)
                db.session.commit()
                flash(f'Successfully added "{new_course.course_code} - {new_course.course_name}"')
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(f'{err}', category='error')
        
    return redirect(url_for('courses_view.courses'))

@courses_view.route('/course-edit', methods=['GET','POST'])
@login_required
def course_edit():
    form = AddCourse(request.form)
    form.college.choices = session['college_choices']
    if request.method == 'POST':
        if form.validate_on_submit():
            course_code = request.form.get('hid')
            new_code = request.form.get('course_code')
            check = Courses.query.get(new_code)
            if check and check.course_code != course_code:
                flash (f'ERROR: Course Code "{new_code}" already in Use', category='error')
            else:
                new_name = request.form.get('course_name')
                new_college = request.form.get('college')

                target = Courses.query.get(course_code)
                target.course_code = new_code
                target.course_name = new_name
                target.college_code = new_college
                db.session.commit()
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(f'{err}', category='error')
        return redirect(url_for('courses_view.courses'))

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
    session['from_search'] = True
    session['search_query'] = request.form.get('searchbar')
    return redirect(url_for('courses_view.courses'))

