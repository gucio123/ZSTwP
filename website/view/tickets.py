from datetime import timedelta, date, datetime

from typing import List
from urllib.request import urlopen

from flask_login import login_required, current_user

from website import db
from flask import Blueprint, request, flash, render_template, abort, json, session, redirect, url_for

from website.models import FaultCategory, FaultSeverity, Fault, Ticket, User, Notification, Maintainer, TicketStatus, \
    NotificationUser
from website.auth import update_user_notifications

ticket_bp = Blueprint('/ticket', __name__)


def is_user_on_loc(user_latitude, user_longitude, latitude, longitude):
    distance = (pow((user_longitude - longitude), 2) + pow((user_latitude - latitude), 2))
    if distance < 0.001:
        return True
    else:
        return False


@ticket_bp.route('/list/<int:maintainer_id>', methods=(['GET', 'POST']))
def list_faults_per_operator(maintainer_id):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        # For purposes of checking location it is right now done here as maintainers' faults and tickets are listed
        # already and only has to check if the location is correct for every fault.
        # TODO: Think about where we want to put this check finally, probably there will be some authentication screen or something like it.
        if current_user.maintainer_id == None:
            abort(401)
        url = 'http://ipinfo.io/json'
        response = urlopen(url)
        data = json.load(response)
        location = data['loc']
        user_latitude = float(location.split(',')[0])
        user_longitude = float((location.split(',')[1]))

        tickets = Ticket.query.filter_by(maintainer_id=maintainer_id).all()
        if len(tickets) == 0:
            return render_template("ticket_list.html")
        ticket_with_fault_list = []
        notifications = get_notifications_from_session()
        tickets_with_notifications = find_tickets_with_notifications_and_mark_as_seen(tickets, notifications)

        for ticket in tickets:
            if tickets_with_notifications is not None and ticket in tickets_with_notifications:
                does_ticket_have_notification = True
            else:
                does_ticket_have_notification = False
            fault = Fault.query.filter_by(id=ticket.fault_id).first()
            reporter = User.query.filter_by(id=ticket.reporter_id).first()
            is_user_on_location = is_user_on_loc(user_latitude, user_longitude, fault.latitude, fault.longitude)
            ticket_status = ticket.status_id
            ticket_with_fault_list.append(
                {"ticket": ticket,
                 "fault": fault,
                 "reporter": reporter,
                 "is_user_on_loc": is_user_on_location,
                 "ticket_status": ticket_status,
                 "does_ticket_have_notification": does_ticket_have_notification
                 }
            )
        return render_template("ticket_list.html", ticket_with_fault_list=ticket_with_fault_list)


