from . import Base
from sqlalchemy import Column, DateTime, Double, ForeignKey, Integer, String, Boolean


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key = True)
    username = Column(String(50), nullable = False, unique = True)
    password = Column(String(50), nullable = False)
    email = Column(String(50), unique = True, nullable = False)
    isAdmin = Column(Boolean, nullable= False)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable = False)
    maintainer_id = Column(Integer, ForeignKey('maintainer.id'), nullable = False)


class Employee(Base):
    __tablename__ = 'employee'
    id = Column(Integer, primary_key = True)
    name = Column(String(50), nullable = False)
    surname = Column(String(50), nullable = False)
    phone = Column(Integer, nullable = False)
    badge_number = Column(Integer, nullable = False)


class Contractor(Base):
    __tablename__ = 'contractor'
    id = Column(Integer, primary_key = True)
    company_name = Column(String(50), nullable = False)
    nip = Column(Integer, nullable = False)


class Maintainer(Base):
    __tablename__ = 'maintainer'
    id = Column(Integer, primary_key = True)
    name = Column(String(50),nullable=False)    
    surname = Column(String(50),nullable=False)    
    phone = Column(Integer,nullable=False)
    employee_id = Column(Integer, ForeignKey('employee.id'), nullable = False)
    contractor_id = Column(Integer, ForeignKey('contractor.id'), nullable = False)


class Ticket(Base):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key = True)
    reported_date = Column(DateTime, nullable = False)
    due_date = Column(DateTime, nullable = False)
    physical_assistance_req = Column(Boolean, nullable = False)
    status_id = Column(Integer, ForeignKey('ticket_status.id'), nullable = False)
    maintainer_id = Column(Integer, ForeignKey('maintainer.id'), nullable = False)
    ticket_id = Column(Integer, ForeignKey('user.id'), nullable = False)


class TicketStatus(Base):
    __tablename__ = 'ticket_status'
    id = Column(Integer, primary_key = True, )
    status = Column(String(50), nullable = False)


class Fault(Base):
    __tablename__ = 'fault'
    id = Column(Integer, primary_key = True)
    latitude = Column(Double, nullable=False)
    longitude = Column(Double, nullable=False)
    description = Column(String(500), nullable=False)
    device_serial_number = Column(Integer, nullable = False)
    category_id = Column(Integer, ForeignKey('fault_category.id'), nullable = False)
    severity_id = Column(Integer, ForeignKey('fault_severity.id'), nullable = False)



class FaultSeverity(Base):
    __tablename__ = 'fault_severity'
    id = Column(Integer, primary_key = True)
    severity = Column(String(500), nullable=False)


class FaultCategory(Base):
    __tablename__ = 'fault_category'
    id = Column(Integer, primary_key = True)
    category = Column(String(500), nullable=False)
