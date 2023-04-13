from datetime import datetime, date, timedelta
from website.models import Ticket
from website import db

PENDING = 1
TIME_REQUIRED_TO_FIX = timedelta(days=7)


def create_ticket():
    try:
        status_id = PENDING
        maintainer_id = choose_maintainer()
        ticket_id = 1
        # TODO how to determine if assistance required
        is_physical_assistance_required = True
        reported_date = datetime.now()
        # TODO how to calculate due date
        due_date = date.today() + TIME_REQUIRED_TO_FIX

        new_ticket = Ticket(status_id=status_id, ticket_id=ticket_id,
                            maintainer_id=maintainer_id, reported_date=reported_date, due_date=due_date,
                            physical_assistance_req=is_physical_assistance_required)
        db.session.add(new_ticket)
        db.session.commit()
    except db.IntegrityError:
        print('Error: failed to insert new ticket')
        return

    notify_maintainer(maintainer_id)
    return True


# TODO create algorithm to choose maintainer (distance, number of ticket per maintainer etc.)
def choose_maintainer():
    maintainer_id = 1
    return maintainer_id


# TODO send email
# TODO make notification: to discuss
def notify_maintainer(maintainer_id):
    print(f'Maintainer {maintainer_id} has new ticket')
