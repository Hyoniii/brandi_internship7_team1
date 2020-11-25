### OS ####
### FLASK ###
from flask import request, Blueprint
### USER ###

def route_order(order_service) :
    order_bp = Blueprint('order', __name__, url_prefix='/order')

    @order_bp.route('/order_info', methods=['get'])
    def get_order():
        return 'account'

"""
TO CREATE A ROUTE
@order_bp.route('/cart', methods=['POST'] >>>> localhost:5000/order/cart will be your route)
def get_info():
    try:
"""