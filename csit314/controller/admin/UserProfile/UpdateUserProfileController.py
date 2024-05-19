from flask import Blueprint, jsonify, render_template, request
from csit314.controller.role_service.decorators import login_required, admin_only
from csit314.entity.UserProfile import UserProfile

class UpdateUserProfileController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule('/update_user_profile', view_func=self.view_user_profile, methods=['GET'])
        self.add_url_rule('/update_user_profile/<profileName>', view_func=self.display_update_form, methods=['GET'])
        self.add_url_rule('/update_user_profile/<profileName>', view_func=self.update_user_profile, methods=['POST'])

    @login_required
    @admin_only
    def view_user_profile(self):
        profileList = UserProfile.getAllProfiles()
        return render_template('UserProfile/UpdateUserProfilePage.html', profiles=profileList)

    @login_required
    @admin_only
    def display_update_form(self, profileName):
        profile = UserProfile.getProfile(profileName)
        return render_template("UserProfile/UpdateUserProfileForm.html", profile=profile)


    def update_user_profile(self, profileName):
        profile = UserProfile.getProfile(profileName)
        new_profileName = request.form['profileName']
        profileDescription = request.form['profileDescription']

        if 'suspended' in request.form:
            status = 'Active'
        else:
            status = 'Suspended'

        updateDetails = {
            'profileName': new_profileName,
            'profileDescription': profileDescription,
            'status': status
        }

        results = UserProfile.updateUserProfile(profile.profileName, updateDetails)
        if results:
            return jsonify({'success': True, 'message': 'User Profile updated successfully'})
        elif new_profileName != profile.profileName and UserProfile.profileNameExists(updateDetails):
            return jsonify({'success': False, 'error': 'Role Name Exists'})