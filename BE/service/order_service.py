from flask import g

from model.order_dao   import OrderDao
from model.account_dao import AccountDao


class OrderService():
    
    def __init__(self):
        pass

    def get_filter_options(self, connection, order_status_id):
        order_dao    = OrderDao()
        account_dao  = AccountDao()
        seller_types = None

        # 마스터일 경우 셀러속성 리스트도 함께 보내줌.
        if g.token_info['account_type_id'] == 1:
            seller_types = account_dao.get_seller_types(connection)

        # 주문상태 변경 버튼 가져오기
        order_actions = order_dao.get_order_actions_by_status(connection, order_status_id)

        filter_options = {
            "seller_types" : seller_types,
            "order_actions": order_actions
        }
        return filter_options

    def get_order_list(self, connection, order_filter):
        order_dao = OrderDao()

        # offset 계산하여 필터에 추가.
        order_filter['offset'] = (order_filter['page'] * order_filter['limit']) - order_filter['limit']

        # end_date가 있을 경우 해당 날짜의 주문까지 포함해서 필터하기 위해 시간 추가.
        if order_filter['end_date']:
            order_filter['end_date'] += " 23:59:59"

        order_info = order_dao.get_order_info(connection, order_filter)
        return order_info

    def update_order_status(self, connection, update_status):
        # 여러 아이템의 주문 상태를 한꺼번에 업데이트하고 아이템마다 로그를 생성함.
        order_dao = OrderDao()

        # 셀러일 경우: 주문 셀러와 업데이트 요청한 셀러가 동일한 셀러인지 확인
        if g.token_info['account_type_id'] == 2:
            seller_validation = order_dao.seller_validation(connection, update_status)
            for order in seller_validation:
                if order['seller_id'] != g.token_info['seller_id']:
                    raise Exception('Unauthorized seller')
                else:
                    update_status['seller_id'] = g.token_info['seller_id']

        # 주문상태-액션 중간테이블에서 액션에 해당하는 새로운 주문상태 id를 가져옴
        new_order_status = order_dao.get_order_status_by_action(connection, update_status)
        update_status['new_order_status_id'] = new_order_status['change_to']

        number_of_orders_updated = order_dao.update_order_status(connection, update_status)

        order_log = [
            [i, update_status['editor_id'], update_status['new_order_status_id']]
            for i in update_status['order_item_id']
        ]
        order_dao.create_order_log(connection, order_log)

        return number_of_orders_updated

    def get_order_detail(self, connection, order_filter):
        # 주문 상세정보, 주문상태 변경이력, 주문상태 변경옵션을 리턴함
        order_dao = OrderDao()

        if g.token_info['account_type_id'] == 2:
            seller_validation = order_dao.seller_validation(connection, order_filter)
            if seller_validation[0]['seller_id'] != g.token_info['seller_id']:
                raise Exception('Unauthorized seller')
            else:
                order_filter['seller_id'] = g.token_info['seller_id']

        order_info = order_dao.get_order_info(connection, order_filter)
        order_logs = order_dao.get_order_logs(connection, order_filter)

        # 가능한 주문상태 변경 옵션 가져오기
        order_filter['order_status_id'] = order_info['order_list'][0]['order_status_id']
        order_status_options = order_dao.get_order_status_options(connection, order_filter)

        order_detail = {
            'order_info'          : order_info,
            'order_logs'          : order_logs,
            'order_status_options': order_status_options
        }
        return order_detail

    def update_order_detail(self, connection, update_order):
        # 주문 상세정보(주문상태, 배송지정보) 업데이트
        order_dao = OrderDao()

        # 셀러일 경우: 주문 셀러와 업데이트 요청한 셀러가 동일한지 확인
        if g.token_info['account_type_id'] == 2:
            seller_validation = order_dao.seller_validation(connection, update_order)
            if seller_validation[0]['seller_id'] != g.token_info['seller_id']:
                raise Exception('Unauthorized seller')
            else:
                update_order['seller_id'] = g.token_info['seller_id']

        if update_order['new_order_status_id']:
            # 현재 주문 상태와 선택 가능한 상태변경 옵션 확인
            order_info = order_dao.get_order_info(connection, update_order)
            update_order['order_status_id'] = order_info['order_list'][0]["order_status_id"]
            order_status_options = order_dao.get_order_status_options(connection, update_order)
            id_available = [status['id'] for status in order_status_options]

            # 선택 가능한 옵션이 아닐 경우 raise exception
            if update_order['new_order_status_id'] not in id_available:
                raise Exception('wrong order status action')

            # 주문상태 변경 후 로그 생성
            order_dao.update_order_status(connection, update_order)
            order_log = [
                [update_order['order_item_id'], update_order['editor_id'], update_order['new_order_status_id']]
            ]
            order_dao.create_order_log(connection, order_log)

        if update_order['phone_number'] \
                or update_order['address_1'] \
                or update_order['address_2'] \
                or update_order['zip_code'] \
                or update_order['delivery_instruction']:
            order_dao.update_delivery_info(connection, update_order)

        else:
            raise Exception('Nothing to update')