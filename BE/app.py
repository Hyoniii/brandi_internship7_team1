### OS ###
import datetime
import decimal
import re
import arrow
import json
### FLASK ###
from flask                              import Flask, jsonify
from flask_mysqldb                      import MySQL
from flask_cors                         import CORS
from flask_request_validator.exceptions import InvalidRequest
from flask.json                         import JSONEncoder
from contextlib                         import suppress
### USER ###

app = Flask(__name__)
def create_app(test_config=None):

    CORS(app, resources={r'*': {'origins':'*'}})

    @app.errorhandler(Exception)
    def identify_invalid_usage(error):
        if isinstance(error, InvalidRequest) :
            return {'message': str(error)}, 400
        else:
            response             = jsonify(error)
            response.status_code = error.status_code
            return response


    class JSONEncoder(json.JSONEncoder):
        """
        Custom encoder for date format and decimal-string>>>float
        """
        def default(self,obj):
            if isinstance(obj, datetime):
                return arrow.get(obj).local.format('YYYY-MM-DD HH:mm:ss ZZ')
            elif isinstance(obj, decimal.Decimal):
                return float(obj)#####FLOAT? DECIMAL
            return json.JSONEncoder.default(self, obj)

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)

    ### Model/Persistence Layer ###
    account_dao = AccountDao()
    order_dao   = OrderDao()
    productDao  = ProductDao()

    ### Service/Business Layer ###
    account_service = AccountService(account_dao, app.config)
    order_service   = OrderService(order_dao, app.config)
    product_service = ProductService(product_dao, app.config)

    ### View/Presentation Layer ###
    app.register_blueprint(route_account) #app.register_blueprint(route_account(account_service)) 이거 써야될지도!
    app.register_blueprint(route_order) #app.register_blueprint(route_order(order_service)) 이거 써야될지도!
    app.register_blueprint(route_product) #app.register_blueprint(route_product(product_service)) 이거 써야될지도!


    return app
