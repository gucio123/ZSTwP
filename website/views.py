from flask import Blueprint, render_template, abort, session
from flask_login import login_required
from werkzeug.security import generate_password_hash

views = Blueprint('view', __name__)



@views.route('/')
def home():
    print(generate_password_hash('admin', method='sha256'))
    return render_template("home.html")

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template("admin.html")