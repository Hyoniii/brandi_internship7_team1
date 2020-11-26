from flask import request
#from exceptions import errors

class OrderService():
    def __init__(self, order_dao):
        self.order_dao = order_dao

    def get_order_detail(self, connection, order_filter):
        order_info        = self.order_dao.get_order_detail(connection, order_filter)
        order_logs        = self.order_dao.get_order_logs(connection, order_filter)
        order_status_list = self.order_dao.get_order_status_list(connection)

        order_detail = {
            'order_info'       : order_info,
            'order_logs'       : order_logs,
            'order_status_list': order_status_list
        }

        return order_detail

    def update_order_detail(self, connection, order_filter, order_update):
        self.order_dao.update_order_status(connection, order_filter, order_update)

        return 업뎃성공!