from flask import Blueprint, render_template
from flask_login import login_required, current_user
from website.models import Ticket, TicketStatus

bp = Blueprint('show_tickets_status', __name__)


@bp.route('/show_tickets_status', methods=['GET'])
@login_required
def show_tickets_status():
    tickets = Ticket.query.filter_by(reporter_id=current_user.id).all()
    ticket_status = TicketStatus.query.all()
    return render_template('show_tickets_status.html', tickets=tickets, ticket_status=ticket_status)

