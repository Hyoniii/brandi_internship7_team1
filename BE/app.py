from flask      import Flask, jsonify
from flask_cors import CORS
from flask.json import JSONEncoder
from decimal    import Decimal
from datetime   import timedelta, datetime, time

### USER ###
from model import ProductDao
from service import ProductService
from view import ProductView

class Services:
    pass

class CustomJSONEncoder(JSONEncoder):
    """
        default JSONEncoder 에 필요한 자료형 추가
    """
    def default(self, obj):
        """
               Args:
                   obj: json 형태로 반환하고자 하는 객체
               Returns: obj 를 json 형태로 변경하는 기능이 추가된 JSONEncoder
               Authors:
                 박현희
               History:
                   2020-11-25 : 초기 생성
               """
        if isinstance(obj, Decimal): #tuple 반환 방지
            return float(obj)
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        if isinstance(obj, datetime.datetime):  #datetime.datetime -> str
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        return JSONEncoder.default(self, obj)

def create_app(test_config=None):
    """
        Returns:
            생성된 플라스크 앱 객체
        Authors:
            박현희
        History:
            2020-11-25 : 초기 생성, blueprint
        """
    app = Flask(__name__)
    app.json_encoder = CustomJSONEncoder
    CORS(app, resources={r'*': {'origins':'*'}})

    if test_config is None:
        app.config.from_pyfile('config.py')
    else:
        app.config.update(test_config)

    ### Model/Persistence Layer ###
    #account_dao = AccountDao()
    #order_dao   = OrderDao()
    product_dao  = ProductDao()

    ### Service/Business Layer ###
    #account_service = AccountService(account_dao, app.config)
    #order_service   = OrderService(order_dao, app.config)
    services = Services
    services.product_service = ProductService(product_dao)

    ### View/Presentation Layer ###
    #app.register_blueprint(route_account(account_service))
    #app.register_blueprint(route_order(order_service))
    #ProductView.create_endpoint(app, services)
    app.register_blueprint(ProductView.product_app)


    return app
