from flask import render_template, redirect, flash, request, url_for, Blueprint
from flaskapp.users.forms import (
    UserRegistrationForm,
    UserLoginForm, UserUpdateAccountForm,
    RequestResetForm, ResetPasswordForm,
    ProviderForm, ProviderTypeForm,
    RoleForm
)
from flaskapp.models import User, Provider, ProviderType, Role
from werkzeug.security import generate_password_hash, check_password_hash
from flaskapp.models import db
from flask_login import login_user, current_user, logout_user, login_required
from flaskapp.users.utils import save_picture, send_reset_email
from flaskapp.decorators import role_required

auth = Blueprint('auth', __name__)


# Create Registration route
@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = UserRegistrationForm()
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    if form.validate_on_submit():
        user = User(first_name=form.first_name.data, last_name=form.last_name.data,
                    email=form.email.data, password=generate_password_hash(form.password.data, method='pbkdf2:sha256'))
        db.session.add(user)
        db.session.commit()
        flash(f'You are successfully registered, you can now login', 'success')
        return redirect(url_for('auth.login'))
    return render_template('users/register.html', title='Register', form=form, user=current_user)


# Create login route
@auth.route('/login', methods=['POST', 'GET'])
def login():
    form = UserLoginForm()
    if current_user.is_authenticated:
        return redirect('home')
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                next_page = request.args.get('next')
                if user.has_role("Admin"):
                    return redirect(url_for('auth.admin'))
                return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else:
            flash('Your username or password does not match!',
                  'error')
    return render_template('users/login.html', title='Login', form=form, user=current_user)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('views.home'))


@auth.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UserUpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated successifully!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email

    image_file = url_for(
        'static', filename=f'profile_pics/{current_user.image_file}')
    return render_template('account.html', title='Account', image_file=image_file, form=form, user=current_user)

 # Create a route for every user posts


@auth.route("/admin", methods=["GET"])
@login_required
@role_required('Admin')
def admin():
    return render_template("admin/index.html", user=current_user)


@auth.route("/providers", methods=["GET"])
@login_required
@role_required('Admin')
def providers():
    providers = Provider.query.filter(Provider.parent_id == 0).all()
    return render_template("admin/providers.html", user=current_user, providers=providers)


@auth.route("/provider-types", methods=["GET"])
@login_required
@role_required('Admin')
def provider_types():
    provider_types = ProviderType.query.all()
    return render_template("admin/provider_types.html", user=current_user, provider_types=provider_types)


# Roles
@auth.route("/roles", methods=["GET"])
@login_required
@role_required('Admin')
def roles():
    roles = Role.query.all()
    return render_template("admin/roles.html", user=current_user, roles=roles)


# Create Provider route
@auth.route("/providers/create", methods=["GET", "POST"])
@login_required
@role_required('Admin')
def create_provider():
    form = ProviderForm()
    if request.method == "POST" and form.validate_on_submit():
        if form.provider.data == "":
            provider = Provider(
                name=form.name.data,
                provider_type_id=int(form.provider_type.data)
            )
        else:
            provider = Provider(
                name=form.name.data,
                parent_id=form.provider.data,
                provider_type_id=form.provider_type.data
            )
        db.session.add(provider)
        db.session.commit()
        flash("Provider is successfully created!", "success")
        return redirect(url_for('auth.providers'))
    return render_template("admin/create_provider.html", form=form, user=current_user)

# Edit Provider Route


@auth.route("/providers/<int:id>/edit", methods=["GET", "POST"])
@login_required
@role_required('Admin')
def edit_provider(id):
    provider = Provider.query.get_or_404(id)
    form = ProviderForm(obj=provider)
    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(provider)
        db.session.commit()
        flash("Provider Updated Successfully!", "success")
        return redirect(url_for("auth.providers"))
    return render_template("admin/edit_provider.html", form=form, user=current_user)

# Delete Provider


