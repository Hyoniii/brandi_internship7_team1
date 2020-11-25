from flask import request, Blueprint,jsonify
from service.product_service import ProductService
from db_connector import connect_db

class ProductView:

    #def create_endpoint(app, services):
    #    product_service = services.product_service

    product_app = Blueprint('product_app', __name__, url_prefix='/product')
    #
    # def __init__(self,app, product_service):
    #     self.app = app
    #     self.product_service = product_service

    @product_app.route('/info', methods=['GET'])
    def get_product():
        conn = None
        try:
            products = product_service.get_product(conn)
        except Exception as e:
            return jsonify({'message' : 'error' }), 400
        else:
            return jsonify(products), 200
            # return jsonify({'access_token' : 'success'}), 200

"""
TO CREATE A ROUTE
@product_bp.route('/info', methods=['POST'] >>>> localhost:5000/product/order will be your route)
def get_info():
    try:
"""