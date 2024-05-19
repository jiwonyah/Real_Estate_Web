from flask import request, jsonify, Blueprint
from csit314.entity.PropertyListing import PropertyListing
from csit314.controller.role_service.decorators import suspended
from csit314.controller.role_service.decorators import login_required, agent_only, buyer_only


class SearchPropertyListingController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/search_property_listings/", view_func=self.search_property_listings, methods=['GET'])

    @suspended
    def search_property_listings(self):
        search_query = request.args.get('query')
        if not search_query:
            return jsonify([])
        property_listings = PropertyListing.search(search_query)
        result = []
        for listing in property_listings:
            result.append({
                'id': listing.id,
                'subject': listing.subject,
                'create_date': listing.create_date.strftime('%Y-%m-%d')
            })
        return jsonify(result)


