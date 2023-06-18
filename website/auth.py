from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from sqlalchemy import text

from website.models import User, NotificationUser, Notification, Employee
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':

          email = request.form.get('email')
          psswd = request.form.get('password')
          user = User.query.filter_by(email=email).first()


          if user:
                if check_password_hash(user.password, psswd):
                      flash("Succesfully logged!", category="success")
                      login_user(user, remember=True)

                      update_user_notifications()

                      return redirect(url_for('view.home'))
                else:
                      flash("Bad password, try again", category="error")

          else:
                flash("Unknown user, try again", category="error")
        
    return render_template("login.html", user = current_user)

@auth.route('logout')
@login_required
def logout():
      logout_user()
      return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
        if request.method == 'POST':
            email = request.form.get('email')
            username = request.form.get('username')
            pswd1 = request.form.get('pswd1')
            pswd2 = request.form.get('pswd2')

            name = request.form.get('name')
            surname = request.form.get('surname')
            phone = request.form.get('phone')
            badge_number = request.form.get('badge_number')

            check_mail = User.query.filter_by(email=email).first()
            check_user = User.query.filter_by(username=username).first()
            check_badge = Employee.query.filter_by(badge_number=badge_number).first()
            if check_mail: 
                  flash('Email address already exists, try again', category='error')
                  return redirect(url_for('auth.register'))
            elif check_user:
                  flash('Usernam already exists, try again', category='error')
                  return redirect(url_for("auth.register"))
            elif check_badge:
                  flash('This badge number is already taken, try again', category='error')
                  return redirect(url_for("auth.register"))
            else:

                try:
                  result = db.session.execute(text('INSERT INTO employee (name, surname, phone, badge_number) VALUES (:name, :surname, :phone, :badge_number)'),
                                           {'name':name, 'surname':surname, 'phone':phone, 'badge_number':badge_number})



                  new_user = User(email = email, username = username, 
                              password = generate_password_hash(pswd1, method='sha256'), employee_id=result.lastrowid, isAdmin=False, isOperator=False)
                  db.session.add(new_user)
                  db.session.commit()
                  login_user(new_user, remember=True)
                  flash('Account created!', category='success')
                  return redirect(url_for('view.home'))
                except:
                  db.session.rollback()
                  flash('Account was not created!', category='failure')
                  return redirect(url_for('view.home'))

        return render_template("register.html", user = current_user)

def update_user_notifications():
    # Storing notifications in session object, available throughout the app
    user_notifications_relation = NotificationUser.query.filter_by(user_id=current_user.id).all()
    notifications = []
    for relation in user_notifications_relation:
        notifications.append(Notification.query.filter_by(id=relation.notification_id).first())
    notifications = [notification.serialize for notification in notifications]
    session["notifications"] = notifications