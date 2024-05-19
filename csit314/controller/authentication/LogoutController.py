from flask import Blueprint, session, jsonify, g
from csit314.entity.UserAccount import UserAccount

class LogoutController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/logout/", view_func=self.logout, methods=['POST'])

    def logout(self):
        if not g.user:
            return jsonify({'success': False, 'message': 'You are already anonymous.'})
        userid = g.user.userid
        userKey = UserAccount.getKey(userid)
        session.pop(userKey, None)
        session.clear()
        return jsonify({'success': True, 'message': 'Logout successful'})





