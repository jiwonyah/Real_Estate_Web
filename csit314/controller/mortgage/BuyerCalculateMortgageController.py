from flask import Blueprint, render_template
from csit314.controller.role_service.decorators import login_required, buyer_only, suspended

# Mortgage function only works in boundary
# The mortgage controller is for just set the link
class BuyerCalculateMortgageController(Blueprint):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_url_rule("/mortgage", view_func=self.calculateMortgage, methods=['GET'])

    @login_required
    @buyer_only
    @suspended
    def calculateMortgage(self):
        return render_template('mortgage/calculateMortgage.html')
