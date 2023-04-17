from flask import Blueprint, render_template
from flask import Blueprint, render_template, request
from . import db

from website.models import Fault
views = Blueprint('views', __name__)
fault_bp = Blueprint('report_fault', __name__)

@views.route('/')
def test():
    return render_template("home.html")


@fault_bp.route('/report_fault', methods=('GET', 'POST'))
def report_fault():

    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        description = request.form['description']
        device_serial_number = request.form['device_serial_number']
        category_id = request.form['category_id']
        severity_id = request.form['severity_id']

        fault = Fault(latitude=latitude, longitude=longitude, description=description,
                      device_serial_number=device_serial_number, category_id=category_id,
                      severity_id=severity_id)
        db.session.add(fault)
        db.session.commit()
        return Fault.query.all()

    elif request.method == 'GET':
        return render_template('/report_fault.html')


# def choose_and_notify_maintainer():
#     notify_maintainer()
#     pass
#
#
# def notify_maintainer():
#     pass


def create_ticket():
    pass


