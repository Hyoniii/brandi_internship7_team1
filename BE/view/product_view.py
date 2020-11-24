### OS ####
### FLASK ###
from flask import request, Blueprint
### USER ###

def route_product(product_service) :
    product_bp = Blueprint('product_bp', __name__, url_prefix='/product')

"""
TO CREATE A ROUTE
@product_bp.route('/info', methods=['POST'] >>>> localhost:5000/product/order will be your route)
def get_info():
    try:
"""