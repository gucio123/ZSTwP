from flask import Blueprint, request, render_template, flash
from flask_login import login_required
from website.models import Contractor,User
from website import db

bp = Blueprint('create-ticket', __name__)


@bp.route('/register_contractor', methods=['GET', 'POST'])
@login_required
def register_contractor():
    if request.method == 'POST':

        company_name = request.form.get('company_name')
        nip = request.form.get('nip')

        if not is_input_data_correct(company_name, nip):
            return render_template('register_contractor.html')

        try:
            new_contractor = Contractor(company_name=company_name, nip=nip)
            db.session.add(new_contractor)
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error: failed to register contractor', category='error')
            return render_template('register_contractor.html')

        flash('Successfully registered!', category='success')
    return render_template('register_contractor.html')


def is_input_data_correct(company_name, nip):
    if company_name == '' or nip == '':
        flash('Some fields are blank!', category='error')
        return False
    if not is_nip_format_correct(nip):
        flash('NIP format not correct, try again', category='error')
        return False
    return True


# NIP should have 10 numbers and have correct checksum
def is_nip_format_correct(nip):
    if len(nip) != 10:
        return False
    elif not nip.isnumeric():
        return False
    elif not is_checksum_correct(nip):
        print('checksum not correct')
        return False
    return True


def is_checksum_correct(nip):
    checksum = int(nip[9])
    sum_to_check = 0
    weights = [6, 5, 7, 2, 3, 4, 5, 6, 7]
    for i, x in enumerate(weights):
        sum_to_check += int(nip[i]) * weights[i]
    sum_to_check %= 11
    return checksum == sum_to_check
