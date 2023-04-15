from sqlalchemy import func
from datetime import datetime, date, timedelta
from website.models import Ticket, Fault
from website import db

PENDING = 1
HARDWARE = 1
COMPLETE = 3


def create_ticket(fault_id, reporter_id):

    fault = Fault.query.filter_by(fault_id=fault_id).first()
    status_id = PENDING
    maintainer_id = choose_maintainer()
    is_physical_assistance_required = is_assistance_required(fault)
    reported_date = datetime.now()
    due_date = calculate_due_date(fault.severity_id)

    try:
        new_ticket = Ticket(status_id=status_id, fault_id=fault_id, reporter_id=reporter_id,
                            maintainer_id=maintainer_id, reported_date=reported_date, due_date=due_date,
                            physical_assistance_req=is_physical_assistance_required)
        db.session.add(new_ticket)
        db.session.commit()
    except db.IntegrityError:
        print('Error: failed to insert new ticket')
        return False

    notify_maintainer(maintainer_id)
    return True


def is_assistance_required(fault):
    return fault.category_id == HARDWARE


def calculate_due_date(severity_id):
    how_much_days_required_to_fix = timedelta(days=severity_id)
    return date.today() + how_much_days_required_to_fix


def choose_maintainer():
    query = db.session.query(Ticket.maintainer_id, func.count(Ticket.ticket_id).label('tickets_per_maintainer')). \
        filter(Ticket.status_id != COMPLETE).group_by(Ticket.maintainer_id).order_by('tickets_per_maintainer')

    least_busy_maintainer_id = query[0][0]
    return least_busy_maintainer_id


# TODO send email
# TODO make notification
def notify_maintainer(maintainer_id):
    print(f'Maintainer {maintainer_id} has new ticket')
