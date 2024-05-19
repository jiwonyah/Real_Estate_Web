from flask import Blueprint, jsonify, request, render_template
from csit314.controller.role_service.decorators import login_required, admin_only
from csit314.entity.UserProfile import UserProfile


class CreateUserProfileController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/create_user_profile", view_func=self.create_user_profile, methods=['GET', 'POST'])

    @login_required
    @admin_only
    def create_user_profile(self):
        if request.method == 'GET':
            return render_template('UserProfile/CreateNewUserProfilePage.html')

        elif request.method == 'POST':
            profileName = request.form['profileName']
            profileDescription = request.form['profileDescription']
            status = 'Active'

            profile_details = {
                'profileName': profileName,
                'profileDescription': profileDescription,
                'status': status
            }

            results = UserProfile.createUserProfile(profile_details)
            if results:
                return jsonify({'success': True, 'message': 'User Profile created successfully'})
            else:
                return jsonify({'success': False, 'error': 'Profile Name Exists'})