from flask import Blueprint, render_template, abort, session
from flask_login import login_required



views = Blueprint('view', __name__)



@views.route('/')
def home():
    return render_template("home.html")

@views.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    return render_template("admin.html")