from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def test():
<<<<<<< HEAD
    # example how to use (creates ticket when on home page)
    create_ticket(3)
def home():
=======
>>>>>>> 460c7825c943e2d8f74cea881beaf3120d607eb5
    return render_template("home.html")

@views.route('/admin')
def admin():
    return render_template("admin.html")
