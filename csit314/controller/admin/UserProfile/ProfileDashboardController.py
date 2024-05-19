from flask import Blueprint, render_template
from csit314.controller.role_service.decorators import login_required, admin_only

bp = Blueprint('profileDashboard', __name__, template_folder="/boundary/templates")


#for displaying profile dashboard
@bp.route('/user_profile_dashboard')
@login_required
@admin_only
def dashboard():
    return render_template("UserProfile/UserProfileDashboardPage.html")