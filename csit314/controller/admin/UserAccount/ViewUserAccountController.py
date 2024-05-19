from flask import Blueprint, jsonify, request, render_template
from csit314.controller.role_service.decorators import login_required, admin_only
from csit314.entity.UserAccount import UserAccount

class ViewUserAccountController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/view_user_account", view_func=self.view_user_accounts, methods=['GET'])
        self.add_url_rule("/view_user_account_details/<userid>",
                          view_func=self.view_account_details, methods=['GET'])

    #for displaying the user account page
    @login_required
    @admin_only
    def view_user_accounts(self):
        userList = UserAccount.getUserAccounts()
        return render_template("UserAccount/ViewUserAccountPage.html", users=userList)


    #for retrieving user account details of a specific username
    @login_required
    @admin_only
    def view_account_details(self, userid):
        #getting the user object from UserAccount class method
        user = UserAccount.getUserDetails(userid)
        full_name = f"{user.firstName} {user.lastName}" if user.firstName and user.lastName else None
        return jsonify({
            'firstName': user.firstName,
            'lastName': user.lastName,
            'full_name': full_name,
            'email': user.email,
            'userid': user.userid,
            'password': user.password,
            'role': user.role,
            'status': user.status
        })
