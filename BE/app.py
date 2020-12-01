from flask      import Flask, jsonify, g
from flask_cors import CORS
from flask.json import JSONEncoder
from decimal    import Decimal
from datetime   import datetime

from view    import ProductView, OrderView, AccountView

# g.acoount_info = {
#     'account_id':1,
#     'account_type_id':1,
#     'seller_id': None
# }

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
        if isinstance(obj, set):
            return list(obj)
        if isinstance(obj, Decimal): #tuple 반환 방지
            return float(obj)
        if isinstance(obj, bytes):
            return obj.decode("utf-8")
        if isinstance(obj, datetime):  #datetime.datetime -> str
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

    app.register_blueprint(ProductView.product_app)
    app.register_blueprint(OrderView.order_app)
    app.register_blueprint(AccountView.account_app)

    return app
