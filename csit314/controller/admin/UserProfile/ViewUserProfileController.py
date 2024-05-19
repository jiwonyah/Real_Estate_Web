from flask import Blueprint, jsonify, render_template
from csit314.controller.role_service.decorators import login_required, admin_only
from csit314.entity.UserProfile import UserProfile


class ViewUserProfileController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule('/view_user_profile', view_func=self.view_all_profile, methods=['GET'])
        self.add_url_rule('/view_user_profile_details/<profileName>',
                          view_func=self.view_account_details, methods=['GET'])

    @login_required
    @admin_only
    def view_all_profile(self):
        profileList = UserProfile.getAllProfiles()
        return render_template('UserProfile/ViewUserProfilePage.html', profiles=profileList)

    @login_required
    @admin_only
    def view_account_details(self, profileName):
        profile = UserProfile.getProfile(profileName)
        return jsonify({
            'profileName': profile.profileName,
            'profileDescription': profile.profileDescription,
            'status': profile.status
        })