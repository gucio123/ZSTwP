from flask import Blueprint, request, render_template, flash
from flask_login import login_required
from website.models import Contractor, User
from website import db

bp = Blueprint('show_faults_status', __name__)


@bp.route('/show_faults_status', methods=['GET', 'POST'])
@login_required
def show_faults_status():

    return render_template('show_faults_status.html')

