from flask import Blueprint, render_template, abort, redirect, url_for, jsonify
from flask import Blueprint, render_template, request
from . import db
from website.models import Fault, FaultCategory, FaultSeverity
from flask import Blueprint, render_template
from flask_login import login_required



views = Blueprint('views', __name__)
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
            return render_template('/report_fault.html', categories=categories, severities=severities, successful=True)
        except IndexError:
            abort(404)


    elif request.method == 'GET':
        categories = [c.category for c in FaultCategory.query.all()]
        severities = [s.severity for s in FaultSeverity.query.all()]
        return render_template('/report_fault.html', categories=categories, severities=severities)


@fault_bp.route('/list', methods=(['GET']))
def list_faults():

        faults = Fault.query.all()
        faults = [f.serialize() for f in faults]
        return jsonify(faults)


@views.route('/')
def home():
    return render_template("home.html")
# def home():
#     return render_template("home.html")

@views.route('/admin')
@login_required
def admin():
    return render_template("admin.html")

