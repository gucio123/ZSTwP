from flask import Blueprint, request, render_template, flash
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from website.models import Ticket, Fault, Maintainer, Notification, NotificationUser, User
from website import db


NOT_READ = 1
HARDWARE = 1
DONE = 4

createTicket = Blueprint('create-ticket', __name__)


@createTicket.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if request.method == 'POST':

        fault_id = request.form.get('fault_id')
        fault = Fault.query.filter_by(id=fault_id).first()

        if fault is None:
            info = f'Unable to create ticket! Check if fault {fault_id} exists'
            flash(info, category='error')
            return render_template("create_ticket.html")

        reporter_id = current_user.id
        status_id = NOT_READ
        # maintainer_id = choose_maintainer()
        # TODO: Fix database entries, maybe add some triggers to database. For now deleted maintainers who didn't have appropriate user accounts,
        # TODO: there is a mismatch in ids for maintainer@maintainer.com. To fix.
        maintainer_id = 3
        is_physical_assistance_required = is_assistance_required(fault)
        reported_date = datetime.now()
        due_date = calculate_due_date(fault.severity_id)

        try:
            new_ticket = Ticket(status_id=status_id, fault_id=fault_id, reporter_id=reporter_id,
                                maintainer_id=maintainer_id, reported_date=reported_date, due_date=due_date,
                                physical_assistance_req=is_physical_assistance_required)


            db.session.add(new_ticket)

            ticket = Ticket.query.filter_by(fault_id=fault_id, maintainer_id=maintainer_id).all()[0]

            new_notification = Notification(ticket_id=ticket.id)
            db.session.add(new_notification)
            notification = Notification.query.filter_by(ticket_id=ticket.id).all()[0]
            # maintainer = Maintainer.query.filter_by(id=maintainer_id).first()
            user = User.query.filter_by(maintainer_id=maintainer_id).first()
            new_notification_user_relationship = NotificationUser(user_id=user.id, notification_id=notification.id)
            db.session.add(new_notification_user_relationship)

            db.session.commit()
        except:

            db.session.rollback()
            flash('Error: failed to insert new ticket', category='error')
            return render_template("create_ticket.html")
            pass

        flash("Ticket created!", category="success")
        notify_maintainer(maintainer_id)
    return render_template("create_ticket.html")


def is_assistance_required(fault):
    return fault.category_id == HARDWARE


def calculate_due_date(severity_id):
    how_much_days_required_to_fix = timedelta(days=severity_id)
    return date.today() + how_much_days_required_to_fix


def choose_maintainer():

    subquery = db.session.query(Ticket.maintainer_id, db.func.count(Ticket.id).label('ticket_count'))\
            .filter(Ticket.status_id != DONE).group_by(Ticket.maintainer_id).subquery()

    query = db.session.query(Maintainer.id, subquery.c.ticket_count.label('ticket_count'))\
        .outerjoin(subquery, Maintainer.id == subquery.c.maintainer_id).order_by(subquery.c.ticket_count.asc())

    least_busy_maintainer_id = query[0][0]
    return least_busy_maintainer_id


# TODO send email 
# TODO make notification
def notify_maintainer(maintainer_id):
    print(f'Maintainer {maintainer_id} has new ticket')
