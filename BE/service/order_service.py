from model.order_dao import OrderDao
from model.account_dao import AccountDao


class OrderService():
    
    def __init__(self):
        pass
    
    def get_order_list(self, connection, order_filter):
        order_dao = OrderDao()

        # page와 limit으로 offset을 계산하여 필터에 추가.
        order_filter['offset'] = (order_filter['page'] * order_filter['limit']) - order_filter['limit']

        # end_date가 있을 경우 해당 날짜의 주문까지 포함해서 필터하기 위해 시간 추가.
        if order_filter['end_date']:
            order_filter['end_date'] += " 23:59:59"

        order_info = order_dao.get_order_info(connection, order_filter)
        return order_info

    def get_filter_options(self, connection, account_type_id, order_status_id):
        order_dao = OrderDao()
        account_dao = AccountDao()
        seller_types = None

        # 마스터일 경우 셀러속성 리스트도 함께 보내줌.
        if account_type_id == 1:
            seller_types = account_dao.get_seller_types(connection)

        # 주문상태 변경 버튼 가져오기
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
        new_order_status = order_dao.get_order_status_by_action(connection, update_status)
        update_status['new_order_status_id'] = new_order_status['change_to']

        # 주문상세 업데이트
        number_of_orders_updated = order_dao.update_order_status(connection, update_status)
        if number_of_orders_updated == 0:
            raise Exception('Failed to update order status')

        # 상태변경 로그 생성
        order_log = [
            [i, update_status['editor_id'], update_status['new_order_status_id']]
            for i in update_status['order_item_id']
        ]
        order_dao.create_order_log(connection, order_log)

        # 구매확정 스케줄러
        if update_status['new_order_status_id'] == 4:
            order_item_id = update_status['order_item_id']
            order_log = [
                [i, update_status['editor_id'], 5]
                for i in update_status['order_item_id']
            ]
            order_dao.confirm_purchase(connection, order_item_id, order_log)

        return number_of_orders_updated

    def get_order_detail(self, connection, order_filter):
        # 주문 상세정보를 가져오는 엔드포인트
        # 주문 상세정보, 주문상태 변경이력, 주문상태 변경옵션 dao를 각각 호출하여 결과를 리턴함
        order_dao = OrderDao()

        # 주문정보, 주문상태 변경이력 가져오기
        order_info = order_dao.get_order_info(connection, order_filter)

        # 해당하는 주문 정보가 없을 경우 raise exception
        if order_info['total_number'] == 0:
            raise Exception('Failed to fetch order info')

        order_logs = order_dao.get_order_logs(connection, order_filter)

        # 가능한 주문상태 변경 옵션 가져오기
        order_filter['order_status_id'] = order_info['order_list'][0]['order_status_id']
        order_status_options = order_dao.get_order_status_options(connection, order_filter)

        order_detail = {
            'order_info': order_info,
            'order_logs': order_logs,
            'order_status_options': order_status_options
        }
        return order_detail

    def update_order_detail(self, connection, update_status, delivery_info):
        # 주문상세정보 업데이트
        # 주문상태 변경하는 dao, 배송지정보 변경하는 dao를 각각 호출함
        order_dao = OrderDao()

        # 주문상태 업데이트
        if update_status['new_order_status_id']:
            # 현재 주문 상태와 선택 가능한 상태변경 옵션 확인
            order_info = order_dao.get_order_info(connection, update_status)
            update_status['order_status_id'] = order_info['order_list'][0]["order_status_id"]
            order_status_options = order_dao.get_order_status_options(connection, update_status)
            ids_available = [status['id'] for status in order_status_options]

            # 선택 가능한 옵션이 아닐 경우 raise exception
            if update_status['new_order_status_id'] not in ids_available:
                raise Exception('wrong order status action')

            # 주문상태 변경, 변경이력 생성
            order_dao.update_order_status(connection, update_status)
            order_log = [
                [update_status['order_item_id'], update_status['editor_id'], update_status['new_order_status_id']]
            ]
            order_dao.create_order_log(connection, order_log)

            # 구매확정 스케줄러(구매확정 상태로 업데이트 후 변경이력 생성)
            if update_status['new_order_status_id'] == 4:
                order_item_id = update_status['order_item_id']
                order_log = [
                    [update_status['order_item_id'], update_status['editor_id'], 5]
                ]
                order_dao.confirm_purchase(connection, order_item_id, order_log)

        if delivery_info['phone_number'] \
                or delivery_info['address_1'] \
                or delivery_info['address_2'] \
                or delivery_info['zip_code'] \
                or delivery_info['delivery_instruction']:
            order_dao.update_delivery_info(connection, delivery_info)
