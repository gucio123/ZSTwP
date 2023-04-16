from flask import Blueprint, render_template
views = Blueprint('views', __name__)


@views.route('/')
def test():
    return render_template("home.html")
