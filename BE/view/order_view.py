from flask import (
    request,
    Blueprint,
    jsonify
)
from flask_request_validator import (
    Param,
    PATH,
    Pattern,
    JSON,
    validate_params
)

from db_connector import connect_db
from service.order_service import OrderService
# from utils import login_required
# from exceptions import errors

class OrderView:
    order_app = Blueprint('order_app', __name__, url_prefix='/orders')

    @order_app.route('/<detailed_order_number>', methods=['GET'])
    @validate_params(
        Param('detailed_order_number', PATH, str, rules=[Pattern('^[0-9]{8,}$')], required=True)
    )
    # @login_required
    def get_order_detail(detailed_order_number):
        order_service = OrderService()

        order_filter = {
            'seller_id': g.seller_id if g.seller_id else None,
            'detailed_order_number': detailed_order_number
        }
        connection = None
        try:
            connection = connect_db()
            order_detail = order_service.get_order_detail(connection, order_filter)
            return jsonify({'order_detail': order_detail}), 200

        # 예외처리 추가
        # except 데이터 없으면:
        #    connection.rollback()
        #    return 데이터없음
        finally:
            if connection:
                connection.close()

    @order_app.route('/<order_number>', methods=['POST'])
    @validate_params(
        Param('order_number', PATH, str, rules=[Pattern('^[0-9]{8,}$')], required=True),
        Param('order_status_id', JSON, int, rules=[Pattern('^[1-5]{1}$')], required=False),
        Param('phone_number', JSON, str, rules=[Pattern('^[0-9]{10,}$')], required=False),
        Param('address_1', JSON, str, required=False),
        Param('address_2', JSON, str, required=False),
        Param('zip_code', JSON, str, required=False),
        Param('delivery_instruction', JSON, str, required=False)
    )
    # @login_required
    def update_order_detail(*args):
        order_service = OrderService()
        order_status = {
            'detailed_order_number': args[0],
            'editor_id': g.account_id,
            'order_status_id': args[1] if args[1] else None
        }
        delivery_info = {
            'detailed_order_number': args[0],
            'editor_id': g.account_id,
            'phone_number': args[2] if args[2] else None,
            'address_1': args[3] if args[3] else None,
            'zip_code': args[4] if args[4] else None,
            'delivery_instruction': args[5] if args[5] else None
        }

        connection = None
        try:
            connection = connect_db()
            order_service.update_order_detail(connection, order_status)
            updated_order_detail = order_service.get_order_detail(connection, delivery_info)
            connection.commit()
            return jsonify({"updated_order_detail": updated_order_detail}), 201
        # except 에러 발생시:
        #    connection.rollback()
        #    return 에러메세지
        finally:
            if connection:
                connection.close()

