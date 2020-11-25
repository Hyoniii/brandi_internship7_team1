### OS ####
### FLASK ###
from flask import request, Blueprint
### USER ###

def route_product(product_service) :
    product_bp = Blueprint('product', __name__, url_prefix='/product')

    @product_bp.route('/product_info', methods=['get'])
    def get_product():
        return 'account'

"""
TO CREATE A ROUTE
@product_bp.route('/info', methods=['POST'] >>>> localhost:5000/product/order will be your route)
def get_info():
    try:
"""