from flask import Blueprint, render_template, request, flash, url_for
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/', methods=['GET'])
def home():
    return render_template("landing.html", user=current_user)


@views.route('/creator-courses-list', methods=['GET', 'POST'])
def creator_courses_list():
    return render_template("creator-courses-list.html", user=current_user)

