from flask import Blueprint, request, render_template, flash
from flask_login import login_required
from website.models import Contractor
from website import db

registerContractor = Blueprint('register-contractor', __name__)


@registerContractor.route('/register_contractor', methods=['GET', 'POST'])
@login_required
def register_contractor():
    if request.method == 'POST':
        company_name = request.form.get('company_name')
        nip = request.form.get('nip')

        if company_name == '' or nip == '':
            flash('Something went wrong, try again', category='error')
            return render_template('register_contractor.html')
        try:
            new_contractor = Contractor(company_name=company_name, nip=nip)
            db.session.add(new_contractor)
            db.session.commit()
        except:
            flash('Error: failed to register contractor', category='error')
            return render_template('register_contractor.html')

        flash('Successfully registered!', category='success')
    return render_template('register_contractor.html')
