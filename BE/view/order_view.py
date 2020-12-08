from flask import (
    Blueprint,
    jsonify,
    g
)
from flask_request_validator import (
    validate_params,
    Param,
    PATH,
    GET,
    Pattern,
    JSON,
    Enum,
    MinLength,
    MaxLength
)

from utils import login_validator
from db_connector import connect_db
from service.order_service import OrderService


class OrderView:
    order_app = Blueprint('order_app', __name__, url_prefix='/orders')

    @order_app.route('/filter_options/<order_status_id>', methods=['GET'])
    @validate_params(
        Param('order_status_id', PATH, int, rules=[Enum(1, 2, 3, 4, 5)])
    )
    @login_validator
    def get_filter_options(order_status_id):
        # 주문관리에 페이지에서 셀러속성 리스트와 주문상태변경 버튼 보내주는 엔드포인트
        order_service = OrderService()

        connection = None
        try:
            connection = connect_db()
            # get_filter_options 서비스 호출
            filter_options = order_service.get_filter_options(connection, order_status_id)
            return jsonify(filter_options), 200

        except Exception as e:
            return jsonify({"message": f'{e}'}), 500

        finally:
            try:
                if connection:
                    connection.close()
            except Exception as e:
                return jsonify({"message": f'{e}'}), 500

    @order_app.route('', methods=['GET'])
    @validate_params(
        Param('order_status_id', GET, int, rules=[Enum(1, 2, 3, 4, 5)], required=True),
        Param('order_number', GET, str, rules=[Pattern('^[0-9]{16,}$')], required=False),
        Param('detailed_order_number', GET, str, rules=[Pattern('^[0-9]{17,}$')], required=False),
        Param('buyer_name', GET, str, rules=[Pattern('[\S]')], required=False),
        Param('phone_number', GET, str, rules=[Pattern('^[0-9]{11}$')], required=False),
        Param('seller_name', GET, str, rules=[Pattern('[\S]')], required=False),
        Param('product_name', GET, str, rules=[Pattern('[\S]')], required=False),
        Param('start_date', GET, str, rules=[Pattern('^(20)[\d]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[0-1])$')],
              required=False),
        Param('end_date', GET, str, rules=[Pattern('^(20)[\d]{2}-(0[1-9]|1[012])-(0[1-9]|[12][0-9]|3[0-1])$')],
              required=False),
        # 셀러속성 다중선택 가능
        Param('seller_type_id', GET, list, rules=[MinLength(1), MaxLength(7)], required=False),
        Param('limit', GET, int, rules=[Enum(10, 20, 50, 100, 150)], required=False),
        Param('order_by', GET, str, rules=[Enum('desc', 'asc')], required=False),
        Param('page', GET, int, required=False)
    )
    @login_validator
    def get_order_list(*args):
        # 주문상태별 주문 리스트 필터하여 보내주는 엔드포인트
        order_service = OrderService()

        # page parameter에 0이나 음수가 들어올 경우 키에러
        if args[12] and args[12] <= 0:
            return jsonify({"key error": "Page cannot be negative"}), 400

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

        # 셀러일 경우 필터에 seller_id 추가
        if g.token_info['account_type_id'] == 2:
            order_filter['seller_id'] = g.token_info['seller_id']

        connection = None
        try:
            connection = connect_db()
            # get_order_list 서비스함수 호출
            order_list = order_service.get_order_list(connection, order_filter)
            return jsonify(order_list), 200

        except Exception as e:
            return jsonify({"message": f"{e}"}), 400

        finally:
            try:
                if connection:
                    connection.close()
            except Exception as e:
                return jsonify({"message": f"{e}"}), 500

    @order_app.route('', methods=['POST'])
    @validate_params(
        Param('order_item_id', JSON, list, required=True),
        # 2: 상품준비 3: 배송중
        Param('order_status_id', JSON, int, rules=[Enum(2, 3)], required=True),
        # 1: 배송처리 2: 배송완료처리
        Param('order_action_id', JSON, int, rules=[Enum(1, 2)], required=True)
    )
    @login_validator
    def update_order_status(*args):
        # 주문 아이템의 주문 상태를 변경하는 엔드포인트
        # 변경할 아이템의 id를 리스트로 받아서 일괄 업데이트
        order_service = OrderService()

        update_status = {
            'editor_id': g.token_info['account_id'],
            'order_item_id': args[0],
            'order_status_id': args[1],
            'order_action_id': args[2]
        }

        # 셀러일 경우 필터에 seller_id 추가
        #if g.token_info['account_type_id'] == 2:
        #    update_status['seller_id'] = g.token_info['seller_id']

        connection = None
        try:
            connection = connect_db()
            # update_order_status 서비스 호출
            number_of_orders_updated = order_service.update_order_status(connection, update_status)
            connection.commit()
            return jsonify({"message": f"{number_of_orders_updated} order(s) successfully updated"}), 201

        except Exception as e:
            connection.rollback()
            return jsonify({"message": f"{e}"}), 400

        finally:
            try:
                if connection:
                    connection.close()
            except Exception as e:
                return jsonify({"message": f"{e}"}), 500

    @order_app.route('/<order_item_id>', methods=['GET'])
    @validate_params(
        Param('order_item_id', PATH, int)
    )
    @login_validator
    def get_order_detail(order_item_id):
        # 주문 상세정보 가져오는 엔드포인트

        order_service = OrderService()

        order_filter = {
            'order_item_id': order_item_id
        }

        # 셀러일 경우 필터에 seller_id 추가
        if g.token_info['account_type_id'] == 2:
            order_filter['seller_id'] = g.token_info['seller_id']

        connection = None
        try:
            connection = connect_db()
            # get_order_detail 서비스 호출
            order_detail = order_service.get_order_detail(connection, order_filter)
            return jsonify(order_detail), 200

        except Exception as e:
            return jsonify({"message": f"{e}"}), 400

        finally:
            try:
                if connection:
                    connection.close()
            except Exception as e:
                return jsonify({"message": f"{e}"}), 500

    @order_app.route('/<order_item_id>', methods=['POST'])
    @validate_params(
        Param('order_item_id', PATH, int, required=True),
        Param('new_order_status_id', JSON, int, rules=[Enum(2, 3, 4, 5)], required=False),
        Param('phone_number', JSON, str, rules=[Pattern('^[0-9]{11}')], required=False),
        Param('address_1', JSON, str, rules=[Pattern('[\S]')], required=False),
        Param('address_2', JSON, str, rules=[Pattern('[\S]')], required=False),
        Param('zip_code', JSON, str, rules=[Pattern('^[0-9]{5}')], required=False),
        Param('delivery_instruction', JSON, str, required=False)
    )
    @login_validator
    def update_order_detail(*args):
        # 주문 상세정보(주문상태, 연락처, 배송지 정보)를 업데이트하는 엔드포인트

        order_service = OrderService()

        order_filter = {
            'order_item_id': args[0]
        }

        update_order = {
            'order_item_id': args[0],
            'editor_id': g.token_info['account_id'],
            'new_order_status_id': args[1],
            'phone_number': args[2],
            'address_1': args[3],
            'address_2': args[4],
            'zip_code': args[5],
            'delivery_instruction': args[6],
        }
        #############################################
        #### 셀러 validation 방법 변경하기  #######
        #############################################

        # 셀러일 경우 필터에 seller_id 추가
        if g.token_info['account_type_id'] == 2:
            order_filter['seller_id'] = g.token_info['seller_id']
            update_order['seller_id'] = g.token_info['seller_id']

        connection = None
        try:
            connection = connect_db()
            # 주문정보 업데이트 후 업데이트된 상세정보 가져오기
            order_service.update_order_detail(connection, update_order)
            updated_order_detail = order_service.get_order_detail(connection, order_filter)

            connection.commit()
            return jsonify({"updated_order_detail": updated_order_detail}), 201

        except Exception as e:
            connection.rollback()
            return jsonify({"message": f"{e}"}), 400

        finally:
            try:
                if connection:
                    connection.close()
            except Exception as e:
                return jsonify({"message": f"{e}"})
