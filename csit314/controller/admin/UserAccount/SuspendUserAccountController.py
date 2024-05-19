from flask import Blueprint, render_template, request, jsonify, g
from csit314.entity.UserAccount import UserAccount
from csit314.controller.role_service.decorators import login_required, admin_only

class SuspendUserAccountController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/suspend_user_account", view_func=self.display_suspend_form, methods=['GET'])
        self.add_url_rule("/suspend_account", view_func=self.suspend_account, methods=['POST'])

    @login_required
    @admin_only
    def display_suspend_form(self):
        return render_template('UserAccount/SuspendUserAccountPage.html')

    @login_required
    @admin_only
    def suspend_account(self):
        userid = request.form['userid']
        if UserAccount.getUserDetails(userid) is None:
            return jsonify({'success': False, 'message': 'Username does not exist'})
        results = UserAccount.suspend_account(userid)
        if results:
            return jsonify({'success': True, 'message': 'User Account suspended successfully'})
        elif UserAccount.getUserDetails(userid) == g.user.userid:
            return jsonify({'success': False, 'message': 'You can\'t suspend yourself.'})
        else:
            return jsonify({'success': False, 'message': 'User Account already suspended'})