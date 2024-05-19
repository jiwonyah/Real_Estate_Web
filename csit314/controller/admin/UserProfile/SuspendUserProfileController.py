from flask import Blueprint, render_template, request, jsonify
from csit314.controller.role_service.decorators import login_required, admin_only
from csit314.entity.UserProfile import UserProfile

class SuspendUserProfileController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule('/suspend_user_profile', view_func=self.display_suspend_form, methods=['GET'])
        self.add_url_rule('/suspend_profile', view_func=self.suspend_profile, methods=['POST'])

    @login_required
    @admin_only
    def display_suspend_form(self):
        profiles = UserProfile.getAllProfiles()
        return render_template('UserProfile/SuspendUserProfilePage.html', profiles=profiles)

    @login_required
    @admin_only
    def suspend_profile(self):
        profileName = request.form['profileName']
        results = UserProfile.suspend_profile(profileName)
        if results:
            return jsonify({'success': True, 'message': 'User Profile suspended successfully'})
        elif UserProfile.getProfile(profileName) is None:
            return jsonify({'success': False, 'message': 'Profile Name does not exist'})
        else:
            return jsonify({'success': False, 'message': 'User Profile already suspended'})