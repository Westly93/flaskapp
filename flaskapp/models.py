from flask_sqlalchemy import SQLAlchemy
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from flask_login import UserMixin
from sqlalchemy.sql import func
from flask import current_app
from enum import Enum


db = SQLAlchemy()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(155), nullable=False)
    last_name = db.Column(db.String(155), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    # image_file= db.Column(db.String(20), default= 'default.jpg')
    password = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    roles = db.relationship('Role', secondary='user_roles',
                            backref=db.backref('users', lazy='dynamic'))
    courses = db.relationship('Course')
    lessons = db.relationship('Lesson')
    topics = db.relationship('Topic')

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def has_role(self, role_name):
        # Check if the user has the specified role
        return any(role.name == role_name for role in self.roles)

    def __repr__(self):
        return f"User('{self.username}'-'{self.email}', '{self.image_file}')"


# Roles# Leaner model
class Learner(db.Model, UserMixin):
    __tablename__ = "learner"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(155), nullable=False)
    last_name = db.Column(db.String(155), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'{self.first_name} {self.last_name} Learner'


class LearnerCredentials(db.Model):
    __tablename__ = "learner_credentials"
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(20), nullable=False)


class LearnerIdentification(db.Model):
    __tablename__ = "learner_identification"
    id = db.Column(db.Integer, primary_key=True)
    identification_number = db.Column(
        db.String(12), nullable=False, unique=True)


class LearnerContact(db.Model):
    __tablename__ = "learner_contact"
    id = db.Column(db.Integer, primary_key=True)
    cellphone = db.Column(db.String(20), nullable=False)
    street_address = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)


class LearnerPersornalDetails(db.Model):
    __tablename__ = "learner_personaldetails"
    id = db.Column(db.Integer, primary_key=True)
    gender = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(20), nullable=False)
    dob = db.Column(db.DateTime(timezone=True))
    


class UserProvider(db.Model):
    __tablename__ = "userprovider"
    id = db.Column(db.Integer, primary_key=True)
    providerid = db.Column(
        db.Integer, db.ForeignKey('provider.id'))
    userid = db.Column(
        db.Integer, db.ForeignKey('user.id'))


class UserSuspended(db.Model):
    __tablename__ = "user_suspended"
    id = db.Column(db.Integer, primary_key=True)
    adminuserid = db.Column(
        db.Integer, db.ForeignKey('user.id'))
    datesuspended = db.Column(db.DateTime(timezone=True), default=func.now())


class UserBio(db.Model):
    __tablename__ = "user_bio"
    id = db.Column(db.Integer, primary_key=True)
    biography = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), default='default.jpg')


class Nationality(db.Model):
    __tablename__ = "nationality"
    id = db.Column(db.Integer(), primary_key=True)
    code = db.Column(db.String(255), unique=True)
    nation = db.Column(db.String(255), unique=True)

# Roles


class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(255), nullable=True)
    # users = db.relationship('User', secondary="roles", back_populates="roles")

    def __repr__(self):
        return self.name

# user roles


class UserRoles(db.Model):
    __tablename__ = "user_roles"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey(
        'user.id', ondelete='CASCADE'))
    roles_id = db.Column(db.Integer(), db.ForeignKey(
        'roles.id', ondelete='CASCADE'))


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(155), nullable=False, unique=True)
    parent_id = db.Column(db.Integer, db.ForeignKey(
        'provider.id'), nullable=True, default=0)
    parent = db.relationship('Provider', remote_side=[
                             id], backref='child_providers')
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    provider_type_id = db.Column(
        db.Integer, db.ForeignKey('provider_type.id'))
    provider_type = db.relationship(
        'ProviderType', backref='provider_type')
    courses = db.relationship('Course')

    def __repr__(self):
        return f"{self.name} Provider"


class ProviderType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(155), nullable=False)
    created = db.Column(db.DateTime(timezone=True), default=func.now())
    # providers = db.relationship('Provider', backref='provider_type', lazy=True)

    def __repr__(self):
        return f"{self.name} Provider Type"


# provider and provider type association
class ProviderProviderType(db.Model):
    __tablename__ = "provider_provider_types"
    id = db.Column(db.Integer, primary_key=True)
    providerid = db.Column(db.Integer(), db.ForeignKey(
        'provider.id', ondelete='CASCADE'))
    providertypeid = db.Column(db.Integer(), db.ForeignKey(
        'provider_type.id', ondelete='CASCADE'))
 # Creator/Instructor MODELS


class Courses(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    providerid = db.Column(db.Integer, db.ForeignKey('provider.id'))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(155), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    datecreated = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"{self.name} Course"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    providerid = db.Column(db.Integer, db.ForeignKey('provider.id'))
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(155), nullable=False)
    description = db.Column(db.String(2000), nullable=False)
    datecreated = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"{self.name} Courses"

# class CourseLesson(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     courseid = db.Column(db.Integer, db.ForeignKey(
#         'course.id'), nullable=False)
#     lessonid = db.Column(db.Integer, db.ForeignKey(
#         'lesson.id'), nullable=False)
#     sequencenumber = db.Column(db.Integer, nullable=False)


#     def __repr__(self):
#         return f"{self.name} Lesson"


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String(100), nullable=False)
    objectives = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(500), nullable=False)
    datecreated = db.Column(db.DateTime(timezone=True), default=func.now())
    duration = db.Column(db.String(50), nullable=False)
    topics = db.relationship('Topic', backref=db.backref('topics', lazy=True))

    def __repr__(self):
        return f"{self.name} Lesson"


# class Lessons(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     summary = db.Column(db.String(500), nullable=False)
#     objectives = db.Column(db.Text, nullable=False)
#     duration = db.Column(db.String(50), nullable=False)

#     def __repr__(self):
#         return f"{self.name} Lessons"


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('user.id'))
    lessonid = db.Column(db.Integer, db.ForeignKey('lesson.id'))
    # contenttypeid = db.Column(db.Integer, db.ForeignKey('contenttype.id'))
    content = db.Column(db.Text, nullable=False)
    datecreated = db.Column(db.DateTime(timezone=True), default=func.now())

    def __repr__(self):
        return f"Topic {self.name}"


class Topics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"Topics {self.name}"


class ContentType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(100), nullable=False)
    # topic = db.relationship('Topic', backref=db.backref('topic', lazy=True))


#     def __repr__(self):
#         return f"ContentType {self.id}: {self.name}"


class CoursePrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    currency_id = db.Column(db.Integer, db.ForeignKey(
        'currency.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    currency = db.relationship('Currency')

    def __repr__(self):
        return f"CoursePrice {self.id}: {self.price} {self.currency.code}"


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(2000), nullable=False)

    def __repr__(self):
        return f"CoursePrice {self.id}: {self.price} {self.currency.code}"
