from flask import Blueprint, render_template
from website.create_ticket import create_ticket

views = Blueprint('views', __name__)


@views.route('/')
def test():
    # example how to use (creates ticket when on home page)
    create_ticket(3)
    return render_template("home.html")
