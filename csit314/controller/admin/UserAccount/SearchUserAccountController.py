from flask import Blueprint, render_template, request, jsonify
from csit314.entity.UserAccount import UserAccount
from csit314.controller.role_service.decorators import login_required, admin_only

class SearchUserAccountController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/search_user_account", view_func=self.search_page, methods=['GET'])
        self.add_url_rule("/search_account", view_func=self.search_account, methods=['GET'])

    #displaying the search account page
    @login_required
    @admin_only
    def search_page(self):
        return render_template("UserAccount/SearchUserAccountPage.html")

    @login_required
    @admin_only
    def search_account(self):
        searchQuery = request.args.get('search')
        accounts = UserAccount.search_account(searchQuery)
        if accounts:
            return jsonify({'accounts': accounts})
        else:
            return jsonify({'error': "No accounts found"})
