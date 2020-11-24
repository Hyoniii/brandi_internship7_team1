# ### OS ####
# ### FLASK ###
# from flask import request, Blueprint
# ### USER ###

# def route_account(account_service):
#     print('1')
#     account_bp = Blueprint('account_bp', __name__, url_prefix='/account')
#     print(account_bp)
#     @account_bp.route('/login', methods=['GET'])
#     def get_account():
#         return account_service.thou()

from flask                      import (
    Blueprint,
    request,
    jsonify
)
from flask_request_validator    import (
    GET,
    PATH,
    Param,
    JSON,
    validate_params
)

from connection import get_connection
from utils      import DatetimeRule, catch_exception, login_required

def create_admin_order_endpoints(order_service):
    admin_order_app = Blueprint('admin_order_app', __name__, url_prefix='/admin/order')

    @admin_order_app.route('/orderCompletedList', methods=['GET'], endpoint='order_list')
    @catch_exception
    @validate_params(
        Param('fromDate', GET, int, required=False, rules=[DatetimeRule()]),
        Param('page', GET, int),
        Param('limit', GET, int),
        Param('sort', GET, bool, default=False, required=False),
        Param('orderId', GET, int, required=False),
        Param('orderDetailId', GET, int, required=False),
        Param('orderer', GET, str, required=False),
        Param('phoneNumber', GET, str, required=False),
        Param('productName', GET, str, required=False),
        Param('toDate', GET, int, required=False, rules=[DatetimeRule()])
    )
    def order_list(*args):

        db_connection = None

        try:

            # db 연결
            db_connection = get_connection()

            # request의 filter 정보 저장
            filter_info = {
                'from_date'         : args[0],
                'page'              : args[1],
                'limit'             : args[2],
                # 정렬 조건 존재하는경우 : 주문일 오래된 순
                'sort'              : args[3],
                'order_id'          : args[4],
                'order_detail_id'   : args[5],
                'orderer'           : args[6],
                'phone_number'      : args[7],
                'product_name'      : args[8],
                'to_date'           : args[9]
            }

            if db_connection:

                # filter 유효성 검사
                filters = order_service.check_filter_list(filter_info)

                if filters:

                    # filter 조건 정보에 해당하는 총 결제 완료 건수 조회
                    count = order_service.get_total_number(filters, db_connection)

                    if count:

                        # filter 정보를 전달하여 결제 완료 리스트 가져와서 result에 저장
                        result = order_service.get_order_list(filters, db_connection)

                        if result:

                            # 총 갯수와 result return
                            return jsonify({"total_number" : count['total_number'], "data" : result}), 200

                        # page에 해당하는 data 없을 시
                        return jsonify({"total_number" : count['total_number'], "data" : []}),200

                    # 존재하는 데이터 없음
                    return jsonify({"total_number" : 0, "data" : []}), 200

                # filter 조건 불충족
                return jsonify({"message" : "INVALID_FILTER"}), 401

            # db 연결이 없을 시
            return jsonify({"message" : "NO_DATABASE_CONNECTION"}), 500

        except ValueError as e:
            return jsonify({"message" : f"VALUE_ERROR_AS_{e}"}), 400

        #정의하지 않은 모든 error를 잡아줌
        except Exception as e:
            return jsonify({"message" : f'{e}'}), 400

        finally:
            if db_connection:
                db_connection.close()