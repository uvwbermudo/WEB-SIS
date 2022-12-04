from flask import Blueprint, render_template, request, flash, redirect, url_for, session, Response
from flask_login import current_user, login_user, login_required, logout_user
from .forms import AddCollege
from .models import Colleges
from flaskr import get_error_items, get_form_fields
import json
import wtforms_json
from flaskr import mysql
import mysql.connector as mcr


colleges_view = Blueprint('colleges_view', __name__)


@colleges_view.route('/colleges', methods=['POST','GET'])
@login_required
def college_view():
    if not current_user.is_authenticated:
        return redirect(url_for('auth.login'))
    form = AddCollege(request.form)
    colleges = Colleges.query_all()

   
    return render_template('colleges/colleges.html', form=form, colleges=colleges)


@colleges_view.route('/college-verify', methods=['POST'])
@login_required
def college_verify():
    temp_json = request.get_json()
    form = AddCollege.from_json(temp_json)
    fields = get_form_fields(form)
    if request.method == 'POST':
        college_name = request.json['college_name']
        college_code = request.json['college_code']
        old_code = request.json['hid']
        check = Colleges.query_get(college_code)
        check_name = Colleges.query_filter(college_name=college_name)
        mode = request.json['mode']
        if form.validate_on_submit():
            if mode == 1:                   # mode = 1 is for editing
                errors = get_error_items(form)
                if check and check['college_code'] != old_code:
                    errors['college_code']= ['College Code is already being used.']
                    if check_name and check_name[0]['college_code'] != old_code:
                        errors['college_name']= ['College name is already being used.']
                    return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
            
                else:
                    target = Colleges.query_get(old_code)
                    try: 
                        Colleges.update(
                            old_code=old_code,
                            new_name=college_name,
                            new_code=college_code
                            )
                        mysql.connection.commit()
                    except mcr.IntegrityError as e:
                        errors['college_name']= ['College name is already being used.']
                        return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
                    else:
                        flash(f"Successfully updated {target['college_name']}")
                    return Response(status=299)
                

            if check:
                errors = get_error_items(form)
                errors['college_code']= ['College Code is already being used.']
                if check_name:
                    errors['college_name']= ['College name is already being used.']
                return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')

            new_college = Colleges(
                college_name=college_name,
                college_code=college_code,
                )
            try: 
                new_college.add()
            except mcr.IntegrityError:
                errors = get_error_items(form)
                errors['college_name']= ['College name is already being used.']
                return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')

            mysql.connection.commit()
            flash(f'Successfully added "{new_college.college_code} - {new_college.college_name}"')
            return Response(status=299)

        else:
            errors = get_error_items(form)
            if mode == '1':
                return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')
            if check and check['college_code'] != old_code:
                errors['college_code']= ['College Code is already being used.']
            if check_name:
                errors['college_name']= ['College name is already being used.']
            return Response(json.dumps([errors, fields]), status=298, mimetype='application/json')


@colleges_view.route('/college-delete', methods=['POST','GET'])
@login_required
def college_delete():
    if request.method == 'POST':
        target_id = request.form.get('hid')
        target = Colleges.query_get(target_id)
        Colleges.delete_college(target_id)
        mysql.connection.commit()
        flash(f"Deleted {target['college_name']} successfully", category='success')
    return redirect(url_for('colleges_view.college_view'))


@colleges_view.route('/college-search', methods=['POST'])
@login_required
def college_search():
    if request.method == 'POST':
        search = request.json['search_query']
        filter = request.json['search_filter']
        result = searchbar_query(filter=filter, search_query=search)
        result = col_to_list(result)
        return Response(json.dumps([result]), status=298, mimetype='application/json')


def col_to_list(list):
    temp = []
    for college in list:
        temp.append([college['college_code'], college['college_name']])
    return temp
        

def searchbar_query(filter, search_query):
    if not search_query.isalnum():
        return Colleges.query_all()
    else:
        if filter == 'college_code':
            return Colleges.query_filter(college_code=search_query, search_pattern=True)
        elif filter == 'college_name':
            return Colleges.query_filter(college_name=search_query, search_pattern=True)
        else:
            return Colleges.query_filter(all=search_query, search_pattern=True)