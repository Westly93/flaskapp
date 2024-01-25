from flask_wtf import FlaskForm
from flask import current_app
from flask_login import current_user
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileAllowed
from flaskapp.models import User, ProviderType, Provider, Role


class UserRegistrationForm(FlaskForm):
    first_name = StringField('First Name', validators=[
        DataRequired(), Length(min=2, max=155)])
    last_name = StringField('Last Name', validators=[
        DataRequired(), Length(min=2, max=155)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    # def validate_field(self, field):
    #    if True:
    #        return ValidationError('Validation Message')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'This email is taken. Please choose a different one!')


class UserLoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('login')


class UserUpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Update profile picture', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError(
                    'This username is taken. Please Choose a different one')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError(
                    'This email is taken. Please choose a different one')


class RequestResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError(
                'There is no account with that email. You need to register')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Old Password', validators=[DataRequired()])
    confirm_password = PasswordField('New Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Password Reset')


class ProviderTypeForm(FlaskForm):
    name = StringField('Provider Type', validators=[
        DataRequired(), Length(min=2, max=155)])
    submit = SubmitField('Create')

    def validate_name(self, name):
        provider_type = ProviderType.query.filter_by(name=name.data).first()
        if provider_type:
            raise ValidationError(
                "The provider type is Already taken, Please chose a different one!")


class ProviderForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(ProviderForm, self).__init__(*args, **kwargs)
        with current_app.app_context():
            providers = Provider.query.all()
            provider_types = ProviderType.query.all()
            empty_choice = [("", "-------------")]
            choices = empty_choice + [(str(provider.id), provider.name)
                                      for provider in providers]
            provider_type_choices = empty_choice + [
                (provider_type.id, provider_type.name) for provider_type in provider_types]
            self.provider_type.choices = provider_type_choices
            self.provider.choices = choices

    name = StringField('Provider Name', validators=[
        DataRequired(), Length(min=2, max=155)])
    provider = SelectField("Select provider")
    provider_type = SelectField("Select provider type")
    submit = SubmitField('Create')

    def validate_name(self, name):
        provider = Provider.query.filter_by(
            name=name.data, parent_id=self.provider.data, provider_type_id=self.provider_type.data).first()
        if provider:
            raise ValidationError(
                "The provider name is Already taken, Please chose a different one!")


class RoleForm(FlaskForm):
    name = StringField('Role', validators=[
        DataRequired(), Length(min=2, max=155)])
    description = TextAreaField('Description', validators=[
                                Length(max=255)], render_kw={"rows": 5})
    submit = SubmitField('Create')

    def validate_name(self, name):
        role = Role.query.filter_by(name=name.data).first()
        if role:
            raise ValidationError(
                "This Role Exist, Please chose a different one!")


class UserBioForm(FlaskForm):
    biography = TextAreaField('Biography', validators=[
        Length(max=255)], render_kw={"rows": 5})
    image = FileField('Update Bio Image', validators=[
        FileAllowed(['jpg', 'png'])])


class LearnerPersornalDetailsForm(FlaskForm):
    title = StringField('Title', validators=[
        DataRequired(), Length(min=2, max=20)])
    dob = StringField('Date ', validators=[
        DataRequired(), Length(min=2, max=155)])
    gender = SelectField("Select Gender", choices=[
        "Male", "Female", "Other"
    ])
    
class LearnerContactForm(FlaskForm):
    cellphone = StringField('Contact', validators=[
        DataRequired(), Length(min=2, max=10)])