@ticket_bp.route('/accept/<ticket_id>', methods=(['GET', 'POST']))
def accept_ticket(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    ticket.status_id = 3
    db.session.commit()
    notify_operator(ticket_id, current_user.maintainer_id, was_accepted=True)
    return redirect(url_for("/ticket.list_faults_per_operator", maintainer_id=current_user.maintainer_id))


@ticket_bp.route('/decline/<ticket_id>', methods=(['GET', 'POST']))
def decline_ticket(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    ticket.status_id = 5
    db.session.commit()
    notify_operator(ticket_id, current_user.maintainer_id, was_accepted=False)
    return redirect(url_for("/ticket.list_faults_per_operator", maintainer_id=current_user.maintainer_id))


@ticket_bp.route('/suspend/<ticket_id>', methods=(['GET', 'POST']))
def suspend_ticket(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    ticket.status_id = 2
    db.session.commit()
    return redirect(url_for("/ticket.list_faults_per_operator", maintainer_id=current_user.maintainer_id))


# Not perfect function name. Ticket will be marked "WaitingForApproval" not "Done"
# But from maintainer point of view the ticket will be done
@ticket_bp.route('/mark_ticket_as_done/<ticket_id>', methods=(['GET', 'POST']))
def mark_ticket_as_done(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    ticket.status_id = 6
    db.session.commit()
    notify_operator_ticket_done(ticket_id)
    return redirect(url_for("/ticket.list_faults_per_operator", maintainer_id=current_user.maintainer_id))


@ticket_bp.route('/approve_ticket/<ticket_id>', methods=(['GET', 'POST']))
def approve_ticket(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    ticket.status_id = 4
    db.session.commit()
    # TODO notify maintainer
    return redirect(url_for("/ticket.show_tickets_status"))


@ticket_bp.route('/decline_ticket_approval/<ticket_id>', methods=(['GET', 'POST']))
def decline_ticket_approval(ticket_id):
    ticket = Ticket.query.filter_by(id=ticket_id).first()
    ticket.status_id = 2
    db.session.commit()
    # TODO notify maintainer
    return redirect(url_for("/ticket.show_tickets_status"))


@ticket_bp.route('/show_tickets_status', methods=['GET'])
@login_required
def show_tickets_status():
    tickets = Ticket.query.filter_by(reporter_id=current_user.id).all()
    ticket_status = TicketStatus.query.all()
    notifications = get_notifications_from_session()
    mark_notifications_as_seen(notifications)
    return render_template('show_tickets_status.html', tickets=tickets, ticket_status=ticket_status)


def find_tickets_with_notifications_and_mark_as_seen(tickets, notifications: List[Notification]):
    if notifications is not None:
        ticket_ids = [notification.ticket_id for notification in notifications]
        tickets_with_notifications = [ticket for ticket in tickets if ticket.id in ticket_ids]
        for notification in notifications:
            # notification.was_seen = 1
            db.session.delete(notification)
        for ticket in tickets:
            if ticket.status_id == 1:
                ticket.status_id = 2
        db.session.commit()
        update_user_notifications()
        return tickets_with_notifications


def mark_notifications_as_seen(notifications: List[Notification]):
    if notifications is not None:
        for notification in notifications:
            # notification.was_seen = 1
            db.session.delete(notification)
        db.session.commit()
        update_user_notifications()


def get_notifications_from_session():
    notifications_as_json = session.get('notifications')
    if notifications_as_json:
        notifications = [Notification.query.filter_by(id=notification['id']).first() for notification in
                         notifications_as_json]
        return notifications
    else:
        return


def notify_operator(ticket_id, maintainer_id, was_accepted):
    if was_accepted:
        content = "The maintainer: {} has accepted the ticket: {} ".format(ticket_id, maintainer_id)
    else:
        content = "The maintainer: {} has declined the ticket: {} ".format(ticket_id, maintainer_id)
    operator_notification = Notification(content=content, for_operator=True, ticket_id=ticket_id)
    db.session.add(operator_notification)
    db.session.commit()


def notify_operator_ticket_done(ticket_id):
    content = "The maintainer: {} has done the ticket: {}. Ticket waits for approval. ".\
        format(ticket_id, current_user.maintainer_id)
    operator_notification = Notification(content=content, for_operator=True, ticket_id=ticket_id)
    db.session.add(operator_notification)
    db.session.commit()


NOT_READ = 1
HARDWARE = 1
DONE = 4


@ticket_bp.route('/create_ticket', methods=['GET', 'POST'])
@login_required
def create_ticket():
    faults = get_faults_without_ticket()
    if request.method == 'POST':
        fault_query = request.form['fault']
        fault = Fault.query.filter_by(id=fault_query).first()
        reporter_id = current_user.id
        status_id = NOT_READ
        maintainer_id = choose_maintainer()
        is_physical_assistance_required = is_assistance_required(fault)
        reported_date = datetime.now()
        due_date = calculate_due_date(fault.severity_id)
        try:
            new_ticket = Ticket(status_id=status_id, fault_id=fault.id, reporter_id=reporter_id,
                                maintainer_id=maintainer_id, reported_date=reported_date, due_date=due_date,
                                physical_assistance_req=is_physical_assistance_required)
            db.session.add(new_ticket)
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error: failed to insert new ticket', category='error')
            return render_template("create_ticket.html", faults=faults)

        flash("Ticket created!", category="success")
        notify_maintainer(maintainer_id, fault.id)
        faults = get_faults_without_ticket()
        return render_template("create_ticket.html", faults=faults)
    elif request.method == 'GET':
        return render_template("create_ticket.html", faults=faults)


def get_faults_without_ticket():
    subquery = (db.session.query(Ticket.fault_id).filter(Ticket.fault_id.isnot(None)).subquery())
    faults = (
        db.session.query(Fault.id).outerjoin(subquery, Fault.id == subquery.c.fault_id).
            filter(subquery.c.fault_id.is_(None)).all()
    )
    return [id_[0] for id_ in faults]


def is_assistance_required(fault):
    return fault.category_id == HARDWARE


def calculate_due_date(severity_id):
    how_much_days_required_to_fix = timedelta(days=severity_id)
    return date.today() + how_much_days_required_to_fix


def choose_maintainer():
    subquery = db.session.query(Ticket.maintainer_id, db.func.count(Ticket.id).label('ticket_count')) \
        .filter(Ticket.status_id != DONE).group_by(Ticket.maintainer_id).subquery()

    query = db.session.query(Maintainer.id, subquery.c.ticket_count.label('ticket_count')) \
        .outerjoin(subquery, Maintainer.id == subquery.c.maintainer_id).order_by(subquery.c.ticket_count.asc())

    least_busy_maintainer_id = query[0][0]
    return least_busy_maintainer_id


def notify_maintainer(maintainer_id, fault_id):
    try:
        ticket = Ticket.query.filter_by(fault_id=fault_id, maintainer_id=maintainer_id).all()[0]
        content = "New ticket with id: {} was created!".format(ticket.id)
        new_notification = Notification(ticket_id=ticket.id, content=content)
        db.session.add(new_notification)
        notification = Notification.query.filter_by(ticket_id=ticket.id).all()[0]
        user = User.query.filter_by(maintainer_id=maintainer_id).first()
        new_notification_user_relationship = NotificationUser(user_id=user.id, notification_id=notification.id)
        db.session.add(new_notification_user_relationship)
        db.session.commit()
    except:
        db.session.rollback()
