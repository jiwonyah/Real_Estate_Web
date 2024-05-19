from .CreateUserAccountController import CreateUserAccountController
from .SearchUserAccountController import SearchUserAccountController
from .SuspendUserAccountController import SuspendUserAccountController
from .UpdateUserAccountController import UpdateUserAccountController
from .ViewUserAccountController import ViewUserAccountController

create_account_controller = CreateUserAccountController(name="CreateUserAccountController", import_name=__name__)
search_account_controller = SearchUserAccountController(name="SearchUserAccountController", import_name=__name__)
suspend_account_controller = SuspendUserAccountController(name="SuspendUserAccountController", import_name=__name__)
update_account_controller = UpdateUserAccountController(name="UpdateUserAccountController", import_name=__name__)
view_account_controller = ViewUserAccountController(name="ViewUserAccountController", import_name=__name__)
