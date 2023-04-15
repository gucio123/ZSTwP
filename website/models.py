from . import db
from sqlalchemy import Column, DateTime, Double, ForeignKey, Integer, String, Boolean


class User(db.Model):
    __tablename__ = 'user'
    user_id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(50))
    email = Column(String(50), unique=True)
    isAdmin = Column(Boolean)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    maintainer_id = Column(Integer, ForeignKey('maintainer.maintainer_id'))


class Employee(db.Model):
    __tablename__ = 'employee'
    employee_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    phone = Column(Integer)
    badge_number = Column(Integer)


class Contractor(db.Model):
    __tablename__ = 'contractor'
    contractor_id = Column(Integer, primary_key=True)
    company_name = Column(String(50))
    nip = Column(Integer)


class Maintainer(db.Model):
    __tablename__ = 'maintainer'
    maintainer_id = Column(Integer, primary_key=True)
    name = Column(String(50))    
    surname = Column(String(50))    
    phone = Column(Integer)
    employee_id = Column(Integer, ForeignKey('employee.employee_id'))
    contractor_id = Column(Integer, ForeignKey('contractor.contractor_id'))


class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = Column(Integer, primary_key=True)
    reported_date = Column(DateTime)
    due_date = Column(DateTime)
    physical_assistance_req = Column(Boolean)
    status_id = Column(Integer, ForeignKey('ticket_status.ticket_status_id'))
    maintainer_id = Column(Integer, ForeignKey('maintainer.maintainer_id'))
    fault_id = Column(Integer, ForeignKey('fault.fault_id'))
    reporter_id = Column(Integer, ForeignKey('user.user_id'))


class TicketStatus(db.Model):
    __tablename__ = 'ticket_status'
    ticket_status_id = Column(Integer, primary_key=True)
    status = Column(String(50))


class Fault(db.Model):
    __tablename__ = 'fault'
    fault_id = Column(Integer, primary_key=True)
    latitude = Column(Double)
    longitude = Column(Double)
    description = Column(String(500))
    device_serial_number = Column(Integer)
    category_id = Column(Integer, ForeignKey('fault_category.fault_category_id'))
    severity_id = Column(Integer, ForeignKey('fault_severity.fault_severity_id'))


class FaultSeverity(db.Model):
    __tablename__ = 'fault_severity'
    fault_severity_id = Column(Integer, primary_key=True)
    severity = Column(String(500))


class FaultCategory(db.Model):
    __tablename__ = 'fault_category'
    fault_category_id = Column(Integer, primary_key=True)
    category = Column(String(500))
