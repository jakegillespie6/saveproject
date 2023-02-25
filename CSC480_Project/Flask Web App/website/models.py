from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Ticket(db.Model):
    ticketID = db.Column(db.Integer, primary_key=True)
    uidCreator = db.Column(db.Integer, db.ForeignKey("User.id"))
    uidEmployee = db.Column(db.Integer, db.ForeignKey("User.id"))
    ticketType = db.Column(db.String(50))
    ticketComments = db.Column(db.String(500))
    empTicketComments = db.Column(db.String(500))
    empDateRespond = db.Column(db.DateTime(timezone=True))
    empDateTaken = db.Column(db.DateTime(timezone=True))
    dateCreated = db.Column(db.DateTime(timezone=True), default=func.now())
    dateResolved = db.Column(db.DateTime(timezone=True))
    Status = db.Column(db.String(24))
    department = db.Column(db.String(50))
    imgName = db.Column(db.String(70))
    def getDepartment(self, type_name=None):
        if type_name is not None:
            deptCalc = db.session.query(DepartmentTickets).filter(DepartmentTickets.ticketType == type_name).first()
            if deptCalc:
                department = deptCalc.department
        else:
            department = None
        return department


class User(db.Model, UserMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50),unique=True)
    password = db.Column(db.String(30))
    firstName = db.Column(db.String(30))
    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
        backref=db.backref('users', lazy='dynamic'))
    empTicket = db.relationship('Ticket', backref='employee', lazy='dynamic', foreign_keys = 'Ticket.uidEmployee')
    creatorTicket = db.relationship('Ticket', backref='creator', lazy='dynamic', foreign_keys = 'Ticket.uidCreator')

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('User.id', ondelete='CASCADE'))
    department = db.Column(db.String(50))

class Base(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('User.id', ondelete='CASCADE'))
    department = db.Column(db.String(50))

# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)

# Define the UserRoles data model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('User.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class DepartmentTickets(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    department = db.Column(db.String(100))
    ticketType = db.Column(db.String(100), unique=True)
