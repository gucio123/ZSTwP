from flask_login import UserMixin
from . import db
from sqlalchemy import Column, DateTime, Double, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship


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

    status = relationship("TicketStatus", backref="tickets")


class TicketStatus(db.Model):
    __tablename__ = 'ticket_status'
    id = Column(Integer, primary_key=True)
    status = Column(String(50))

class Notification(db.Model):
    __tablename__ = 'notification'
    id = Column(Integer, primary_key=True)
    content = Column(String(500))
    was_seen = Column(Boolean, default=False)
    # for_admin and for_operator are created with the intention to use when a notification should be visible for all operators or admins.
    # There will be one notification in the database, but multiple NotificationUser entries, so it will be easy to check if a user should
    # have a notification visible.
    # TODO: Add trigger in database for inserting NotificationUser entries when one of these fields is set to true so it doesn't have to
    # TODO: be added from flask. For now these fields don't have any particular meaning.
    for_admin = Column(Boolean, default=False)
    for_operator = Column(Boolean, default=False)
    ticket_id = Column(Integer, ForeignKey('ticket.id'))

    @property
    def serialize(self):
        return {
            'id': self.id,
            'content': self.content,
            'was_seen': self.was_seen,
            'for_admin': self.for_admin,
            'for_operator': self.for_operator,
            'ticket_id': self.ticket_id
        }


class NotificationUser(db.Model):
    # This is the table used for mapping a many-to-many relationship between users and notifications
    __tablename__ = 'notification_user'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    notification_id = Column(Integer, ForeignKey('notification.id'))


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
