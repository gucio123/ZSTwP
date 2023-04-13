from flask import Blueprint, render_template
from website.create_ticket import test1

views = Blueprint('views', __name__)


@views.route('/')
def test():
    test1()
    return render_template("home.html")
