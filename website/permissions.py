from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import User
from . import db


permissions = Blueprint('permissions', __name__)
@permissions.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():

    users = User.query.all()
    # TESTOWE PRINTY, NIC NIE WYPLUWA 
    print(current_user.isAdmin)
    for user in users:
        print(user.username, user.email)

    db.session.add(users)
    db.session.commit()
    return render_template('/admin.html', user = users)

# @permissions.route('/admin', methods = ['GET', 'POST'])
# @login_required
# def assign_admin():


