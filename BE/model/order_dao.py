import pymysql

class OrderDao:

    def get_order_info(self, connection, order_filter):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                item.id,
                item.detailed_order_number,
                item.quantity,
                item.product_price,
                item.discount_rate,
                item.total_price,
                item.seller_id,
                item.order_status_id,
                ticket.order_number,
                ticket.purchase_date,
                ticket.total_price,
                status.status,
                Max(log.created_at) as updated_at,
                seller_name_kr,
                products.name,
                products.number,
                color,
                size, 
                buyer.buyer_name,
                buyer.phone_number,
                buyer.address_1,
                buyer.address_2,
                buyer.zip_code,
                buyer.delivery_instruction
            FROM order_items AS item
            INNER JOIN order_tickets AS ticket ON item.order_ticket_id = ticket.id
            INNER JOIN order_logs AS log ON log.order_item_id = item.id
            INNER JOIN order_statuses AS status ON item.order_status_id = status.id
            INNER JOIN sellers ON item.seller_id = sellers.id
            INNER JOIN products ON item.product_id = products.id
            INNER JOIN product_options ON item.product_option_id = product_options.id
            INNER JOIN product_colors ON product_options.color_id = product_colors.id
            INNER JOIN product_sizes ON product_options.size_id = product_sizes.id
            INNER JOIN delivery_info AS buyer ON ticket.delivery_info_id = buyer.id
            """

            if 'order_status_id' in order_filter:

                query += """
                WHERE item.order_status_id = %(order_status_id)s
                """

                if order_filter['order_number']:
                    query += """
                    AND ticket.order_number = %(order_number)s
                    """

                if order_filter['detailed_order_number']:
                    query += """
                    AND item.detailed_order_number = %(detailed_order_number)s
                    """

                if order_filter['buyer_name']:
                    query += """
                    AND buyer.buyer_name = %(buyer_name)s
                    """

                if order_filter['phone_number']:
                    query += """
                    AND buyer.phone_number = %(phone_number)s
                    """

                if order_filter['seller_name']:
                    query += """
                    AND (seller_name_kr = %(seller_name)s or seller_name_en = %seller_name)s
                    """

                if order_filter['product_name']:
                    query += """
                    AND products.name = %(product_name)s
                    """
                if order_filter['start_date']:
                    query += """
                    AND updated_at >= %(start_date)s
                    """

                if order_filter['end_date']:
                    query += """
                    AND updated_at <= %(end_date)s
                    """

                if order_filter['seller_type_id']:
                    query += """
                    AND sellers.subcategory_id = %(seller_type_id)s
                    """

                if order_filter['order_by'] == 'desc':
                    query += """
                    ORDER BY updated_at DESC
                    """

                elif order_filter['order_by'] == 'asc':
                    query += """
                    ORDER BY updated_at ASC
                    """

                query += """
                LIMIT %(limit)s OFFSET %(offset)s
                """

            else:

                query += """
                WHERE item.id = %(order_item_id)s
                """

            order_detail = cursor.execute(query, order_filter)

            if not order_detail:
                return 400

            return cursor.fetchall()

    def get_order_logs(self, connection, order_filter):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT 
                status,
                created_at
            FROM order_logs
            INNER JOIN order_statuses ON order_logs.order_status_id = order_statuses.id
            WHERE order_item_id = %(order_item_id)s 
            ORDER BY created_at DESC             
            """
            cursor.execute(query, order_filter)

            #if not order_logs:
            #    raise error

            return cursor.fetchall()

    def get_order_status_options(self, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT 
                id,
                status
            FROM order_statuses
            """

            cursor.execute(query)

            return cursor.fetchall()

    def update_delivery_info(self, connection, delivery_info):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            UPDATE delivery_info
            INNER JOIN order_tickets ON order_tickets.delivery_info_id = delivery_info.id
            INNER JOIN order_items AS item ON order_items.order_ticket_id = order_tickets.id 
            SET 
                phone_number = %(phone_number)s,
                address_1 = %(address_1)s,
                address_2 = %(address_2)s,
                zip_code = %(zip_code)s,
                delivery_instruction = %(delivery_instruction)s,
                editor_id = %(account_id)s
            WHERE item.id = %(order_item_id)s
            """

            cursor.execute(query, delivery_info)

            return True

    def update_order_status(self, connection, order_status):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:

            query = """
            UPDATE order_items
            SET 
                order_status_id = %(new_order_status)s
            WHERE id IN %(order_item_id)s
            """
            cursor.execute(query, order_status)


            query = """
            INSERT INTO order_logs (
                order_item_id,
                editor_id,
                order_status_id
            )
            VALUES (
                %(order_item_id)s,
                %(editor_id)s,
                %(new_order_status)s
            )
            """
            cursor.executemany(query, order_status)

            return True

