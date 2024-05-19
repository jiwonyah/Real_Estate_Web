from flask import Blueprint, render_template
from csit314.entity.UserAccount import UserAccount
from csit314.app import db
from flask import Blueprint, url_for, render_template, flash, request, redirect, session, g
from csit314.controller.role_service.decorators import suspended

bp = Blueprint('profile', __name__)

# this is just for checking the information of the user that I'm currently logged in to
@bp.route('/profile/<userid>/')
@suspended
def profile(userid):
    user = UserAccount.query.filter_by(userid=userid).first()
    if not user:
        # error if user doesn't exist
        return render_template('error/error.html', message='User not found'), 404

    return render_template('profile/profile.html', user=user)