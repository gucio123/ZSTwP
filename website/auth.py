from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
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

            check_mail = User.query.filter_by(email=email).first()
            check_user = User.query.filter_by(username=username).first()
            if check_mail: 
                  flash('Email address already exists, try again', category='error')
                  return redirect(url_for('auth.register'))
            elif check_user:
                  flash('Usernam already exists, try again', category='error')
                  return redirect(url_for("auth.register"))
            else:
                  new_user = User(email = email, username = username, 
                              password = generate_password_hash(pswd1, method='sha256'))
                  db.session.add(new_user)
                  db.session.commit()
                  login_user(new_user, remember=True)
                  flash('Account created!', category='success')
                  return redirect(url_for('view.home'))

        return render_template("register.html", user = current_user)