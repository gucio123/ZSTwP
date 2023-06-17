from werkzeug.security import generate_password_hash

from .. import db
from flask import Blueprint, request, flash, render_template, redirect, url_for

from website.models import Contractor, User, Maintainer

maintainer_bp = Blueprint('/add_maintainer', __name__)


@maintainer_bp.route('/add_maintainer', methods=('GET', 'POST'))
def assign_maintainer_to_contractor():
    contractors = [c.company_name for c in Contractor.query.all()]
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        pswd1 = request.form.get('pswd1')
        pswd2 = request.form.get('pswd2')
        name = request.form.get('name')
        surname = request.form.get('surname')
        phone = request.form.get('phone')
        contractor = request.form['contractor']
        contractor_id = Contractor.query.filter_by(company_name=contractor).first().id

        check_mail = User.query.filter_by(email=email).first()
        check_user = User.query.filter_by(username=username).first()
        if check_mail:
            flash('Email address already exists, try again', category='error')
            return redirect(url_for('/add_maintainer.assign_maintainer_to_contractor'))
        elif check_user:
            flash('Username already exists, try again', category='error')
            return redirect(url_for("/add_maintainer.assign_maintainer_to_contractor"))
        if pswd1 != pswd2:
            flash('Passwords do not match, check password!', category='error')
            return redirect(url_for("/add_maintainer.assign_maintainer_to_contractor"))


        else:
            try:
                new_user = User(email=email, username=username,
                                password=generate_password_hash(pswd1, method='sha256'))
                new_maintainer = Maintainer(name=name, surname=surname, phone=phone, contractor_id=contractor_id)
                db.session.add(new_user)
                db.session.add(new_maintainer)
                db.session.commit()
                flash("Maintainer added!", category="success")
                return render_template('/add_maintainer.html', contractors=contractors)

            except db.IntegrityError:
                flash('Error: failed to add new maintainer', category='error')
                return redirect(url_for("maintainer_bp.add_maintainer"))



    elif request.method == 'GET':
        return render_template('/add_maintainer.html', contractors=contractors)
