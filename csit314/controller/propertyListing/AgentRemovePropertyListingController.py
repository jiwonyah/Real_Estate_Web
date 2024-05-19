from flask import Blueprint, g, jsonify
from csit314.entity.PropertyListing import PropertyListing
from csit314.controller.role_service.decorators import login_required, admin_only, suspended

class AgentRemovePropertyListingController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/propertyListing/remove/<int:listing_id>/",
                          view_func=self.remove_property_listing, methods=['DELETE'])

    @suspended
    def remove_property_listing(self, listing_id):
        property_listing = PropertyListing.getPropertyListing(listing_id)
        if not property_listing:
            return jsonify(success=False, message='Property listing not found'), 404
        if g.user.id != property_listing.agent_id:
            return jsonify(success=False, message='You are not authorized to delete this property listing'), 403
        PropertyListing.removePropertyListing(listing_id)
        return jsonify(success=True, message='Property listing successfully removed.'), 200
