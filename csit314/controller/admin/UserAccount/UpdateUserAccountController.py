from flask import Blueprint, jsonify, request, render_template
from csit314.entity.UserAccount import UserAccount
from csit314.controller.role_service.decorators import login_required, admin_only
import bcrypt

class UpdateUserAccountController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/update_user_account", view_func=self.view_user_accounts, methods=['GET'])
        self.add_url_rule("/update_user_account/<userid>", view_func=self.display_update_form, methods=['GET'])
        self.add_url_rule("/update_user_account/<userid>", view_func=self.update_user_account, methods=['POST'])

    #for displaying all users page
    @login_required
    @admin_only
    def view_user_accounts(self):
        userList = UserAccount.getUserAccounts()
        return render_template("UserAccount/UpdateUserAccountPage.html", users=userList)


    #for displaying the account update form
    @login_required
    @admin_only
    def display_update_form(self, userid):
        user = UserAccount.getUserDetails(userid)
        return render_template("UserAccount/UpdateUserAccountForm.html", user=user)

    @login_required
    @admin_only
    def update_user_account(self, userid):
        user = UserAccount.getUserDetails(userid)
        firstName= request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        new_username = request.form['userid']
        password = request.form['password']
        role = request.form['role']

        if 'suspended' in request.form:
            status = 'Active'
        else:
            status = 'Suspended'

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        updateDetails = {
            'firstName': firstName,
            'lastName': lastName,
            'email': email,
            'userid': new_username,
            'password': hashed_password.decode('utf-8'),
            'role': role,
            'status': status
        }

        results = UserAccount.updateUserAccount(user.userid, updateDetails)
        if results:
            return jsonify({'success': True, 'message': 'User Account updated successfully'})
        elif new_username != user.userid and UserAccount.useridExists(updateDetails):
            return jsonify({'success': False, 'error': 'Username Exists'})
        elif email != user.email and UserAccount.emailExists(updateDetails):
            return jsonify({'success': False, 'error': 'Email Exists'})

