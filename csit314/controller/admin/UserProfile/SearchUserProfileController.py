from flask import Blueprint, render_template, request, jsonify
from csit314.controller.role_service.decorators import login_required, admin_only
from csit314.entity.UserProfile import UserProfile


class SearchUserProfileController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule('/search_user_profile', view_func=self.search_page, methods=['GET'])
        self.add_url_rule('/search_profile', view_func=self.search_profile, methods=['GET'])

    @login_required
    @admin_only
    def search_page(self):
        return render_template("UserProfile/SearchUserProfilePage.html")

    @login_required
    @admin_only
    def search_profile(self):
        searchQuery = request.args.get('search')
        profiles = UserProfile.search_profile(searchQuery)
        if profiles:
            return jsonify({'profiles': profiles})
        else:
            return jsonify({'error': "No profiles found"})