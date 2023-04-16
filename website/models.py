from flask_login import UserMixin
from . import db
from sqlalchemy import Column, DateTime, Double, ForeignKey, Integer, String, Boolean


class User(db.Model, UserMixin):
    __tablename__ = 'user'
<<<<<<< Updated upstream
    user_id = Column(Integer, primary_key = True)
    username = Column(String(50), unique = True)
    password = Column(String(50))
    email = Column(String(50), unique = True)
    isAdmin = Column(Boolean)
    employee_id = Column(Integer, ForeignKey('employee.id') )
=======
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(500))
    email = Column(String(50), unique=True)
    isAdmin = Column(Boolean)
    employee_id = Column(Integer, ForeignKey('employee.id'))
>>>>>>> Stashed changes
    maintainer_id = Column(Integer, ForeignKey('maintainer.id'))


class Employee(db.Model):
    __tablename__ = 'employee'
<<<<<<< Updated upstream
    employee_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
    name = Column(String(50))
    surname = Column(String(50))
    phone = Column(Integer)
    badge_number = Column(Integer)


class Contractor(db.Model):
    __tablename__ = 'contractor'
<<<<<<< Updated upstream
    contractor_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
    company_name = Column(String(50))
    nip = Column(Integer)


class Maintainer(db.Model):
    __tablename__ = 'maintainer'
<<<<<<< Updated upstream
    maintainer_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
    name = Column(String(50))    
    surname = Column(String(50))    
    phone = Column(Integer)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    contractor_id = Column(Integer, ForeignKey('contractor.id'))


class Ticket(db.Model):
    __tablename__ = 'ticket'
<<<<<<< Updated upstream
    ticket_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
    reported_date = Column(DateTime)
    due_date = Column(DateTime)
    physical_assistance_req = Column(Boolean)
    status_id = Column(Integer, ForeignKey('ticket_status.id'))
    maintainer_id = Column(Integer, ForeignKey('maintainer.id'))
<<<<<<< Updated upstream
    fault_id = Column(Integer,ForeignKey('fault.id'))
=======
    fault_id = Column(Integer, ForeignKey('fault.id'))
>>>>>>> Stashed changes
    reporter_id = Column(Integer, ForeignKey('user.id'))


class TicketStatus(db.Model):
    __tablename__ = 'ticket_status'
<<<<<<< Updated upstream
    ticketStatus_id = Column(Integer, primary_key = True, )
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
    status = Column(String(50))


class Fault(db.Model):
    __tablename__ = 'fault'
<<<<<<< Updated upstream
    fault_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
    latitude = Column(Double)
    longitude = Column(Double)
    description = Column(String(500))
    device_serial_number = Column(Integer)
    category_id = Column(Integer, ForeignKey('fault_category.id'))
    severity_id = Column(Integer, ForeignKey('fault_severity.id'))
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes


class FaultSeverity(db.Model):
    __tablename__ = 'fault_severity'
<<<<<<< Updated upstream
    faultSeverity_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
    severity = Column(String(500))


class FaultCategory(db.Model):
    __tablename__ = 'fault_category'
<<<<<<< Updated upstream
    faultCategory_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
    category = Column(String(500))
