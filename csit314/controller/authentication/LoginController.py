from flask import jsonify, Blueprint, render_template, session
from csit314.entity.UserAccount import UserAccount
from flask import request, g
import bcrypt
from .Form.UserLoginForm import UserLoginForm
from csit314.controller.role_service.decorators import already_logged_in, is_logged_in

class LoginController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/login/", view_func=self.index, methods=['GET'])
        self.add_url_rule("/login/", view_func=self.login, methods=['POST'])
        self.before_app_request(self.load_logged_in_user)
    @already_logged_in
    def index(self):
        form = UserLoginForm()
        return render_template('authentication/login.html', form=form)

    @already_logged_in
    def login(self):
        credential = request.json
        userid = credential['userid']
        password = credential['password']
        user = UserAccount.findAUserByUserID(userid=userid)  # entity method
        if user and bcrypt.checkpw(password.encode('UTF-8'), user.password.encode('UTF-8')):
            session['user_id'] = user.id
            return jsonify({'success': True, 'message': 'Login successful', 'role': user.role})
        return jsonify({'success': False, 'error': 'User information does not exist.'}), 401


    def load_logged_in_user(self):
        user_id = session.get('user_id')
        if user_id is None:
            g.user = None
        else:
            g.user = UserAccount.query.get(user_id)




