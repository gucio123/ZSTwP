from flask import Blueprint, render_template

from website import create_ticket

views = Blueprint('views', __name__)


# @views.route('/')
# def test():
#     # example how to use (creates ticket when on home page)
#     create_ticket(3)
def home():
    return render_template("home.html")

@views.route('/admin')
def admin():
    return render_template("admin.html")
