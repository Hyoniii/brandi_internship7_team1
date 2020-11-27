from model.order_dao import OrderDao

class OrderService():
    def get_order_detail(self, connection, order_filter):
        order_dao = OrderDao()
        order_info        = order_dao.get_order_detail(connection, order_filter)
        order_logs        = order_dao.get_order_logs(connection, order_filter)
        order_status_list = order_dao.get_order_status_list(connection)
        # except error:
        #     raise error
        # if order_info['seller_id'] != order_filter['seller_id']:
        #     raise error
        order_detail = {
            'order_info'       : order_info,
            'order_logs'       : order_logs,
            'order_status_list': order_status_list
        }
        return order_detail

    def update_order_detail(self, connection, order_status, delivery_info):
        order_dao = OrderDao()
        if order_status['order_status_id']:
            order_dao.update_order_status(connection, order_status)
        if delivery_info: # value가 None이 아닐 경우:
            order_dao.update_delivery_info(connection, delivery_info)

