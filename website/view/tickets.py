from flask_login import login_required, current_user

from .. import db
from flask import Blueprint, request, flash, render_template, abort

from website.models import FaultCategory, FaultSeverity, Fault, Ticket, User

ticket_bp = Blueprint('/ticket', __name__)

@ticket_bp.route('/list/<int:maintainer_id>', methods=(['GET']))
def list_faults_per_operator(maintainer_id):
    if current_user.maintainer_id == None:
        abort(401)
    tickets = Ticket.query.filter_by(maintainer_id=maintainer_id).all()
    if len(tickets) == 0:
        return render_template("ticket_list.html")
    ticket_with_fault_list = []
    for ticket in tickets:
        fault = Fault.query.filter_by(id=ticket.fault_id).first()
        reporter = User.query.filter_by(id=ticket.reporter_id).first()
        ticket_with_fault_list.append(
            {"ticket": ticket,
             "fault": fault,
             "reporter": reporter
             }
        )
        print(reporter)

    return render_template("ticket_list.html", ticket_with_fault_list=ticket_with_fault_list)