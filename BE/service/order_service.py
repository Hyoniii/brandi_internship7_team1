from model.order_dao import OrderDao


class OrderService():

    def get_order_list(self, connection, order_filter):

        order_dao = OrderDao()

        order_filter['offset'] = (order_filter['page'] * order_filter['limit']) - order_filter['limit']

        order_info = order_dao.get_order_info(connection, order_filter)

        # if account_info['account_type_id'] == 2 and account_info['seller_id'] != order_info['seller_id']:
        #    raise error

        return order_info

        # except error:
        #     raise error

    def update_order_status(self, connection, order_status):

        order_dao = OrderDao()

        order_dao.update_order_status(connection, order_status)

    def get_order_detail(self, connection, order_filter):

        order_dao = OrderDao()

        order_info = order_dao.get_order_info(connection, order_filter)
        order_logs = order_dao.get_order_logs(connection, order_filter)

        order_status_options = order_dao.get_order_status_options(connection)

        # if account_info['seller_id'] != order_info['seller_id']:
        #     raise error

        order_detail = {
            'order_info': order_info,
            'order_logs': order_logs,
            'order_status_options': order_status_options
        }

        return order_detail

        # except error:
        #     raise error


    # def update_order_detail(self, connection, order_status, delivery_info):
    #     order_dao = OrderDao()
    #
    #     if order_status['order_status_id']:
    #         order_dao.update_order_status(connection, order_status)
    #
    #     if delivery_info['phone_number'] \
    #             or delivery_info['address_1'] \
    #             or delivery_info['address_2'] \
    #             or delivery_info['zip_code'] \
    #             or delivery_info['delivery_instruction']:
    #
    #         order_dao.update_delivery_info(connection, delivery_info)
    #
    #     return True