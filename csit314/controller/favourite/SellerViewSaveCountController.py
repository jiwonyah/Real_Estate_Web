from flask import Blueprint
from sqlalchemy import func
from csit314.app import db
from csit314.entity.Favourite import Favourite
from csit314.entity.PropertyListing import PropertyListing

bp = Blueprint('view_save_count_controller', __name__, template_folder='boundary/templates')

def update_shortlist_count():
    # Calculate the number of favorites per propertyListing_id in the Favourite model
    shortlist_counts = db.session.query(
        Favourite.propertyListing_id,
        func.count(Favourite.id).label('count')
    ).group_by(Favourite.propertyListing_id).all()

    # Update the shortlist_count field in the PropertyListing model accordingly
    for property_id, count in shortlist_counts:
        property_listing = PropertyListing.query.get(property_id)
        property_listing.shortlist_count = count
        db.session.add(property_listing)
    db.session.commit()
