import pymysql


class SellerDao:

    def __init__(self):
        pass

    def count_seller_products(self, connection, seller_id):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT
                COUNT(*) as cnt
            FROM products
            WHERE seller_id = %s
            """
            cursor.execute(query, seller_id)
            total_products = cursor.fetchone()

            query += """
            AND is_visible = 1
            """
            cursor.execute(query, seller_id)
            visible_products = cursor.fetchone()

            return {"total_products": total_products['cnt'], "visible_products": visible_products['cnt']}