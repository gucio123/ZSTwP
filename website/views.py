from flask import Blueprint, render_template
from website.create_ticket import create_ticket

views = Blueprint('views', __name__)


@views.route('/')
def test():
    create_ticket()
    return render_template("home.html")
