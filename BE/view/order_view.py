### OS ####
### FLASK ###
from flask import request, Blueprint
### USER ###

def route_order(order_service) :
    order_bp = Blueprint('order_bp', __name__, url_prefix='/order')

"""
TO CREATE A ROUTE
@order_bp.route('/cart', methods=['POST'] >>>> localhost:5000/order/cart will be your route)
def get_info():
    try:
"""