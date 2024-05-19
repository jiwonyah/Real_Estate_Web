from csit314.entity.UserAccount import UserAccount
from flask import Blueprint, render_template, request, jsonify
import bcrypt
from .Form.UserSignUpForm import UserSignUpForm
from csit314.controller.role_service.decorators import already_logged_in, is_logged_in

class SignUpController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/signup/", view_func=self.index, methods=['GET'])
        self.add_url_rule("/signup/", view_func=self.signUp, methods=['POST'])

    @already_logged_in
    def index(self):
        form = UserSignUpForm()
        return render_template('authentication/SignUpBoundary.html', form=form)


    @already_logged_in
    def signUp(self):
        userid = request.form['userid']
        password = request.form['password']
        password2 = request.form['password2']
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        role = request.form['role']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_details = {
            'userid': userid,
            'password': hashed_password.decode('utf-8'),
            'email': email,
            'firstName': firstName,
            'lastName': lastName,
            'role': role
        }
        if password != password2:
            return jsonify({'success': False, 'error': 'Password does not match.'})

        userid_exists = UserAccount.query.filter_by(userid=user_details["userid"]).one_or_none()
        email_exists = UserAccount.query.filter_by(email=user_details["email"]).one_or_none()
        if userid_exists:
            return jsonify({'error': 'The ID is already registered.'})
        if len(userid) < 5 or len(userid) > 25:
            return jsonify({'error': 'ID length must be 5~25.'})
        if len(password) < 8 or len(password) > 25:
            return jsonify({'error': 'Password must be 8~25.'})
        if email_exists:
            return jsonify({'error': 'The email is already registered.'})
        success = UserAccount.createNewUser(user_details)
        if success:
            return jsonify({'success': True, 'message': 'User created successfully'})
        else:
            return jsonify({'success': False, 'message': 'Failed to register new account.'})


