from flask import (
    request,
    Blueprint,
    jsonify
)
from flask_request_validator import (
    Param,
    PATH,
    GET,
    Pattern,
    JSON,
    Enum,
    validate_params
)

# from utils import login_required
# from exceptions import errors
from db_connector          import connect_db
from service.order_service import OrderService


class OrderView:

    order_app = Blueprint('order_app', __name__, url_prefix='/orders')

    @order_app.route('', methods=['GET'])
    @validate_params(
        Param('order_status_id', GET, int, required=True),
        Param('order_number', GET, str, required=False),
        Param('detailed_order_number', GET, str, required=False),
        Param('buyer_name', GET, str, required=False),
        Param('phone_number', GET, str, required=False),
        Param('seller_name', GET, str, required=False),
        Param('product_name', GET, str, required=False),
        Param('start_date', GET, str, required=False),
        Param('end_date', GET, str, required=False),
        Param('seller_type_id', GET, int, required=False),
        Param('limit', GET, int, required=False),
        Param('order_by', GET, str, rules=[Enum('desc', 'asc')], required=False),
        Param('page', GET, int, required=False)
    )
    # @login_required
    def get_order_list(*args):

        order_service = OrderService()

        #account_info = {
        #    "account_id": g.account_id,
        #    "account_type_id": g.account_type_id,
        #    "seller_id": g.seller_id if g.seller_id else None
        #}

        order_filter = {
            'order_status_id': args[0],
            'order_number': args[1],
            'detailed_order_number': args[2],
            'buyer_name': args[3],
            'phone_number': args[4],
            'seller_name': args[5],
            'product_name': args[6],
            'start_date': args[7],
            'end_date': args[8],
            'seller_type_id': args[9],
            'limit': args[10] if args[10] else 50,
            'order_by': args[11] if args[11] else 'desc',
            'page': args[12] if args[12] else 1
        }

        connection = None
        try:
            connection = connect_db()
            order_list = order_service.get_order_list(connection, order_filter)
            return jsonify({"order_list": order_list}), 200

        finally:
            if connection:
                connection.close()

    @order_app.route('', methods=['POST'])
    @validate_params(
        Param('order_item_id', JSON, list),
        Param('new_order_status', JSON, int)
    )
    #@login_required
    def update_order_status(*args):

        order_service = OrderService()
        data = request.json

        # account_info = {
        #    "account_id": g.account_id,
        #    "account_type_id": g.account_type_id,
        #    "seller_id": g.seller_id if g.seller_id else None
        # }

        order_status = {
            'order_item_id': data['order_item_id'],
            'new_order_status': data['new_order_status']
        }

        connection = connect_db()
        order_service.update_order_status(connection, order_status)

        return jsonify({"message": "status successfully updated"})

    @order_app.route('/<order_item_id>', methods=['GET'])
    @validate_params(
        Param('order_item_id', PATH, int)
    )
    # @login_required
    def get_order_detail(order_item_id):

        order_service = OrderService()

        #account_info = {
        #    "account_id": g.account_id,
        #    "account_type_id": g.account_type_id,
        #    "seller_id": g.seller_id if g.seller_id else None
        #}

        order_filter = {
            'order_item_id': order_item_id
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

    @order_app.route('/<order_item_id>', methods=['POST'])
    @validate_params(
        Param('order_item_id', PATH, int, required=True),
        Param('order_status_id', JSON, int, required=False),
        Param('phone_number', JSON, str, required=False),
        Param('address_1', JSON, str, required=False),
        Param('address_2', JSON, str, required=False),
        Param('zip_code', JSON, str, required=False),
        Param('delivery_instruction', JSON, str, required=False)
    )
    # @login_required
    def update_order_detail(*args):
        order_service = OrderService()
        data = request.json

        #account_info = {
        #    "account_id": g.account_id,
        #    "account_type_id": g.account_type_id,
        #    "seller_id": g.seller_id if g.seller_id else None
        #}

        order_filter = {
            'order_item_id': args[0],
        }

        order_status = {
        #    #'editor_id': g.account_id,
            'order_item_id': args[0],
            'new_order_status': data['new_order_status']
        }

        delivery_info = {
        #    #'editor_id': g.account_id,
            'order_item_id': args[0],
            'phone_number': data['phone_number'],
            'address_1': data['address_1'],
            'address_2': data['address_2'],
            'zip_code': data['zip_code'],
            'delivery_instruction': data['delivery_instruction']
        }

        connection = None
        try:
            connection = connect_db()
            order_service.update_order_detail(connection, order_status, delivery_info)
            updated_order_detail = order_service.get_order_detail(connection, order_filter)

            connection.commit()
            return jsonify({"updated_order_detail": updated_order_detail}), 201

        # except 에러 발생시:
        #    connection.rollback()
        #    return 에러메세지

        finally:
            if connection:
                connection.close()