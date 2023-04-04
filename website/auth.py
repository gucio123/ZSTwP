from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
#     if request.method == 'POST':
          
#           email = request.form.get('email')
#           psswd = request.form.get('password')
#           user = User.query.filter_by(email=email).first()
#           if user:
#                 if check_password_hash(user.password, psswd):
#                       flash("Jestes zalogowany", category="success")
#                       login_user(user, remember=True)
#                       return redirect(url_for('views.home'))
#                 else:
#                       flash("Zle haslo kasztanie", category="error")

#           else:
#                 flash("Nie ma takiego usera ziomek", category="error")
        
    return "<p>login</p>s"

@auth.route('logout')
# @login_required
def logout():
      return "<p>Logout</p>"

@auth.route('/register')
def register():
        return "<p>Register</p>"    