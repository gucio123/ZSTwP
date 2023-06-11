from typing import List
from urllib.request import urlopen

from flask_login import login_required, current_user

from .. import db
from flask import Blueprint, request, flash, render_template, abort, json, session, redirect, url_for

from website.models import FaultCategory, FaultSeverity, Fault, Ticket, User, Notification, Maintainer, TicketStatus
from ..auth import update_user_notifications

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

@ticket_bp.route('/show_tickets_status', methods=['GET'])
@login_required
def show_tickets_status():
    tickets = Ticket.query.filter_by(reporter_id=current_user.id).all()
    ticket_status = TicketStatus.query.all()
    notifications = get_notifications_from_session()
    mark_notifications_as_seen(tickets, notifications)
    return render_template('show_tickets_status.html', tickets=tickets, ticket_status=ticket_status)

def find_tickets_with_notifications_and_mark_as_seen(tickets, notifications: List[Notification]):
    if notifications is not None:
        ticket_ids = [notification.ticket_id for notification in notifications]
        tickets_with_notifications = [ticket for ticket in tickets if ticket.id in ticket_ids]
        for notification in notifications:
            notification.was_seen = 1
        for ticket in tickets:
            if ticket.status_id == 1:
                ticket.status_id = 2
        db.session.commit()
        update_user_notifications()
        return tickets_with_notifications

def mark_notifications_as_seen(notifications: List[Notification]):
    if notifications is not None:
        for notification in notifications:
            notification.was_seen = 1
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