@auth.route("/providers/<int:id>/delete", methods=["POST"])
@login_required
@role_required('Admin')
def delete_provider(id):
    provider = Provider.query.get_or_404(id)
    db.session.delete(provider)
    db.session.commit()
    flash('Provider deleted successfully!', 'success')
    return redirect(url_for('auth.providers'))

# List all users


@auth.route("/", methods=["GET", "POST"])
@login_required
@role_required('Admin')
def users():
    users = User.query.all()
    return render_template("admin/users.html", user=current_user, users=users)

# user detail


@auth.route("/<int:id>", methods=["GET", "POST"])
@login_required
# @role_required('Admin')
def user_detail(id):
    obj = User.query.get_or_404(id)
    roles = Role.query.all()
    return render_template("admin/user_detail.html", user=current_user, users=users, obj=obj, roles=roles)


@auth.route("/provider-type/create", methods=["GET", "POST"])
@login_required
@role_required('Admin')
def create_provider_type():
    form = ProviderTypeForm()
    if request.method == "POST":
        # print(request.form.get("provider"))
        if form.validate_on_submit():
            provider_type = ProviderType(
                name=form.name.data,
            )
            db.session.add(provider_type)
            db.session.commit()
            flash("Provider type is successfully created!", "success")
            return redirect(url_for('auth.provider_types'))
    return render_template("admin/create_provider_type.html", form=form, user=current_user)


# edit Provider Type
@auth.route("/provider-types/<int:id>/edit", methods=["GET", "POST"])
@login_required
@role_required('Admin')
def edit_provider_type(id):
    provider_type = ProviderType.query.get_or_404(id)
    form = ProviderTypeForm(obj=provider_type)
    if request.method == "POST" and form.validate_on_submit():
        form.populate_obj(provider_type)
        db.session.commit()
        flash("Provider Type Updated Successfully!", "success")
        return redirect(url_for("auth.provider_types"))
    return render_template("admin/edit_provider_type.html", form=form, user=current_user)


# Delete provider Type
@auth.route("/provider-types/<int:id>/delete", methods=["POST"])
@login_required
@role_required('Admin')
def delete_provider_type(id):
    provider_type = ProviderType.query.get_or_404(id)
    db.session.delete(provider_type)
    db.session.commit()
    flash('Provider Type deleted successfully!', 'success')
    return redirect(url_for('auth.provider_types'))


# User Dashboard
@auth.route("/dashboard", methods=["GET"])
@login_required
def dashboard():
    return render_template("users/dashboard.html", title="Dashboard", user=current_user)

# new role


@auth.route("/roles/create", methods=["GET", "POST"])
@login_required
# @role_required('Admin')
def create_role():
    form = RoleForm()
    if request.method == "POST" and form.validate_on_submit():
        role = Role(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(role)
        db.session.commit()
        flash("Role added successfully", "success")
        return redirect(url_for('auth.roles'))
    return render_template("admin/create_role.html", user=current_user, form=form)

# assign user roles


@auth.route("/<int:id>/roles", methods=["POST"])
@login_required
# @role_required('Admin')
def assign_roles(id):
    user = User.query.get_or_404(id)
    roles = request.form.getlist('roles')
    print(roles)
    user.roles = []

    # Assign new roles to the user
    for role_id in roles:
        role = Role.query.get(role_id)
        if role:
            user.roles.append(role)
    db.session.commit()
    return redirect(url_for('auth.user_detail', id=user.id))


@auth.route('/user/<string:username>/')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=2)
    return render_template('user_posts.html', posts=posts, user=user)


# create a route for password request
@auth.route('/password_reset', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data)
        send_reset_email(user)
        flash('The email has been send with instructions to reset your password', 'info')
        return redirect(url_for('users.login'))
    return render_template('users/reset_request.html', title='Password Reset', form=form, user=current_user)

# create a route for them to finally reset their password


@auth.route('/password_reset/<token>/', methods=['GET', 'POST'])
def request_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That token is invalid or expired', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password is updated successfully, you can now login', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='password Reset', form=form)
