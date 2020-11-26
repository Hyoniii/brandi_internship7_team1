import pymysql

class OrderDao:
    def get_order_detail(self, connection, order_filter):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                order_number,
                seller_id,
                purchase_date,
                order_tickets.total_price,
                detailed_order_number,
                products.name,
                products.number,
                quantity,
                product_price,
                order_items.discount_rate,
                order_items.total_price,
                order_statuses.status,
                color,
                size,
                seller_id,
                seller_name_kr,
                buyer_name,
                phone_number,
                delivery_info.address_1,
                delivery_info.address_2,
                delivery_info.zip_code,
                delivery_instruction
            FROM order_items
            INNER JOIN order_tickets ON order_items.order_ticket_id = order_tickets.id
            INNER JOIN delivery_info ON order_tickets.delivery_info_id = delivery_info.id
            INNER JOIN products ON order_items.product_id = products.id
            INNER JOIN sellers ON order_items.seller_id = sellers.id
            INNER JOIN product_options ON order_items.product_option_id = product_options.id
            INNER JOIN product_colors ON product_options.color_id = product_colors.id
            INNER JOIN product_sizes ON product_options.size_id = product_sizes.id
            INNER JOIN order_statuses ON order_items.order_status_id = order_statuses.id
            WHERE detailed_order_number = %(detailed_order_number)s;
            """

            order_detail = cursor.execute(query, order_filter)

            #if not order_detail:
            #    raise error

            return cursor.fetchone()

    def get_order_logs(self, connection, order_filter):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT 
                status,
                created_at,
            FROM order_logs
            INNER JOIN order_statuses ON order_logs.order_status_id = order_statuses.id
            INNER JOIN order_items ON order_logs.order_item_id = order_items.id
            WHERE detailed_order_number = %(detailed_order_number)s 
            ORDER BY created_at DESC             
            """
            order_logs = cursor.execute(query, order_filter)

            #if not order_logs:
            #    raise error

            return cursor.fetchall()

    def get_order_status_list(self, connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT status
            FROM order_statuses
            """

            return cursor.execute(query).fetchall()

    def update_delivery_info(self, connection, delivery_info):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            UPDATE delivery_info
            INNER JOIN order_tickets ON order_tickets.delivery_info_id = delivery_info.id
            INNER JOIN order_items ON order_items.order_ticket_id = order_tickets.id 
            SET 
                phone_number = %(phone_number)s,
                address_1 = %(address_1)s,
                address_2 = %(address_2)s,
                zip_code = %(zip_code)s,
                delivery_instruction = %(delivery_instruction)s,
                editor_id = %(account_id)s
            WHERE detailed_order_number = %(detailed_oder_number)s
            """

            cursor.execute(query, delivery_info)

            return 업뎃성공

    def update_order_status(self, connection, order_status):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            UPDATE order_items
            SET 
                order_status_id = %(order_status_id)s
                editor_id = %(editor_id)s
            WHERE detailed_order_number = %(detailed_order_number)s
            """
            cursor.execute(query, order_status)

            order_item_id = cursor.execute("""
            SELECT order_item_id 
            FROM order_items 
            WEHRE detailed_order_number = %(detailed_order_number)s
            """, order_status).fetchone()

            query = """
            INSERT INTO order_logs (
                order_item_id,
                editor_id,
                order_status_id
            )
            VALUES (
                %(order_item_id)s,
                %(editor_id)s,
                %(order_status_id)s
            )
            """
            cursor.execute(query, order_status)

            return 업뎃성공

