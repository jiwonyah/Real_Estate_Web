from csit314.entity.PropertyListing import PropertyListing
from csit314.app import db
from csit314.controller.role_service.decorators import login_required, agent_only, seller_only
from flask import Blueprint, render_template, g, request
from csit314.controller.role_service.decorators import suspended
import json

class ViewPropertyListingController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/propertyListing/", view_func=self.index, methods=['GET'])
        self.add_url_rule("/propertyListing/detail/<int:propertyListing_id>/", view_func=self.detail, methods=['GET'])
        self.add_url_rule("/agent/my_property_listing/", view_func=self.agentViewPropertyListingHistory, methods=['GET'])
        self.add_url_rule("/seller/my_property_listing/", view_func=self.sellerViewOwnPropertyListing, methods=['GET'])

    @suspended
    def index(self):
        propertyListing_table = PropertyListing.displayAllNotSoldPropertyListing()
        return render_template('property_listing/propertyListingTable.html',
                               propertyListing_table=propertyListing_table)

    @suspended
    def detail(self, propertyListing_id):
        propertyListing = PropertyListing.getPropertyListing(propertyListing_id)
        images = json.loads(propertyListing.images) if propertyListing.images else []
        if g.user:
            if g.user.status == "Suspended":
                return render_template('error/error.html',
                                       message='Your account is suspended.'
                                               'Send Active Request to Administrator.'
                                               'admin@minyong.com'), 403
        else:
            if propertyListing.is_sold:
                return render_template('error/error.html',
                                       message='Login required'), 401
        propertyListing.view_counts += 1
        db.session.commit()
        return render_template('property_listing/propertyListingDetailPage.html',
                               propertyListing=propertyListing,
                               images=images)



    @login_required
    @agent_only
    @suspended
    def agentViewPropertyListingHistory(self):
        agent_id = g.user.id
        agent_listings = PropertyListing.query.filter_by(agent_id=agent_id).all()
        return render_template('property_listing/private_page/AgentPropertyListingHistoryPage.html',
                               agent_listings=agent_listings)

    @seller_only
    @suspended
    def sellerViewOwnPropertyListing(self):
        client_id = g.user.userid
        sort_by = request.args.get('sort_by', 'recent')
        if sort_by == 'most_viewed':
            propertylistings = PropertyListing.sortByMostView(client_id)
        elif sort_by == 'most_favourited':
            propertylistings = PropertyListing.sortByMostFavourite(client_id)
        else:
            propertylistings = PropertyListing.sortByRecent(client_id)
        return render_template('property_listing/private_page/SellerPropertyListingPage.html',
                               propertylistings=propertylistings, sort_by=sort_by)  # 여기 sort_by=sort_by 추가






