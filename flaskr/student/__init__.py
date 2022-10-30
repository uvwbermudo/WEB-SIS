from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, login_required, logout_user
from flaskr import db
from flaskr.student.models import Students
from .forms import AddStudent
from flaskr.courses.models import Courses

student_view = Blueprint('student_view', __name__)

@student_view.route('/students')
@login_required
def students():
    x=Students.query.all()

    for stud in x:
        print(stud.last_name)
        print(stud.course.course_name)


    form = AddStudent(request.form)
    courses = Courses.query.all()
    courses = [(course.course_code,course.course_name) for course in courses]
    form.course.choices = courses
    session['course_choices'] = courses
    students = Students.query.all()
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    
    if 'from_search' in session and session['from_search'] == True:
        session['from_search'] = False
        search_filter = str(session['search_query'])
        students = Students.query.filter(
            Students.last_name.contains(search_filter) | 
            Students.first_name.contains(search_filter) |
            Students.id.contains(search_filter)).all()

    
    return render_template('student/students.html', form=form, students=students)

@student_view.route('/student-add', methods=['POST','GET'])
@login_required
def student_add():
    form = AddStudent(request.form)
    form.course.choices = session['course_choices']
    if request.method == 'POST':
        if form.validate_on_submit():
            id_number = request.form.get('id')
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            year = request.form.get('year')
            gender = request.form.get('gender')
            course = request.form.get('course')

            check = Students.query.get(id_number)
            if check:
                flash(f'ERROR: Course code "{id_number}" already in use', category='error')
            else:
                new_student = Students(last_name=last_name,first_name=first_name, id=id_number, year=year, gender=gender, course_code=course)
                db.session.add(new_student)
                db.session.commit()
                flash(f'Successfully added "{id_number} - {"".join((last_name,first_name))}"')
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(f'{err}', category='error')
        
    return redirect(url_for('student_view.students'))


@student_view.route('/student-edit', methods=['POST'])
@login_required
def student_edit():
    form = AddStudent(request.form)
    form.course.choices = session['course_choices']
    if request.method == 'POST':
        if form.validate_on_submit():
            student_id = request.form.get('hid')
            new_id = request.form.get('id')

            check = Students.query.get(new_id)
            if check and check.id != student_id:
                flash (f'ERROR: Course Code "{new_id}" already in Use', category='error')
            else:
                new_first_name = request.form.get('first_name')
                new_last_name = request.form.get('last_name')
                new_gender = request.form.get('gender')
                new_year = request.form.get('year')
                new_course_code = request.form.get('course')

                target = Students.query.get(student_id)
                target.first_name = new_first_name
                target.last_name = new_last_name
                target.gender = new_gender
                target.id = new_id
                target.year = new_year
                target.course_code = new_course_code

                db.session.commit()
                flash(f'Successfully updated student: {", ".join([new_last_name, new_first_name])}!', category='success')
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(f'{err}', category='error')
        return redirect(url_for('student_view.students'))

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
        session['from_search'] = True
        session['search_query'] = request.form.get('searchbar')
        return redirect(url_for('student_view.students'))