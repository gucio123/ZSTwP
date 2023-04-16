from flask import Blueprint, render_template

views = Blueprint('views', __name__)


# @views.route('/')
# def test():
#     # example how to use (creates ticket when on home page)
#     create_ticket(1, 1)
def home():
    return render_template("home.html")

@views.route('/admin')
def admin():
    return render_template("admin.html")
