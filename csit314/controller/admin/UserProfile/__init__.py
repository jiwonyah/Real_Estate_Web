from .CreateUserProfileController import CreateUserProfileController
from .SearchUserProfileController import SearchUserProfileController
from .SuspendUserProfileController import SuspendUserProfileController
from .UpdateUserProfileController import UpdateUserProfileController
from .ViewUserProfileController import ViewUserProfileController

create_profile_controller = CreateUserProfileController(name="CreateUserProfileController", import_name=__name__)
search_profile_controller = SearchUserProfileController(name="SearchUserProfileController", import_name=__name__)
suspend_profile_controller = SuspendUserProfileController(name="SuspendUserProfileController", import_name=__name__)
update_profile_controller = UpdateUserProfileController(name="UpdateUserProfileController", import_name=__name__)
view_profile_controller = ViewUserProfileController(name="ViewUserProfileController", import_name=__name__)