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

    def __init__(self):
        pass

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
        # 셀러속성 다중선택 가능
        Param('seller_type_id', GET, list, required=False),
        Param('limit', GET, int, required=False),
        Param('order_by', GET, str, rules=[Enum('desc', 'asc')], required=False),
        Param('page', GET, int, required=False)
    )
    # @login_required
    def get_order_list(*args):
        # 주문상태별로 필터하여 주문 리스트 전달하는 엔드포인트

        order_service = OrderService()

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
            # 디폴트값: 최신주문일순, 50개씩 보기
            'limit': args[10] if args[10] else 50,
            'order_by': args[11] if args[11] else 'desc',
            'page': args[12] if args[12] else 1
        }

        #셀러일 경우 필터에 seller_id 추가
        #if g.account_type_id == 2:
        #    order_filter['seller_id'] = g.seller_id

        connection = None
        try:
            connection = connect_db()
            order_list = order_service.get_order_list(connection, order_filter)
            return jsonify(order_list), 200

        except Exception as e:
            return jsonify({"message": f"{e}"})

        finally:
            try:
                if connection:
                    connection.close()
            except Exception as e:
                return jsonify({"message": f"{e}"})

    @order_app.route('', methods=['POST'])
    @validate_params(
        Param('order_item_id', JSON, list),
        Param('order_status_id', JSON, int),
        Param('order_action_id', JSON, int)
    )
    # @login_required
    def update_order_status(*args):
        # 주문 아이템의 주문 상태를 변경하는 엔드포인트
        # 변경할 아이템의 id를 리스트로 받아서 일괄 업데이트

        order_service = OrderService()
        data = request.json

        update_order = {
            #'editor_id': g.account_id,
            'order_item_id': data['order_item_id'],
            'order_status_id': data['order_status_id'],
            'order_action_id': data['order_action_id']
        }

        # 셀러일 경우 필터에 seller_id 추가
        # if g.account_type_id == 2:
        #    update_order['seller_id'] = g.seller_id

        connection = None
        try:
            connection = connect_db()
            order_service.update_order_status(connection, update_order)

            return jsonify({"message": "status successfully updated"})

        except Exception as e:
            connection.rollback()
            return jsonify({"message": f"{e}"})

        finally:
            try:
                if connection:
                    connection.close()
            except Exception as e:
                return jsonify({"message": f"{e}"})

    @order_app.route('/<order_item_id>', methods=['GET'])
    @validate_params(
        Param('order_item_id', PATH, int)
    )
    # @login_required
    def get_order_detail(order_item_id):
        # 주문 상세정보 가져오는 엔드포인트

        order_service = OrderService()

        order_filter = {
            'order_item_id': order_item_id
        }

        # 셀러일 경우 필터에 seller_id 추가
        # if g.account_type_id == 2:
        #    order_filter['seller_id'] = g.seller_id

        connection = None
        try:
            connection = connect_db()
            order_detail = order_service.get_order_detail(connection, order_filter)

            return jsonify(order_detail), 200

        except Exception as e:
            return jsonify({"message": f"{e}"})

        finally:
            try:
                if connection:
                    connection.close()
            except Exception as e:
                return jsonify({"message": f"{e}"})

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
        # 주문 상세정보(주문상태, 연락처, 배송지 정보)를 업데이트하는 엔드포인트

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

        except Exception as e:
            connection.rollback()
            return jsonify({"message": f"{e}"})


        finally:
            try:
                if connection:
                    connection.close()
            except Exception as e:
                return jsonify({"message": f"{e}"})