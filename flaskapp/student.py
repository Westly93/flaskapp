from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Provider, Courses, Course, Lesson, Topic, ContentType, CoursePrice, Currency
from . import db

student = Blueprint('student', __name__)

@student.route('/student_courses_list', methods=['GET', 'POST'])
@login_required
def student_courses_list():
    return render_template("student_courses_list.html", user=current_user)



         

