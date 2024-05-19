from flask import Blueprint, render_template, g, jsonify
from csit314.entity.Review import Review
from csit314.entity.UserAccount import UserAccount
from csit314.controller.role_service.decorators import login_required, agent_only, suspended

class AgentViewReviewController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/agent/reviews/", view_func=self.agentViewReviews_index, methods=['GET'])
        self.add_url_rule("/api/agent/reviews/", view_func=self.agentViewReviews, methods=['GET'])
        self.add_url_rule("/agent/reviewDetail/<int:review_id>", view_func=self.review_detail_index, methods=['GET'])
        self.add_url_rule("/api/agent/reviewDetail/<int:review_id>", view_func=self.review_detail, methods=['GET'])

    @login_required
    @agent_only
    @suspended
    def agentViewReviews_index(self):
        return render_template('review/viewReviewList.html')

    @login_required
    @agent_only
    @suspended
    def agentViewReviews(self):
        reviews = Review.displayReviewsList()
        review_data = []
        for review in reviews:
            user = UserAccount.query.filter_by(userid=review.author_userid).first()
            review_data.append({
                'id': review.id,
                'author_name': f"{user.firstName} {user.lastName}",
                'create_date': review.create_date.strftime('%a, %d %b %Y'),
                'rating': review.rating,
                'content': review.content
            })
        return jsonify(reviews=review_data)

    @login_required
    @agent_only
    @suspended
    def review_detail_index(self, review_id):
        review = Review.query.filter_by(id=review_id).first()
        return render_template('review/reviewDetailPage.html', review=review)

    @login_required
    @agent_only
    @suspended
    def review_detail(self, review_id):
        review = Review.displayReviewDetails(review_id)
        if not review:
            return jsonify({'error': 'The review ID doesn\'t exist'}), 404
        if g.user.id != review.agent_id:
            return jsonify({'error': 'You do not have permission to access the review detail page.'}), 404

        user = UserAccount.query.filter_by(userid=review.author_userid).first()
        return jsonify({
            'id': review.id,
            'author_name': f"{user.firstName} {user.lastName}",
            'create_date': review.create_date.strftime('%a, %d %b %Y %H:%M:%S GMT'),
            'rating': review.rating,
            'content': review.content
        })