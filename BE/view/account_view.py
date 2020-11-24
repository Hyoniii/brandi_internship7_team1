### OS ####
### FLASK ###
from flask import request, Blueprint
### USER ###

def route_account(account_service) :
    account_bp = Blueprint('account_bp', __name__, url_prefix='/account')

"""
TO CREATE A ROUTE
@account_bp.route('/login', methods=['POST'] >>>> localhost:5000/account/login will be your route)
def get_info():
    try:
"""