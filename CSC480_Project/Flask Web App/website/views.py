from flask import Blueprint, render_template, request, flash, get_flashed_messages, jsonify, redirect, url_for, send_file
from flask_login import login_required, current_user
views = Blueprint('views', __name__)
from . import db
import json
from functools import wraps
from .models import User, Ticket, Employee, DepartmentTickets
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
import os
from flask import session
from datetime import datetime

"""
@roles_required(roles)
Use: check if current_user contains one or multiple roles as part of the requirement
Parameters: (roles) is passed as a dict of strings... roles_required(['Base','Employee']), and checks the parameter against the current_user's roles as a subset.
Useful link for *args,**kwargs: https://www.digitalocean.com/community/tutorials/how-to-use-args-and-kwargs-in-python-3
Useful link for @wraps https://stackoverflow.com/questions/308999/what-does-functools-wraps-do
returns either a validated user or redirects them back to the login page
"""
def roles_required(roles):
    def decorated_function(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if set(roles).issubset({r.name for r in current_user.roles}):
                return f(*args, **kwargs)
            else:
                print("Not Authorized!!!!")
                return redirect(url_for('auth.login'))
        return wrapper
    return decorated_function

"""
Route Directory for all Users... accessing 
"""
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    ticketTypes = db.session.query(DepartmentTickets).all()
    if request.method =='POST' and 'createTicket' in request.form:
        ticketType = request.form.get('ticketType')
        ticketComments = request.form.get('ticketComments')
        file = request.files['img']
        file.save(secure_filename(file.filename))
        if len(ticketType) < 1:     #input validation
            flash('Please Select a Type!', category='error')
        elif len(ticketComments) < 1:
            flash('Please add comments to the ticket!', category='error')
        else:
            new_ticket = Ticket(ticketType = ticketType, uidCreator = current_user.id, ticketComments = ticketComments, Status = "Pending", imgName = str(file.filename))
            db.session.add(new_ticket)
            db.session.commit()
            Ticket.query.filter_by(ticketID=new_ticket.ticketID).update(dict(department = new_ticket.getDepartment(ticketType)))
            db.session.commit()
            flash('Ticket Created!', category = 'success') 
    if request.method =='POST' and 'baseTempID' in request.form:
        session['baseTempID'] = request.form.get('baseTempID')
        return redirect(url_for('views.baseTicketView'))
    if request.method =='POST' and 'cancelTicket' in request.form:
        ticketID = request.form.get('ticketID')
        Ticket.query.filter_by(ticketID=ticketID).update(dict(Status="Cancelled"))
        db.session.commit()
    if (current_user.roles[0].name == 'Employee'):
        return redirect(url_for("views.empHome", user=current_user))
    return render_template("home.html", user=current_user, ticketTypes = ticketTypes)

@views.route('/empHome', methods=['GET', 'POST'])
@roles_required(['Employee'])
def empHome():
    if request.method=='POST':
        session['tempID'] = request.form.get('tempID')
        return redirect(url_for('views.empTicketView'))
    return render_template("empHome.html", user=current_user)

#employee view for all tickets that have not been claimed by another employee yet
@views.route('/empTicketHub', methods=['GET','POST'])
@roles_required(['Employee'])
def empTicketHub():   
    employee = Employee.query.filter_by(user_id=current_user.id).first()
    tickets = Ticket.query.filter_by(uidEmployee = None)
    if (request.method == 'POST'):
        ticketID = request.form.get('ticketID')
        uidEmployee = current_user.id
        Ticket.query.filter_by(ticketID=ticketID).update(dict(uidEmployee=uidEmployee, Status="Active", empDateTaken = datetime.now().date()))
        db.session.commit()
    return render_template("empTicketHub.html", tickets=tickets, user=current_user, employee = employee)

@views.route('/baseTicketView', methods=['GET','POST'])
@roles_required(['Base'])
def baseTicketView():
    tempID = session['baseTempID']
    ticket = Ticket.query.filter_by(ticketID = tempID).first()
    creator = User.query.filter_by(id = ticket.uidCreator).first()
    employee = User.query.filter_by(id = ticket.uidEmployee).first()
    queueTime = datetime.now() - ticket.dateCreated
    queueTime = queueTime.days
    if ticket.empDateTaken == None:
        progress = 3
    elif ticket.empDateRespond == None:
        progress = 23
    elif  ticket.dateResolved == None:
        progress = 55
    else: 
        progress=100
    if (request.method=='POST' and 'TicketComments' in request.form):
        TicketComments = request.form.get('TicketComments')
        Ticket.query.filter_by(ticketID=tempID).update(dict(ticketComments=TicketComments, empDateRespond = datetime.now().date()))
        db.session.commit()
        return render_template("baseTicketView.html", user=current_user, ticket=ticket, creator=creator,employee=employee, progress=progress)
    return render_template("baseTicketView.html", user=current_user, ticket=ticket, creator=creator,employee=employee, progress=progress, queueTime = queueTime)


@views.route('/empTicketView', methods=['GET','POST'])
@roles_required(['Employee'])
def empTicketView():
    tempID = session['tempID']
    ticket = Ticket.query.filter_by(ticketID = tempID).first()
    creator = User.query.filter_by(id = ticket.uidCreator).first()
    employee = User.query.filter_by(id = ticket.uidEmployee).first()
    queueTime = datetime.now() - ticket.dateCreated
    queueTime = queueTime.days
    if ticket.empDateTaken == None:
        progress = 3
    elif ticket.empDateRespond == None:
        progress = 23
    elif  ticket.dateResolved == None:
        progress = 55
    else: 
        progress=100
    if (request.method=='POST' and 'empTicketComments' in request.form):
        empTicketComments = request.form.get('empTicketComments')
        Ticket.query.filter_by(ticketID=tempID).update(dict(empTicketComments=empTicketComments, empDateRespond = datetime.now().date()))
        db.session.commit()
        return redirect(url_for("views.empTicketView", user=current_user, ticket=ticket, creator=creator,employee=employee, progress=progress))
    if (request.method=='POST' and 'resolve' in request.form):
        Ticket.query.filter_by(ticketID=tempID).update(dict(Status = "Resolved", dateResolved = datetime.now().date()))
        db.session.commit()
        return redirect(url_for("views.empTicketView", user=current_user, ticket=ticket, creator=creator,employee=employee, progress=progress))
    return render_template("empTicketView.html", user=current_user, ticket=ticket, creator=creator,employee=employee, progress=progress, queueTime = queueTime)





#route for deleting a ticket...
#will validate a ticket ID, that it exists, and that it belongs to the user to delete the ticket.
@views.route('/delete-ticket', methods=['POST'])
def delete_ticket():
    ticket = json.loads(request.data)
    ticketID = ticket['ticketID']
    ticket = Ticket.query.get(ticketID)
    if ticket:
        if ticket.uidCreator == current_user.id:
            db.session.delete(ticket)
            db.session.commit()
    return jsonify({})


