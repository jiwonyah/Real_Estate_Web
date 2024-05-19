from .LoginController import LoginController
from .LogoutController import LogoutController
from .SignUpController import SignUpController

login_controller = LoginController(name="LoginController", import_name=__name__)
logout_controller = LogoutController(name="LogoutController", import_name=__name__)
signup_controller = SignUpController(name="SignUpController", import_name=__name__)
