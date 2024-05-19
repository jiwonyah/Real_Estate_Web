from csit314.app import db
from flask import g
from datetime import datetime

class Review(db.Model):
    __tablename__ = 'review'

    id = db.Column(db.Integer, primary_key=True)
    author_userid = db.Column(db.String(50), db.ForeignKey('user.userid', ondelete='CASCADE'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    create_date = db.Column(db.DateTime(), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

    @classmethod
    def displayReviewsList(cls):
        return cls.query.filter_by(agent_id=g.user.id).all()

    @classmethod
    def createReview(cls, details: dict, agent_id: int) -> bool:
        # Log the details received
        print(f"Creating review with details: {details}")

        new_review = Review(rating=details.get('rating'),
                            content=details.get('content'),
                            create_date=datetime.now(),
                            author_userid=details.get('author_userid'),
                            agent_id=agent_id)

        db.session.add(new_review)
        try:
            db.session.commit()
            print("Review committed successfully.")
            return True
        except Exception as e:
            db.session.rollback()
            print(f"Error committing review: {e}")
            return False

    @classmethod
    def displayReviewDetails(cls, review_id: int):
        return cls.query.filter_by(id=review_id).first()
