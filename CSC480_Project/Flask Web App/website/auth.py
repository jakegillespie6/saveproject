from flask import Blueprint, render_template, request, flash, get_flashed_messages, redirect, url_for
from .models import *
from . import db
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if password == user.password:
                flash('Logged in!', category='success')
                login_user(user, remember=True)
                if (current_user.roles[0].name == 'Employee'):
                    print(current_user.roles[0].name)
                    return redirect(url_for('views.empTicketHub', user=current_user))
                elif (current_user.roles[0].name == 'Base'):
                    print(current_user.roles[0].name)
                    return redirect(url_for('views.home', user=current_user))
            else:
                flash('Incorrect Password', category='error')
        else: 
            flash('Email does not exist', category='error')
    return render_template("login.html", user=current_user)


#logout route
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        department = request.form.get('department')
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
        elif (len(email) < 4):
            flash('Email must be > 4 characters', category = 'error')
            pass
        elif (len(firstName) < 2):
            flash('First name must be > 2 cahracters', category = 'error')
            pass
        elif (len(password1) < 7):
            flash('Password must be > 7 characters', category = 'error')
            pass
        elif(password1 != password2):
            flash('Password do not match', category = 'error')
            pass
        else:
            new_user = User(email = email, firstName = firstName, password=password1)
            db.session.add(new_user)
            db.session.commit()
            new_user_roles = UserRoles(user_id = new_user.id, role_id = 1)
            db.session.add(new_user_roles)
            db.session.commit()
            new_base = Base(user_id = new_user.id, department=department)
            db.session.add(new_base)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home', user=current_user))  
    return render_template("signup.html")

@auth.route('/empSignup', methods=['GET','POST'])
def empSignup():
    departments = db.session.query(DepartmentTickets).distinct(DepartmentTickets.department).group_by(DepartmentTickets.department)
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        department = request.form.get('department2')
        print(department)
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!', category='error')
        elif (len(email) < 4):
            flash('Email must be > 4 characters', category = 'error')
            pass
        elif (len(firstName) < 2):
            flash('First name must be > 2 cahracters', category = 'error')
            pass
        elif (len(password1) < 7):
            flash('Password must be > 7 characters', category = 'error')
            pass
        elif(password1 != password2):
            flash('Password do not match', category = 'error')
            pass
        else:
            new_user = User(email = email, firstName = firstName, password=password1)
            db.session.add(new_user)
            db.session.commit()
            new_user_roles = UserRoles(user_id = new_user.id, role_id = 2) #role_id 2 == employee role
            db.session.add(new_user_roles)
            db.session.commit()
            new_employee = Employee(user_id = new_user.id, department = department)
            db.session.add(new_employee)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home', user=current_user))  
    return render_template("empSignup.html", departments=departments)

