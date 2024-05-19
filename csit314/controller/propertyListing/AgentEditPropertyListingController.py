import json

from flask import Blueprint, render_template, request, g, jsonify
from .Form.PropertyListingForm import PropertyListingForm
from csit314.controller.role_service.decorators import login_required, agent_only, suspended
from datetime import datetime
from csit314.entity.PropertyListing import PropertyListing

class AgentEditPropertyListingController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule('/propertyListing/edit/<propertyListing_id>/', view_func=self.index, methods=['GET'])
        self.add_url_rule('/propertyListing/edit/<propertyListing_id>/', view_func=self.editPropertyListing, methods=['POST'])

    @login_required
    @agent_only
    @suspended
    def index(self, propertyListing_id):
        propertyListing = PropertyListing.getPropertyListing(propertyListing_id)
        images = json.loads(propertyListing.images) if propertyListing.images else []
        if g.user != propertyListing.agent:
            return render_template('error/error.html',
                                   message='You don\'t have authority to edit the post.'), 403
        else:
            form = PropertyListingForm(obj=propertyListing)
            return render_template('property_listing/propertyListingEditForm.html', form=form, images=images
                                   ,propertyListing=propertyListing)

    @login_required
    @agent_only
    @suspended
    def editPropertyListing(self, propertyListing_id):
        propertyListing = PropertyListing.getPropertyListing(propertyListing_id)
        if not propertyListing:
            return jsonify({'success': False, 'error': 'Property listing not found'}), 404
        is_sold = request.form['is_sold'] == 'true'
        client_id = request.form['client_id']
        form = PropertyListingForm(request.form)
        details = {
            'id': propertyListing_id,
            'subject': request.form['subject'],
            'content': request.form['content'],
            'price': request.form['price'],
            'address': request.form['address'],
            'floorSize': request.form['floorSize'],
            'floorLevel': request.form['floorLevel'],
            'propertyType': request.form['propertyType'],
            'furnishing': request.form['furnishing'],
            'builtYear': request.form['builtYear'],
            'client_id': client_id,
            'is_sold': is_sold,
            'files': request.files.getlist('images')
        }
        success = PropertyListing.editPropertyListing(propertyListing.id, details)
        if success:
            return jsonify({'success': True, 'message': 'Property listing updated successfully.'})
        elif not PropertyListing.validate_client_id(client_id):
            return jsonify({'success': False, 'error': 'Client ID is not validate.'})
        else:
            return jsonify({'success': False, 'error': 'Failed to edit Property Listing.'})






