from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from src.models.user import User
from src.models.build import Build

bp = Blueprint('user', __name__)

@bp.route('/profile/<username>')
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    builds = Build.query.filter_by(author_id=user.id).all()
    return render_template('user/profile.html', user=user, builds=builds)

@bp.route('/my-builds')
@login_required
def my_builds():
    builds = Build.query.filter_by(author_id=current_user.id).all()
    return render_template('user/my_builds.html', builds=builds)