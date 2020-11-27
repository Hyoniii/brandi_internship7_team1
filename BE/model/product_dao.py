import pymysql
from flask import jsonify
from mysql.connector.errors import Error

class ProductDao:
    """
    상품 모델
    """
    def product_list(self,data,connection):
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            query = """
            SELECT * 
            FROM products
            WHERE id 
            """

            cursor.execute(query,data)
            products = cursor.fetchall()

            return products

