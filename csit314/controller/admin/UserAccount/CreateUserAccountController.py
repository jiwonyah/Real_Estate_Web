from flask import Blueprint, jsonify, request, render_template
from csit314.controller.role_service.decorators import login_required, admin_only
from csit314.entity.UserAccount import UserAccount
from csit314.entity.UserProfile import UserProfile
import bcrypt

class CreateUserAccountController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/create_user_account", view_func=self.create_user_account, methods=['GET', 'POST'])

    @login_required
    @admin_only
    def create_user_account(self):
        # if request is get display the create page
        if request.method == 'GET':
            profiles = UserProfile.getAllProfiles()
            return render_template('UserAccount/CreateUserAccountPage.html', profiles=profiles)

        # if request method is post do validation and return success type
        elif request.method == 'POST':
            firstName = request.form['firstName']
            lastName = request.form['lastName']
            email = request.form['email']
            userid = request.form['userid']
            password = request.form['password']
            role = request.form['role']
            status = 'Active'

            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            account_details = {
                'firstName': firstName,
                'lastName': lastName,
                'email': email,
                'userid': userid,
                'password': hashed_password.decode('utf-8'),
                'role': role,
                'status': status
            }

            results = UserAccount.createUserAccount(account_details)
            if results:
                return jsonify({'success': True, 'message': 'User Account created successfully'})
            elif UserAccount.useridExists(account_details):
                return jsonify({'success': False, 'error': 'Username Exists'})
            elif UserAccount.emailExists(account_details):
                return jsonify({'success': False, 'error': 'Email Exists'})