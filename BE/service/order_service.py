from model.order_dao import OrderDao
from model.account_dao import AccountDao


class OrderService():
    
    def __init__(self):
        pass
    
    def get_order_list(self, connection, order_filter):
        # 필터를 전달하여 주문 리스트를 가져오는 로직.

        order_dao = OrderDao()

        # page와 limit으로 offset 계산하여 필터에 추가
        order_filter['offset'] = (order_filter['page'] * order_filter['limit']) - order_filter['limit']

        # 해당 날짜의 주문까지 포함해서 필터하기 위해 시간 추가.
        if order_filter['end_date']:
            order_filter['end_date'] += " 23:59:59"

        # dao로 필터 전달하여 데이터 받아오기.
        order_info = order_dao.get_order_info(connection, order_filter)

        return order_info

    def get_filter_options(self, connection, account_type_id, order_status_id):

        order_dao = OrderDao()
        account_dao = AccountDao()
        seller_types = None

        # 마스터일 경우 셀러속성 리스트를 보냄
        if account_type_id == 1:
            seller_types = account_dao.get_seller_types(connection)

        order_actions = order_dao.get_order_actions_by_status(connection, order_status_id)

        filter_options = {
            "seller_types": seller_types,
            "order_actions": order_actions
        }

        return filter_options

    def update_order_status(self, connection, update_status):
        # 여러 아이템의 주문 상태를 한꺼번에 업데이트하고 아이템마다 로그를 생성함.

        order_dao = OrderDao()

        # 주문상태-액션 중간테이블에서 액션에 해당하는 새로운 주문상태 id를 가져옴
        new_order_status_id = order_dao.get_order_status_by_action(connection, update_status)
        update_status['new_order_status_id'] = new_order_status_id['change_to']

        # 주문상세 업데이트
        number_of_orders_updated = order_dao.update_order_status(connection, update_status)

        # 상태변경 로그 생성
        order_log = [
            [i, update_status['editor_id'], update_status['new_order_status_id']]
            for i in update_status['order_item_id']
        ]
        number_of_logs_created = order_dao.create_order_log(connection, order_log)

        # 업데이트된 주문 수와 생성된 상태변경 로그 수가 일치하는지 확인
        if number_of_orders_updated == number_of_logs_created:
            return number_of_orders_updated

    def get_order_detail(self, connection, order_filter):
        # 주문 상세정보를 가져오는 엔드포인트
        # 주문 상세정보, 주문상태 변경이력, 주문상태 변경옵션 dao를 각각 호출하여 결과를 리턴함.
        order_dao = OrderDao()

        # 주문정보, 주문상태 변경이력 가져오기.
        order_info = order_dao.get_order_info(connection, order_filter)
        order_logs = order_dao.get_order_logs(connection, order_filter)

        #가능한 주문상태 변경 옵션 가져오기
        order_filter['order_status_id'] = order_info['order_list'][0]['order_status_id']
        order_status_options = order_dao.get_order_status_options(connection, order_filter)

        order_detail = {
            'order_info': order_info,
            'order_logs': order_logs,
            'order_status_options': order_status_options
        }

        return order_detail

    def update_order_detail(self, connection, order_status, delivery_info):
        # 주문상세정보 업데이트
        # 주문상태 변경하는 dao, 배송지정보 변경하는 dao를 각각 호출함
        order_dao = OrderDao()

        if order_status['new_order_status_id']:
            # 주문상세 업데이트
            order_dao.update_order_status(connection, order_status)

            # 주문상태 변경로그 생성
            order_log = [order_status['order_item_id'], order_status['editor_id'], order_status['new_order_status_id']]
            order_dao.create_order_log(connection, order_log)

        if delivery_info['phone_number'] \
                or delivery_info['address_1'] \
                or delivery_info['address_2'] \
                or delivery_info['zip_code'] \
                or delivery_info['delivery_instruction']:
            order_dao.update_delivery_info(connection, delivery_info)




