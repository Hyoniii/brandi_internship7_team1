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
from model   import AccountDao, OrderDao, ProductDao
from service import AccountService, OrderService, ProductService
from view    import route_account, route_order, route_product

app = Flask(__name__)
def create_app(test_config=None):

    CORS(app, resources={r'*': {'origins':'*'}})

    app.config.from_pyfile('config.py')

    ### Model/Persistence Layer ###
    account_dao = AccountDao()
    #order_dao   = OrderDao()
    #product_dao  = ProductDao()

    ### Service/Business Layer ###
    account_service = AccountService(account_dao)
    #order_service   = OrderService(order_dao)
    #product_service = ProductService(product_dao)

    ### View/Presentation Layer ###
    app.register_blueprint(route_account(account_service))
    #app.register_blueprint(route_order(order_service))
    #app.register_blueprint(route_product(product_service))


    return app

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
