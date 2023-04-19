from flask import Blueprint, render_template
from flask_login import login_required

from website import create_ticket

views = Blueprint('views', __name__)


# @views.route('/')
# def test():
#     # example how to use (creates ticket when on home page)
#     create_ticket(3)
@views.route('/')
def home():
    return render_template("home.html")

@views.route('/admin')
@login_required
def admin():
    return render_template("admin.html")
