from flask_login import UserMixin
from . import db
from sqlalchemy import Column, DateTime, Double, ForeignKey, Integer, String, Boolean


class User(db.Model, UserMixin):
    __tablename__ = 'user'
<<<<<<< HEAD
<<<<<<< Updated upstream
    user_id = Column(Integer, primary_key = True)
    username = Column(String(50), unique = True)
=======
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
>>>>>>> 460c7825c943e2d8f74cea881beaf3120d607eb5
    password = Column(String(50))
    email = Column(String(50), unique=True)
    isAdmin = Column(Boolean)
<<<<<<< HEAD
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
=======
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    maintainer_id = Column(Integer, ForeignKey('maintainer.maintainer_id'))
>>>>>>> 460c7825c943e2d8f74cea881beaf3120d607eb5


class Employee(db.Model):
    __tablename__ = 'employee'
<<<<<<< HEAD
<<<<<<< Updated upstream
    employee_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
=======
    employee_id = Column(Integer, primary_key=True)
>>>>>>> 460c7825c943e2d8f74cea881beaf3120d607eb5
    name = Column(String(50))
    surname = Column(String(50))
    phone = Column(Integer)
    badge_number = Column(Integer)


class Contractor(db.Model):
    __tablename__ = 'contractor'
<<<<<<< HEAD
<<<<<<< Updated upstream
    contractor_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
=======
    contractor_id = Column(Integer, primary_key=True)
>>>>>>> 460c7825c943e2d8f74cea881beaf3120d607eb5
    company_name = Column(String(50))
    nip = Column(Integer)


class Maintainer(db.Model):
    __tablename__ = 'maintainer'
<<<<<<< HEAD
<<<<<<< Updated upstream
    maintainer_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
=======
    maintainer_id = Column(Integer, primary_key=True)
>>>>>>> 460c7825c943e2d8f74cea881beaf3120d607eb5
    name = Column(String(50))    
    surname = Column(String(50))    
    phone = Column(Integer)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    contractor_id = Column(Integer, ForeignKey('contractor.contractor_id'))


class Ticket(db.Model):
    __tablename__ = 'ticket'
<<<<<<< HEAD
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
=======
    ticket_id = Column(Integer, primary_key=True)
    reported_date = Column(DateTime)
    due_date = Column(DateTime)
    physical_assistance_req = Column(Boolean)
    status_id = Column(Integer, ForeignKey('ticket_status.ticket_status_id'))
    maintainer_id = Column(Integer, ForeignKey('maintainer.maintainer_id'))
    fault_id = Column(Integer, ForeignKey('fault.fault_id'))
    reporter_id = Column(Integer, ForeignKey('user.user_id'))
>>>>>>> 460c7825c943e2d8f74cea881beaf3120d607eb5


class TicketStatus(db.Model):
    __tablename__ = 'ticket_status'
<<<<<<< HEAD
<<<<<<< Updated upstream
    ticketStatus_id = Column(Integer, primary_key = True, )
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
=======
    ticket_status_id = Column(Integer, primary_key=True)
>>>>>>> 460c7825c943e2d8f74cea881beaf3120d607eb5
    status = Column(String(50))


class Fault(db.Model):
    __tablename__ = 'fault'
<<<<<<< HEAD
<<<<<<< Updated upstream
    fault_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
=======
    fault_id = Column(Integer, primary_key=True)
>>>>>>> 460c7825c943e2d8f74cea881beaf3120d607eb5
    latitude = Column(Double)
    longitude = Column(Double)
    description = Column(String(500))
    device_serial_number = Column(Integer)
<<<<<<< HEAD
    category_id = Column(Integer, ForeignKey('fault_category.id'))
    severity_id = Column(Integer, ForeignKey('fault_severity.id'))
<<<<<<< Updated upstream

=======
>>>>>>> Stashed changes
=======
    category_id = Column(Integer, ForeignKey('fault_category.fault_category_id'))
    severity_id = Column(Integer, ForeignKey('fault_severity.fault_severity_id'))
>>>>>>> 460c7825c943e2d8f74cea881beaf3120d607eb5


class FaultSeverity(db.Model):
    __tablename__ = 'fault_severity'
<<<<<<< HEAD
<<<<<<< Updated upstream
    faultSeverity_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
=======
    fault_severity_id = Column(Integer, primary_key=True)
>>>>>>> 460c7825c943e2d8f74cea881beaf3120d607eb5
    severity = Column(String(500))


class FaultCategory(db.Model):
    __tablename__ = 'fault_category'
<<<<<<< HEAD
<<<<<<< Updated upstream
    faultCategory_id = Column(Integer, primary_key = True)
=======
    id = Column(Integer, primary_key=True)
>>>>>>> Stashed changes
=======
    fault_category_id = Column(Integer, primary_key=True)
>>>>>>> 460c7825c943e2d8f74cea881beaf3120d607eb5
    category = Column(String(500))
