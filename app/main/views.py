from flask import render_template, session, redirect, url_for, abort, flash \
,current_app, request
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import User, Role
from ..decorators import admin_required, permission_required
from ..models import Permission

@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@main.route('/posts')
@login_required
def posts():
    return render_template('index.html')

@main.route('/admin')
@login_required
@admin_required
def admin():
    return "Admin Only"

@main.route('/moderate')
@login_required
@permission_required(Permission.MODERATE_COMMENTS)
def moderate():
    return "Moderate only"

@main.route('/user/<id>')
@login_required
def user(id):
    user = User.query.get_or_404(id)
    if user == None:
        abort(404)
    return render_template('user.html', user=user)

@main.route('/user/<id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    print(id)
    if current_user.id != int(id):
        abort(403)
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('Profile updated')
        return redirect(url_for('.user', id=id))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/user/<id>/admin_edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.location = form.location.data
        user.about_me = form.about_me.data
        user.update_gravatar_hash()
        db.session.add(user)
        flash('The profile has been updated')
        return redirect(url_for('.user', id=user.id))
    form.email.data = user.email
    form.username.data = user.username
    form.role.data = user.role_id
    form.name.data = user.name
    form.location.data = user.location
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form)

@main.route('/shutdown')
def server_shutdown():
    if not current_app.testing:
        abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'
