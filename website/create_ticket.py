from datetime import datetime, date, timedelta
from website.models import Ticket, Fault
from website import db

PENDING = 1
HARDWARE = 1


def test1():
    fault = Fault.query.filter_by(id=3).first()
    create_ticket(fault)


def create_ticket(fault):
    status_id = PENDING
    maintainer_id = choose_maintainer()
    # TODO change to reporter_id
    ticket_id = 1
    is_physical_assistance_required = is_assistance_required(fault)
    reported_date = datetime.now()
    due_date = calculate_due_date(fault.severity_id)

    try:
        new_ticket = Ticket(status_id=status_id, ticket_id=ticket_id,
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


# TODO create algorithm to choose maintainer (distance, number of ticket per maintainer etc.)
def choose_maintainer():
    maintainer_id = 1
    return maintainer_id


# TODO send email
# TODO make notification: to discuss
def notify_maintainer(maintainer_id):
    print(f'Maintainer {maintainer_id} has new ticket')
