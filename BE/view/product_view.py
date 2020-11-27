from flask                   import request, Blueprint,jsonify
from flask.views             import MethodView
from service.product_service import ProductService
from db_connector            import connect_db

class ProductView:
    product_app = Blueprint('product_app', __name__, url_prefix='/product')

    @product_app.route('', methods=['GET'])
    #@decorator(mastrer or seller)
    def get_product_list(*args):
        connection = None
        data = None

        try:
            connection = connect_db()
            data = dict(request.args)
            print(data)
            print(1)
            product_service = ProductService()
            products = product_service.get_product_list( data, connection )
        except Exception as e:
            return jsonify({'message' : f'{e}'}), 400
        else:
            return jsonify(products), 200
            #return jsonify({'access_token' : 'success'}), 200
        finally:
            connection.close()

