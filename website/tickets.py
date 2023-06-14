from urllib.request import urlopen

from flask_login import login_required, current_user

from .. import db
from flask import Blueprint, request, flash, render_template, abort, json

from website.models import FaultCategory, FaultSeverity, Fault, Ticket, User

ticket_bp = Blueprint('/ticket', __name__)

def is_user_on_loc(user_latitude, user_longitude, latitude, longitude):
    distance = (pow((user_longitude - longitude), 2) + pow((user_latitude - latitude), 2))
    if distance < 0.001:
        return True
    else:
        return False

@ticket_bp.route('/list/<int:maintainer_id>', methods=(['GET']))
def list_faults_per_operator(maintainer_id):
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
    for ticket in tickets:
        fault = Fault.query.filter_by(id=ticket.fault_id).first()
        reporter = User.query.filter_by(id=ticket.reporter_id).first()
        is_user_on_location = is_user_on_loc(user_latitude, user_longitude, fault.latitude, fault.longitude)
        ticket_with_fault_list.append(
            {"ticket": ticket,
             "fault": fault,
             "reporter": reporter,
             "is_user_on_loc": is_user_on_location
             }
        )
    return render_template("ticket_list.html", ticket_with_fault_list=ticket_with_fault_list)