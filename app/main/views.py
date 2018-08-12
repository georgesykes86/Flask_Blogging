from flask import render_template, session, redirect, url_for
from flask_login import login_required
from . import main
from .forms import NameForm
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
