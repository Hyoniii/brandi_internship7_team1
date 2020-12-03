import os, io, jwt, uuid
import pymysql

from functools import wraps
from flask        import request, jsonify, g
from db_connector import connect_db
from mysql.connector.errors import Error
from config       import SECRET_KEY, ALGORITHM


def login_validator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('AUTHORIZATION', None)

        if access_token:
            try:

                payload = jwt.decode(access_token, SECRET_KEY, ALGORITHM)
                account_id = payload['account_id']
                connection = connect_db()

                if connection:
                    try:
                        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
                            query = """
                                SELECT
                                    accounts.account_type_id,
                                    accounts.is_active,
                                    accounts.id,
                                    sellers.id as seller_id
                                FROM
                                    accounts
                                LEFT JOIN
                                    sellers ON sellers.account_id = accounts.id
                                WHERE
                                    accounts.id = %(account_id)s
                            """
                            cursor.execute(query, {'account_id': account_id})
                            account = cursor.fetchone()
                        if account:
                            if account['is_active'] == 1:
                                g.token_info = {
                                    'account_id': account_id,
                                    'account_type_id': account['account_type_id'],
                                    'seller_id': None}
                                return func(*args, **kwargs)
                            return jsonify({'MESSAGE': 'account_not_active'}), 400
                        return jsonify({'MESSAGE': 'account_nonexistant'}), 404

                    except Error as e:
                        return Jsonify({'MESSAGE': 'DB_error'}), 400

            except jwt.InvalidTokenError:
                return jsonify({'MESSAGE': 'invalid_token'}), 401

            return jsonify({'MESSAGE': 'no_db_connection'}), 400
        return jsonify({'MESSAGE': 'invalid_token'}), 401
    return wrapper
