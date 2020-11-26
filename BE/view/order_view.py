from flask import (
    request,
    Blueprint,
    jsonify
)
from flask_request_validator import (
    Param,
    PATH,
    Pattern,
    validate_params
)

from db_connector import connect_db
from service.order_service import OrderService
#from utils import login_required, check_account_type
#from exceptions import errors

class OrderView:
    order_app = Blueprint('orders', __name__, url_prefix='/orders')

    @order_app.route('/<order_number>', methods=('GET', 'POST'))
    @validate_params(
        Param('order_number', PATH, str, rules=[Pattern['^[0-9]{8,}$'], required = True)
    )
    #@login_required
    #@check_account_type
    def order_detail(order_number):
        if request.method == 'GET':
            order_filter = {
                'detailed_order_number': order_number
            }
            connection = connect_db()
            #추가: account type 셀러일 경우 주문과 셀러id 일치하는지 확인하고 아니면 에러메세지 리턴
            try:
                order_detail = OrderService.get_order_detail(connection, order_filter)
                return jsonify(order_detail), 200

            #예외처리 추가
            #except 데이터 없으면:
            #    connection.rollback()
            #    return 데이터없음

            finally:
                connection.close()

        if request.method == 'POST':
            order_filter = {
                'detailed_order_number': order_number
            }
            data = request.json
            #account_id = 로그인 데코레이터에서 받아오기
            order_update = {
                #    "editor_id": account_id
            }
            if data['phone_number']:
                order_update['phone_number'] = data['phone_number']
            if data['address_1']:
                order_update['address_1'] = data['address_1']
            if data['address_2']:
                order_update['address_2'] = data['address_2']
            if data['zip_code']:
                order_update['zip_code'] = data['zip_code']
            if data['delivery_instruction']:
                order_update['delivery_instruction'] = data['delivery_instruction']
            if data['order_status_id']:
                order_update['order_status_id'] = data['order_status_id']

            connection = connect_db()
            #추가: account type 셀러일 경우 주문과 셀러id 일치하는지 확인하고 아니면 에러메세지 리턴
            try:
                OrderService.update_order_detail(connection, order_filter, order_update)
                updated_order_detail = OrderService.get_order_detail(connection, order_filter)

                return jsonify(updated_order_detail)

            # except 에러 발생시:
            #    connection.rollback()
            #    return 에러메세지

            finally:
                connection.close()