from model.order_dao import OrderDao


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


    def update_order_status(self, connection, update_order):
        # 리스트에서 여러 아이템의 주문 상태를 한꺼번에 업데이트하는 엔드포인트

        order_dao = OrderDao()

        new_order_status_id = order_dao.get_order_status_by_action(connection, update_order)
        update_order['new_order_status_id'] = new_order_status_id['change_to']

        #주문상세 테이블 상태 업데이트
        number_of_orders_updated = order_dao.update_order_status(connection, update_order)

        #주문상태 로그 생성
        log_list = [{
            "order_item_id": i,
            "editor_id": update_order['editor_id'],
            "order_status_id": update_order['new_order_status_id']
        } for i in update_order['order_item_id']]

        order_dao.create_order_log(connection, log_list)

        return number_of_orders_updated


    def get_order_detail(self, connection, order_filter):
        # 주문 상세정보를 가져오는 엔드포인트
        # 주문 상세정보, 주문상태 변경이력, 주문상태 변경옵션 dao를 각각 호출하여 결과를 리턴함.

        order_dao = OrderDao()

        # 주문정보, 주문상태 변경이력 가져오기.
        order_info = order_dao.get_order_info(connection, order_filter)
        order_logs = order_dao.get_order_logs(connection, order_filter)

        # 현재 주문상태와 다음 주문상태 id를 리스트에 담아 dao에 파라미터로 전달.
        current_status_id = order_info['order_list'][0]['order_status_id']
        new_status_id = current_status_id + 1
        order_filter['order_status_options'] = [current_status_id, new_status_id]

        # 가능한 주문상태 변경 옵션 가져오기.
        order_status_options = order_dao.get_order_status_options(connection, order_filter)

        order_detail = {
            'order_info': order_info,
            'order_logs': order_logs,
            'order_status_options': order_status_options
        }

        return order_detail

    def update_order_detail(self, connection, order_status, delivery_info):
        order_dao = OrderDao()

        if order_status['order_status_id']:
            order_dao.update_order_status(connection, order_status)

        if delivery_info['phone_number'] \
                or delivery_info['address_1'] \
                or delivery_info['address_2'] \
                or delivery_info['zip_code'] \
                or delivery_info['delivery_instruction']:

            order_dao.update_delivery_info(connection, delivery_info)

        return True