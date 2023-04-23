from .. import db
from flask import Blueprint, request, flash, render_template

from website.models import FaultCategory, FaultSeverity, Fault

fault_bp = Blueprint('/report', __name__)


@fault_bp.route('/report', methods=('GET', 'POST'))
def report_fault():
    if request.method == 'POST':
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        description = request.form['description']
        device_serial_number = request.form['device_serial_number']
        category = request.form['category_id']
        severity = request.form['severity_id']
        category_id = FaultCategory.query.filter_by(category=category).first().id
        severity_id = FaultSeverity.query.filter_by(severity=severity).first().id

        try:
            fault = Fault(latitude=latitude, longitude=longitude, description=description,
                          device_serial_number=device_serial_number, category_id=category_id,
                          severity_id=severity_id)
            db.session.add(fault)
            db.session.commit()
            categories = [c.category for c in FaultCategory.query.all()]
            severities = [s.severity for s in FaultSeverity.query.all()]


        except db.IntegrityError:
            flash('Error: failed to add new fault', category='error')
            return render_template("/report_fault.html")

        flash("Fault created!", category="success")
        return render_template('/report_fault.html', categories=categories, severities=severities, successful=True)


    elif request.method == 'GET':
        categories = [c.category for c in FaultCategory.query.all()]
        severities = [s.severity for s in FaultSeverity.query.all()]
        return render_template('/report_fault.html', categories=categories, severities=severities)


@fault_bp.route('/list', methods=(['GET']))
def list_faults():
    faults = Fault.query.all()
    # Uncomment to return faults as json
    # faults = [f.serialize() for f in faults]
    # return jsonify(faults)
    return render_template("fault_list.html", faults=faults)