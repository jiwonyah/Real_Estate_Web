from flask import Blueprint, render_template, g, jsonify
from csit314.entity.PropertyListing import PropertyListing
from csit314.entity.UserAccount import UserAccount    #, Role
from csit314.controller.role_service.decorators import login_required, buyer_only, suspended

class BuyerViewOldPropertyListingController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/oldPropertyListing", view_func=self.view_old_property_listings_index, methods=['GET'])
        self.add_url_rule("/api/oldPropertyListing", view_func=self.view_old_property_listings, methods=['GET'])

    @login_required
    @buyer_only
    @suspended
    def view_old_property_listings_index(self):
        return render_template('old_property_listing/oldPropertyListingTable.html')

    @login_required
    @buyer_only
    @suspended
    def view_old_property_listings(self):
        old_property_listings = PropertyListing.displayAllSoldPropertyListing()
        old_property_listing_data = [
            {
                'subject': listing.subject,
                'create_date': listing.create_date.strftime('%Y-%m-%d'),
                'agent_id': listing.agent_id,
                'is_sold': listing.is_sold,
                'id': listing.id,
                'address': listing.address,
                'price': listing.price,
                'propertyType': listing.propertyType.value,
                'modify_date': listing.modify_date.strftime('%Y-%m-%d') if listing.modify_date else None
            } for listing in old_property_listings
        ]
        return jsonify(old_property_listings=old_property_listing_data)



