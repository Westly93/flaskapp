from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import db
from .models import User, Provider, Course, Courses, Lesson, Topic, CoursePrice, Currency
from .decorators import role_required

creator = Blueprint('creator', __name__)

@creator.route('/creator-courses-list', methods=['GET', 'POST'])
# @login_required
def creator_courses_list():
    user = User.query.filter_by(email=current_user.email).first_or_404()
    
    courses = user.courses
    return render_template("creator-courses-list.html", user=user, courses=courses)

@creator.route('/course_details/<course_id>/lessons', methods=['GET', 'POST'])
# @login_required
def course_details(course_id):
    course = Course.query.get_or_404(course_id)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    lessons = user.lessons
    return render_template("course_lessons.html", course=course, lessons=lessons)



@creator.route('/create_course', methods=['GET', 'POST'])
@login_required
# @role_required('Content Creator')
def create_course():
    if request.method == "POST":
        title = request.form.get('title')
        description = request.form.get('description')
        providerid = request.form.get('providerid')
        
        course = Course(title=title, description=description, providerid=providerid, userid=current_user.id)
        db.session.add(course)
        db.session.commit()
        
        return redirect(url_for('creator.creator_courses_list'))
    
    return render_template("create_course.html", user=current_user)
         

@creator.route('/lessons_list>', methods=['GET', 'POST'])
# @login_required
def lessons_list():
    
    
    # if request.method == 'POST':
    #     return redirect(url_for('creator.create_lesson'))
        
    return render_template("lessons_list.html", user=current_user)

@creator.route('/create_lesson', methods=['GET', 'POST'])
@login_required
def create_lesson():
    
    if request.method == 'POST':
        title = request.form.get('title')
        summary = request.form.get('summary')
        objectives = request.form.get('objectives')
        duration = request.form.get('duration')

        
        lesson = Lesson(title=title, summary=summary, objectives=objectives, duration=duration, userid=current_user.id)
        db.session.add(lesson)
        db.session.commit()
        return redirect(url_for('creator.create_topic'))
        
    return render_template("create_lesson.html", user=current_user)

@creator.route('/create_topic', methods=['GET', 'POST'])
@login_required
def create_topic():
    lesson = Lesson.query.all()
    if request.method == 'POST':
        content = request.files.get('content')
        
        # file_path = 'path/to/save/' + file.filename  # Update the path to your desired location
        # file.save(file_path)

        topic = Topic(content=content)
        db.session.add(topic)
        db.session.commit()

        return redirect(url_for('creator.creator_courses_list'))
        
    return render_template("create_topic.html", user=current_user)

#Updates Operations
@creator.route('/course/<course_id>/update', methods=['GET', 'POST'])
def update_course(course_id):
    course = Course.query.get_or_404(course_id)
    
    if request.method == 'POST':
        course.title = request.form.get('title')
        course.decsription = request.form.get('description')
        
        db.session.commit()
        # flash('Update Success!', category='success')
        return redirect(url_for('creator.creator_courses_list'))
        
    return render_template('edit_course.html', course=course)

@creator.route('/lesson/<lesson_id>/update', methods=['GET', 'POST'])
def update_lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    
    if request.method == 'POST':
        lesson.title = request.form.get('title')
        lesson.decsription = request.form.get('description')
        
        db.session.commit()
        # flash('Update Success!', category='success')
        return redirect(url_for('creator.creator_courses_list'))
        
    return render_template('edit_lesson.html', lesson=lesson)


