from flask_login import UserMixin
from . import db
from sqlalchemy import Column, DateTime, Double, ForeignKey, Integer, String, Boolean


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(500))
    email = Column(String(50), unique=True)
    isAdmin = Column(Boolean)
    isOperator = Column(Boolean)
    employee_id = Column(Integer, ForeignKey('employee.id'))
    maintainer_id = Column(Integer, ForeignKey('maintainer.id'))


class Employee(db.Model):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    surname = Column(String(50))
    phone = Column(Integer)
    badge_number = Column(Integer)


class Contractor(db.Model):
    __tablename__ = 'contractor'
    id = Column(Integer, primary_key=True)
    company_name = Column(String(50))
    nip = Column(Integer)


class Maintainer(db.Model):
    __tablename__ = 'maintainer'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))    
    surname = Column(String(50))    
    phone = Column(Integer)
    contractor_id = Column(Integer, ForeignKey('contractor.id'))


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True)
    reported_date = Column(DateTime)
    due_date = Column(DateTime)
    physical_assistance_req = Column(Boolean)
    status_id = Column(Integer, ForeignKey('ticket_status.id'))
    maintainer_id = Column(Integer, ForeignKey('maintainer.id'))
    fault_id = Column(Integer, ForeignKey('fault.id'))
    reporter_id = Column(Integer, ForeignKey('user.id'))


class TicketStatus(db.Model):
    __tablename__ = 'ticket_status'
    id = Column(Integer, primary_key=True)
    status = Column(String(50))


class Fault(db.Model):
    __tablename__ = 'fault'
    id = Column(Integer, primary_key=True)
    latitude = Column(Double)
    longitude = Column(Double)
    description = Column(String(500))
    device_serial_number = Column(Integer)
    category_id = Column(Integer, ForeignKey('fault_category.id'))
    severity_id = Column(Integer, ForeignKey('fault_severity.id'))

    def serialize(self):
        return {"id": self.id,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "description": self.description,
                "device_serial_number": self.device_serial_number,
                "category_id": self.category_id,
                "severity_id": self.severity_id}

    @property
    def serialized(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'description': self.description,
            'device_serial_number': self.device_serial_number,
            'category_id': self.category_id,
            'severity_id': self.severity_id,

        }


class FaultSeverity(db.Model):
    __tablename__ = 'fault_severity'
    id = Column(Integer, primary_key=True)
    severity = Column(String(500))


# class FaultCategory(db.Model):
class FaultCategory(db.Model):
    __tablename__ = 'fault_category'
    id = Column(Integer, primary_key=True)
    category = Column(String(500))
