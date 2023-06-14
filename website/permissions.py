from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import current_user, login_required
from .models import User
from . import db


permissions = Blueprint('permissions', __name__)
@permissions.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_panel():

    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)
        if user.isAdmin:
            flash('This user is already an admin.', 'warning')
        else:
            user.isAdmin = True
            db.session.commit()

        return redirect(url_for('permissions.admin_panel'))
    
    users = User.query.all()    
    db.session.commit()
    return render_template('admin.html', users = users)

@permissions.route('/admin/remove', methods = ['GET', 'POST'])
@login_required
def remove_admin():
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        user = User.query.get(user_id)
        if not user.isAdmin:
            flash('This user is not an admin.', 'warning')
        else:
            user.isAdmin = False
            db.session.commit()

        return redirect(url_for('permissions.admin_panel'))

    users = User.query.all()
    db.session.commit()
    return render_template('/admin', users = users)







