### OS ####
### FLASK ###
from flask import request, Blueprint
### USER ###

def route_account(account_service):
    account_bp = Blueprint('account', __name__, url_prefix='/account')

    @account_bp.route('/login', methods=['GET'])
    def get_account():
        return 'account'
