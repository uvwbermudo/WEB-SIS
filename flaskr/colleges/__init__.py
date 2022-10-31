from sqlalchemy import exc
from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from flask_login import current_user, login_user, login_required, logout_user
from flaskr import db
from .forms import AddCollege
from .models import Colleges


colleges_view = Blueprint('colleges_view', __name__)


def searchbar_query(filter, search_query):
    if filter == 'college_code':
        return Colleges.query.filter(
            Colleges.college_code.contains(search_query)
            ).all()
    elif filter == 'college_name':
        return Colleges.query.filter(
            Colleges.college_name.contains(search_query)
            ).all()
    else:
        return Colleges.query.filter(
            Colleges.college_code.contains(search_query)|
            Colleges.college_name.contains(search_query)
            ).all()


@colleges_view.route('/colleges', methods=['POST','GET'])
@login_required
def college_view():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    form = AddCollege(request.form)
    colleges = Colleges.query.all()
   
    if 'from_search' in session and session['from_search']==True:
        session['from_search'] = False
        colleges = searchbar_query(
            filter=session['search_filter'], 
            search_query=session['search_query'],
            )

    return render_template('colleges/colleges.html', form=form, colleges=colleges)


@colleges_view.route('/college-add', methods=['POST'])
@login_required
def college_add():
    form = AddCollege(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            college_name = request.form.get('college_name')
            college_code = request.form.get('college_code')
            check = Colleges.query.get(college_code)

            if check:
                flash(f'ERROR: College code "{college_code}" already in use', category='error')
                print(check)
            else:
                new_college = Colleges(
                    college_name=college_name,
                    college_code=college_code,
                    )
                db.session.add(new_college)
                try: 
                    db.session.commit()
                except exc.IntegrityError:
                    flash(f'ERROR - College name "{college_name}" is already in use. ', category='error')
                else:
                    flash(f'Successfully added "{new_college.college_code} - {new_college.college_name}"')
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(f'{err}', category='error')
        
    return redirect(url_for('colleges_view.college_view'))


@colleges_view.route('/college-edit', methods=['POST'])
@login_required
def college_edit():
    form = AddCollege(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_code = request.form.get('college_code')
            new_name = request.form.get('college_name')
            college_code = request.form.get('hid')
            check = Colleges.query.get(new_code)

            if check and check.college_code != college_code:
                flash(f'ERROR: College code "{new_code}" already in use', category='error')
            else:
                target = Colleges.query.filter(Colleges.college_code==college_code).first()
                target.college_code = new_code
                target.college_name = new_name
                
                try: 
                    db.session.commit()
                except exc.IntegrityError as e:
                    print(e)
                    flash(f'ERROR - College name "{new_name}" is already in use. ', category='error')
                else:
                    flash(f'Successfully updated "{target}"')
        else:
            for fieldName, errorMessages in form.errors.items():
                for err in errorMessages:
                    flash(f'{err}', category='error')

    return redirect(url_for('colleges_view.college_view'))


@colleges_view.route('/college-delete', methods=['POST','GET'])
@login_required
def college_delete():
    if request.method == 'POST':
        target = request.form.get('hid')
        target = Colleges.query.get(target)
        db.session.delete(target)
        db.session.commit()
        flash(f'Deleted "{target.college_name}" successfully', category='success')
    return redirect(url_for('colleges_view.college_view'))


@colleges_view.route('/college-search', methods=['POST','GET'])
@login_required
def college_search():
    session['from_search'] = True
    session['search_query'] = request.form.get('searchbar')
    session['search_filter'] = request.form.get('searchfield')
    return redirect(url_for('colleges_view.college_view'))

        

