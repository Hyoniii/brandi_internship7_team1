import pymysql


class OrderDao:

    def __init__(self):
        pass

    def get_order_info(self, connection, order_filter):
        # 데이터베이스에서 주문 정보를 필터링하여 가져옴.

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            count = """
            SELECT 
                count(item.detailed_order_number) AS cnt
            """

            data = """
            SELECT
                item.id AS id,
                item.detailed_order_number,
                item.quantity AS order_quantity,
                item.product_price,
                item.discount_rate,
                item.total_price AS item_subtotal,
                item.seller_id,
                item.order_status_id,
                ticket.order_number,
                ticket.purchase_date,
                ticket.total_price AS total_order_amount,
                status.status AS order_status,
                log.created_at AS updated_at,
                seller_name_kr,
                products.name AS product_name,
                products.number AS product_number,
                color AS option_color,
                size AS option_size, 
                buyer.buyer_name,
                buyer.phone_number,
                buyer.address_1 AS delivery_address_1,
                buyer.address_2 AS delivery_address_2,
                buyer.zip_code AS delivery_zip_code,
                buyer.delivery_instruction
            """

            condition = """
            FROM order_items AS item
            INNER JOIN order_tickets AS ticket ON item.order_ticket_id = ticket.id
            INNER JOIN order_logs AS log ON (log.order_item_id = item.id AND log.order_status_id = item.order_status_id)
            INNER JOIN order_statuses AS status ON item.order_status_id = status.id
            INNER JOIN sellers ON item.seller_id = sellers.id
            INNER JOIN products ON item.product_id = products.id
            INNER JOIN delivery_info AS buyer ON ticket.delivery_info_id = buyer.id
            INNER JOIN product_options ON item.product_option_id = product_options.id
            LEFT JOIN product_colors ON product_options.color_id = product_colors.id
            LEFT JOIN product_sizes ON product_options.size_id = product_sizes.id
            """

            # 주문 리스트에서 보낸 요청일 경우(주문 "상태" id가 있을때)
            if 'order_status_id' in order_filter:

                condition += """
                WHERE item.order_status_id = %(order_status_id)s
                """

                # 셀러일 경우 셀러 아이디 확인
                if 'seller_id' in order_filter:
                    condition += """
                    AND item.seller_id = %(seller_id)s
                    """

                if order_filter['order_number']:
                    condition += """
                    AND ticket.order_number = %(order_number)s
                    """

                if order_filter['detailed_order_number']:
                    condition += """
                    AND item.detailed_order_number = %(detailed_order_number)s
                    """

                if order_filter['buyer_name']:
                    condition += """
                    AND buyer.buyer_name = %(buyer_name)s
                    """

                if order_filter['phone_number']:
                    condition += """
                    AND buyer.phone_number = %(phone_number)s
                    """

                if order_filter['seller_name']:
                    condition += """
                    AND (seller_name_kr LIKE %(seller_name)s or seller_name_en Like %(seller_name)s)
                    """

                if order_filter['product_name']:
                    condition += """
                    AND products.name = %(product_name)s
                    """
                if order_filter['start_date']:
                    condition += """
                    AND updated_at >= %(start_date)s
                    """

                if order_filter['end_date']:
                    condition += """
                    AND updated_at <= %(end_date)s
                    """

                if order_filter['seller_type_id']:
                    condition += """
                    AND sellers.subcategory_id IN %(seller_type_id)s
                    """

                if order_filter['order_by'] == 'desc':
                    condition += """
                    ORDER BY updated_at DESC
                    """

                elif order_filter['order_by'] == 'asc':
                    condition += """
                    ORDER BY updated_at ASC
                    """

                condition += """
                LIMIT %(limit)s OFFSET %(offset)s
                """

            # 주문 상세에서 보낸 요청일 경우(주문 "상세" id가 있을때)
            else:

                condition += """
                WHERE item.id = %(order_item_id)s
                """

                # 셀러일 경우 셀러 아이디 확인
                if 'seller_id' in order_filter:
                    condition += """
                    AND item.seller_id = %(seller_id)s
                    """

            # 주문 정보 가져오는 쿼리문
            query = data + condition
            cursor.execute(query, order_filter)
            order_list = cursor.fetchall()

            # 주문 갯수 가져오는 쿼리문
            query = count + condition
            cursor.execute(query, order_filter)
            total_number = cursor.fetchone()

            return {"order_list": order_list, "total_number": total_number["cnt"]}

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

            return cursor.fetchall()

    def get_order_status_by_action(self, connection, update_status):
        # 클릭된 주문처리 버튼에 따라 변경할 상태 id를 리턴
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT change_to
            FROM order_status_actions
            WHERE order_action_id = %(order_action_id)s
            AND order_status_id = %(order_status_id)s
            """
            cursor.execute(query, update_status)

            return cursor.fetchone()

    def get_order_status_options(self, connection, order_filter):
        # 현재 주문 상태에서 선택 가능한 상태 id들을 리턴
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT 
                id,
                status
            FROM order_statuses
            WHERE id IN %(order_status_options)s
            """

            cursor.execute(query, order_filter)

            return cursor.fetchall()


    def update_delivery_info(self, connection, delivery_info):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            UPDATE delivery_info
            INNER JOIN order_tickets ON order_tickets.delivery_info_id = delivery_info.id
            INNER JOIN order_items ON order_items.order_ticket_id = order_tickets.id 
            SET 
            """

            if delivery_info['phone_number']:
                query += """
                phone_number = %(phone_number)s,
                """
            if delivery_info['address_1']:
                query += """
                address_1 = %(address_1)s,
                """
            if delivery_info['address_2']:
                query += """
                address_2 = %(address_2)s,
                """
            if delivery_info['zip_code']:
                query += """
                zip_code = %(zip_code)s,
                """
            if delivery_info['delivery_instruction']:
                query += """
                delivery_instruction = %(delivery_instruction)s
                """

            query += """
                editor_id = %(editor_id)s
            WHERE order_items.id = %(order_item_id)s
            """

            if 'seller_id' in delivery_info:
                query += """
                AND order_items.seller_id = %(seller_id)s
                """
            cursor.execute(query, delivery_info)

            return cursor.lastrowid

    def update_order_status(self, connection, update_status):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            UPDATE order_items
            SET 
                order_status_id = %(new_order_status_id)s
            """

            if type(update_status['order_item_id']) == list:
                query += """
                WHERE id IN %(order_item_id)s
                """

            if type(update_status['order_item_id']) == int:
                query += """
                WHERE id = %(order_item_id)s
                """

            # 셀러일 경우 셀러id 확인
            if 'seller_id' in update_status:
                query += """
                AND seller_id = %(seller_id)s
                """
            cursor.execute(query, update_status)

            return cursor.rowcount

    def create_order_log(self, connection, order_log):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # 주문상태 변경 로그 생성
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

            cursor.executemany(query, order_log)

            return cursor.rowcount

