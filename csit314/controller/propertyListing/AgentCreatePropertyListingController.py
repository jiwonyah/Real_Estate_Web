from flask import Blueprint, render_template, request, jsonify, session
from csit314.entity.PropertyListing import PropertyListing
from csit314.controller.role_service.decorators import login_required, agent_only,suspended
from .Form.PropertyListingForm import PropertyListingForm


class AgentCreatePropertyListingController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/propertyListing/create/", view_func=self.index, methods=['GET'])
        self.add_url_rule("/propertyListing/create/", view_func=self.createPropertyListing, methods=['POST'])

    @login_required
    @agent_only
    @suspended
    def index(self):
        form = PropertyListingForm()
        return render_template('property_listing/propertyListingCreatingForm.html',
                               form=form)

    @login_required
    @agent_only
    @suspended
    def createPropertyListing(self):
        try:
            client_id = request.form['client_id']
            details = {
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
                'agent_id': session['user_id'],
                'files': request.files.getlist('images')
            }
            print("Files received in request:", request.files)
            print("Files received in form data:", request.files.getlist('images'))

            if not PropertyListing.validate_client_id(client_id):
                return jsonify({'success': False, 'error': 'Client ID is not valid.'}), 400

            success = PropertyListing.createPropertyListing(details)
            if success:
                return jsonify({'success': True, 'message': 'Property listing created successfully'}), 200
            else:
                return jsonify({'success': False, 'error': 'Failed to create property listing'}), 400

        except Exception as e:
            return jsonify({'success': False, 'error': str(e)})

