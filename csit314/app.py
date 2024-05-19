from flask import Flask, render_template
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config
from sqlalchemy import MetaData
from csit314.controller.role_service.decorators import suspended


naming_convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(column_0_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}
db = SQLAlchemy(metadata=MetaData(naming_convention=naming_convention))
migrate = Migrate()

def create_app():
    app = Flask(__name__,
                static_folder='boundary/static',
                template_folder='boundary/templates')
    app.config['UPLOAD_FOLDER'] = 'csit314/boundary/static/images/property_listings/'
    app.config.from_object(config)
    app.config['SECRET_KEY'] = '1q2w3e4r!'
    app.config['JWT_SECRET_KEY'] = 'csit314'

    # Load app configuration from config.py
    app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = config.SQLALCHEMY_TRACK_MODIFICATIONS

    # ORM
    db.init_app(app)
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith("sqlite"):
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

    # Blueprint
    from csit314.controller.additional.profile import ViewProfileController
    from csit314.controller.favourite import (SaveFavouriteController, ViewSavedFavouriteController)
    app.register_blueprint(ViewProfileController.bp)

    app.register_blueprint(SaveFavouriteController.bp)
    app.register_blueprint(ViewSavedFavouriteController.bp)


#-----------------------------------------------------------------------------------
    # Blueprint
    from csit314.controller.authentication import (login_controller, logout_controller,
                                                   signup_controller)
    from csit314.controller.propertyListing import (agent_create_property_listing_controller,
                                                    agent_edit_property_listing_controller,
                                                    agent_remove_property_listing_controller,
                                                    view_property_listing_controller,
                                                    buyer_view_old_property_listing_controller,
                                                    search_property_listing_controller)
    from csit314.controller.admin.UserAccount import (create_account_controller, update_account_controller,
                                                      view_account_controller, search_account_controller,
                                                      suspend_account_controller, AccountDashboardController)
    from csit314.controller.admin.UserProfile import (create_profile_controller, update_profile_controller,
                                                      view_profile_controller, search_profile_controller,
                                                      suspend_profile_controller, ProfileDashboardController)
    from csit314.controller.review import (agent_view_review_controller)

    from csit314.controller.mortgage import buyer_calculate_mortgage_controller

    #authentication
    app.register_blueprint(login_controller)
    app.register_blueprint(logout_controller)
    app.register_blueprint(signup_controller)

    #Property Listing
    app.register_blueprint(agent_create_property_listing_controller)
    app.register_blueprint(agent_edit_property_listing_controller)
    app.register_blueprint(agent_remove_property_listing_controller)
    app.register_blueprint(view_property_listing_controller)
    app.register_blueprint(buyer_view_old_property_listing_controller)
    app.register_blueprint(search_property_listing_controller)

    #Review
    app.register_blueprint(agent_view_review_controller)
    #app.register_blueprint(buyer_seller_write_review_controller)

    #Admin Home
    from csit314.controller.admin.UserAccount import AdminHomePageController
    app.register_blueprint(AdminHomePageController.bp)

    #UserAccount
    app.register_blueprint(AccountDashboardController.bp)
    app.register_blueprint(create_account_controller)
    app.register_blueprint(view_account_controller)
    app.register_blueprint(update_account_controller)
    app.register_blueprint(search_account_controller)
    app.register_blueprint(suspend_account_controller)

    #UserProfile
    app.register_blueprint(ProfileDashboardController.bp)
    app.register_blueprint(create_profile_controller)
    app.register_blueprint(view_profile_controller)
    app.register_blueprint(update_profile_controller)
    app.register_blueprint(search_profile_controller)
    app.register_blueprint(suspend_profile_controller)

    # Mortgage
    app.register_blueprint(buyer_calculate_mortgage_controller)



    from csit314.controller.review import BuyerSellerWriteReviewController
    app.register_blueprint(BuyerSellerWriteReviewController.bp)
    #Main Home Page
    @suspended
    @app.route('/')
    def index():
        return render_template('index.html')

    return app



