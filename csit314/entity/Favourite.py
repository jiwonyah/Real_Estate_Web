from csit314.app import db
from flask import g, current_app
from datetime import datetime
from sqlalchemy import desc


class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_userid = db.Column(db.String(32), db.ForeignKey('user.userid', ondelete='CASCADE'), nullable=False)
    propertyListing_id = db.Column(db.Integer, db.ForeignKey('propertyListing.id', ondelete='CASCADE'), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    # Add relationship with PropertyListing model
    propertyListing = db.relationship('PropertyListing', back_populates='favourites') # backref=db.backref('favourites')

    @classmethod
    def displayShortlist(cls): # Shortlist is favourite list
        # View created_date favorites that match the userid of the current user in descending order
        return cls.query.filter_by(user_userid=g.user.userid).order_by(desc(Favourite.create_date)).all()

    @classmethod
    def createPropertyShortlist(cls, propertyListing_id: str, user_userid: str) -> bool:

        user_id = g.user.userid
        # Initialize new shortlist
        new_favourite = Favourite(user_userid=user_id, propertyListing_id=propertyListing_id,
                                  create_date=datetime.now())
        # Commit to DB
        with current_app.app_context():
            db.session.add(new_favourite)
            db.session.commit()
        return True
    @classmethod
    def removeShortlist(cls, propertyListing_id: str, user_userid: str) -> bool:
        user_id = g.user.userid

        favourite = Favourite.query.filter_by(user_userid=user_id, propertyListing_id=propertyListing_id).first()

        if favourite:
            # Delete from shortlist
            db.session.delete(favourite)
            db.session.commit()
            return True
