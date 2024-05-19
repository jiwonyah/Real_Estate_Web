import enum
from csit314.app import db
from csit314.entity.UserAccount import UserAccount
from flask import current_app, request
from datetime import datetime
from werkzeug.utils import secure_filename
import os
import json

class FloorLevel(enum.Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'

class PropertyType(enum.Enum):
    HDB = 'hdb'
    CONDO = 'condo'
    APARTMENT = 'apartment'
    STUDIO = 'studio'

class Furnishing(enum.Enum):
    PartiallyFurnished = 'partially_furnished'
    FullyFurnished = 'fully_furnished'
    NotFurnished = 'not_furnished'

class PropertyListing(db.Model):
    __tablename__ = 'propertyListing'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    images = db.Column(db.Text, nullable=True)
    content = db.Column(db.Text(), nullable=True)
    price = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(200), nullable=False)
    floorSize = db.Column(db.Integer, nullable=False)
    floorLevel = db.Column(db.Enum(FloorLevel, values_callable=lambda x: [str(member.value) for member in FloorLevel]), nullable=False)
    propertyType = db.Column(db.Enum(PropertyType, values_callable=lambda x: [str(member.value) for member in PropertyType]), nullable=False)
    furnishing = db.Column(db.Enum(Furnishing, values_callable=lambda x: [str(member.value) for member in Furnishing]), nullable=False)
    builtYear = db.Column(db.Integer, nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    modify_date = db.Column(db.DateTime(), nullable=True)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    agent = db.relationship('UserAccount', foreign_keys=[agent_id], backref=db.backref('property_listing_set'))
    client_id = db.Column(db.String, db.ForeignKey('user.userid', ondelete='CASCADE'), nullable=False)
    client = db.relationship('UserAccount', foreign_keys=[client_id], backref=db.backref('client_property_listings'))
    view_counts = db.Column(db.Integer, default=0, nullable=False)
    favourites = db.relationship('Favourite', back_populates='propertyListing', lazy='dynamic')
    is_sold = db.Column(db.Boolean(), default=False)
    shortlist_count = db.Column(db.Integer, default=0)

    @classmethod
    def validate_client_id(self, client_id) -> bool:
        # Check if the userid exists in the User table
        user_with_client_id = UserAccount.query.filter_by(userid=client_id).first()
        seller_user = UserAccount.query.filter_by(userid=client_id, role='seller').first() #role=Role.SELLER
        if not user_with_client_id:
            return False
        elif not seller_user:
            return False

        return True

    @classmethod
    def displayAllPropertyListing(cls):
        property_listings = PropertyListing.query.order_by(PropertyListing.create_date.desc()).all()
        return property_listings

    @classmethod
    def createPropertyListing(cls, details: dict) -> bool:
        try:
            subject = details.get('subject')
            content = details.get('content')
            price = details.get('price')
            address = details.get('address')
            floorSize = details.get('floorSize')
            floorLevel = details.get('floorLevel')
            propertyType = details.get('propertyType')
            furnishing = details.get('furnishing')
            builtYear = details.get('builtYear')
            client_id = details.get('client_id')
            agent_id = details.get('agent_id')
            files = details.get('files', [])

            print("Details received:")
            print(details)

            image_paths = []
            upload_folder = current_app.config['UPLOAD_FOLDER']
            print("Upload folder:", upload_folder)

            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
                print(f"Created upload folder: {upload_folder}")

            for file in files:
                print("Processing file:", file)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    filepath = os.path.join(upload_folder, filename)
                    print("Saving file to:", filepath)
                    file.save(filepath)
                    if os.path.exists(filepath):
                        print(f"File saved successfully: {filepath}")
                    else:
                        print(f"Failed to save file: {filepath}")
                    image_paths.append(filename)

            print("Image paths:", image_paths)

            property_listing = cls(
                subject=subject,
                content=content,
                price=price,
                address=address,
                floorSize=floorSize,
                floorLevel=floorLevel,
                propertyType=propertyType,
                furnishing=furnishing,
                builtYear=builtYear,
                client_id=client_id,
                agent_id=agent_id,
                images=json.dumps(image_paths),
                create_date=datetime.now()
            )
            print("Property listing created:", property_listing)
            db.session.add(property_listing)
            db.session.commit()
            return True

        except Exception as e:
            print("Exception occurred:", e)
            db.session.rollback()
            return False

    @classmethod
    def editPropertyListing(cls, propertyListing_id, details: dict) -> bool:
        listing = cls.getPropertyListing(propertyListing_id)
        if not listing:
            return False

        client_id = details.get('client_id')
        if not cls.validate_client_id(client_id):
            return False

        listing.subject = details.get('subject', listing.subject)
        listing.content = details.get('content', listing.content)
        listing.price = details.get('price', listing.price)
        listing.address = details.get('address', listing.address)
        listing.floorSize = details.get('floorSize', listing.floorSize)
        listing.floorLevel = details.get('floorLevel', listing.floorLevel)
        listing.propertyType = details.get('propertyType', listing.propertyType)
        listing.furnishing = details.get('furnishing', listing.furnishing)
        listing.builtYear = details.get('builtYear', listing.builtYear)
        listing.modify_date = datetime.now()

        if 'modify_date' in details:
            listing.modify_date = datetime.now()
        if 'client_id' in details:
            listing.client_id = details['client_id']
        if 'is_sold' in details:
            listing.is_sold = details['is_sold']

        existing_images = request.form.getlist('existing_images')
        files = details.get('files', [])
        upload_folder = current_app.config['UPLOAD_FOLDER']
        image_paths = existing_images

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(upload_folder, filename)
                file.save(filepath)
                image_paths.append(filename)

        listing.images = json.dumps(image_paths)

        db.session.commit()
        return True

    @classmethod
    def getPropertyListing(cls, listing_id: int):
        return cls.query.filter_by(id=listing_id).one_or_none()

    @classmethod
    def removePropertyListing(cls, listing_id: int) -> bool:
        property_listing = cls.getPropertyListing(listing_id)
        db.session.delete(property_listing)
        db.session.commit()
        return True

    @classmethod
    def displayAllSoldPropertyListing(cls):
        return cls.query.filter_by(is_sold=True).order_by(cls.create_date.desc()).all()

    @classmethod
    def displayAllNotSoldPropertyListing(cls):
        return cls.query.filter_by(is_sold=False).order_by(cls.create_date.desc()).all()

    @classmethod
    def search(cls, search_query):
        return cls.query.filter(cls.subject.ilike(f'%{search_query}%')).all()

    @classmethod
    def sortByMostView(cls, client_id: int):
        return cls.query.filter_by(client_id=client_id).order_by(
            PropertyListing.view_counts.desc()).all()

    @classmethod
    def sortByMostFavourite(cls, client_id: int):
        return cls.query.filter_by(client_id=client_id).order_by(
            PropertyListing.shortlist_count.desc()).all()

    @classmethod
    def sortByRecent(cls, client_id: int):
        return cls.query.filter_by(client_id=client_id).order_by(
            PropertyListing.create_date.desc()).all()




def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}




